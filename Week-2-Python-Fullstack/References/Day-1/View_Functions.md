# View Functions

## Objective
The callable units in Flask that receive an HTTP request and return an HTTP response, serving as the direct structural equivalent of Express route handler callbacks.

## JavaScript Equivalent
Express route handler callbacks: `app.get('/path', (req, res) => { res.json(data); })`.

## Implementation Details

In Express, a route handler is an anonymous or named function passed as an argument to a routing method. Flask inverts this pattern: a regular Python function is decorated with `@app.route()`, and Flask registers it internally as the handler for that URL rule. The decorated function is the **view function**.

Flask's routing system matches an incoming request URL against its registered rules and dispatches to the corresponding view function. The view function must return a value that Flask can convert into a `Response` object. Acceptable return types include:

- A `str` (Flask wraps it in a 200 response with `text/html` content type)
- A `dict` or `list` (Flask serializes it as JSON automatically, equivalent to `res.json()`)
- A `tuple` of `(body, status_code)` or `(body, status_code, headers)`
- A `flask.Response` object constructed explicitly via `flask.make_response()`

The function name serves as the **endpoint name** -- the internal identifier Flask uses to generate URLs via `url_for()`. This name must be unique within the application.

```python
from flask import Flask

app = Flask(__name__)

@app.route('/users')
def get_users():
    # Function name 'get_users' is the endpoint name
    return {'users': []}
```

### The Application Factory Pattern

Defining routes on a module-level `app` instance creates tight coupling that complicates testing and multi-environment configuration. The standard production pattern is the **application factory**: a function that creates and configures the `Flask` instance, registers Blueprints, and returns it.

```python
# app/__init__.py
from flask import Flask

def create_app(config_object=None):
    app = Flask(__name__)

    if config_object:
        app.config.from_object(config_object)

    # Blueprints registered here (covered in Flask Blueprints topic)
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
```

This pattern is the Flask analogue of the `createServer` wrapper pattern in Node.js, enabling isolated test instances and environment-specific configuration without modifying global state.

### HTTP Method Binding

By default, `@app.route()` only responds to `GET` requests. The `methods` parameter accepts a list of HTTP method strings.

```python
@app.route('/users', methods=['GET', 'POST'])
def users():
    ...
```

Flask provides shorthand decorators (`app.get()`, `app.post()`, `app.put()`, `app.delete()`, `app.patch()`) introduced in Flask 2.0, which are syntactically closer to the Express method-chaining pattern.

## Code Comparison

**JavaScript (Express)**
```javascript
const express = require('express');
const app = express();

app.get('/users', (req, res) => {
    res.status(200).json({ users: [] });
});

app.listen(3000);
```

**Python (Flask)**
```python
from flask import Flask

app = Flask(__name__)

@app.get('/users')
def get_users():
    return {'users': []}, 200

if __name__ == '__main__':
    app.run(port=3000)
```

The structural difference is the **decorator registration model** versus the **method-argument model**. Both associate a URL pattern with a callable, but Flask's decorator binds the association at definition time, making the route-to-handler mapping explicit in the source code without requiring the handler to be passed as a parameter.

## Documentation
- [Flask Quickstart: Routing](https://flask.palletsprojects.com/en/stable/quickstart/#routing)
- [Flask API: flask.Flask.route](https://flask.palletsprojects.com/en/stable/api/#flask.Flask.route)
