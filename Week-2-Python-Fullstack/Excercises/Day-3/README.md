# Feature Request: Integrated CRUD API with Validation

## Context

The data-access module (`app/data/products.py`) was built and validated in isolation on Day 2. The Flask routes (`app/products/routes.py`) still use the in-memory list from Day 1. Today those two layers are connected.

This iteration has three distinct tasks:

1. **Wire the database** -- replace the in-memory list in the route layer with calls to `app/data/products.py`, initializing the `boto3` resource in the application factory.
2. **Add Pydantic validation** -- enforce a typed schema on all write endpoints before any data reaches the database.
3. **Centralize error handling** -- register a Flask application-level error handler for `botocore.exceptions.ClientError` so that unhandled SDK exceptions produce structured JSON responses automatically.

The Day 1 response envelope contract (`{ "products": [...] }`, `{ "error": "..." }`) must be preserved. The Day 2 data-access function signatures must not be changed.

---

## Technical Requirements

### 1. Application Factory: Client Initialization

Modify `app/__init__.py` to initialize the `boto3` resource and attach the `Table` reference to the `app` object. The `Table` object is initialized once at startup, not per request.

```python
# app/__init__.py
import os
import boto3
from flask import Flask
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config['AWS_REGION'] = os.environ['AWS_REGION']
    app.config['DYNAMODB_TABLE'] = os.environ['DYNAMODB_TABLE']

    dynamodb = boto3.resource(
        'dynamodb',
        region_name=app.config['AWS_REGION'],
        endpoint_url=os.environ.get('DYNAMODB_ENDPOINT_URL')
    )
    app.table = dynamodb.Table(app.config['DYNAMODB_TABLE'])

    from .products.routes import products_bp
    app.register_blueprint(products_bp)

    return app
```

`app.table` is the single `Table` instance used by all routes. It is attached to the app object so that each call to `create_app()` (including in tests) produces an isolated instance.

**Node.js Map:** `DynamoDBClient()` in `createServer()`, attaching `DynamoDBDocumentClient` to `app.locals` -> `boto3.resource()` in `create_app()`, attaching `Table` to `app.table`.

---

### 2. Route Layer: Replace In-Memory Store

Remove `_products: list[dict] = []` from `app/products/routes.py`. Replace all references to `_products` with calls to the data-access functions from `app/data/products.py`.

Add a helper at the top of `routes.py` to retrieve the table from the application context:

```python
from flask import current_app

def get_table():
    return current_app.table
```

`current_app` is Flask's proxy to the active application instance. It is only valid inside a request context, which is always the case inside a view function.

Update each view function to call the corresponding data-access function:

| View Function | Data-Access Call |
|---------------|-----------------|
| `list_products()` | `get_all_products(get_table())` |
| `get_product(product_id)` | `get_product_by_id(get_table(), product_id)` |
| `add_product()` | `create_product(get_table(), validated_payload)` |
| `update_product_endpoint(product_id)` | `update_product(get_table(), product_id, validated_payload)` |
| `delete_product_endpoint(product_id)` | `delete_product(get_table(), product_id)` |

For `GET /products/<id>`: return `404` when `get_product_by_id()` returns `None`.
For `PUT /products/<id>`: return `404` when `update_product()` returns `None`.
For `DELETE /products/<id>`: return `204` on `True`, `404` on `False`.

---

### 3. Pydantic Models

Install Pydantic v2:

```bash
pip install pydantic
pip freeze > requirements.txt
```

Create `app/products/schemas.py`. Define two models:

```python
# app/products/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    price: float = Field(gt=0)
    description: Optional[str] = None
    tags: list[str] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    price: Optional[float] = Field(default=None, gt=0)
    description: Optional[str] = None
    tags: Optional[list[str]] = None
```

`ProductCreate` is used on `POST /products/`. `name` and `price` are required.

`ProductUpdate` is used on `PUT /products/<id>`. All fields are optional -- the update merges into the existing document via `update_item`.

Apply validation in the view functions:

```python
from pydantic import ValidationError
from .schemas import ProductCreate, ProductUpdate

@products_bp.post('/')
def add_product():
    payload = request.get_json()
    if payload is None:
        return {'error': 'JSON body required'}, 400

    try:
        validated = ProductCreate(**payload)
    except ValidationError as e:
        return {'error': 'Validation failed', 'details': e.errors()}, 422

    product_data = validated.model_dump(exclude_none=True)
    created = create_product(get_table(), product_data)
    return created, 201
```

Apply the same pattern to `PUT /products/<id>` using `ProductUpdate`. Pass `validated.model_dump(exclude_none=True)` as `updated_fields` to `update_product()`.

**Node.js Map:** `schema.parse(req.body)` (Zod) -> `ProductCreate(**payload)` with `ValidationError` catch. `result.error.issues` -> `e.errors()`. `result.data` -> `validated.model_dump()`.

---

### 4. Centralized ClientError Handler

Register an application-level error handler in `create_app()` to catch any `ClientError` that escapes the data-access layer:

```python
# app/__init__.py (inside create_app(), after Blueprint registration)
from botocore.exceptions import ClientError

@app.errorhandler(ClientError)
def handle_dynamodb_error(e: ClientError):
    code = e.response['Error']['Code']
    status = e.response['ResponseMetadata']['HTTPStatusCode']
    return {
        'error': 'Database error',
        'code': code,
        'detail': e.response['Error']['Message']
    }, status
```

This handler fires for any `ClientError` not explicitly caught in a view function or data-access function. It is the equivalent of Express's centralized error middleware (`app.use((err, req, res, next) => {...})`).

With this handler in place, view functions only need explicit exception handling when they require custom behavior (e.g., returning `404` for a specific code rather than the generic database error format).

---

### 5. Manual Verification

Start the server (DynamoDB Local must be running):

```bash
flask --app app run --debug
```

Exercise all five endpoints:

1. `POST /products/` with `{ "name": "Wireless Keyboard", "price": 79.99 }` -- confirm `201` and a persisted `product_id`.
2. `POST /products/` with `{ "name": "", "price": 79.99 }` -- confirm `422` with validation details.
3. `GET /products/` -- confirm the item appears.
4. `GET /products/<product_id>` -- confirm the item is returned.
5. `PUT /products/<product_id>` with `{ "price": 89.99 }` -- confirm the price is updated.
6. `DELETE /products/<product_id>` -- confirm `204`.
7. `GET /products/<product_id>` -- confirm `404`.

---

## Definition of Done

- `app/__init__.py` initializes `boto3.resource` and attaches `app.table` to the application object.
- `app/products/routes.py` contains no references to the `_products` in-memory list.
- `app/products/schemas.py` defines `ProductCreate` and `ProductUpdate` with the specified fields and `Field()` constraints.
- `POST /products/` with an invalid payload returns `422` with a `details` array from `e.errors()`.
- All five endpoints exercise the DynamoDB Local emulator -- verify by running the manual verification steps.
- The centralized `ClientError` handler is registered on the app.
- `requirements.txt` reflects `pydantic`, `boto3`, and `python-dotenv`.
- Code is pushed to the organizational GitHub repository on the branch `feature/week2-dynamodb-integration`.
