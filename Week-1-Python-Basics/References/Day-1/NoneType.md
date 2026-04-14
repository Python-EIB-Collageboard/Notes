# NoneType

## Objective
Python's `NoneType` singleton and its behavioral differences from JavaScript's `null` and `undefined`.

## JavaScript Equivalent
JavaScript has two "absence of value" primitives: `null` (intentional absence) and `undefined` (uninitialized or missing). Python has a single type for both concepts: `None`, the sole instance of `NoneType`. There is no `undefined` equivalent in Python -- an unbound name raises a `NameError` rather than resolving to a default value.

## Implementation Details

### `None` as a Singleton
`None` is a singleton -- there is exactly one `None` object in a Python process. All references to `None` point to the same object.

```python
type(None)      # <class 'NoneType'>
None is None    # True -- always

x = None
y = None
x is y          # True -- same object
```

Because `None` is a singleton, the correct comparison operator is `is`, not `==`.

```python
value = None

# Correct
if value is None:
    print("no value")

if value is not None:
    print("has value")

# Technically works but non-idiomatic -- avoid
if value == None:
    pass
```

Using `==` for `None` checks is non-idiomatic and can produce unexpected results if an object overrides `__eq__`.

### Implicit `None` Return
Functions that do not contain a `return` statement, or that execute a bare `return`, implicitly return `None`.

```python
def no_return():
    x = 1 + 1  # no return statement

result = no_return()
print(result)           # None
print(type(result))     # <class 'NoneType'>

def early_return(flag):
    if flag:
        return "done"
    return  # explicit bare return -- returns None

early_return(False)  # None
```

This is equivalent to JavaScript functions that fall off the end without a `return` statement, which also return `undefined`.

### `None` vs `undefined` -- Key Differences
| Behavior | JavaScript | Python |
|---|---|---|
| Uninitialized variable | `undefined` | `NameError` -- variable does not exist |
| Missing function argument | `undefined` | `TypeError` -- unless a default is defined |
| Missing object property | `undefined` | `AttributeError` or `KeyError` |
| Intentional absence | `null` | `None` |
| Function with no return | Returns `undefined` | Returns `None` |

Python does not silently produce a "missing" value. Accessing a name that has not been assigned raises an exception immediately.

```python
print(z)  # NameError: name 'z' is not defined
           # JavaScript: console.log(z) would print undefined (or ReferenceError for let/const)
```

### `None` in Default Arguments
`None` is the standard sentinel value for optional function parameters. This pattern is covered in depth in Day 3 (Functions), but the idiom appears frequently.

```python
def connect(host, port=None):
    if port is None:
        port = 443  # apply default logic
    # proceed with host and port
```

Avoid using mutable default arguments (`[]`, `{}`) -- use `None` as the sentinel and construct the mutable object inside the function body. This is a well-known Python gotcha.

```python
# Incorrect -- mutable default shared across all calls
def add_item(item, collection=[]):
    collection.append(item)
    return collection

# Correct
def add_item(item, collection=None):
    if collection is None:
        collection = []
    collection.append(item)
    return collection
```

### Truthiness of `None`
`None` is falsy.

```python
bool(None)  # False

if not None:
    print("None is falsy")  # prints
```

This enables idiomatic truthiness checks in place of explicit `is None` tests in some contexts, though explicit `is None` is preferred for clarity when the intent is specifically to test for the absence of a value.

## Code Comparison

**JavaScript (Node.js)**
```javascript
// Two distinct absence primitives
let a = null;        // intentional absence
let b;               // undefined -- uninitialized
let c = undefined;   // explicit undefined

typeof null;         // "object" (historical quirk)
typeof undefined;    // "undefined"

// Loose equality conflates null and undefined
null == undefined;   // true
null === undefined;  // false

// Accessing missing property
const obj = {};
obj.missing;         // undefined -- no error
```

**Python**
```python
# One absence value
a = None
type(None)   # <class 'NoneType'>

# Accessing missing attribute
class Obj:
    pass

o = Obj()
o.missing    # AttributeError: 'Obj' object has no attribute 'missing'
# No silent fallback to None

# Correct None check
if a is None:
    print("absent")

# Equivalence
a is None    # True
a is not None  # False
```

## Documentation
- [Python Built-in Constants: None](https://docs.python.org/3/library/constants.html#None)
- [Python Reference: The `is` Operator](https://docs.python.org/3/reference/expressions.html#is)
