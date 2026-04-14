# For Loops

## Objective
Python's standard sequential iteration abstraction mechanics.

## JavaScript Equivalent
JavaScript `for...of` loops. Python lacks a traditional index-based C-style `for (let i = 0; i < limit; i++)` loop completely operations must target Iterables directly.

## Implementation Details

### Iterable Execution
A Python `for` loop interacts directly with lists, tuples, dictionaries, sets, and strings. You do not maintain an external counter variable.

```python
servers = ["web01", "db01", "cache01"]

# Idiomatic iteration
for server in servers:
    print(f"Pinging {server}")
```

### The `enumerate()` Function
When an operational index is explicitly required alongside the value, Python relies on the built-in `enumerate()` function. It yields a tuple `(index, value)` on each iteration, which you can unpack inline.

```python
# Similar behavior to JS array.map((val, i) => {...}) or array.entries()
for index, server in enumerate(servers):
    print(f"[{index}] Pinging {server}")
```

### Unpacking Multiple Values
Because tuple unpacking is a core Python feature, iterating over complex data structures like dictionaries natively supports mapping keys and values simultaneously. 

```python
config = {"host": "localhost", "port": 8080}

# Iterating object entries
for key, val in config.items():
    print(key, val)
```

### The loop `else` Clause
Identical to `while` loops, Python `for` loops support an `else` block that is completely skipped if the loop is short-circuited via `break`. It is most frequently used for "search and find" operations.

```python
for server in servers:
    if "db" in server:
        print("Database found!")
        break
else:
    # Executes only if 'break' was never hit
    print("No database configured in cluster.")
```

## Code Comparison

**JavaScript (Node.js)**
```javascript
const fruits = ["apple", "banana", "cherry"];

// Index-based (Traditional)
for (let i = 0; i < fruits.length; i++) {
    console.log(i, fruits[i]);
}

// Element-based (for...of)
for (const fruit of fruits) {
    console.log(fruit);
}
```

**Python**
```python
fruits = ["apple", "banana", "cherry"]

# Enumerate-based (Indexed)
for i, fruit in enumerate(fruits):
    print(i, fruit)

# Element-based iteration (Standard)
for fruit in fruits:
    print(fruit)
```

## Documentation
- [Python Compound Statements: The for statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement)
