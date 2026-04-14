# Tuples

## Objective
Python's immutable, ordered sequence data structure.

## JavaScript Equivalent
JavaScript has no direct equivalent to a Python Tuple. Passing an array through `Object.freeze()` approximates the behavior, but lacks the specific performance optimization Python offers.

## Implementation Details

### Syntax & Immutability
Tuples are declared using parentheses `()`, though the comma is the actual defining characteristic. They are sequence types like lists, but cannot be modified (no append, insert, or reassignment).

```python
# Initialization
dimensions = (1920, 1080)
# dimensions[0] = 1024 # TypeError: 'tuple' object does not support item assignment

# Single element tuple requires a trailing comma
single = (1,)  # correct
not_single = (1) # evaluates mathematically to integer 1
```

### Data Modeling vs Collections
While lists are typically used for homogeneous collections of items (e.g., `["alice", "bob", "charlie"]`), tuples are idiomatic for heterogeneous collections representing a single record or coordinate (e.g., `("alice", 25, "admin")`).

### Packing and Unpacking
Tuples are heavily utilized for variable assignment, destructuring (unpacking), and functions returning multiple values. 

```python
def fetch_system_metrics():
    # Returns a packed tuple spontaneously
    return 80.5, 95.1

# Unpacking the tuple into variables
cpu, memory = fetch_system_metrics()

# Variable swapping is performed natively using tuple packing/unpacking
cpu, memory = memory, cpu
```

### Hashability
Unlike lists, tuples containing only immutable dependencies are themselves immutable and thus hashable. This allows them to act as dictionary keys or exist in `sets` — situations where lists would explicitly crash.

```python
cache = {}
route = ("GET", "/api/v1/users")

cache[route] = "{...}" # Valid because route is a tuple
```

## Code Comparison

**JavaScript (Node.js)**
```javascript
const coords = Object.freeze([40.7128, -74.0060]);
const lat = coords[0];
const lon = coords[1];

// Swapping
let a = 1, b = 2;
[a, b] = [b, a]; // Using array destructuring
```

**Python**
```python
coords = (40.7128, -74.0060)
lat, lon = coords # Clean tuple unpacking

# Swapping
a, b = 1, 2
a, b = b, a # Pythonic tuple unpacking
```

## Documentation
- [Python Built-in Types: Tuples](https://docs.python.org/3/library/stdtypes.html#tuples)
