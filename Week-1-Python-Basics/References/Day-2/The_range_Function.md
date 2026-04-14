# The range Function

## Objective
Python's native numeric sequence generator mechanism.

## JavaScript Equivalent
JavaScript lacks a native equivalent and typically relies on traditional index `for` loops or manual list mappings (`Array.from({length: n}, (_, i) => i)`).

## Implementation Details

### Generation vs Memory Allocation
The `range()` function creates an iterable object representing an arithmetic progression. Crucially, it evaluates the sequence *lazily*. `range(1000000)` does not instantiate one million integers in memory; it holds the bounds mathematically and yields the next sequential number only when directly requested by the interpreter.

```python
# Evaluates lazily
r = range(10) 
print(type(r)) # <class 'range'>

# Coercing into a List immediately instantiates it into memory
print(list(r)) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Step Control
`range()` absorbs up to three arguments: `start` (inclusive), `stop` (exclusive), and an iterative `step`.

```python
# One argument: Stop limit (Starts at 0 implicitly)
for i in range(5):
    pass # 0, 1, 2, 3, 4

# Two arguments: Start limit, Stop limit
for i in range(2, 6):
    pass # 2, 3, 4, 5

# Three arguments: Start limit, Stop limit, Step
for i in range(0, 10, 2):
    pass # 0, 2, 4, 6, 8
```

### Negative Sequences
By passing a negative step parameter, the generator yields backwards.

```python
for count_down in range(5, 0, -1):
    print(count_down) # 5, 4, 3, 2, 1
```

## Code Comparison

**JavaScript (Node.js)**
```javascript
// Iterating 0 through 4
for (let i = 0; i < 5; i++) {
    console.log(i);
}

// Iterating backward
for (let i = 5; i > 0; i--) {
    console.log(i);
}
```

**Python**
```python
# Iterating 0 through 4
for i in range(5):
    print(i)

# Iterating backward
for i in range(5, 0, -1):
    print(i)
```

## Documentation
- [Python Built-in Types: range](https://docs.python.org/3/library/stdtypes.html#ranges)
