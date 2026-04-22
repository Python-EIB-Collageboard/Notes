# Environment Variable Configuration

## Objective
Externalizing application configuration to environment variables in a Flask application using `python-dotenv`, including loading strategy, access patterns, and the `flask.Config` object.

## JavaScript Equivalent
`dotenv` npm package (`require('dotenv').config()`), with values accessed via `process.env.VARIABLE_NAME`.

## Implementation Details

Hardcoding configuration values (database URIs, API keys, ports) in source files is a security and deployment anti-pattern. The standard practice is to externalize these values to environment variables, loaded from a `.env` file during development and injected by the host environment (Docker, Azure App Service, CI/CD pipeline) in production.

Python's `python-dotenv` library is the direct equivalent of Node.js's `dotenv` package.

### Installation

```bash
pip install python-dotenv
```

### `.env` File Structure

```
COSMOS_ENDPOINT=https://localhost:8081
COSMOS_KEY=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw==
COSMOS_DATABASE=dev_db
COSMOS_CONTAINER=items
FLASK_ENV=development
SECRET_KEY=change-me-in-production
```

This file must be listed in `.gitignore`:

```
# .gitignore
.env
```

### Loading `.env` with `python-dotenv`

`load_dotenv()` reads the `.env` file and populates `os.environ`. It must be called before any `os.environ` access. The conventional location is the application entry point or the top of the application factory module.

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env into os.environ

# Access values
cosmos_endpoint = os.environ['COSMOS_ENDPOINT']         # Raises KeyError if missing
cosmos_key = os.environ.get('COSMOS_KEY', 'fallback')   # Returns default if missing
```

`os.environ['KEY']` (bracket notation) raises `KeyError` if the variable is not set. `os.environ.get('KEY', default)` returns the default. Use bracket notation for required variables so that missing configuration fails fast at startup.

### Flask Configuration Object

Flask provides a `Config` object at `app.config` that functions as a dict. It is the intended location for application-level configuration values. Loading from environment variables into `app.config` centralizes access and enables testing overrides:

```python
# app/__init__.py
import os
from flask import Flask
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, PartitionKey

def create_app():
    load_dotenv()

    app = Flask(__name__)

    # Load configuration from environment into Flask config
    app.config['COSMOS_ENDPOINT'] = os.environ['COSMOS_ENDPOINT']
    app.config['COSMOS_KEY'] = os.environ['COSMOS_KEY']
    app.config['COSMOS_DATABASE'] = os.environ['COSMOS_DATABASE']
    app.config['COSMOS_CONTAINER'] = os.environ['COSMOS_CONTAINER']
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-insecure-key')

    # Initialize Cosmos client using app.config values
    client = CosmosClient(
        url=app.config['COSMOS_ENDPOINT'],
        credential=app.config['COSMOS_KEY'],
        connection_verify=False
    )
    db = client.create_database_if_not_exists(app.config['COSMOS_DATABASE'])
    app.cosmos_container = db.create_container_if_not_exists(
        id=app.config['COSMOS_CONTAINER'],
        partition_key=PartitionKey(path='/category')
    )

    return app
```

### Accessing Config in View Functions

Within a request context, `current_app.config` provides access to the Flask config dict:

```python
from flask import current_app

@products_bp.get('/config-check')
def config_check():
    return {'database': current_app.config['COSMOS_DATABASE']}
```

### `from_object()` for Multi-Environment Configuration

For more structured configuration management, define configuration classes and load them by name:

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-insecure-key')
    COSMOS_ENDPOINT = os.environ['COSMOS_ENDPOINT']
    COSMOS_KEY = os.environ['COSMOS_KEY']

class DevelopmentConfig(BaseConfig):
    COSMOS_DATABASE = 'dev_db'
    COSMOS_VERIFY_SSL = False

class ProductionConfig(BaseConfig):
    COSMOS_DATABASE = os.environ['COSMOS_DATABASE']
    COSMOS_VERIFY_SSL = True

# app/__init__.py
def create_app(config_name='development'):
    app = Flask(__name__)
    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig
    }
    app.config.from_object(configs[config_name])
    return app
```

## Code Comparison

**JavaScript (Node.js)**
```javascript
// Load .env
require('dotenv').config();

// Access values
const cosmosEndpoint = process.env.COSMOS_ENDPOINT;
const cosmosKey = process.env.COSMOS_KEY;

if (!cosmosEndpoint || !cosmosKey) {
    throw new Error('Missing required environment variables');
}
```

**Python (Flask)**
```python
from dotenv import load_dotenv
import os

load_dotenv()

cosmos_endpoint = os.environ['COSMOS_ENDPOINT']  # Raises KeyError if missing
cosmos_key = os.environ['COSMOS_KEY']
```

The pattern is identical: load from `.env`, access via the environment dictionary, fail fast on missing required values. Python's `os.environ['KEY']` raises `KeyError`; Node.js's `process.env.KEY` returns `undefined`, requiring an explicit `if (!value)` check.

## Documentation
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Flask Configuration Handling](https://flask.palletsprojects.com/en/stable/config/)
