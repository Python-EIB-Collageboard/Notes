# Query and Scan Operations

## Objective
The two DynamoDB multi-item read operations -- `query` and `scan` -- their performance characteristics, filtering mechanics, and the correct selection criteria between them.

## JavaScript Equivalent
There is no direct Express/Node.js equivalent. The closest conceptual mapping is the difference between a MongoDB indexed query (`collection.find({ userId: 'x' })`) and a full collection scan (`collection.find({})`). In DynamoDB, `query` targets a specific partition; `scan` reads every item in the table.

## Implementation Details

### scan

`scan` reads every item in the table and optionally applies a `FilterExpression` to the results client-side. It is the operational equivalent of `SELECT * FROM table WHERE ...` in a relational database -- the filter does not reduce the number of items read from storage, only the number returned to the caller.

```python
# Unfiltered scan -- returns all items
response = table.scan()
items = response['Items']
```

With a `FilterExpression`:

```python
from boto3.dynamodb.conditions import Attr

response = table.scan(
    FilterExpression=Attr('price').lt(100) & Attr('in_stock').eq(True)
)
items = response['Items']
```

`Attr` is imported from `boto3.dynamodb.conditions`. It constructs condition expressions for attribute values. Operators: `.eq()`, `.ne()`, `.lt()`, `.lte()`, `.gt()`, `.gte()`, `.begins_with()`, `.between()`, `.exists()`, `.not_exists()`, `.contains()`.

`FilterExpression` reduces the items returned in the response but does **not** reduce read capacity consumed. All items in the table are read regardless of the filter.

### Pagination

DynamoDB returns at most 1 MB of data per API call. When the result set exceeds this, the response contains a `LastEvaluatedKey`. The next page is fetched by passing `ExclusiveStartKey`:

```python
def scan_all(table, filter_expression=None) -> list[dict]:
    kwargs = {}
    if filter_expression:
        kwargs['FilterExpression'] = filter_expression

    items = []
    while True:
        response = table.scan(**kwargs)
        items.extend(response['Items'])
        last_key = response.get('LastEvaluatedKey')
        if not last_key:
            break
        kwargs['ExclusiveStartKey'] = last_key

    return items
```

This pattern is equivalent to cursor-based pagination in MongoDB (`cursor.hasNext()` / `cursor.next()`).

### query

`query` retrieves all items with a specific partition key value. It operates only on a single partition and can optionally apply a `KeyConditionExpression` on the sort key to narrow the result set within that partition.

`query` is dramatically more efficient than `scan` for single-partition access patterns: it reads only the target partition rather than the entire table.

```python
from boto3.dynamodb.conditions import Key

# All items with category = 'electronics'
response = table.query(
    KeyConditionExpression=Key('category').eq('electronics')
)
items = response['Items']
```

With a sort key condition:

```python
# Items in 'electronics' where product_id begins with 'prod-'
response = table.query(
    KeyConditionExpression=(
        Key('category').eq('electronics') &
        Key('product_id').begins_with('prod-')
    )
)
items = response['Items']
```

`Key` (from `boto3.dynamodb.conditions`) constructs key condition expressions. Only key attributes may be used in `KeyConditionExpression`. Non-key attributes require a separate `FilterExpression`.

### query vs scan Decision Rule

| Use | When |
|-----|------|
| `query` | You know the partition key value -- preferred for all production access patterns |
| `scan` | You need all items in the table, or the access pattern cannot target a specific partition |

A table design that requires `scan` with a `FilterExpression` for common access patterns is a signal that the key design does not match the access patterns. In production, `scan` on large tables is expensive and slow. In the Flask API being built this week, `query` is preferred whenever the client provides a partition key value.

## Code Comparison

**JavaScript (AWS SDK v3)**
```javascript
const { QueryCommand, ScanCommand } = require('@aws-sdk/lib-dynamodb');

// scan
const scanResult = await docClient.send(new ScanCommand({
    TableName: 'products',
    FilterExpression: 'price < :maxPrice',
    ExpressionAttributeValues: { ':maxPrice': 100 }
}));

// query
const queryResult = await docClient.send(new QueryCommand({
    TableName: 'products',
    KeyConditionExpression: 'category = :cat',
    ExpressionAttributeValues: { ':cat': 'electronics' }
}));
```

**Python (boto3 resource)**
```python
from boto3.dynamodb.conditions import Key, Attr

# scan
response = table.scan(
    FilterExpression=Attr('price').lt(100)
)
items = response['Items']

# query
response = table.query(
    KeyConditionExpression=Key('category').eq('electronics')
)
items = response['Items']
```

The `boto3` resource uses the `Key` and `Attr` condition builder objects rather than raw expression strings. The condition builder is the `boto3` equivalent of the AWS SDK v3's expression string + `ExpressionAttributeValues` pattern -- it constructs both automatically.

## Documentation
- [boto3 DynamoDB: Querying and Scanning](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#querying-and-scanning)
- [DynamoDB Query API Reference](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html)
