# Functions

## Objective
Syntax and mechanics for declaring and invoking named blocks of reusable code, including parameter handling, variable-length arguments, and return values.

## JavaScript Equivalent
JavaScript `function` declarations, expressions, or arrow functions. JavaScript handles parameters loosely, passing `undefined` for missing arguments and ignoring excess arguments. JavaScript does not natively support keyword arguments out of the box, relying instead on passing an object literal for configuration.

## Implementation Details

### The `def` Keyword and Arity Enforcement
Python uses the `def` keyword. While structurally similar to JavaScript, Python enforces strict arity (parameter count). Passing fewer arguments than required, or more arguments than accepted, raises a `TypeError` immediately instead of failing silently.

### Implicit Returns
Functions without an explicit `return` statement, or with a bare `return`, implicitly return `None`. This directly maps to a JavaScript function returning `undefined`.

### Positional vs. Keyword Arguments
Python natively supports keyword arguments. When calling a function, arguments can be explicitly bound to the parameter name, allowing developers to provide arguments out of positional order. This eliminates the need for the common JavaScript pattern of parsing an options object.

### The Mutable Default Argument Gotcha
Python evaluates default arguments exactly once, when the function is defined, not dynamically on each invocation. This is a critical divergence from JavaScript. If a default argument is a mutable type (e.g., a `list` or `dict`), mutations to that object will persist across subsequent function calls. The standard idiom is to use `None` as the default and initialize the object inside the function body.

### Variable-Length Arguments
Python uses the `*` (asterisk) operator to gather excess positional arguments into a tuple, mapping conceptually to JavaScript's `...rest` parameters. 

However, Python introduces `**` (double asterisk) for gathering excess *keyword* arguments into a dictionary, a concept absent in JavaScript parameter definitions.

### Type Hinting
While Python is dynamically typed, the standard library supports optional type annotations (similar to TypeScript's goals, but purely for static analysis). The interpreter ignores them at runtime, but tooling leverages them extensively.

## Code Comparison

**JavaScript (Node.js)**
```javascript
// Loose arity and default parameters
function connect(host, port = 8080) {
    console.log(`Connecting to ${host}:${port}`);
}
connect("localhost"); // Valid
connect("localhost", 443, "extra"); // Valid, "extra" ignored
// connect() -> host is undefined

// The "options object" pattern to simulate keyword args
function configure(options = {}) {
    const timeout = options.timeout || 3000;
    const verbose = options.verbose || false;
}

// Rest parameters
function sumAll(...numbers) {
    return numbers.reduce((acc, curr) => acc + curr, 0);
}
```

**Python**
```python
# Strict arity and default parameters
def connect(host, port=8080):
    print(f"Connecting to {host}:{port}")

connect("localhost") # Valid
# connect("localhost", 443, "extra")  # Raises TypeError
# connect()  # Raises TypeError: missing 'host'

# Native Keyword arguments (no dictionary needed)
def configure(timeout=3000, verbose=False):
    pass

configure(verbose=True, timeout=5000) # Out of order execution

# Variable positional arguments (tuples)
def sum_all(*numbers):
    return sum(numbers)

# Variable keyword arguments (dictionaries)
def log_metadata(**kwargs):
    # kwargs resolves to a dictionary: {"user": "admin", "id": 12}
    if "user" in kwargs:
        print(kwargs["user"])

log_metadata(user="admin", id=12)

# The Mutable Default Gotcha
# INCORRECT
def add_item_bad(item, data=[]):
    data.append(item)
    return data

# CORRECT
def add_item_good(item, data=None):
    if data is None:
        data = []
    data.append(item)
    return data

# Type Hinting Example
def greet(name: str) -> str:
    return f"Hello, {name}"
```

## Documentation
- [Python Tutorial: Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Python Reference: Function Definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)
