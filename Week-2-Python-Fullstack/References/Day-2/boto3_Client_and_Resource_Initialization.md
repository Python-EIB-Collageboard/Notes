# boto3 Client and Resource Initialization

## Objective
The two boto3 abstraction layers for interacting with DynamoDB -- the low-level `client` and the higher-level `resource` -- and the configuration parameters required to initialize either against a local or production endpoint.

## JavaScript Equivalent
The AWS SDK v3 for JavaScript uses a `DynamoDBClient` for low-level API calls and a `DynamoDBDocumentClient` wrapper for higher-level document operations. The `boto3` `client`/`resource` split maps directly to this pattern.

## Implementation Details

`boto3` exposes two distinct abstraction layers for every AWS service:

| Layer | boto3 | AWS SDK v3 (JS) |
|-------|-------|-----------------|
| Low-level | `boto3.client('dynamodb')` | `DynamoDBClient` |
| High-level | `boto3.resource('dynamodb')` | `DynamoDBDocumentClient` |

### The Low-Level Client

`boto3.client('dynamodb')` maps directly to the DynamoDB HTTP API. All request and response data uses DynamoDB's **AttributeValue** type descriptor format, where every value is wrapped in a type tag dict.

```python
import boto3

client = boto3.client(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id='local',
    aws_secret_access_key='local',
    endpoint_url='http://localhost:8000'
)

# All values require explicit type descriptors
response = client.put_item(
    TableName='products',
    Item={
        'product_id': {'S': 'prod-001'},
        'name':       {'S': 'Wireless Keyboard'},
        'price':      {'N': '79.99'}
    }
)
```

The type descriptor format (`{'S': ...}`, `{'N': ...}`, `{'BOOL': ...}`, `{'L': ...}`, `{'M': ...}`) is verbose and error-prone. It mirrors exactly what the DynamoDB service receives over the wire.

### The High-Level Resource

`boto3.resource('dynamodb')` provides a `Table` abstraction that handles type descriptor serialization and deserialization automatically. Python native types -- `str`, `int`, `float`, `bool`, `list`, `dict` -- are used directly.

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

# Native Python types -- no type descriptors required
table.put_item(Item={
    'product_id': 'prod-001',
    'name': 'Wireless Keyboard',
    'price': 79.99
})
```

`dynamodb.Table('products')` returns a `Table` resource object. This call does not make a network request -- it is a local reference. The network call occurs only when an operation method (`put_item`, `get_item`, etc.) is invoked.

### Configuration Parameters

| Parameter | Purpose | Production value |
|-----------|---------|-----------------|
| `region_name` | AWS region for signing and endpoint resolution | `'us-east-1'` or equivalent |
| `aws_access_key_id` | AWS credential | IAM key or instance role (omit to use default credential chain) |
| `aws_secret_access_key` | AWS credential | IAM secret (omit to use default credential chain) |
| `endpoint_url` | Override service endpoint | `None` (omit entirely) |

In production, credentials are sourced automatically from the AWS credential chain (environment variables, `~/.aws/credentials`, EC2 instance role, ECS task role). Explicit `aws_access_key_id` and `aws_secret_access_key` parameters are only required when the default chain is unavailable or must be bypassed.

### Recommended Pattern for Flask Applications

Initialize a single `dynamodb.resource` in the application factory and attach the `Table` reference to the `app` object. This prevents re-initialization on every request.

```python
import os
import boto3
from flask import Flask

def create_app():
    app = Flask(__name__)

    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.environ['AWS_REGION'],
        endpoint_url=os.environ.get('DYNAMODB_ENDPOINT_URL')
    )
    app.table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    return app
```

Table access in route handlers:

```python
from flask import current_app

def get_table():
    return current_app.table
```

Database client lifecycle management is covered in Day 3.

## Code Comparison

**JavaScript (AWS SDK v3)**
```javascript
const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient } = require('@aws-sdk/lib-dynamodb');

const client = new DynamoDBClient({
    region: 'us-east-1',
    endpoint: 'http://localhost:8000',
    credentials: { accessKeyId: 'local', secretAccessKey: 'local' }
});

// DocumentClient handles marshalling/unmarshalling of native JS types
const docClient = DynamoDBDocumentClient.from(client);
```

**Python (boto3)**
```python
import boto3

# resource() is the equivalent of DynamoDBDocumentClient --
# native Python types, no manual marshalling required.
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id='local',
    aws_secret_access_key='local',
    endpoint_url='http://localhost:8000'
)

table = dynamodb.Table('products')
```

## Documentation
- [boto3 DynamoDB Resource Guide](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html)
- [boto3 DynamoDB.ServiceResource.Table](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/index.html)
