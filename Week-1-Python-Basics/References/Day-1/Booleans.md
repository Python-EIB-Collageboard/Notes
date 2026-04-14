# Booleans

## Objective
Python's `bool` type, its subclass relationship with `int`, and the truthiness evaluation rules that differ from JavaScript.

## JavaScript Equivalent
JavaScript treats `boolean` as a primitive type. Python's `bool` is a subclass of `int`, making `True` and `False` literal instances of both `bool` and `int`. The truthiness rules ("truthy"/"falsy") overlap significantly with JavaScript but differ in key areas.

## Implementation Details

### `bool` as `int` Subclass
`True` is literally equal to `1` and `False` to `0`. This is an intentional design choice that enables compact summation of boolean conditions.

```python
isinstance(True, int)   # True
isinstance(False, int)  # True

True + True   # 2
True * 5      # 5
False + 1     # 1

# Practical use: count matching items
values = [1, -2, 3, -4, 5]
positive_count = sum(v > 0 for v in values)  # sum([True, False, True, False, True]) = 3
```

### Literal Syntax
Python's boolean literals are capitalized: `True` and `False`. JavaScript uses lowercase `true` and `false`.

```python
flag = True
is_valid = False
```

### Logical Operators
Python uses English-word operators instead of symbols.

| Operation | Python | JavaScript |
|---|---|---|
| AND | `and` | `&&` |
| OR | `or` | `\|\|` |
| NOT | `not` | `!` |

```python
a = True
b = False

a and b   # False
a or b    # True
not a     # False
```

### Short-Circuit Evaluation and Return Values
`and` and `or` do not return `True`/`False` -- they return one of their operands, identical to JavaScript's `&&` and `||`. Evaluation short-circuits.

```python
# `or` returns the first truthy value, or the last value if all are falsy
None or "default"       # "default"
"value" or "default"    # "value"
0 or [] or "fallback"   # "fallback"

# `and` returns the first falsy value, or the last value if all are truthy
"hello" and 42          # 42
None and "anything"     # None
```

This pattern is used as a default-value idiom in Python, analogous to JavaScript's `value || default`.

### Truthiness Rules
The `bool()` function applies Python's truthiness evaluation to any object. The rules for falsy values:

| Falsy Value | Type |
|---|---|
| `False` | `bool` |
| `None` | `NoneType` |
| `0` | `int` |
| `0.0` | `float` |
| `""` | `str` |
| `[]` | `list` |
| `{}` | `dict` |
| `()` | `tuple` |
| `set()` | `set` |

Everything else evaluates as truthy. This includes non-zero numbers, non-empty collections, and all object instances (unless the class defines `__bool__` or `__len__`).

**JavaScript comparison:**
- JavaScript also treats `0`, `""`, `null`, `undefined`, `NaN` as falsy.
- Python has no `null` or `undefined` -- `None` covers both.
- Python treats `0.0` as falsy; JavaScript treats `NaN` as falsy but Python has `float("nan")` which is truthy:

```python
bool(float("nan"))  # True -- this differs from JavaScript's NaN
```

### Comparison Operators
Comparison operators return `bool` values.

```python
5 > 3    # True
5 == 5   # True
5 != 4   # True
5 >= 5   # True
5 <= 4   # False
```

Python allows chained comparisons, which are not valid in JavaScript:

```python
1 < x < 10          # equivalent to: x > 1 and x < 10
0 <= score <= 100   # range validation in one expression
```

### Identity vs Equality
`==` tests value equality. `is` tests object identity (reference equality, equivalent to `===` for primitives in JavaScript).

```python
a = [1, 2, 3]
b = [1, 2, 3]

a == b  # True  -- same contents
a is b  # False -- different objects in memory

# `is` is the correct operator for None checks
value = None
if value is None:
    print("no value")
```

Do not use `==` to test for `None` -- `is None` is the idiomatic form and avoids custom `__eq__` interference.

## Code Comparison

**JavaScript (Node.js)**
```javascript
const a = true;
const b = false;

a && b;   // false
a || b;   // true
!a;       // false

// Falsy check
const value = null;
if (!value) {
    console.log("falsy");
}

// Default value pattern
const name = userInput || "anonymous";

// Chain comparison not valid in JS
// 1 < x < 10 evaluates as (1 < x) < 10 -- always true for x > 1
```

**Python**
```python
a = True
b = False

a and b   # False
a or b    # True
not a     # False

# Falsy check
value = None
if not value:
    print("falsy")

# Default value pattern
name = user_input or "anonymous"

# Chained comparison -- valid and idiomatic
x = 5
1 < x < 10  # True
```

## Documentation
- [Python Built-in Types: bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)
- [Python Expressions: Boolean Operations](https://docs.python.org/3/reference/expressions.html#boolean-operations)
