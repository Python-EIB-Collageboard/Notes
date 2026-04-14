# Operators

## Objective
Python's numeric and object comparison syntax behavior.

## JavaScript Equivalent
JavaScript Mathematical (`+, -, *, /, %, **`), Logical (`&&, ||, !`), and Relational (`==, ===, !=, !==`) Operators.

## Implementation Details

### Logical Keywords
Python substitutes logical symbolic operators (`&&`, `||`, `!`) with English keywords (`and`, `or`, `not`). They provide exactly the same short-circuit logic as JS equivalents.

```python
is_admin = True
is_active = False

if is_admin and not is_active:
    print("Archived Admin")
```

### Identity vs Equality
In JS, `==` attempts silent type coercion and `===` enforces exact identity lock. In Python, variables are inherently strongly typed preventing implicit casting (i.e. `"5" == 5` is always `False` in Python). 

Therefore, Python breaks equality into **Value** and **Identity**:
- **Value Evaluation (`==`)**: Evaluates if the underlying data holds the same information. 
- **Memory Identity Evaluation (`is`)**: Evaluates if the operators point to the absolute same address in system memory.

```python
list_a = [1, 2, 3]
list_b = [1, 2, 3]
list_c = list_a

print(list_a == list_b) # True: The values match
print(list_a is list_b) # False: They are two distinct objects in memory
print(list_a is list_c) # True: Both point to the same memory block
```

### Assignment Expressions (Walrus Operator)
JavaScript regularly allows immediate assignment during condition checks: `if ((res = process()) !== null)`. Python added the `:=` "Walrus Operator" in v3.8 specifically to isolate variable assignment occurring concurrently during an expression. Normal assignments (`=`) are forbidden in expressions.

```python
# The operator assigns the length to 'n', and then evaluates 'n > 10'
if (n := len(data_set)) > 10:
    print(f"Data set too large: {n} items")
```

### Specific Numeric Operations
Python natively adds floor division operator `//` which trims trailing decimal floats.

```python
val = 10 / 3  # 3.3333333333333335 (Always yields a float in Python 3)
val = 10 // 3 # 3 (Truncates to integer block)
val = 2 ** 3  # 8 (Exponentiation - JS adopted this same operator later)
```

## Code Comparison

**JavaScript (Node.js)**
```javascript
// Truthiness + Equality
const a = [];
const b = [];
console.log(a == b); // false (checking memory reference via weak equality)
console.log(a === b); // false (checking memory reference via strong equality)

// Math
const intDiv = Math.floor(10 / 3);

// Assignment expression
let match;
if (match = fetchRegex()) {
    console.log(match);
}
```

**Python**
```python
# Truthiness + Equality
a = []
b = []
print(a == b) # True (checks internal value representation)
print(a is b) # False (checks hardware memory reference)

# Math
int_div = 10 // 3

# Assignment expression (Walrus operator)
if match := fetch_regex():
    print(match)
```

## Documentation
- [Python Expressions: Operator Precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence)
- [Python Built-in Constants: is](https://docs.python.org/3/reference/expressions.html#is)
