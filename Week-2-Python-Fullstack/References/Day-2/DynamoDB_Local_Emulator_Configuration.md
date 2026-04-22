# DynamoDB Local Emulator Configuration

## Objective
Configuration and startup of the DynamoDB Local emulator via Docker and verification of a working connection using the `boto3` client with a custom endpoint URL.

## JavaScript Equivalent
Running a local DynamoDB instance is analogous to running a local MongoDB instance via Docker or MongoDB Atlas Local for development -- a network-accessible service whose endpoint you override in the SDK client rather than pointing at the production cloud endpoint.

## Implementation Details

DynamoDB Local is an official AWS-provided local emulation of the DynamoDB service distributed as a Docker image (`amazon/dynamodb-local`). It exposes the same HTTP API as the production service on a configurable local port (default: `8000`). No AWS account or credentials are required; any non-empty string values for `aws_access_key_id`, `aws_secret_access_key`, and `region_name` are accepted.

### Docker Startup

```bash
docker run -d \
  --name dynamodb-local \
  -p 8000:8000 \
  amazon/dynamodb-local \
  -jar DynamoDBLocal.jar -sharedDb
```

The `-sharedDb` flag forces DynamoDB Local to use a single database file regardless of the credentials passed, which simplifies development by ensuring all clients see the same state.

To confirm the container is running:

```bash
docker ps --filter name=dynamodb-local
```

### Endpoint Override in boto3

The production `boto3` DynamoDB client targets `https://dynamodb.<region>.amazonaws.com`. For local development, this endpoint is overridden via the `endpoint_url` parameter on the client or resource constructor. This is the single configuration change separating a local client from a production client.

```python
import boto3

# Local emulator client
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id='local',
    aws_secret_access_key='local',
    endpoint_url='http://localhost:8000'
)
```

The `region_name`, `aws_access_key_id`, and `aws_secret_access_key` values are arbitrary strings when targeting DynamoDB Local -- they are not validated. Using `'local'` is a common convention that makes intent explicit.

### Environment Variable Pattern

Hard-coding `endpoint_url` in application code violates the twelve-factor app configuration principle. The correct pattern is to read the endpoint from an environment variable and fall back to `None` (which causes `boto3` to use the production endpoint) when the variable is absent.

```python
import os
import boto3

endpoint_url = os.environ.get('DYNAMODB_ENDPOINT_URL')  # None in production

dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.environ['AWS_REGION'],
    endpoint_url=endpoint_url
)
```

In production, `DYNAMODB_ENDPOINT_URL` is unset, so `endpoint_url=None` causes `boto3` to resolve the endpoint from the region. In local development, `DYNAMODB_ENDPOINT_URL=http://localhost:8000` redirects all calls to the emulator. No code change is required between environments.

### Health Check

A lightweight connectivity check lists all tables. An empty list is a valid response for a fresh emulator instance; the absence of an exception confirms connectivity.

```python
def verify_connection(dynamodb_resource) -> bool:
    try:
        tables = list(dynamodb_resource.tables.all())
        print(f'Connection verified. Tables: {len(tables)}')
        return True
    except Exception as e:
        print(f'Connection failed: {e}')
        return False
```

## Code Comparison

**JavaScript (AWS SDK v3 for DynamoDB Local)**
```javascript
const { DynamoDBClient, ListTablesCommand } = require('@aws-sdk/client-dynamodb');

const client = new DynamoDBClient({
    region: 'us-east-1',
    endpoint: 'http://localhost:8000',
    credentials: { accessKeyId: 'local', secretAccessKey: 'local' }
});

async function verify() {
    const result = await client.send(new ListTablesCommand({}));
    console.log('Tables:', result.TableNames);
}
```

**Python (boto3)**
```python
import boto3

dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id='local',
    aws_secret_access_key='local',
    endpoint_url='http://localhost:8000'
)

tables = list(dynamodb.tables.all())
print('Tables:', [t.name for t in tables])
```

The structural difference is the `endpoint_url` parameter on the `boto3` resource constructor versus the `endpoint` property in the AWS SDK v3 `DynamoDBClient` config object. Both override the default service endpoint with no other code changes required.

## Documentation
- [DynamoDB Local (Amazon Documentation)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)
- [boto3 DynamoDB Resource](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html)
