# Feature Request: Middleware, Configuration, and Test Suite

## Context

The product catalog API is functionally complete: Flask routing (Day 1), DynamoDB persistence (Day 2), Pydantic validation and error handling (Day 3). Today's iteration adds the operational layer that would be required before any real deployment: structured request lifecycle hooks, externalized configuration, CORS support for browser clients, and an automated test suite using `moto` to mock DynamoDB.

At the end of today, the repository must contain:
- Request logging via `@app.before_request` / `@app.after_request`
- All configuration sourced from environment variables and loaded into `app.config`
- CORS enabled via `flask-cors`
- A `pytest` test suite in `tests/` that covers all five endpoints with mocked DynamoDB via `moto`

No new routes. No schema changes. No new database operations.

---

## Technical Requirements

### 1. Request Lifecycle Hooks

Register `@app.before_request` and `@app.after_request` hooks in `create_app()`. These execute before and after every request handled by the application, in the same way Express's `app.use()` middleware functions execute in the pipeline for every request.

Add the hooks inside `create_app()`, after Blueprint registration but before `return app`:

```python
import time
import logging
from flask import request, g

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inside create_app():

@app.before_request
def log_request_start():
    g.start_time = time.time()
    logger.info('Request started: %s %s', request.method, request.path)

@app.after_request
def log_request_end(response):
    duration_ms = (time.time() - g.start_time) * 1000
    logger.info(
        'Request completed: %s %s -> %d (%.2fms)',
        request.method,
        request.path,
        response.status_code,
        duration_ms
    )
    return response
```

`g` is Flask's per-request context storage object. `g.start_time` is set in `before_request` and read in `after_request` -- both hooks share the same `g` instance for a given request.

`@after_request` functions must accept the `Response` object as a parameter and return it. Omitting the return terminates the response.

**Node.js Map:** `app.use((req, res, next) => { ... next(); })` -> `@app.before_request`. `res.on('finish', () => {...})` -> `@app.after_request`. Express's `req` -> Flask's `g` for within-request storage.

---

### 2. CORS Configuration

Install `flask-cors`:

```bash
pip install flask-cors
pip freeze > requirements.txt
```

Add the following to `.env`:

```
CORS_ORIGIN=http://localhost:3000
```

Enable CORS in `create_app()`, after the app object is created and configured but before Blueprint registration:

```python
from flask_cors import CORS

# Inside create_app():
cors_origin = os.environ.get('CORS_ORIGIN', '*')
CORS(app, origins=[cors_origin])
```

Reading the allowed origin from an environment variable is required. In production, `CORS_ORIGIN` points to the deployed frontend URL.

**Node.js Map:** `app.use(cors({ origin: process.env.CORS_ORIGIN }))` -> `CORS(app, origins=[os.environ.get('CORS_ORIGIN')])`.

---

### 3. Configuration Audit

Review `app/__init__.py`. Every value that varies between environments must be sourced from `os.environ` and loaded into `app.config`. The complete set of required keys:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
DYNAMODB_TABLE
DYNAMODB_ENDPOINT_URL  (optional -- absent in production)
CORS_ORIGIN
SECRET_KEY
```

Use `os.environ['KEY']` (bracket notation) for required keys so that the application fails fast at startup if a variable is missing. Use `os.environ.get('KEY', default)` only for keys with acceptable fallback values (`DYNAMODB_ENDPOINT_URL`, `CORS_ORIGIN`).

Add `SECRET_KEY` to `.env` with any non-empty string value. Flask uses `SECRET_KEY` for session signing. Its absence generates a warning.

---

### 4. Test Suite Setup

Install `pytest` and `moto`:

```bash
pip install pytest moto[dynamodb]
pip freeze > requirements.txt
```

Create the following structure:

```
week2-flask-api/
  tests/
    __init__.py
    conftest.py
    test_products.py
```

`tests/__init__.py` is an empty file that makes `tests/` a package.

---

### 5. Test Fixtures

In `tests/conftest.py`, define the fixtures using `moto`'s `mock_aws` context manager:

```python
# tests/conftest.py
import os
import pytest
import boto3
from moto import mock_aws
from app import create_app

@pytest.fixture(scope='function')
def aws_credentials():
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    os.environ['AWS_REGION'] = 'us-east-1'
    os.environ['DYNAMODB_TABLE'] = 'products'
    # DYNAMODB_ENDPOINT_URL intentionally absent -- moto intercepts boto3 calls

@pytest.fixture(scope='function')
def dynamodb_table(aws_credentials):
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.create_table(
            TableName='products',
            KeySchema=[{'AttributeName': 'product_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'product_id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        table.wait_until_exists()
        yield table

@pytest.fixture(scope='function')
def client(dynamodb_table):
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client
```

`mock_aws()` intercepts all `boto3` calls for the duration of the `with` block. Because `create_app()` is called inside the `mock_aws()` context (via the `client` fixture depending on `dynamodb_table`), the `boto3.resource()` call in the factory is intercepted and returns a mock resource backed by `moto`'s in-memory DynamoDB simulation.

Each test function receives a fresh `mock_aws()` context -- test state is never shared between tests.

**Node.js Map:** `jest.mock('../db')` -> `mock_aws()` context. `jest.spyOn(...).mockResolvedValue(...)` -> `moto` in-memory DynamoDB behavior. `beforeEach` table state -> per-function fixture scope.

---

### 6. Integration Tests

In `tests/test_products.py`, implement the following tests:

```python
def test_list_products_returns_200(client):
    response = client.get('/products/')
    assert response.status_code == 200
    assert 'products' in response.get_json()

def test_list_products_empty_on_fresh_table(client):
    data = client.get('/products/').get_json()
    assert data['products'] == []

def test_create_product_returns_201(client):
    response = client.post('/products/', json={
        'name': 'Wireless Keyboard',
        'price': 79.99
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'product_id' in data
    assert data['name'] == 'Wireless Keyboard'

def test_create_product_invalid_payload_returns_422(client):
    response = client.post('/products/', json={'name': '', 'price': -5.0})
    assert response.status_code == 422
    assert 'details' in response.get_json()

def test_get_product_found_returns_200(client):
    create_resp = client.post('/products/', json={'name': 'Hub', 'price': 29.99})
    product_id = create_resp.get_json()['product_id']

    response = client.get(f'/products/{product_id}')
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Hub'

def test_get_product_not_found_returns_404(client):
    response = client.get('/products/nonexistent-id')
    assert response.status_code == 404

def test_delete_product_returns_204(client):
    create_resp = client.post('/products/', json={'name': 'Mouse', 'price': 19.99})
    product_id = create_resp.get_json()['product_id']

    response = client.delete(f'/products/{product_id}')
    assert response.status_code == 204

def test_delete_product_not_found_returns_404(client):
    response = client.delete('/products/nonexistent-id')
    assert response.status_code == 404
```

Each test function must target a single behavior. Create-then-operate patterns (create a product, then get/delete it) are acceptable within a single test function. Do not share state between test functions via module-level variables.

---

### 7. Test Execution

Run the full test suite:

```bash
pytest tests/ -v
```

All tests must pass. DynamoDB Local does not need to be running -- `moto` provides the full DynamoDB simulation without a network connection.

---

## Definition of Done

- `@app.before_request` logs the HTTP method and path for every request. Verify in server output when running `flask --app app run --debug`.
- `@app.after_request` logs method, path, status code, and elapsed time in milliseconds.
- CORS headers are present on API responses. Verify with: `curl -H "Origin: http://localhost:3000" -I http://localhost:5000/products/` -- the response must include `Access-Control-Allow-Origin`.
- `CORS_ORIGIN` and `SECRET_KEY` are present in `.env` and loaded into `app.config`.
- All required environment variables are accessed with `os.environ['KEY']` (not `os.getenv`).
- `tests/conftest.py` defines the `aws_credentials`, `dynamodb_table`, and `client` fixtures using `mock_aws()`.
- `pytest tests/ -v` runs to completion with all tests passing and zero failures.
- The test suite does not make real network calls to DynamoDB Local or AWS -- confirm by stopping the Docker container and verifying tests still pass.
- `requirements.txt` reflects `flask-cors`, `pytest`, and `moto[dynamodb]`.
- Code is pushed to the organizational GitHub repository on the branch `feature/week2-middleware-tests`.
