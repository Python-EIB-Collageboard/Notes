# Feature Request: Database Provisioning and Standalone CRUD Script

## Context

Day 1 produced a Flask application with five working routes backed by an in-memory list. That list is disposable. Today you replace the persistence layer with a real database: a locally running Amazon DynamoDB instance via Docker.

The work splits into two distinct phases:

1. **Provision** -- start the DynamoDB Local emulator, configure the SDK client, and create the table programmatically.
2. **Implement** -- write a standalone data-access module with isolated functions for all CRUD operations, and verify them with a runner script before touching the Flask layer.

The Flask routes are **not modified today**. They still call the in-memory list. The database integration happens on Day 3. Today's goal is to build and validate the data layer in isolation, which is standard practice before wiring it into the HTTP layer.

---

## Technical Requirements

### 1. Emulator Setup

Start the DynamoDB Local Docker container:

```bash
docker run -d \
  --name dynamodb-local \
  -p 8000:8000 \
  amazon/dynamodb-local \
  -jar DynamoDBLocal.jar -sharedDb
```

Confirm it is running:

```bash
docker ps --filter name=dynamodb-local
```

Verify connectivity from Python before writing any application code:

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
print(f'Connected. Tables: {len(tables)}')
```

DynamoDB Local uses plain HTTP on port 8000. No TLS configuration is required.

---

### 2. Environment Variables

Install `python-dotenv`:

```bash
pip install python-dotenv boto3
pip freeze > requirements.txt
```

Create a `.env` file in `week2-flask-api/`:

```
AWS_ACCESS_KEY_ID=local
AWS_SECRET_ACCESS_KEY=local
AWS_REGION=us-east-1
DYNAMODB_ENDPOINT_URL=http://localhost:8000
DYNAMODB_TABLE=products
```

Confirm `.env` is listed in `.gitignore`. The credentials are arbitrary strings for the local emulator, but the pattern of externalizing all configuration must be established now. In production, `DYNAMODB_ENDPOINT_URL` is absent and real IAM credentials are used.

**Node.js Map:** `require('dotenv').config()` + `process.env.KEY` -> `load_dotenv()` + `os.environ['KEY']`.

---

### 3. Provisioning Script

Create `week2-flask-api/scripts/provision_table.py`. This script is a one-time setup utility. It must:

1. Load `.env` via `load_dotenv()`.
2. Initialize `boto3.resource('dynamodb', ...)` using `os.environ` values.
3. Create the `products` table with `product_id` (String) as the partition key and `BillingMode='PAY_PER_REQUEST'`.
4. Call `table.wait_until_exists()`.
5. Print a confirmation message.
6. Handle `ClientError` with code `ResourceInUseException` gracefully (table already exists).

```
week2-flask-api/
  scripts/
    provision_table.py
```

Run this script once before beginning the data-access module:

```bash
python scripts/provision_table.py
```

**Node.js Map:** Mongoose's schema definition + `mongoose.connect()` -> `dynamodb.create_table()` with `KeySchema` and `AttributeDefinitions`.

---

### 4. Data-Access Module

Create `week2-flask-api/app/data/products.py`. This module contains all `boto3` interactions for the products table. View functions will call these functions -- they will never interact with `boto3` directly.

Implement the following functions with the exact signatures below:

```python
# app/data/products.py
import uuid
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from typing import Optional

def get_all_products(table) -> list[dict]:
    """Return all items in the table via scan."""
    ...

def get_product_by_id(table, product_id: str) -> Optional[dict]:
    """
    Return the item matching product_id via get_item.
    Return None if the item does not exist (response has no 'Item' key).
    """
    ...

def create_product(table, product_data: dict) -> dict:
    """
    Assign a UUID to product_data['product_id'] if not present.
    Write via put_item. Return the product_data dict as written.
    """
    ...

def update_product(table, product_id: str, updated_fields: dict) -> Optional[dict]:
    """
    Build an UpdateExpression from updated_fields.
    Call update_item with ReturnValues='ALL_NEW'.
    Return the updated item dict.
    Return None if the item does not exist (use ConditionExpression).
    """
    ...

def delete_product(table, product_id: str) -> bool:
    """
    Delete the item. Return True on success.
    Return False if the item does not exist (ConditionalCheckFailedException).
    """
    ...
```

Type annotations are required. Use `Optional[dict]` (from `typing`) for functions that may return `None`. Use `list[dict]` for list returns.

For `get_product_by_id`: a missing item does **not** raise an exception. Check `response.get('Item')` -- it is `None` when absent.

For `delete_product`: use a `ConditionExpression=Attr('product_id').exists()` to detect non-existent items. Catch `ClientError` with code `ConditionalCheckFailedException` and return `False`.

For `update_product`: `update_item` with `ReturnValues='ALL_NEW'` returns `{'Attributes': {...}}`. Extract `response['Attributes']`.

---

### 5. Validation Runner Script

Create `week2-flask-api/scripts/test_data_access.py`. This script is not a `pytest` test -- it is a manual validation runner. It exercises each function in `app/data/products.py` against the live emulator and prints the results.

It must:

1. Load `.env` and initialize the `boto3.resource` and `Table` object.
2. Call `create_product()` with a sample payload. Print the returned dict -- confirm `product_id` is present.
3. Call `get_all_products()` and print the count.
4. Call `get_product_by_id()` with the new item's `product_id`. Confirm it is returned.
5. Call `update_product()` to change the `price` field. Print the returned updated item.
6. Call `delete_product()` and confirm `True` is returned.
7. Call `get_product_by_id()` again and confirm `None` is returned.
8. Call `delete_product()` on the already-deleted item and confirm `False` is returned.

```bash
python scripts/test_data_access.py
```

All eight steps must complete without exceptions and produce meaningful console output before Day 3 work begins.

---

## Definition of Done

- `scripts/provision_table.py` runs without error and confirms the `products` table exists in the emulator. Running it a second time prints "Table already exists" and does not raise an exception.
- `app/data/products.py` contains all five functions with correct type annotations.
- `scripts/test_data_access.py` runs to completion, exercising all five data-access functions against the live emulator.
- `get_product_by_id()` returns `None` (not an exception) when the item does not exist.
- `delete_product()` returns `True` on success and `False` for a non-existent item (confirm both cases in the runner).
- `requirements.txt` reflects `boto3` and `python-dotenv`.
- Code is pushed to the organizational GitHub repository on the branch `feature/week2-dynamodb-data-layer`.
