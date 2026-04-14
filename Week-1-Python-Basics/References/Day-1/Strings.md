# Strings

## Objective
Python's string type, its immutability model, formatting mechanisms, and method surface as they map to JavaScript string behavior.

## JavaScript Equivalent
JavaScript strings are primitive values (with a `String` wrapper object). Python strings are immutable sequence objects of type `str`. Both languages use UTF-16/UTF-8 encoding internally, and both provide a rich set of built-in methods. The primary behavioral difference is that Python strings are sequences -- they support iteration, slicing, and membership testing natively.

## Implementation Details

### String Literals
Python accepts single quotes, double quotes, and triple quotes. There is no functional difference between single and double quotes; convention picks one and stays consistent within a project.

```python
a = 'single'
b = "double"
c = '''triple single -- spans
multiple lines'''
d = """triple double -- spans
multiple lines"""
```

Triple-quoted strings preserve literal newlines and are the standard for docstrings.

### Immutability
`str` objects are immutable. No in-place modification is possible; every operation that appears to modify a string returns a new `str` object.

```python
s = "hello"
s[0] = "H"  # TypeError: 'str' object does not support item assignment

s = "H" + s[1:]  # correct -- creates a new string
```

### String Formatting

#### f-strings (Python 3.6+) -- Preferred
```python
name = "Alice"
score = 98.5
result = f"User {name} scored {score:.2f}"
# "User Alice scored 98.50"
```

Expressions inside `{}` are evaluated at runtime. Format specifiers follow the `:` separator and use the same mini-language as `format()`.

#### `str.format()`
```python
result = "User {} scored {:.2f}".format(name, score)
result = "User {name} scored {score}".format(name=name, score=score)
```

#### `%` Formatting (Legacy)
```python
result = "User %s scored %.2f" % (name, score)
```

The `%` style is still seen in logging calls (for performance -- the string is only formatted if the log level is active).

### Common String Methods
Python string methods return new strings; they do not mutate the original.

```python
s = "  Hello, World  "

s.strip()          # "Hello, World"       -- trim whitespace (cf. JS .trim())
s.lower()          # "  hello, world  "
s.upper()          # "  HELLO, WORLD  "
s.replace("o", "0")  # "  Hell0, W0rld  "
s.split(", ")      # ["  Hello", "World  "]
"---".join(["a", "b", "c"])  # "a---b---c"
s.startswith("  He")  # True
s.endswith("ld  ")    # True
s.find("World")       # 9  (-1 if not found, unlike JS .indexOf)
s.count("l")          # 3
```

### String as Sequence
Because `str` is a sequence type, slicing and iteration work without conversion.

```python
s = "Python"

s[0]      # "P"
s[-1]     # "n"
s[1:4]    # "yth"    [start:stop] -- stop is exclusive
s[::2]    # "Pto"    [start:stop:step]
s[::-1]   # "nohtyP" -- reverse

for char in s:
    print(char)

"Py" in s  # True -- membership test
```

### Raw Strings
The `r` prefix disables escape sequence processing. Used for regular expressions and file paths on Windows.

```python
pattern = r"\d+\.\d+"          # literal backslashes, not escape sequences
path = r"C:\Users\name\file"   # no need to double-escape backslashes
```

### Multiline and String Encoding
```python
# Explicit newline
line = "first\nsecond"

# Unicode character by code point
em_dash = "\u2014"

# Encode to bytes / decode back
b = "hello".encode("utf-8")   # b'hello' -- bytes object
s = b.decode("utf-8")          # "hello"
```

## Code Comparison

**JavaScript (Node.js)**
```javascript
const name = "Alice";
const score = 98.5;

// Template literals
const result = `User ${name} scored ${score.toFixed(2)}`;

// String methods
"  hello  ".trim();         // "hello"
"hello".toUpperCase();      // "HELLO"
"hello world".split(" ");   // ["hello", "world"]
["a","b","c"].join("-");    // "a-b-c"
"hello".includes("ell");    // true
"hello".slice(1, 4);        // "ell"
```

**Python**
```python
name = "Alice"
score = 98.5

# f-string
result = f"User {name} scored {score:.2f}"

# String methods
"  hello  ".strip()          # "hello"
"hello".upper()              # "HELLO"
"hello world".split(" ")     # ["hello", "world"]
"-".join(["a", "b", "c"])   # "a-b-c"
"ell" in "hello"             # True (membership operator, not a method)
"hello"[1:4]                 # "ell" (slice notation, not a method)
```

Key differences:
- Python uses `in` for membership; JavaScript uses `.includes()`
- Python uses slice notation `[start:stop]`; JavaScript uses `.slice()`
- Python's `join` is called on the delimiter string, not the list -- the inverse of JS

## Documentation
- [Python Built-in Types: str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)
- [Python String Methods](https://docs.python.org/3/library/stdtypes.html#string-methods)
