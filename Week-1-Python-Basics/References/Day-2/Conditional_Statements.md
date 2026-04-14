# Conditional Statements

## Objective
Syntax for controlling execution flow through boolean evaluation.

## JavaScript Equivalent
JavaScript `if / else if / else` and ternary statements.

## Implementation Details

### Indentation and `elif`
Python relies entirely on indentation instead of curly braces. Conditions do not require surrounding parentheses. Python substitutes `else if` for the `elif` keyword.

```python
status_code = 403

if status_code == 200:
    print("Success")
elif status_code == 403:
    print("Forbidden")
else:
    print("Unknown")
```

### Truthiness Differences
The definition of truthiness in Python varies significantly from JavaScript, mostly concerning collections. In JavaScript, an empty array `[]` or object `{}` evaluates to `True`. In Python, any empty collection (list, dict, set, string) evaluates natively to `False`.

```python
records = []

# Idiomatic check for empty sequence
if not records:
    print("No records found (Evaluates to False)")

# JS-style explicit length check is considered non-idiomatic in Python
if len(records) == 0:
    pass
```

### The Ternary Operator Expression
Python has a conditional expression acting as a ternary operator, but it flips the order compared to JavaScript's `condition ? truth_val : falsy_val`.

```python
mode = "production"
# Syntax: {truthy_outcome} if {condition} else {falsy_outcome}
connection_string = "prod_db" if mode == "production" else "local_db"
```

## Code Comparison

**JavaScript (Node.js)**
```javascript
const items = [];

if (items.length > 0) {
    console.log("Processing");
} else if (items === "flag") {
    console.log("Flagged");
} else {
    console.log("Empty");
}

const tag = isActive ? "ON" : "OFF";
```

**Python**
```python
items = []

# Truthiness handles length implicitly
if items:
    print("Processing")
elif items == "flag":
    print("Flagged")
else:
    print("Empty")

tag = "ON" if is_active else "OFF"
```

## Documentation
- [Python Compound Statements: The if statement](https://docs.python.org/3/reference/compound_stmts.html#the-if-statement)
- [Python Expressions: Conditional Expressions](https://docs.python.org/3/reference/expressions.html#conditional-expressions)
