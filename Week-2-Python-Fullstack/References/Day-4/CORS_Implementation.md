# CORS Implementation

## Objective
Cross-Origin Resource Sharing configuration in a Flask application using the `flask-cors` extension, including per-origin allowlisting and per-route configuration.

## JavaScript Equivalent
The `cors` npm package (`app.use(cors({ origin: 'http://localhost:3000' }))`).

## Implementation Details

CORS is an HTTP mechanism that restricts cross-origin HTTP requests from browsers. A browser making a fetch or XHR request to a different origin (scheme + domain + port) than the one serving the HTML will block the response unless the server includes the appropriate `Access-Control-Allow-*` headers. This is a browser enforcement -- non-browser HTTP clients (curl, Postman, server-to-server calls) are not subject to CORS restrictions.

Flask does not set CORS headers by default. The `flask-cors` extension (`Flask-CORS`) adds them.

### Installation

```bash
pip install flask-cors
```

### Global CORS Configuration

`CORS()` applied to the entire application is the equivalent of `app.use(cors())` in Express. It adds CORS headers to all routes.

```python
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow all origins -- development only
    return app
```

With no arguments, `CORS(app)` allows all origins (`Access-Control-Allow-Origin: *`). This is appropriate only for fully public APIs or development environments.

### Restricting Origins

Limit CORS to specific origins using the `origins` parameter:

```python
CORS(app, origins=['http://localhost:3000', 'https://myapp.example.com'])
```

Multiple origins are supplied as a list. Only requests from those exact origins receive CORS headers. `*` can be included in the list to allow all origins.

### Allowing Credentials

If the client sends cookies or `Authorization` headers with cross-origin requests, both the client and server must opt in. On the server:

```python
CORS(app, origins=['http://localhost:3000'], supports_credentials=True)
```

`supports_credentials=True` adds `Access-Control-Allow-Credentials: true`. Note: when credentials are enabled, the origin cannot be `*` -- a specific origin list is required.

### Per-Blueprint CORS Configuration

`flask-cors` can be applied to specific Blueprints rather than the entire application, enabling different CORS policies per route group:

```python
from flask import Blueprint
from flask_cors import CORS

api_bp = Blueprint('api', __name__, url_prefix='/api')
CORS(api_bp, origins=['https://trusted-client.example.com'])

@api_bp.get('/data')
def get_data():
    return {'data': []}
```

### Per-Route CORS with `@cross_origin()`

The `@cross_origin()` decorator provides route-level CORS control:

```python
from flask_cors import cross_origin

@app.get('/public-endpoint')
@cross_origin()  # Applies CORS to this route only, allows all origins
def public_endpoint():
    return {'public': True}
```

### Preflight Requests

For non-simple requests (those with custom headers, non-GET/POST methods, or JSON content type), browsers send a preflight `OPTIONS` request before the actual request. `flask-cors` handles preflight responses automatically -- no additional view function is required for `OPTIONS` routes.

### Configured Headers

`flask-cors` supports configuring which request headers are permitted:

```python
CORS(app, origins=['http://localhost:3000'], allow_headers=['Content-Type', 'Authorization'])
```

This controls the `Access-Control-Allow-Headers` response header, which lists headers the browser is permitted to include in cross-origin requests.

## Code Comparison

**JavaScript (Express with `cors` package)**
```javascript
const cors = require('cors');

// Global CORS -- all origins
app.use(cors());

// Restricted to specific origins
app.use(cors({
    origin: ['http://localhost:3000', 'https://myapp.example.com'],
    credentials: true
}));

// Per-route CORS
app.get('/public', cors(), (req, res) => {
    res.json({ public: true });
});
```

**Python (Flask with `flask-cors`)**
```python
from flask_cors import CORS, cross_origin

# Global CORS -- all origins
CORS(app)

# Restricted to specific origins
CORS(app, origins=['http://localhost:3000', 'https://myapp.example.com'], supports_credentials=True)

# Per-route CORS
@app.get('/public')
@cross_origin()
def public():
    return {'public': True}
```

The API surface of `flask-cors` is intentionally parallel to the `cors` npm package. Both support global application, origin allowlisting, credentials, and per-route configuration through the same conceptual mechanisms.

## Documentation
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/en/latest/)
- [MDN: Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
