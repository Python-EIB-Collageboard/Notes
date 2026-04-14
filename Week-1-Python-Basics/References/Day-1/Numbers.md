# Numbers

## Objective
Python's numeric types (`int`, `float`, `complex`), their behavioral differences from JavaScript's single `Number` type, and the arithmetic operators that govern them.

## JavaScript Equivalent
JavaScript has one numeric primitive: `Number` (64-bit IEEE 754 double-precision float). Python separates numeric types into distinct classes: `int` (arbitrary precision), `float` (64-bit double), and `complex`. The practical consequence is that Python integers do not overflow and integer division has explicit control.

## Implementation Details

### `int` -- Arbitrary Precision
Python `int` has no maximum size. It grows as needed using an internal bignum representation.

```python
big = 10 ** 100  # a googol -- no overflow, no BigInt required
print(type(big))  # <class 'int'>
```

JavaScript requires `BigInt` (with the `n` suffix) for integers beyond `Number.MAX_SAFE_INTEGER` (2^53 - 1). Python handles this transparently.

### `float`
Python `float` is a 64-bit IEEE 754 double, identical to JavaScript's `Number`.

```python
x = 3.14
y = 1.5e10   # scientific notation
z = float("inf")
n = float("nan")

import math
math.isinf(z)  # True
math.isnan(n)  # True
```

Floating-point precision issues are present in Python for the same reason as in JavaScript:

```python
0.1 + 0.2  # 0.30000000000000004
```

Use the `decimal` module (covered in Day 4 -- standard library) for arbitrary-precision decimal arithmetic.

### `complex`
Python has a native complex number type with real and imaginary parts.

```python
c = 3 + 4j
c.real  # 3.0
c.imag  # 4.0
abs(c)  # 5.0 -- magnitude
```

This has no direct JavaScript equivalent.

### Arithmetic Operators
| Operator | Python | JavaScript | Notes |
|---|---|---|---|
| Addition | `+` | `+` | Same |
| Subtraction | `-` | `-` | Same |
| Multiplication | `*` | `*` | Same |
| Division | `/` | `/` | Python `/` always returns `float` |
| Floor Division | `//` | `Math.floor(a/b)` | Python-only infix operator |
| Modulo | `%` | `%` | Same symbol, same behavior for positive numbers |
| Exponentiation | `**` | `**` | Same in modern JS |

### Division Behavior -- Critical Difference
In Python, `/` performs true (float) division regardless of operand types. `//` performs floor division (integer result truncated toward negative infinity).

```python
7 / 2    # 3.5  (float -- not 3)
7 // 2   # 3    (floor division)
-7 // 2  # -4   (floors toward negative infinity, not toward zero)
7 % 2    # 1
```

In JavaScript, `7 / 2` produces `3.5` (same as Python's `/`), but JavaScript has no `//` floor division operator -- developers use `Math.floor()` or bitwise `|0`.

### Augmented Assignment Operators
```python
x = 10
x += 5   # 15
x -= 3   # 12
x *= 2   # 24
x //= 5  # 4  (floor division assignment)
x **= 3  # 64
x %= 10  # 4
```

Python does not have `++` or `--` increment/decrement operators.

### Type Conversion
```python
int("42")       # 42
int(3.9)        # 3  (truncates, does not round)
float("3.14")   # 3.14
str(100)        # "100"
round(3.567, 2) # 3.57
```

### Numeric Literals
```python
# Underscores as separators (PEP 515)
million = 1_000_000
pi_approx = 3.141_592_653

# Integer bases
binary = 0b1010   # 10
octal  = 0o17     # 15
hex_   = 0xFF     # 255
```

JavaScript supports the same integer literal formats (`0b`, `0o`, `0x`) but not underscore separators in all environments.

### Built-in Numeric Functions
```python
abs(-5)          # 5
pow(2, 10)       # 1024  (same as 2 ** 10 but accepts a modulus third argument)
pow(2, 10, 100)  # (2**10) % 100 = 24
round(2.675)     # 3
round(2.675, 2)  # 2.67  (banker's rounding -- be aware)
divmod(17, 5)    # (3, 2) -- quotient and remainder as a tuple
```

## Code Comparison

**JavaScript (Node.js)**
```javascript
// Single Number type
const a = 7;
const b = 2;

a / b;           // 3.5
Math.floor(a/b); // 3
a % b;           // 1
a ** 3;          // 343

// BigInt for large integers
const big = 10n ** 100n;

// Type conversion
parseInt("42");   // 42
parseFloat("3.14"); // 3.14
String(100);      // "100"
```

**Python**
```python
a = 7
b = 2

a / b    # 3.5  (true division)
a // b   # 3    (floor division -- infix operator)
a % b    # 1
a ** 3   # 343

# No BigInt suffix needed -- int is arbitrary precision
big = 10 ** 100

# Type conversion
int("42")     # 42
float("3.14") # 3.14
str(100)      # "100"
```

## Documentation
- [Python Built-in Types: Numeric Types](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)
- [Python Built-in Functions: Numeric](https://docs.python.org/3/library/functions.html#built-in-functions)
