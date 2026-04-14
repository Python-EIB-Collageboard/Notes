# Lists

## Objective
Python's standard mutable, ordered collection and its distinction from JavaScript arrays.

## JavaScript Equivalent
JavaScript arrays are dynamic, weakly typed collections that behave like hash maps under the hood for sparse indices. Python's `list` is a dense, dynamically-sized array of references. It requires contiguous memory, guarantees order, and prevents out-of-bounds assignment.

## Implementation Details

### Initialization and Modification
Python lists are mutable but strictly zero-indexed. Unlike JavaScript, assigning to an index beyond the current length raises an `IndexError` rather than creating empty slots.

```python
data = [1, 2, 3]
data[0] = 10         # Mutates first element
# data[5] = 20       # IndexError (JavaScript would create a sparse array)
data.append(4)       # JS Equivalent: data.push(4)
data.extend([5, 6])  # JS Equivalent: data = data.concat([5, 6])
data.pop()           # Removes and returns the last element
```

### Negative Indexing
Python supports native negative indexing, returning elements from the right end of the sequence.

```python
data = ["a", "b", "c", "d"]
print(data[-1]) # 'd' (JS Equivalent: data[data.length - 1])
print(data[-2]) # 'c'
```

### Slicing
Python introduces syntax for array slicing that is highly idiomatic and widely used heavily favored over function calls like JS's `.slice()`. The syntax is `[start:stop:step]`.

```python
data = [0, 1, 2, 3, 4, 5]
data[1:4]   # [1, 2, 3] (Exclusive of stop index)
data[:3]    # [0, 1, 2] (Start defaults to 0)
data[3:]    # [3, 4, 5] (Stop defaults to end)
data[::2]   # [0, 2, 4] (Step by 2)
data[::-1]  # [5, 4, 3, 2, 1, 0] (Idiomatic sequence reversal)
```

### List Comprehensions
List comprehensions provide a concise way to generate lists, generally replacing JS's `.map()` and `.filter()`.

```python
numbers = [1, 2, 3, 4]
# Equivalent to JS: numbers.map(x => x * 2)
doubled = [x * 2 for x in numbers]

# Equivalent to JS: numbers.filter(x => x % 2 === 0).map(x => x * 2)
doubled_evens = [x * 2 for x in numbers if x % 2 == 0]
```

## Code Comparison

**JavaScript (Node.js)**
```javascript
const items = [1, 2, 3];
items.push(4);
const reversed = items.slice().reverse();

const oddSquares = items
    .filter(n => n % 2 !== 0)
    .map(n => n * n);
```

**Python**
```python
items = [1, 2, 3]
items.append(4)
reversed_items = items[::-1]

odd_squares = [n * n for n in items if n % 2 != 0]
```

## Documentation
- [Python Built-in Types: Sequence Types — list, tuple, range](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range)
