# botocore ClientError Handling

## Objective
The structure and handling of `botocore.exceptions.ClientError` -- the single exception class raised for all DynamoDB service-level errors -- and the pattern for branching on specific error codes.

## JavaScript Equivalent
In the AWS SDK v3 for JavaScript, service errors are instances of `ServiceException` subclasses (e.g., `ResourceNotFoundException`, `ConditionalCheckFailedException`). Each has a `name` property matching the error code. The `botocore` `ClientError` is the Python equivalent: a single exception class that wraps all service errors, inspected via `e.response['Error']['Code']`.

## Implementation Details

### ClientError Structure

All DynamoDB service-level errors (validation errors, not-found errors, condition failures, throughput exceptions) are raised as `botocore.exceptions.ClientError`. The exception carries the raw HTTP response from DynamoDB in its `response` attribute.

```python
from botocore.exceptions import ClientError

try:
    response = table.get_item(Key={'product_id': 'missing'})
except ClientError as e:
    error_code = e.response['Error']['Code']
    error_message = e.response['Error']['Message']
    http_status = e.response['ResponseMetadata']['HTTPStatusCode']
    print(f'{error_code}: {error_message} (HTTP {http_status})')
```

`e.response['Error']['Code']` is the canonical identifier for branching. Common DynamoDB error codes:

| Code | Trigger |
|------|---------|
| `ResourceNotFoundException` | `get_item`, `put_item`, etc. called on a table that does not exist |
| `ConditionalCheckFailedException` | `ConditionExpression` not satisfied |
| `ValidationException` | Malformed request (missing key, wrong type) |
| `ProvisionedThroughputExceededException` | Read/write capacity exceeded (provisioned mode) |
| `ItemCollectionSizeLimitExceededException` | Item collection exceeds 10 GB (composite key tables) |

**Note:** `get_item` for a non-existent item does **not** raise `ClientError`. It returns a response with no `'Item'` key. `ClientError` is raised only for errors in the API call itself, not for logical "not found" results.

### Branching on Error Code

```python
from botocore.exceptions import ClientError

def get_item_safe(table, key: dict) -> dict | None:
    try:
        response = table.get_item(Key=key)
        return response.get('Item')
    except ClientError as e:
        code = e.response['Error']['Code']
        if code == 'ResourceNotFoundException':
            return None  # Table does not exist -- treat as not found
        raise  # Re-raise unexpected errors

def delete_item_confirmed(table, key: dict) -> bool:
    from boto3.dynamodb.conditions import Attr
    try:
        table.delete_item(
            Key=key,
            ConditionExpression=Attr(list(key.keys())[0]).exists()
        )
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return False
        raise
```

The pattern is: catch `ClientError`, inspect the code, handle known codes explicitly, re-raise anything unexpected. This is identical in intent to the Node.js pattern of inspecting `err.name` or `err.$metadata.httpStatusCode` in an AWS SDK v3 catch block.

### Flask Error Handler Integration

Register a Flask application-level error handler for `ClientError` to convert unhandled SDK errors into structured JSON responses without wrapping every view function in try/except.

```python
# app/__init__.py
from botocore.exceptions import ClientError

def create_app():
    app = Flask(__name__)
    # ... initialization ...

    @app.errorhandler(ClientError)
    def handle_dynamodb_error(e: ClientError):
        code = e.response['Error']['Code']
        status = e.response['ResponseMetadata']['HTTPStatusCode']
        return {
            'error': 'Database error',
            'code': code,
            'detail': e.response['Error']['Message']
        }, status

    return app
```

With this handler, any `ClientError` that escapes a view function or data-access function is caught at the application level and serialized as JSON. View functions only need explicit exception handling for codes that require custom behavior (e.g., returning `404` for a `ResourceNotFoundException` rather than a generic `500`).

### ValidationException

`ValidationException` is raised by DynamoDB when the request itself is malformed -- typically a missing key attribute or a type mismatch. This is a programming error, not a runtime condition.

```python
try:
    # Missing required partition key 'product_id'
    table.get_item(Key={'wrong_key': 'value'})
except ClientError as e:
    if e.response['Error']['Code'] == 'ValidationException':
        print('Request malformed:', e.response['Error']['Message'])
```

`ValidationException` in DynamoDB is equivalent to a `400 Bad Request` from a REST API. In a well-implemented data-access layer, Pydantic validation (covered in Day 3 Instructor Demo) prevents malformed requests from reaching the DynamoDB call.

## Code Comparison

**JavaScript (AWS SDK v3)**
```javascript
const { GetCommand } = require('@aws-sdk/lib-dynamodb');

try {
    const result = await docClient.send(new GetCommand({
        TableName: 'products',
        Key: { product_id: 'missing' }
    }));
    const item = result.Item ?? null;
} catch (err) {
    if (err.name === 'ResourceNotFoundException') {
        console.log('Table does not exist');
    } else {
        throw err;
    }
}
```

**Python (boto3)**
```python
from botocore.exceptions import ClientError

try:
    response = table.get_item(Key={'product_id': 'missing'})
    item = response.get('Item')  # None if key not found -- no exception raised
except ClientError as e:
    code = e.response['Error']['Code']
    if code == 'ResourceNotFoundException':
        print('Table does not exist')
    else:
        raise
```

The key behavioral difference: in both SDKs, a missing **item** (key exists in request, item absent in table) does not raise an exception -- the response simply lacks an `Item` field. A missing **table** raises a service error in both SDKs, inspected via `err.name` in JavaScript and `e.response['Error']['Code']` in Python.

## Documentation
- [botocore.exceptions.ClientError](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/exceptions.html)
- [DynamoDB Error Handling (AWS Docs)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Programming.Errors.html)
