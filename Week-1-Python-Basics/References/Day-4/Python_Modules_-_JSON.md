# Python Modules -- JSON

## Objective
Serialization and deserialization of JSON objects, managing data type mappings, and configuring serialization behavior.

## JavaScript Equivalent
JavaScript leverages the globally available `JSON.parse()` for string deserialization and `JSON.stringify()` for object serialization. Python encapsulates this functionality within the standard library `json` module, which exposes string and file-stream methods.

## Implementation Details

### The Four Core Methods
The Python `json` module provides four primary functions that strictly delineate between memory-based string manipulation and stream-based file I/O:
- `json.loads(string)`: "Load string". Deserializes a JSON-formatted string into a Python dictionary. Maps directly to `JSON.parse()`.
- `json.dumps(obj)`: "Dump string". Serializes a Python dictionary or list into a JSON-formatted string. Maps directly to `JSON.stringify()`.
- `json.load(file_object)`: "Load". Reads JSON data directly from a file object and parses it into a Python dictionary.
- `json.dump(obj, file_object)`: "Dump". Writes a serialized Python dictionary directly into a file object.

### Data Type Mapping
JSON is a JavaScript-derived format. Python handles the conceptual mismatch by automatically converting underlying types during serialization and deserialization.

| JSON Format | JavaScript Type | Python Type |
|---|---|---|
| `{"a": "b"}` | Object | `dict` |
| `[1, 2, 3]` | Array | `list` |
| `"string"` | String | `str` |
| `123` | Number | `int` or `float` |
| `true` | Boolean (`true`) | `True` |
| `false` | Boolean (`false`) | `False` |
| `null` | `null` | `None` |

Attempting to serialize a Python type that has no direct JSON equivalent (e.g., `set`, `datetime`, or custom class objects) will raise a `TypeError`.

### Advanced Formatting and Custom Serializers
JavaScript's `JSON.stringify` accepts a replacer function for custom serialization. Python's `json.dumps` accepts a `default` parameter, which is a function that gets called for objects that cannot otherwise be serialized.

Additionally, Python allows for extensive formatting controls:
- `indent=4`: Pretty-prints the output with a 4-space indent.
- `separators=(',', ':')`: Removes trailing whitespace.
- `sort_keys=True`: Alphabetizes dictionary keys in the resulting output.

## Code Comparison

**JavaScript (Node.js)**
```javascript
const userData = {
    id: 1,
    active: true,
    roles: ["admin", "user"],
    metadata: null
};

// Serialize object to string with formatting
const jsonString = JSON.stringify(userData, null, 4);

// Deserialize string to object
const parsedObj = JSON.parse(jsonString);

// Handling un-serializable objects (e.g., Set)
// Output: {}
const setExample = JSON.stringify(new Set([1, 2, 3]));
```

**Python**
```python
import json

user_data = {
    "id": 1,
    "active": True,
    "roles": ["admin", "user"],
    "metadata": None
}

# Serialize dictionary to string with formatting
json_string = json.dumps(user_data, indent=4, sort_keys=True)

# Deserialize string to dictionary
parsed_dict = json.loads(json_string)

# Handling un-serializable objects (e.g., set)
# json.dumps(set([1, 2, 3])) -> raises TypeError

# Custom serialization using the 'default' parameter
def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

safe_string = json.dumps(set([1, 2, 3]), default=set_default)
# Output: '[1, 2, 3]'
```

## Documentation
- [Python Standard Library: json](https://docs.python.org/3/library/json.html)
