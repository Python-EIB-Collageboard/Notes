# Pydantic Schema Validation

## Objective
Input validation and data modeling using Pydantic v2, including model definition, request payload parsing, and error serialization within a Flask view function.

## JavaScript Equivalent
Zod or Joi schema validation applied to `req.body` before processing; analogous to `schema.parse(req.body)` in Zod, which throws `ZodError` on invalid input.

## Implementation Details

Pydantic is a Python library for data validation using type annotations. A Pydantic model defines the expected structure and types of a data payload. When a `dict` is passed to the model constructor, Pydantic validates field types, applies coercion where permitted, and raises a `ValidationError` if the data does not conform. This is the Python equivalent of Zod's `parse()` or Joi's `validate()`.

### Installation

```bash
pip install pydantic
```

Pydantic v2 is the current major version. The syntax differs significantly from v1. All code in this topic uses v2.

### Model Definition

Pydantic models are classes that inherit from `pydantic.BaseModel`. Fields are declared as class attributes with type annotations. Python's standard type hints are used directly:

```python
from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    description: Optional[str] = None
    tags: list[str] = []
```

| Annotation | Behavior |
|------------|----------|
| `str` | Required field, must be a string |
| `Optional[str] = None` | Optional field, `None` if not provided |
| `list[str] = []` | Optional list field, defaults to empty list |
| `float` | Required field; Pydantic coerces `int` to `float` |

### Validation in Flask View Functions

Flask's `request.get_json()` returns a raw Python `dict`. Pass this directly to the Pydantic model constructor:

```python
from flask import Blueprint, request
from pydantic import BaseModel, ValidationError
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    description: Optional[str] = None

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.post('/')
def create_product():
    payload = request.get_json()

    if payload is None:
        return {'error': 'JSON body required'}, 400

    try:
        validated = ProductCreate(**payload)
    except ValidationError as e:
        return {'error': 'Validation failed', 'details': e.errors()}, 422

    # validated.model_dump() returns a plain dict for passing to the SDK
    product_data = validated.model_dump()
    product_data['id'] = str(uuid.uuid4())

    created = get_container().upsert_item(product_data)
    return created, 201
```

`ValidationError.errors()` returns a list of dicts describing each validation failure -- field name, error type, and message. This structure is directly serializable to JSON.

### Field Constraints with `Field()`

Pydantic's `Field()` function adds validation constraints beyond type checks:

```python
from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1)
    price: float = Field(gt=0)  # greater than 0
    quantity: int = Field(ge=0, default=0)  # greater than or equal to 0
```

| Constraint | Meaning |
|------------|---------|
| `min_length` / `max_length` | String length bounds |
| `gt` | Greater than (strict) |
| `ge` | Greater than or equal |
| `lt` / `le` | Less than / less than or equal |
| `pattern` | Regex pattern match |

### `model_dump()` -- Serialization

`model_dump()` converts the validated Pydantic model back to a plain `dict`, suitable for passing to the Cosmos DB SDK or any JSON serializer. This is the v2 replacement for v1's `.dict()`.

```python
validated = ProductCreate(name='Keyboard', category='electronics', price=79.99)
data = validated.model_dump()
# {'name': 'Keyboard', 'category': 'electronics', 'price': 79.99, 'description': None, 'tags': []}

# Exclude None values from the output dict
data = validated.model_dump(exclude_none=True)
# {'name': 'Keyboard', 'category': 'electronics', 'price': 79.99, 'tags': []}
```

### `ValidationError.errors()` Output Structure

```python
try:
    ProductCreate(name='', category='electronics', price=-5.0)
except ValidationError as e:
    print(e.errors())
# [
#   {'type': 'string_too_short', 'loc': ('name',), 'msg': 'String should have at least 1 character', ...},
#   {'type': 'greater_than', 'loc': ('price',), 'msg': 'Input should be greater than 0', ...}
# ]
```

`loc` is a tuple of field names (and indices for nested structures) indicating the path to the failing field. `msg` is a human-readable description.

## Code Comparison

**JavaScript (Zod)**
```javascript
import { z } from 'zod';

const ProductSchema = z.object({
    name: z.string().min(1).max(200),
    category: z.string().min(1),
    price: z.number().positive(),
    description: z.string().optional()
});

app.post('/products', (req, res) => {
    const result = ProductSchema.safeParse(req.body);
    if (!result.success) {
        return res.status(422).json({
            error: 'Validation failed',
            details: result.error.issues
        });
    }
    const data = result.data;
    // proceed with data
});
```

**Python (Pydantic v2)**
```python
from pydantic import BaseModel, Field, ValidationError
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1)
    price: float = Field(gt=0)
    description: Optional[str] = None

@products_bp.post('/')
def create_product():
    payload = request.get_json()
    try:
        validated = ProductCreate(**payload)
    except ValidationError as e:
        return {'error': 'Validation failed', 'details': e.errors()}, 422

    product_data = validated.model_dump(exclude_none=True)
    # proceed with product_data
```

Pydantic and Zod occupy the same functional role. Both define schema separately from validation logic, raise structured errors on failure, and return validated data objects. Pydantic uses Python class syntax and type annotations; Zod uses a fluent builder API.

## Documentation
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
- [Pydantic v2: BaseModel](https://docs.pydantic.dev/latest/concepts/models/)
