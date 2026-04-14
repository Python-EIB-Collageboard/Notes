# User Input and Output

## Objective
Python's built-in mechanisms for reading input from stdin and writing output to stdout and stderr.

## JavaScript Equivalent
In Node.js, console I/O requires the `readline` module (or third-party libraries) to read from stdin. Writing to stdout uses `process.stdout.write()` or `console.log()`. Python provides `input()` and `print()` as built-in functions, requiring no imports for basic terminal I/O.

## Implementation Details

### `print()` -- Standard Output

`print()` writes to `sys.stdout` by default. It accepts any number of positional arguments and separates them with a configurable separator.

```python
print("Hello, World")             # Hello, World
print("Name:", "Alice", "Age:", 30)  # Name: Alice Age: 30
```

#### `sep` -- Separator
The `sep` keyword argument controls the string placed between multiple arguments. Default is a single space `" "`.

```python
print("2026", "04", "14", sep="-")  # 2026-04-14
print("a", "b", "c", sep="")        # abc
print("col1", "col2", "col3", sep="\t")  # tab-separated
```

#### `end` -- Line Terminator
The `end` keyword argument controls what is appended after the last argument. Default is `"\n"`.

```python
print("loading", end="")  # no newline -- cursor stays on same line
print(".", end="")
print(".", end="")
print("done")              # loading...done
```

#### `file` -- Output Destination
The `file` keyword argument redirects output to any object with a `write()` method.

```python
import sys

print("Critical error", file=sys.stderr)  # write to stderr instead of stdout
```

#### `flush` -- Buffer Control
```python
import time

for i in range(5):
    print(i, end=" ", flush=True)  # forces immediate write -- no buffering
    time.sleep(0.5)
```

### `input()` -- Standard Input
`input()` reads a line from stdin, strips the trailing newline, and returns the value as a `str`. An optional prompt string is displayed before reading.

```python
name = input("Enter your name: ")
print(f"Hello, {name}")
```

The return value is always `str`. Type conversion must be done explicitly.

```python
age_str = input("Enter your age: ")
age = int(age_str)  # explicit conversion required

# Inline conversion (common pattern)
age = int(input("Enter your age: "))
```

If the user presses Ctrl-D (Unix) or Ctrl-Z (Windows) at the `input()` prompt, an `EOFError` is raised. Robust programs handle this:

```python
try:
    value = input("Enter value: ")
except EOFError:
    value = None
```

### `sys.stdout` and `sys.stderr` Directly
For fine-grained control, write directly to the standard streams. This bypasses `print()`'s separator and newline logic.

```python
import sys

sys.stdout.write("no newline appended")
sys.stderr.write("error message\n")
```

### `pprint` -- Pretty-Print Structured Data
The `pprint` module formats complex data structures for readable terminal output.

```python
from pprint import pprint

data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}
pprint(data)
# {'users': [{'id': 1, 'name': 'Alice'},
#            {'id': 2, 'name': 'Bob'}]}

# Compact output
pprint(data, compact=True)
```

`pprint` is a development and debugging aid. For structured logging in production, use the `logging` module (Day 4).

### Output Formatting Summary
`print()` uses Python's standard string formatting. The f-string form is most readable for inline use.

```python
name = "Alice"
score = 98.5

# f-string (preferred)
print(f"User: {name}, Score: {score:.2f}")

# str.format()
print("User: {}, Score: {:.2f}".format(name, score))

# Column alignment example
print(f"{'Name':<10} {'Score':>8}")
print(f"{name:<10} {score:>8.2f}")
# Name          Score
# Alice          98.50
```

## Code Comparison

**JavaScript (Node.js)**
```javascript
const readline = require("readline");

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question("Enter your name: ", (name) => {
    console.log(`Hello, ${name}`);
    rl.close();
});

// Writing to stdout / stderr
process.stdout.write("no newline\n");
process.stderr.write("error message\n");
console.log("Name:", "Alice", "Age:", 30);  // space-separated
console.error("error to stderr");
```

**Python**
```python
# No import needed for basic I/O

name = input("Enter your name: ")
print(f"Hello, {name}")

# Synchronous -- execution blocks at input() until user presses Enter
# No callbacks, no event loop required for terminal input

import sys
sys.stdout.write("no newline\n")
sys.stderr.write("error message\n")

print("Name:", "Alice", "Age:", 30)  # Name: Alice Age: 30 (space-separated by default)
print("error to stderr", file=sys.stderr)
```

Key differences:
- Python's `input()` is synchronous and blocking. Node.js stdin reading is asynchronous by default -- it requires either callbacks (`readline`) or the `--input-type` module with `process.stdin` streams.
- Python requires no import for `print()` or `input()` -- both are built-ins.
- `print()` automatically converts arguments to `str` via `str()`. Node.js `console.log()` does the same.

## Documentation
- [Python Built-in Functions: print()](https://docs.python.org/3/library/functions.html#print)
- [Python Built-in Functions: input()](https://docs.python.org/3/library/functions.html#input)
