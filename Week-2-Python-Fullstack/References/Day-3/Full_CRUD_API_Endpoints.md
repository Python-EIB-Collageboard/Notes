# Full CRUD API Endpoints

## Objective
The implementation of complete Create, Read, Update, and Delete HTTP endpoints in a Flask application wired to a Cosmos DB container via a data-access module.

## JavaScript Equivalent
A complete Express router with `POST`, `GET`, `PUT`/`PATCH`, and `DELETE` handlers wired to a database client module.

## Implementation Details

This topic covers the integration layer between the Flask routing system (established in Day 1) and the Cosmos DB SDK operations (established in Day 2). The pattern follows a layered architecture: Flask routes delegate to a separate data-access module rather than embedding SDK calls directly in view functions.

### Data-Access Module Structure

Isolate all Cosmos DB operations in a dedicated module. View functions call these functions rather than interacting with the SDK directly.

```python
# data/products.py
from azure.cosmos import ContainerProxy, exceptions
from typing import Optional

def get_all_products(container: ContainerProxy) -> list[dict]:
    return list(container.read_all_items())

def get_product_by_id(container: ContainerProxy, product_id: str, category: str) -> Optional[dict]:
    try:
        return container.read_item(item=product_id, partition_key=category)
    except exceptions.CosmosResourceNotFoundError:
        return None

def create_product(container: ContainerProxy, product_data: dict) -> dict:
    return container.upsert_item(product_data)

def update_product(container: ContainerProxy, product_id: str, category: str, updated_data: dict) -> Optional[dict]:
    try:
        existing = container.read_item(item=product_id, partition_key=category)
        existing.update(updated_data)
        return container.replace_item(item=product_id, body=existing)
    except exceptions.CosmosResourceNotFoundError:
        return None

def delete_product(container: ContainerProxy, product_id: str, category: str) -> bool:
    try:
        container.delete_item(item=product_id, partition_key=category)
        return True
    except exceptions.CosmosResourceNotFoundError:
        return False
```

### Flask Route Integration

Access the container from the Flask application context (`current_app`) to avoid passing it as a module-level global:

```python
# products/routes.py
import uuid
from flask import Blueprint, request, current_app
from data.products import (
    get_all_products, get_product_by_id,
    create_product, update_product, delete_product
)

products_bp = Blueprint('products', __name__, url_prefix='/products')

def get_container():
    return current_app.cosmos_container

@products_bp.get('/')
def list_products():
    products = get_all_products(get_container())
    return {'products': products}, 200

@products_bp.get('/<string:product_id>')
def get_product(product_id):
    category = request.args.get('category')
    if not category:
        return {'error': 'category query parameter required'}, 400

    product = get_product_by_id(get_container(), product_id, category)
    if product is None:
        return {'error': 'Product not found'}, 404

    return product, 200

@products_bp.post('/')
def add_product():
    payload = request.get_json()
    if not payload:
        return {'error': 'JSON body required'}, 400

    payload.setdefault('id', str(uuid.uuid4()))
    created = create_product(get_container(), payload)
    return created, 201

@products_bp.put('/<string:product_id>')
def update_product_endpoint(product_id):
    payload = request.get_json()
    if not payload:
        return {'error': 'JSON body required'}, 400

    category = payload.get('category')
    if not category:
        return {'error': 'category required in body'}, 400

    result = update_product(get_container(), product_id, category, payload)
    if result is None:
        return {'error': 'Product not found'}, 404

    return result, 200

@products_bp.delete('/<string:product_id>')
def delete_product_endpoint(product_id):
    category = request.args.get('category')
    if not category:
        return {'error': 'category query parameter required'}, 400

    deleted = delete_product(get_container(), product_id, category)
    if not deleted:
        return {'error': 'Product not found'}, 404

    return '', 204
```

### Route-to-HTTP Method Mapping

| HTTP Method | Flask Decorator | Cosmos DB Operation | Success Status |
|-------------|----------------|---------------------|----------------|
| `GET` (collection) | `@bp.get('/')` | `read_all_items()` | `200` |
| `GET` (single) | `@bp.get('/<id>')` | `read_item()` | `200` |
| `POST` | `@bp.post('/')` | `upsert_item()` | `201` |
| `PUT` | `@bp.put('/<id>')` | `replace_item()` | `200` |
| `DELETE` | `@bp.delete('/<id>')` | `delete_item()` | `204` |

### Partition Key in REST Endpoints

Cosmos DB's partition key requirement surfaces as an API design constraint. For `GET` and `DELETE` single-item operations, the partition key value must be provided by the caller. The common patterns are:

- **Query parameter:** `GET /products/item-001?category=electronics`
- **URL segment:** `GET /products/electronics/item-001` (partition key as a path segment)
- **Request header:** `X-Partition-Key: electronics`

For the exercise, the query parameter pattern is sufficient and the most transparent.

## Code Comparison

**JavaScript (Express + Cosmos SDK)**
```javascript
router.get('/:id', async (req, res) => {
    const { id } = req.params;
    const { category } = req.query;
    try {
        const { resource } = await container.item(id, category).read();
        res.json(resource);
    } catch (err) {
        if (err.code === 404) return res.status(404).json({ error: 'Not found' });
        throw err;
    }
});
```

**Python (Flask + azure-cosmos)**
```python
@products_bp.get('/<string:product_id>')
def get_product(product_id):
    category = request.args.get('category')
    product = get_product_by_id(get_container(), product_id, category)
    if product is None:
        return {'error': 'Not found'}, 404
    return product, 200
```

Flask's synchronous model eliminates `async/await` and `try/except` from the route layer when error handling is delegated to the data-access module.

## Documentation
- [Flask Routing](https://flask.palletsprojects.com/en/stable/quickstart/#routing)
- [azure-cosmos: ContainerProxy](https://learn.microsoft.com/en-us/python/api/azure-cosmos/azure.cosmos.containerproxy)
