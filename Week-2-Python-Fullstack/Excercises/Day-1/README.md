# Feature Request: Flask Application Scaffolding and Route Layer

## Context

You are initializing the Week 2 phase of the cumulative repository. The Node.js/Express service you have been mentally referencing as a design model is not being ported -- it is being replaced. This week you build a Flask REST API from scratch, using your existing Express fluency as a translation map rather than a migration target.

By end of day, the repository must contain a running Flask application with a full Blueprint-based routing layer backed by in-memory data structures. No database. No persistence between restarts. The purpose is to isolate and validate the Flask routing mechanics before any external dependency is introduced.

The domain for the week is a **product catalog service**. Every day's exercise extends this same codebase. Name things accordingly from the start.

---

## Technical Requirements

### 1. Repository and Environment Setup

Initialize the Python project inside the existing cumulative repository under a new top-level directory:

```
week2-flask-api/
```

Inside that directory, establish the following:

- A Python virtual environment (`.venv/`). This is the `npm install` equivalent -- Python does not use a global runtime module cache.
- A `requirements.txt` file. This is the `package.json` equivalent for tracking dependencies.
- A `.gitignore` that excludes `.venv/`, `__pycache__/`, `.env`, and `*.pyc`.

Install Flask into the virtual environment:

```bash
pip install flask
pip freeze > requirements.txt
```

**Node.js Map:** `npm init` + `npm install express` + `.gitignore` -> `venv creation` + `pip install flask` + `requirements.txt`.

---

### 2. Application Factory

Create the following directory structure:

```
week2-flask-api/
  app/
    __init__.py
    products/
      __init__.py
      routes.py
  run.py
```

Implement the **application factory pattern** in `app/__init__.py`. The factory is a function named `create_app()` that instantiates the Flask object, registers Blueprints, and returns the configured app. It must not be called at module import time.

```python
# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)
    from .products.routes import products_bp
    app.register_blueprint(products_bp)
    return app
```

The entry point `run.py` calls the factory and starts the dev server:

```python
# run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Node.js Map:** `createServer()` wrapper in `server.js` + `app.use('/products', productsRouter)` -> `create_app()` + `app.register_blueprint(products_bp)`.

---

### 3. In-Memory Data Store

In `app/products/routes.py`, define a module-level `list` as the temporary data store. This is intentionally non-persistent -- it resets on every server restart. It exists solely to give the route handlers something to read from and write to while the database layer is absent.

```python
# app/products/routes.py
_products: list[dict] = []
```

This list is the only acceptable form of persistence for Day 1. No JSON files. No SQLite. No external services.

---

### 4. Blueprint and Route Definitions

Define a Blueprint named `products` with `url_prefix='/products'` in `app/products/routes.py`.

Implement the following routes as view functions on the Blueprint:

| HTTP Method | Path | Description | Success Status |
|-------------|------|-------------|----------------|
| `GET` | `/products/` | Return the full `_products` list | `200` |
| `POST` | `/products/` | Accept a JSON body, append to `_products`, return the created item | `201` |
| `GET` | `/products/<string:product_id>` | Find and return a single item by `id` field | `200` or `404` |
| `PUT` | `/products/<string:product_id>` | Replace a matching item by `id` | `200` or `404` |
| `DELETE` | `/products/<string:product_id>` | Remove a matching item by `id` | `204` or `404` |

All response bodies must be valid JSON. Do not return plain strings or HTML.

**JSON body parsing:** Use `request.get_json()` on all `POST` and `PUT` handlers. Return `400` if the result is `None` (missing body or incorrect `Content-Type`).

**`id` field:** On `POST`, generate a UUID string and assign it to the payload before storing:

```python
import uuid
payload['id'] = str(uuid.uuid4())
```

This establishes the `id` contract that the Cosmos DB SDK will enforce in Day 2.

**Node.js Map:** `req.body` -> `request.get_json()`. `res.status(201).json(data)` -> `return data, 201`. `router.delete(...)` -> `@products_bp.delete(...)`.

---

### 5. Response Structure Contract

All success responses must conform to the following envelope structure. This contract will be maintained through Day 4 and tested against in the Day 4 test suite.

| Endpoint | Response Body |
|----------|---------------|
| `GET /products/` | `{ "products": [ ... ] }` |
| `POST /products/` | The created item dict directly |
| `GET /products/<id>` | The item dict directly |
| `PUT /products/<id>` | The updated item dict directly |
| `DELETE /products/<id>` | Empty body (`''`) with `204` |

All error responses must use the structure `{ "error": "<message>" }`.

---

## Definition of Done

- `python run.py` starts the development server on port 5000 without errors.
- All five routes respond correctly when exercised with `curl` or a REST client (Postman, Insomnia, HTTPie).
- `POST /products/` with a valid JSON body returns the item with an auto-generated `id` field and status `201`.
- `GET /products/<id>` returns `404` with `{ "error": "..." }` for a non-existent `id`.
- `DELETE /products/<id>` returns `204` with no response body.
- `requirements.txt` reflects the installed packages.
- Code is pushed to the organizational GitHub repository on the branch `feature/week2-flask-scaffold`.
