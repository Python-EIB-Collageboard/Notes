# CRUD Operations with the boto3 SDK

## Objective
The four core DynamoDB item operations -- Create, Read, Update, Delete -- using the `boto3` resource `Table` abstraction and their direct mapping to AWS SDK v3 equivalents.

## JavaScript Equivalent
The `boto3` `Table` methods map to the AWS SDK v3 `DynamoDBDocumentClient` commands: `PutCommand`, `GetCommand`, `UpdateCommand`, and `DeleteCommand`.

## Implementation Details

All examples assume a `Table` object initialized against the DynamoDB Local emulator with a `product_id` (String) partition key.

```python
import boto3

dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id='local',
    aws_secret_access_key='local',
    endpoint_url='http://localhost:8000'
)
table = dynamodb.Table('products')
```

### Create: `put_item`

`put_item` writes an item to the table. If an item with the same key already exists, it is replaced entirely.

```python
table.put_item(Item={
    'product_id': 'prod-001',
    'name': 'Wireless Keyboard',
    'price': 79.99,
    'in_stock': True,
    'tags': ['peripherals', 'wireless']
})
```

To write only when no item with that key exists, add a `ConditionExpression`:

```python
from boto3.dynamodb.conditions import Attr

table.put_item(
    Item={'product_id': 'prod-001', 'name': 'Keyboard', 'price': 79.99},
    ConditionExpression=Attr('product_id').not_exists()
)
```

If the condition fails, `botocore` raises `ClientError` with code `ConditionalCheckFailedException`.

### Read: `get_item`

`get_item` performs a point read -- the most efficient read operation in DynamoDB. It requires the complete primary key.

```python
response = table.get_item(Key={'product_id': 'prod-001'})
item = response.get('Item')  # None if the item does not exist
```

`response['Item']` is absent (not `None`) when the item does not exist. Use `.get('Item')` rather than `response['Item']` to avoid a `KeyError`.

### Update: `update_item`

`update_item` modifies specific attributes of an existing item without replacing the entire document. This is distinct from `put_item`, which replaces the item entirely.

```python
from boto3.dynamodb.conditions import Key

table.update_item(
    Key={'product_id': 'prod-001'},
    UpdateExpression='SET price = :new_price, in_stock = :stock',
    ExpressionAttributeValues={
        ':new_price': 89.99,
        ':stock': False
    },
    ReturnValues='UPDATED_NEW'
)
```

`UpdateExpression` uses a DSL with `SET`, `REMOVE`, `ADD`, and `DELETE` clauses. `:new_price` is an **expression attribute value placeholder** -- all literal values in expressions must be passed as placeholders to prevent injection and handle reserved word conflicts.

`ReturnValues='UPDATED_NEW'` returns only the attributes that were modified. `ReturnValues='ALL_NEW'` returns the full item after the update.

### Delete: `delete_item`

`delete_item` removes an item by primary key. It succeeds even if the item does not exist (idempotent by default).

```python
table.delete_item(Key={'product_id': 'prod-001'})
```

To confirm the item existed before deletion, use `ConditionExpression`:

```python
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

try:
    table.delete_item(
        Key={'product_id': 'prod-001'},
        ConditionExpression=Attr('product_id').exists()
    )
    deleted = True
except ClientError as e:
    if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
        deleted = False
    else:
        raise
```

## Code Comparison

**JavaScript (AWS SDK v3 DocumentClient)**
```javascript
const { PutCommand, GetCommand, UpdateCommand, DeleteCommand } = require('@aws-sdk/lib-dynamodb');

// Create
await docClient.send(new PutCommand({
    TableName: 'products',
    Item: { product_id: 'prod-001', name: 'Keyboard', price: 79.99 }
}));

// Read
const { Item } = await docClient.send(new GetCommand({
    TableName: 'products',
    Key: { product_id: 'prod-001' }
}));

// Update
await docClient.send(new UpdateCommand({
    TableName: 'products',
    Key: { product_id: 'prod-001' },
    UpdateExpression: 'SET price = :p',
    ExpressionAttributeValues: { ':p': 89.99 }
}));

// Delete
await docClient.send(new DeleteCommand({
    TableName: 'products',
    Key: { product_id: 'prod-001' }
}));
```

**Python (boto3 resource)**
```python
# Create
table.put_item(Item={'product_id': 'prod-001', 'name': 'Keyboard', 'price': 79.99})

# Read
response = table.get_item(Key={'product_id': 'prod-001'})
item = response.get('Item')

# Update
table.update_item(
    Key={'product_id': 'prod-001'},
    UpdateExpression='SET price = :p',
    ExpressionAttributeValues={':p': 89.99},
    ReturnValues='UPDATED_NEW'
)

# Delete
table.delete_item(Key={'product_id': 'prod-001'})
```

The `boto3` resource API eliminates the `Command` wrapper class pattern. Each operation is a direct method call on the `Table` object with keyword arguments. `UpdateExpression` and `ExpressionAttributeValues` are identical between the two SDKs.

## Documentation
- [boto3 DynamoDB: CRUD Operations](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#creating-a-new-item)
- [DynamoDB UpdateExpression Syntax](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html)
