# Flask Blueprints

## Objective
The Flask modular routing mechanism for partitioning an application's routes and handlers into isolated, registerable components.

## JavaScript Equivalent
Express `Router`: `const router = express.Router(); router.get(...); app.use('/prefix', router)`.

## Implementation Details

In Express, an `express.Router()` instance encapsulates a set of route definitions and middleware. It is mounted onto the application with a URL prefix via `app.use()`. Flask's **Blueprint** is the structural equivalent: a standalone object that records route definitions, error handlers, and request lifecycle hooks, then registers them onto the application at startup.

A Blueprint does not become active until it is registered on a Flask application instance. Before registration, it is a deferred record of intended routes.

### Blueprint Creation

```python
# users/routes.py
from flask import Blueprint

users_bp = Blueprint(
    'users',        # Endpoint namespace -- must be unique across the application
    __name__,       # Determines the Blueprint's root path for template/static resolution
    url_prefix='/users'
)
```

The first argument is the **name** of the Blueprint. This string becomes a namespace prefix for all endpoint names defined within it. A route named `get_user` inside the `users` Blueprint has a fully qualified endpoint name of `users.get_user`, referenced as `url_for('users.get_user', user_id=1)`.

The `url_prefix` parameter prepends a URL segment to all routes defined on the Blueprint.

### Defining Routes on a Blueprint

Route decorators are called on the Blueprint instance instead of the application instance:

```python
# users/routes.py
from flask import Blueprint, request

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.get('/')
def get_users():
    return {'users': []}

@users_bp.post('/')
def create_user():
    payload = request.get_json()
    return {'created': payload}, 201

@users_bp.get('/<int:user_id>')
def get_user(user_id):
    return {'id': user_id}
```

### Blueprint Registration

Blueprints are registered on the application instance via `app.register_blueprint()`, typically inside the application factory:

```python
# app/__init__.py
from flask import Flask
from .users.routes import users_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(users_bp)
    return app
```

The `url_prefix` can also be overridden at registration time:

```python
app.register_blueprint(users_bp, url_prefix='/api/v1/users')
```

### Blueprint-Scoped Lifecycle Hooks

Blueprints can define request lifecycle hooks that apply only to routes within that Blueprint, as opposed to application-wide hooks defined on the `app` instance:

```python
@users_bp.before_request
def authenticate():
    # Runs before every request handled by users_bp
    token = request.headers.get('Authorization')
    if not token:
        return {'error': 'Unauthorized'}, 401
```

### Recommended Project Structure

```
app/
  __init__.py          # Application factory
  users/
    __init__.py
    routes.py          # users_bp defined here
  products/
    __init__.py
    routes.py          # products_bp defined here
```

This layout mirrors the standard Express router pattern where each domain (users, products) has its own router module mounted at a prefix.

## Code Comparison

**JavaScript (Express)**
```javascript
// users/router.js
const router = require('express').Router();

router.get('/', (req, res) => {
    res.json({ users: [] });
});

router.post('/', (req, res) => {
    res.status(201).json({ created: req.body });
});

module.exports = router;

// app.js
const usersRouter = require('./users/router');
app.use('/users', usersRouter);
```

**Python (Flask)**
```python
# users/routes.py
from flask import Blueprint, request

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.get('/')
def get_users():
    return {'users': []}

@users_bp.post('/')
def create_user():
    return {'created': request.get_json()}, 201

# app/__init__.py
from flask import Flask
from .users.routes import users_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(users_bp)
    return app
```

The Blueprint registration model is functionally identical to the Express `app.use('/prefix', router)` pattern. The primary behavioral difference is the **endpoint namespace**: Flask's Blueprint name creates a `blueprint_name.endpoint_name` dot-notation identifier, which is surfaced in `url_for()` calls and error messages.

## Documentation
- [Flask Blueprints](https://flask.palletsprojects.com/en/stable/blueprints/)
- [Flask API: flask.Blueprint](https://flask.palletsprojects.com/en/stable/api/#flask.Blueprint)
