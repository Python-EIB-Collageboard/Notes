# HTTP Endpoint Integration Tests

## Objective
Writing integration tests for Flask HTTP endpoints using `pytest` and the Flask test client, including fixture-based setup and Cosmos DB SDK mocking.

## JavaScript Equivalent
Supertest with Jest (`request(app).get('/users').expect(200)`), with Jest's `jest.mock()` or `jest.spyOn()` used to mock database calls.

## Implementation Details

Flask provides a built-in test client that simulates HTTP requests against the application without starting a network server. The client is obtained from the Flask app instance via `app.test_client()`. Combined with `pytest` fixtures, this enables fully isolated integration tests for each endpoint.

### Test Client Creation

The test client is created from a configured application instance. Tests operate against the same routing, middleware, and error handling as the production application. The difference is that external dependencies (the Cosmos DB SDK) are replaced with mocks.

```python
# tests/conftest.py
import pytest
from app import create_app

@pytest.fixture
def app():
    test_app = create_app()
    test_app.config['TESTING'] = True
    yield test_app

@pytest.fixture
def client(app):
    return app.test_client()
```

`TESTING = True` changes Flask's error propagation behavior: unhandled exceptions surface in tests rather than being caught by Flask's internal error handler.

### Basic GET Request

```python
# tests/test_products.py

def test_list_products_returns_200(client):
    response = client.get('/products/')
    assert response.status_code == 200

def test_list_products_returns_json(client):
    response = client.get('/products/')
    data = response.get_json()
    assert 'products' in data
```

`response.get_json()` deserializes the JSON body, equivalent to `response.json` in Supertest's response object.

### POST Request with JSON Body

```python
def test_create_product_returns_201(client):
    payload = {
        'name': 'Wireless Keyboard',
        'category': 'electronics',
        'price': 79.99
    }
    response = client.post(
        '/products/',
        json=payload  # Sets Content-Type: application/json and serializes payload
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Wireless Keyboard'
```

The `json=` parameter on test client methods is equivalent to `request(app).post('/').send(payload)` in Supertest -- it handles serialization and sets the correct `Content-Type` header automatically.

### Mocking the Cosmos DB SDK

Tests must not make real network calls to the Cosmos DB emulator. The SDK must be replaced with a mock. Use `unittest.mock.patch` (from the Python standard library) to substitute the SDK methods. `pytest` fixtures allow `patch` to be applied for the duration of a test:

```python
from unittest.mock import patch, MagicMock

def test_get_product_found(client):
    mock_item = {
        'id': 'item-001',
        'category': 'electronics',
        'name': 'Keyboard',
        'price': 79.99
    }

    # Patch the read_item method on the container stored on app
    with patch.object(client.application.cosmos_container, 'read_item', return_value=mock_item):
        response = client.get('/products/item-001?category=electronics')

    assert response.status_code == 200
    assert response.get_json()['name'] == 'Keyboard'

def test_get_product_not_found(client):
    from azure.cosmos import exceptions

    not_found_error = exceptions.CosmosResourceNotFoundError(
        message="Not found",
        response=MagicMock(status_code=404)
    )

    with patch.object(client.application.cosmos_container, 'read_item', side_effect=not_found_error):
        response = client.get('/products/missing-id?category=electronics')

    assert response.status_code == 404
```

`patch.object(target, attribute, return_value=...)` replaces `target.attribute` with a `MagicMock` that returns `return_value` when called. `side_effect=exception_instance` causes the mock to raise the specified exception when called.

### Fixture-Based Mock Pattern

For tests requiring consistent mocks across multiple test functions, define mocks in a fixture:

```python
@pytest.fixture
def mock_container(app):
    mock = MagicMock()
    app.cosmos_container = mock
    return mock

def test_list_products(client, mock_container):
    mock_container.read_all_items.return_value = [
        {'id': '1', 'name': 'Keyboard', 'category': 'electronics'}
    ]
    response = client.get('/products/')
    assert response.status_code == 200
    assert len(response.get_json()['products']) == 1

def test_create_product(client, mock_container):
    mock_container.upsert_item.return_value = {
        'id': 'new-id', 'name': 'Mouse', 'category': 'electronics', 'price': 29.99
    }
    response = client.post('/products/', json={
        'name': 'Mouse',
        'category': 'electronics',
        'price': 29.99
    })
    assert response.status_code == 201
    mock_container.upsert_item.assert_called_once()
```

`assert_called_once()` and `assert_called_once_with(...)` verify that the mock was invoked with the expected arguments, equivalent to Jest's `expect(mockFn).toHaveBeenCalledWith(...)`.

### Test Execution

```bash
pytest tests/
pytest tests/ -v          # Verbose output
pytest tests/ -k "product" # Run only tests with 'product' in the name
```

## Code Comparison

**JavaScript (Jest + Supertest)**
```javascript
const request = require('supertest');
const app = require('../app');
const container = require('../data/container');

jest.mock('../data/container');

test('GET /products returns 200', async () => {
    container.read_all_items = jest.fn().mockResolvedValue([]);
    const res = await request(app).get('/products/');
    expect(res.status).toBe(200);
    expect(res.body).toHaveProperty('products');
});
```

**Python (pytest + Flask test client)**
```python
from unittest.mock import patch

def test_list_products(client, mock_container):
    mock_container.read_all_items.return_value = []
    response = client.get('/products/')
    assert response.status_code == 200
    assert 'products' in response.get_json()
```

Both patterns: create the app, replace the database dependency with a mock, make an HTTP request, assert on the response. The Flask test client and `unittest.mock` provide the same capability as Supertest and Jest mocks -- with synchronous execution rather than `async/await`.

## Documentation
- [Flask Testing](https://flask.palletsprojects.com/en/stable/testing/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
