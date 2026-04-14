# Python Modules -- Math

## Objective
Advanced mathematical operations, type conversions, and precision handling using the Python standard library.

## JavaScript Equivalent
JavaScript exposes mathematical functions solely through the globally available `Math` object (e.g., `Math.floor()`, `Math.PI`). Python separates fundamental arithmetic and numeric built-ins from advanced mathematical operations, requiring the `math` module for the latter.

## Implementation Details

### Built-in vs Module Functions
Python distinguishes between basic numeric operations that are built into the language and complex mathematical functions that reside in the `math` module. Functions like `abs()`, `pow()`, and `round()` are built-in and require no import, akin to global functions, while operations like trigonometry, logarithms, and floor/ceiling require `import math`.

### Handling Floating-Point Precision
Both JavaScript and Python use IEEE 754 double-precision floats, meaning they share the same precision anomalies (e.g., `0.1 + 0.2 === 0.30000000000000004`). In JavaScript, developers typically check equality using `Number.EPSILON`. Python's `math` module provides the `math.isclose()` function, abstracting the relative and absolute tolerance calculations required to safely compare floating-point values.

### Modular Division and specialized functions
Python includes functions tailored for data manipulation that JavaScript lacks natively, such as `math.factorial()`, `math.gcd()` (Greatest Common Divisor), and `math.trunc()` for truncating the fractional part of a number. Additionally, Python has the built-in `divmod(a, b)` function, which returns a tuple containing the quotient and the remainder, an operation that requires manual calculation in JavaScript.

### Complex Numbers
JavaScript does not natively support complex numbers. Python supports them at the language level (e.g., `3 + 4j`) and provides a parallel standard library module, `cmath`, specifically designed for mathematical operations on complex numbers.

## Code Comparison

**JavaScript (Node.js)**
```javascript
// Global Math object
const pi = Math.PI;
const ceiled = Math.ceil(4.2);
const floored = Math.floor(4.8);
const power = Math.pow(2, 3); // es6 support 2 ** 3

// Floating point equality check
const a = 0.1 + 0.2;
const b = 0.3;
const isClose = Math.abs(a - b) < Number.EPSILON;

// Absolute value
const absolute = Math.abs(-10);
```

**Python**
```python
import math

# Requires math module
pi_val = math.pi
ceiled = math.ceil(4.2)
floored = math.floor(4.8)
factorial = math.factorial(5)  # 120

# Floating point equality check
a = 0.1 + 0.2
b = 0.3
is_close = math.isclose(a, b)  # True

# Built-in mathematical functions (No import required)
absolute = abs(-10)
power = pow(2, 3) # Or 2 ** 3
quotient, remainder = divmod(10, 3)  # Returns tuple (3, 1)

# Complex numbers (j suffix)
complex_num = 3 + 4j
```

## Documentation
- [Python Standard Library: math](https://docs.python.org/3/library/math.html)
- [Python Built-in Functions](https://docs.python.org/3/library/functions.html)
- [Python Standard Library: cmath](https://docs.python.org/3/library/cmath.html)
