# HTTP Responses and Status Codes

## Objective
The mechanics of constructing and returning HTTP responses in Flask, including status codes, headers, and response object construction.

## JavaScript Equivalent
`res.status()`, `res.json()`, `res.set()`, and `res.send()` on the Express `Response` object.

## Implementation Details

Express exposes the response object as the `res` parameter of every route handler, providing a fluent API for chaining status codes, headers, and body serialization. Flask has no such parameter. Instead, the view function's return value is what Flask transforms into an HTTP response.

### Return Value Conventions

Flask evaluates the return value of a view function and applies the following conversion rules:

| Return Type | Result |
|-------------|--------|
| `str` | 200 response, `Content-Type: text/html` |
| `dict` or `list` | 200 response, serialized to JSON |
| `(body, status_code)` tuple | Response with specified status |
| `(body, status_code, headers)` tuple | Response with status and headers |
| `flask.Response` | Used directly |

A two-element tuple is the most common pattern for non-200 responses:

```python
@app.post('/users')
def create_user():
    return {'id': 42, 'name': 'NewUser'}, 201
```

A three-element tuple appends response headers. The headers element accepts a `dict`:

```python
@app.get('/resource')
def get_resource():
    return {'data': 'value'}, 200, {'X-Custom-Header': 'active'}
```

### `flask.make_response()`

For full programmatic control over the response object -- equivalent to constructing a response manually in Express -- Flask provides `make_response()`:

```python
from flask import make_response, jsonify

@app.delete('/users/<int:user_id>')
def delete_user(user_id):
    # Perform deletion...
    response = make_response('', 204)
    response.headers['X-Deleted-Id'] = str(user_id)
    return response
```

`make_response()` accepts the same arguments as the return tuple shorthand and returns a `flask.Response` object whose `.status_code`, `.headers`, and `.data` attributes can be set directly before returning.

### Standard HTTP Status Codes in Flask

Flask does not define named status code constants natively. The `http` module from the Python standard library provides `http.HTTPStatus`, which contains named members. The `flask` package re-exports these via `flask.HTTPStatus` in some configurations, but direct integer literals are the idiomatic Flask pattern:

```python
# Standard integer literals are idiomatic
return {'error': 'Not found'}, 404
return {'error': 'Unprocessable'}, 422
return {'message': 'Created'}, 201
return '', 204  # No Content -- empty body
```

### Error Responses with `flask.abort()`

`flask.abort()` raises an `HTTPException`, terminating the request and returning an error response immediately -- analogous to calling `return res.status(404).send()` and exiting the handler in Express, but implemented as an exception:

```python
from flask import abort

@app.get('/users/<int:user_id>')
def get_user(user_id):
    user = find_user(user_id)
    if user is None:
        abort(404)
    return user
```

Custom error handlers can intercept these exceptions via the `@app.errorhandler()` decorator:

```python
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Resource not found'}, 404
```

## Code Comparison

**JavaScript (Express)**
```javascript
app.post('/users', (req, res) => {
    const user = createUser(req.body);
    res.status(201).json(user);
});

app.get('/users/:id', (req, res) => {
    const user = findUser(req.params.id);
    if (!user) {
        return res.status(404).json({ error: 'Not found' });
    }
    res.json(user);
});
```

**Python (Flask)**
```python
@app.post('/users')
def create_user():
    user = create_user_record(request.get_json())
    return user, 201

@app.get('/users/<int:user_id>')
def get_user(user_id):
    user = find_user(user_id)
    if user is None:
        return {'error': 'Not found'}, 404
    return user
```

The key structural difference: Express mutates the `res` object via method calls. Flask derives the response from the function's return value. Both result in identical HTTP wire output.

## Documentation
- [Flask Quickstart: About Responses](https://flask.palletsprojects.com/en/stable/quickstart/#about-responses)
- [Flask API: flask.make_response](https://flask.palletsprojects.com/en/stable/api/#flask.make_response)
