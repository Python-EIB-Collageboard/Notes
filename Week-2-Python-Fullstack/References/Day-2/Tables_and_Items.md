# Tables and Items

## Objective
The core DynamoDB storage primitives -- tables and items -- their structural constraints, and the programmatic API for creating and inspecting them via `boto3`.

## JavaScript Equivalent
A DynamoDB table is loosely analogous to a MongoDB collection: a named container for schema-flexible documents. A DynamoDB item maps to a MongoDB document or a Mongoose model instance -- a set of key-value attribute pairs stored as a single unit.

## Implementation Details

DynamoDB's storage model differs from both relational databases and MongoDB in a specific way: the only attributes the table enforces at the schema level are the **key attributes** (partition key and optional sort key). All other attributes are unconstrained per item and do not need to be declared at table creation time.

### Table Creation

Tables are created via `dynamodb.create_table()`. The minimum required parameters are:

- `TableName`: unique identifier within the AWS account and region
- `KeySchema`: defines which attributes form the primary key
- `AttributeDefinitions`: type declarations for key attributes only
- `BillingMode`: `'PAY_PER_REQUEST'` (on-demand) eliminates the need to specify throughput capacity for development

```python
import boto3

dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id='local',
    aws_secret_access_key='local',
    endpoint_url='http://localhost:8000'
)

table = dynamodb.create_table(
    TableName='products',
    KeySchema=[
        {'AttributeName': 'product_id', 'KeyType': 'HASH'},   # Partition key
        {'AttributeName': 'category',   'KeyType': 'RANGE'}   # Sort key (optional)
    ],
    AttributeDefinitions=[
        {'AttributeName': 'product_id', 'AttributeType': 'S'},
        {'AttributeName': 'category',   'AttributeType': 'S'}
    ],
    BillingMode='PAY_PER_REQUEST'
)

table.wait_until_exists()
print(f'Table status: {table.table_status}')
```

`wait_until_exists()` polls the `DescribeTable` API until the table status is `ACTIVE`. For DynamoDB Local, this is near-instantaneous. In production, creation can take several seconds.

`AttributeType` values: `'S'` (String), `'N'` (Number), `'B'` (Binary). DynamoDB Local accepts these and no others in `AttributeDefinitions`.

### Idempotent Table Creation

For provisioning scripts that may run multiple times, catch `ResourceInUseException` rather than querying for the table before creating it:

```python
from botocore.exceptions import ClientError

def create_table_if_not_exists(dynamodb, table_name: str):
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'product_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'product_id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        table.wait_until_exists()
        print(f'Created table: {table_name}')
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f'Table already exists: {table_name}')
        else:
            raise
    return dynamodb.Table(table_name)
```

### Items

An item is a collection of attributes. The only required attributes are the key attributes defined in the `KeySchema`. All other attributes are optional and can vary between items in the same table.

```python
table = dynamodb.Table('products')

# Item with key attribute and additional attributes
table.put_item(Item={
    'product_id': 'prod-001',      # Partition key -- required
    'name': 'Wireless Keyboard',
    'price': 79.99,                # Stored as DynamoDB Number type
    'in_stock': True,
    'tags': ['peripherals', 'wireless']  # Stored as DynamoDB List type
})

# Second item with a different attribute shape -- valid
table.put_item(Item={
    'product_id': 'prod-002',      # Only the key attribute is required
    'name': 'USB-C Hub',
    'ports': 7
})
```

Items have no enforced schema beyond the key attributes. `prod-001` and `prod-002` coexist in the same table with entirely different non-key attribute sets.

### Listing Tables

```python
# Via resource
tables = list(dynamodb.tables.all())
for t in tables:
    print(t.name, t.table_status)

# Via client (returns names only)
client = boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1', aws_access_key_id='local', aws_secret_access_key='local')
response = client.list_tables()
print(response['TableNames'])
```

## Code Comparison

**JavaScript (AWS SDK v3 DocumentClient)**
```javascript
const { CreateTableCommand } = require('@aws-sdk/client-dynamodb');
const { PutCommand } = require('@aws-sdk/lib-dynamodb');

// Table creation via DynamoDBClient
await client.send(new CreateTableCommand({
    TableName: 'products',
    KeySchema: [{ AttributeName: 'product_id', KeyType: 'HASH' }],
    AttributeDefinitions: [{ AttributeName: 'product_id', AttributeType: 'S' }],
    BillingMode: 'PAY_PER_REQUEST'
}));

// Item write via DocumentClient (native JS types)
await docClient.send(new PutCommand({
    TableName: 'products',
    Item: { product_id: 'prod-001', name: 'Wireless Keyboard', price: 79.99 }
}));
```

**Python (boto3 resource)**
```python
# Table creation
table = dynamodb.create_table(
    TableName='products',
    KeySchema=[{'AttributeName': 'product_id', 'KeyType': 'HASH'}],
    AttributeDefinitions=[{'AttributeName': 'product_id', 'AttributeType': 'S'}],
    BillingMode='PAY_PER_REQUEST'
)
table.wait_until_exists()

# Item write (native Python types)
table.put_item(Item={
    'product_id': 'prod-001',
    'name': 'Wireless Keyboard',
    'price': 79.99
})
```

The `resource` layer eliminates the `DynamoDBDocumentClient` wrapper requirement present in the JavaScript SDK -- native type marshalling is built into the `Table` abstraction.

## Documentation
- [boto3 DynamoDB: Working with Tables](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#creating-a-new-table)
- [DynamoDB Core Components (AWS Docs)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html)
