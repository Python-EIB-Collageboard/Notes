# Routing Variables

## Objective
Dynamic URL segments in Flask routes, including type converters and the mechanisms for extracting path parameters within view functions.

## JavaScript Equivalent
Express route parameters: `app.get('/users/:id', ...)` accessed via `req.params.id`.

## Implementation Details

Express uses the `:paramName` colon-prefix syntax in URL patterns to declare dynamic segments. Flask uses angle-bracket syntax: `<variable_name>`. The declared variable is injected as a keyword argument into the view function -- not accessed through a request proxy.

### Basic Variable Rules

```python
@app.get('/users/<user_id>')
def get_user(user_id):
    # user_id is a str by default
    return {'id': user_id}
```

The view function's parameter name must exactly match the variable name declared in the route string.

### Type Converters

Flask's routing system includes built-in **converters** that both constrain the matching pattern (rejecting non-conforming URLs at the routing layer) and coerce the value to a Python type before injection. This is automatic type validation that Express does not provide natively.

| Converter | Matched Pattern | Python Type |
|-----------|----------------|-------------|
| `string` (default) | Any text without a slash | `str` |
| `int` | Positive integers | `int` |
| `float` | Positive floating-point values | `float` |
| `path` | Any text, including slashes | `str` |
| `uuid` | UUID-formatted strings | `uuid.UUID` |

Syntax: `<converter:variable_name>`

```python
@app.get('/users/<int:user_id>')
def get_user(user_id):
    # user_id is already an int -- no int() casting required
    return {'id': user_id}

@app.get('/files/<path:filepath>')
def get_file(filepath):
    # Matches /files/images/avatars/profile.png
    return {'path': filepath}
```

When the `int` converter is specified, a request to `/users/abc` is immediately rejected with a `404` at the routing layer -- no view function execution occurs. This eliminates a class of manual type-checking that Express routes require.

### Multiple Path Variables

Multiple variables can appear in a single route pattern. Each maps to a separate keyword argument:

```python
@app.get('/orgs/<int:org_id>/users/<int:user_id>')
def get_org_user(org_id, user_id):
    return {'org_id': org_id, 'user_id': user_id}
```

### URL Building with `url_for()`

Flask's `url_for()` function generates URLs from endpoint names and keyword arguments -- the inverse of routing. This is used to avoid hardcoded URL strings across the codebase, analogous to building paths programmatically rather than concatenating strings in Express.

```python
from flask import url_for

# Inside a request context:
url = url_for('get_user', user_id=42)
# Returns: '/users/42'
```

`url_for()` accepts the view function's name (the endpoint name) as its first argument, followed by keyword arguments for each path variable.

## Code Comparison

**JavaScript (Express)**
```javascript
// Route declaration
app.get('/users/:userId/posts/:postId', (req, res) => {
    const userId = parseInt(req.params.userId, 10); // Manual cast required
    const postId = parseInt(req.params.postId, 10);

    if (isNaN(userId) || isNaN(postId)) {
        return res.status(400).json({ error: 'Invalid ID format' });
    }

    res.json({ userId, postId });
});
```

**Python (Flask)**
```python
# Route declaration with type converters
@app.get('/users/<int:user_id>/posts/<int:post_id>')
def get_user_post(user_id, post_id):
    # Both are already int -- routing layer enforced the format
    # A non-integer URL returns 404 before this function is called
    return {'user_id': user_id, 'post_id': post_id}
```

The converter system moves type enforcement from the handler body into the routing layer, eliminating manual validation code for URL segment types.

## Documentation
- [Flask Quickstart: Variable Rules](https://flask.palletsprojects.com/en/stable/quickstart/#variable-rules)
- [Flask API: URL Route Registrations](https://flask.palletsprojects.com/en/stable/api/#url-route-registrations)
