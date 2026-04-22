# Partition and Sort Keys

## Objective
The DynamoDB primary key model -- partition keys, sort keys, and composite keys -- and their effect on item addressing, data distribution, and query capability.

## JavaScript Equivalent
There is no direct JavaScript equivalent. Relational databases use surrogate primary keys. MongoDB uses a single `_id` field. DynamoDB's primary key model determines both the physical location of data and the queries that are possible without a full table scan.

## Implementation Details

Every DynamoDB table requires a primary key defined at creation time. The primary key is immutable after table creation. There are two structures:

| Key Type | Components | Access Pattern |
|----------|-----------|---------------|
| Simple | Partition key only | Point read by partition key |
| Composite | Partition key + Sort key | Point read by both; range queries on sort key within a partition |

### Partition Key

The partition key value is hashed to determine which DynamoDB partition stores the item. When a table uses only a partition key, each value must be unique across the table.

```python
# Simple partition key
table = dynamodb.create_table(
    TableName='sessions',
    KeySchema=[{'AttributeName': 'session_id', 'KeyType': 'HASH'}],
    AttributeDefinitions=[{'AttributeName': 'session_id', 'AttributeType': 'S'}],
    BillingMode='PAY_PER_REQUEST'
)

# Point read -- requires only the partition key
response = table.get_item(Key={'session_id': 'abc-123'})
item = response.get('Item')  # None if not found
```

### Sort Key

A composite primary key adds a sort key (`'RANGE'`). Uniqueness is enforced by the combination of partition key + sort key. Items sharing a partition key are stored together, sorted by sort key, enabling range-based queries within a partition.

```python
table = dynamodb.create_table(
    TableName='products',
    KeySchema=[
        {'AttributeName': 'category',   'KeyType': 'HASH'},
        {'AttributeName': 'product_id', 'KeyType': 'RANGE'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'category',   'AttributeType': 'S'},
        {'AttributeName': 'product_id', 'AttributeType': 'S'}
    ],
    BillingMode='PAY_PER_REQUEST'
)
table.wait_until_exists()
```

With this key structure, `('electronics', 'prod-001')` and `('electronics', 'prod-002')` are distinct items with the same partition key. `('clothing', 'prod-001')` is a distinct item with the same sort key value but a different partition.

### Point Read with Composite Key

`get_item` requires both key attributes when the table has a composite key:

```python
response = table.get_item(
    Key={
        'category': 'electronics',
        'product_id': 'prod-001'
    }
)
item = response.get('Item')
```

Omitting either key attribute raises a `ClientError` with `ValidationException`.

### Key Attribute Type Constraints

Key attributes must use one of three attribute types:

| Code | Type | Python types |
|------|------|-------------|
| `'S'` | String | `str` |
| `'N'` | Number | `int`, `float`, `Decimal` |
| `'B'` | Binary | `bytes` |

`bool`, `list`, `dict`, and `None` cannot be key attributes.

### Partition Key Cardinality

High-cardinality partition key values (UUIDs, user IDs) distribute items evenly across partitions. Low-cardinality values (e.g., a boolean flag or a small set of status strings) concentrate load on a single partition, degrading throughput under load.

```python
import uuid

item = {
    'product_id': str(uuid.uuid4()),  # High cardinality -- preferred
    'name': 'Wireless Keyboard',
    'price': 79.99
}
table.put_item(Item=item)
```

## Code Comparison

**JavaScript (AWS SDK v3)**
```javascript
await client.send(new CreateTableCommand({
    TableName: 'products',
    KeySchema: [
        { AttributeName: 'category',   KeyType: 'HASH' },
        { AttributeName: 'product_id', KeyType: 'RANGE' }
    ],
    AttributeDefinitions: [
        { AttributeName: 'category',   AttributeType: 'S' },
        { AttributeName: 'product_id', AttributeType: 'S' }
    ],
    BillingMode: 'PAY_PER_REQUEST'
}));

const result = await docClient.send(new GetCommand({
    TableName: 'products',
    Key: { category: 'electronics', product_id: 'prod-001' }
}));
```

**Python (boto3)**
```python
table = dynamodb.create_table(
    TableName='products',
    KeySchema=[
        {'AttributeName': 'category',   'KeyType': 'HASH'},
        {'AttributeName': 'product_id', 'KeyType': 'RANGE'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'category',   'AttributeType': 'S'},
        {'AttributeName': 'product_id', 'AttributeType': 'S'}
    ],
    BillingMode='PAY_PER_REQUEST'
)
table.wait_until_exists()

response = table.get_item(
    Key={'category': 'electronics', 'product_id': 'prod-001'}
)
item = response.get('Item')
```

## Documentation
- [DynamoDB Primary Key (AWS Docs)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html#HowItWorks.CoreComponents.PrimaryKey)
- [boto3 DynamoDB Table.get_item](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/get_item.html)
