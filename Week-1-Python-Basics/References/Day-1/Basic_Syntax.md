# Basic Syntax

## Objective
Python's structural conventions and execution model as they differ from JavaScript.

## JavaScript Equivalent
JavaScript uses curly braces `{}` for block scoping, semicolons as statement terminators, and requires an explicit runtime (Node.js) outside the browser. Python replaces all of these with indentation-based blocks, newlines as terminators, and a directly invokable interpreter.

## Implementation Details

### Indentation as Syntax
Python has no curly-brace block delimiters. Indentation is not stylistic -- it is enforced by the parser. The standard is 4 spaces. Mixed tabs and spaces will raise an `IndentationError`.

```python
# Valid block
if True:
    x = 1
    y = 2

# IndentationError -- inconsistent indentation
if True:
    x = 1
  y = 2  # wrong indentation level
```

### Statement Terminators
Python uses the newline character as the statement terminator. Semicolons are syntactically valid but idiomatic Python omits them.

```python
x = 1       # standard
y = 2;      # valid but non-idiomatic
a = 1; b = 2  # valid multi-statement, non-idiomatic
```

### Line Continuation
Long expressions can be continued on the next line using a backslash `\` or implicitly inside any unmatched bracket pair `()`, `[]`, or `{}`.

```python
# Explicit continuation
result = 1 + 2 + 3 + \
         4 + 5

# Implicit continuation (preferred)
result = (
    1 + 2 + 3 +
    4 + 5
)
```

### Comments
Single-line comments use `#`. Python has no multi-line comment syntax; consecutive `#` lines or a bare string literal (docstring) serve that purpose.

```python
# Single-line comment

"""
This is a docstring, typically used to document modules, classes, and functions.
It is not a true block comment -- it is a string expression that is evaluated
and discarded (or stored as __doc__).
"""
```

### Naming Conventions
Python enforces no naming rules beyond identifier validity, but PEP 8 is the authoritative style guide for the language.

| Construct | Convention | Example |
|---|---|---|
| Variable | `snake_case` | `user_count` |
| Function | `snake_case` | `get_user()` |
| Class | `PascalCase` | `UserProfile` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Private member | `_leading_underscore` | `_internal_cache` |

JavaScript uses `camelCase` for variables and functions, `PascalCase` for classes -- the only overlap is at the class level.

### The `pass` Statement
Python requires syntactically non-empty blocks. `pass` is a no-op placeholder used where a block is required but no logic is needed yet.

```python
def stub_function():
    pass  # equivalent to an empty function body in JS: function stub() {}

class EmptyClass:
    pass
```

### Entry Point Convention
Python files execute top-to-bottom when run directly. The `if __name__ == "__main__":` guard prevents top-level code from executing when the file is imported as a module. This is the Python equivalent of Node.js distinguishing between `require()` and direct execution.

```python
def main():
    print("Entry point")

if __name__ == "__main__":
    main()
```

## Code Comparison

**JavaScript (Node.js)**
```javascript
function greet(name) {
    if (name) {
        console.log("Hello, " + name);
    } else {
        console.log("Hello, world");
    }
}

greet("Alice");
```

**Python**
```python
def greet(name):
    if name:
        print("Hello, " + name)
    else:
        print("Hello, world")

greet("Alice")
```

Key structural differences:
- No `function` keyword -- Python uses `def`
- No curly braces -- indentation defines the block
- No `console.log` -- Python uses `print()`
- No parentheses required on `if` conditions (though valid if present)

## Documentation
- [Python Language Reference: Lexical Analysis](https://docs.python.org/3/reference/lexical_analysis.html)
- [PEP 8 -- Style Guide for Python Code](https://peps.python.org/pep-0008/)
