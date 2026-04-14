# Dictionaries

## Objective
Python's built-in key-value mapping structure and its execution differences.

## JavaScript Equivalent
JavaScript `Object` (for general use) or `Map` (for complex key mapping). Python `dict` enforces hashability on keys, maintains insertion order (as of Python 3.7), and strictly differentiates between dictionary keys and object attributes.

## Implementation Details

### Key Integrity
Unlike JS Objects, which silently cast keys to Strings, Python dictionaries retain the key's type. However, keys must be immutable/hashable (Strings, Numbers, Tuples).

```python
data = {
    "name": "System",
    1: "one",           # Valid: integer key
    (1, 2): "matrix",   # Valid: tuple key
    # [1, 2]: "array"   # TypeError: unhashable type: 'list'
}
```

### Missing Keys
Accessing a missing key in Python using bracket notation raises a `KeyError`. Python does not silently return an `undefined` value. To mirror JS behavior or provide a fallback, use `.get()`.

```python
user = {"id": 100}
# print(user["name"])      # KeyError

# The get method returns None (or a specified default) if the key is missing
print(user.get("name"))          # None
print(user.get("name", "N/A"))   # "N/A"
```

### Iteration
Dictionaries provide specific methods to iterate over keys, values, or key-value pairs concurrently.

```python
config = {"mode": "dev", "workers": 4}

for k in config.keys():         # Explicit key iteration
    pass

for v in config.values():       # Value iteration
    pass

for k, v in config.items():     # Tuple unpacking for key-value (JS Equivalent: Object.entries())
    print(f"{k}: {v}")
```

### Dictionary Comprehensions
Similar to list comprehensions, Python supports dictionary generation.

```python
keys = ["a", "b", "c"]
# { 'a': 0, 'b': 1, 'c': 2 }
indexed = {key: idx for idx, key in enumerate(keys)}
```

## Code Comparison

**JavaScript (Node.js)**
```javascript
const response = { status: 200, count: 50 };

// Access
const result = response.data || []; // Silent missing property

// Iteration
for (const [key, value] of Object.entries(response)) {
    console.log(key, value);
}

// Assignment
response.latency = 120;
```

**Python**
```python
response = {"status": 200, "count": 50}

# Access
result = response.get("data", [])

# Iteration
for key, value in response.items():
    print(key, value)

# Assignment
response["latency"] = 120
```

## Documentation
- [Python Built-in Types: Mapping Types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
