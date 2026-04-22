# JSON Payload Parsing

## Objective
Extraction and deserialization of JSON request bodies in Flask, mapping directly to the `express.json()` middleware pattern used in Node.js.

## JavaScript Equivalent
`req.body` populated by the `express.json()` middleware; `res.json()` for serialized responses.

## Implementation Details

In Express, JSON body parsing requires mounting the `express.json()` middleware, after which the parsed payload is available as `req.body`. Flask handles this differently: JSON parsing is available on demand through the `request` proxy object, with no global middleware registration required.

### The `request` Proxy

Flask exposes a thread-local (or context-local) proxy object `flask.request` that provides access to all incoming request data. It is not passed as a parameter to the view function -- it is imported at the module level and accessed directly. This is the primary structural departure from Express.

```python
from flask import request
```

This proxy is only valid within an active request context. Accessing it outside of a view function or request lifecycle raises a `RuntimeError`.

### Parsing JSON Bodies

**`request.get_json()`** is the canonical method for deserializing a JSON request body. It returns the parsed Python object (`dict`, `list`, etc.) or `None` if the body is empty, the `Content-Type` header is not `application/json`, or parsing fails.

| Parameter | Type | Default | Effect |
|-----------|------|---------|--------|
| `force` | `bool` | `False` | Parses even if `Content-Type` is not `application/json` |
| `silent` | `bool` | `False` | Returns `None` on parse failure instead of raising `400` |

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.post('/users')
def create_user():
    payload = request.get_json()

    if payload is None:
        return {'error': 'Invalid or missing JSON body'}, 400

    name = payload.get('name')
    return {'created': name}, 201
```

`request.json` is a property alias that calls `get_json(silent=True)` internally. Prefer `get_json()` explicitly when you need to control error behavior.

### Other Request Data Accessors

| Express | Flask | Data Source |
|---------|-------|-------------|
| `req.body` | `request.get_json()` | JSON request body |
| `req.query` | `request.args` | URL query string parameters |
| `req.params` | `request.view_args` | URL path variables |
| `req.headers` | `request.headers` | HTTP request headers |
| `req.method` | `request.method` | HTTP method string |

### Returning JSON Responses

Flask 2.2+ automatically serializes `dict` and `list` return values to JSON. For explicit control, use `flask.jsonify()`, which creates a `Response` object with `Content-Type: application/json`:

```python
from flask import jsonify

@app.get('/users')
def get_users():
    users = [{'id': 1, 'name': 'SystemAdmin'}]
    return jsonify(users), 200
```

Returning a raw `dict` is functionally equivalent in modern Flask. Use `jsonify()` when you need to set custom headers or status codes on the same response object.

## Code Comparison

**JavaScript (Express)**
```javascript
const express = require('express');
const app = express();

app.use(express.json()); // Global middleware required

app.post('/users', (req, res) => {
    const { name } = req.body;

    if (!name) {
        return res.status(400).json({ error: 'Name required' });
    }

    res.status(201).json({ created: name });
});
```

**Python (Flask)**
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# No global middleware registration for JSON parsing

@app.post('/users')
def create_user():
    payload = request.get_json()

    if not payload or 'name' not in payload:
        return {'error': 'Name required'}, 400

    name = payload['name']
    return jsonify({'created': name}), 201
```

The core distinction: Express attaches parsed body data to `req` via pipeline middleware. Flask makes request data available through an imported context-local proxy, bypassing the middleware pipeline for JSON parsing entirely.

## Documentation
- [Flask API: flask.Request](https://flask.palletsprojects.com/en/stable/api/#flask.Request)
- [Flask Quickstart: Accessing Request Data](https://flask.palletsprojects.com/en/stable/quickstart/#accessing-request-data)
