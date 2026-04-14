# Variables

## Objective
Python's variable declaration model and its type system as they differ from JavaScript's `var`, `let`, and `const`.

## JavaScript Equivalent
JavaScript requires an explicit declaration keyword (`var`, `let`, `const`) before a variable can be used. Python has no such keyword -- assignment is declaration. Python is dynamically typed like JavaScript, but its type system behaves differently at the implementation level.

## Implementation Details

### Assignment is Declaration
In Python, a variable comes into existence at the moment of assignment. There is no `let`, `const`, or `var`.

```python
x = 10
name = "Alice"
is_active = True
```

### No `const` Equivalent
Python has no language-enforced constant. The PEP 8 convention of `UPPER_SNAKE_CASE` signals intent, but nothing prevents reassignment. Type checkers (e.g., `mypy`) can enforce `Final` annotations at static analysis time.

```python
MAX_CONNECTIONS = 100  # convention only, not enforced by the runtime

from typing import Final
MAX_CONNECTIONS: Final = 100  # mypy will flag reassignment
```

### Dynamic Typing
Python variables hold references to objects, not values directly. A variable's type is the type of the object it currently references and can change across assignments.

```python
x = 10       # x references an int object
x = "hello"  # x now references a str object -- no error
```

### Type Annotations (Optional)
PEP 526 introduced variable annotations. These are metadata for static analysis tools -- they do not change runtime behavior.

```python
user_id: int = 42
username: str = "alice"
active: bool = True
```

### Multiple Assignment
Python supports simultaneous assignment to multiple targets in a single statement.

```python
a, b, c = 1, 2, 3       # tuple unpacking
x = y = z = 0            # chained assignment -- all point to the same object
first, *rest = [1, 2, 3, 4]  # star unpacking: first=1, rest=[2,3,4]
```

### Scope Rules (LEGB)
Python resolves names using the LEGB rule: Local, Enclosing, Global, Built-in. This differs from JavaScript's scope chain in one critical way: Python functions do not create new bindings for outer variables without an explicit `global` or `nonlocal` declaration.

```python
count = 0

def increment():
    global count  # required to rebind the module-level variable
    count += 1
```

Without `global count`, the line `count += 1` raises an `UnboundLocalError` because Python sees the assignment and treats `count` as a local variable that has not yet been assigned.

### Deletion
Variables can be unbound from their name using `del`.

```python
x = 10
del x
print(x)  # NameError: name 'x' is not defined
```

## Code Comparison

**JavaScript (Node.js)**
```javascript
let score = 100;
const MAX = 500;
let label = "active";

// Destructuring
const [first, second, ...remaining] = [1, 2, 3, 4, 5];

// Block-scoped: label is not accessible outside this block
{
    let label = "inside";
}
```

**Python**
```python
score = 100
MAX = 500          # convention only
label = "active"

# Unpacking
first, second, *remaining = [1, 2, 3, 4, 5]

# Python has no block scope -- variables assigned inside if/for/while
# are accessible outside the block in the same function scope
if True:
    label = "inside"
print(label)  # "inside" -- accessible
```

The absence of block scope in Python is a frequent source of confusion for JavaScript developers. Python scoping boundaries are: module, function, class, and comprehension.

## Documentation
- [Python Reference: Assignment Statements](https://docs.python.org/3/reference/simple_stmts.html#assignment-statements)
- [PEP 526 -- Syntax for Variable Annotations](https://peps.python.org/pep-0526/)
