# Lambda Functions

## Objective
Syntax and constraints for defining anonymous, inline functions evaluated as single expressions.

## JavaScript Equivalent
JavaScript Arrow Functions (e.g., `(x) => x * 2`). However, JavaScript arrow functions support full code blocks and multiple statements; Python lambda functions are strictly limited to single expressions.

## Implementation Details

### The `lambda` Keyword
Python employs the `lambda` keyword to declare anonymous functions. Unlike standard `def` functions, lambdas do not require an identifier name, nor do they enclose their body in a block. 

### Core Limitations
A lambda function in Python is an expression, not a statement.
1. **Single Expression Only:** A lambda can only evaluate a single expression. It cannot contain multi-line logic, assignments, or iterative statements (like `for` or `while`).
2. **Implicit Return:** The result of the evaluated expression is automatically returned. The explicit `return` keyword is forbidden inside a lambda.
3. **No Annotations:** Lambdas do not support type hinting annotations.

### Primary Use Case
While JavaScript uses arrow functions extensively as callbacks across the entire application ecosystem, Python restricts lambdas primarily to short-lived, trivial operations, typically passed as arguments to higher-order functions (e.g., `sorted()`, `map()`, `filter()`).

In Python, if a lambda requires complex logic, it is idiomatic to define a standard named function using `def` instead. 

## Code Comparison

**JavaScript (Node.js)**
```javascript
const numbers = [1, 5, 2, 8, 3];

// Arrow function used for simple mapping
const doubled = numbers.map(x => x * 2);

// Arrow function used for sorting with complex logic inside a block
const sortedData = numbers.sort((a, b) => {
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
});
```

**Python**
```python
numbers = [1, 5, 2, 8, 3]

# Lambda for short, single-expression logic
# Syntax: lambda arguments: expression
doubled = list(map(lambda x: x * 2, numbers))

# Commonly used as a 'key' function for sorting
# Sort a list of dictionaries by the 'score' key
users = [
    {"name": "Alice", "score": 88},
    {"name": "Bob", "score": 95},
    {"name": "Charlie", "score": 72}
]

users_sorted = sorted(users, key=lambda user: user["score"], reverse=True)

# Calling a lambda immediately (IIFE equivalent)
result = (lambda x, y: x + y)(5, 10) # 15

# Assignment to variable is possible but discouraged by PEP 8
# Idiomatic python prefers 'def format_name(name): return name.lower()'
format_name = lambda name: name.lower()
```

## Documentation
- [Python Tutorial: Lambda Expressions](https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions)
- [Python Reference: Expressions - Lambdas](https://docs.python.org/3/reference/expressions.html#lambda)
