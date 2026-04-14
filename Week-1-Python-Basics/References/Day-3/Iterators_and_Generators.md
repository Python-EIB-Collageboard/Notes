# Iterators and Generators

## Objective
Implementation of lazy evaluation, stateful chronological data streams, and the underlying Iterator Protocol.

## JavaScript Equivalent
JavaScript Iterators (`[Symbol.iterator]` and `.next()`) and Generator functions (`function*` and the `yield` keyword).

## Implementation Details

### The Iterator Protocol
Both JavaScript and Python operate heavily on iterators -- objects that represent a stream of data. An object is considered iterable in Python if it implements the Iterator Protocol via two specific dunder methods:
1. `__iter__()`: Must return the iterator object itself.
2. `__next__()`: Must return the next value from the stream.

While JavaScript signals the end of a stream by returning an object `{ value: undefined, done: true }`, Python signals termination by explicitly raising the `StopIteration` built-in exception. The standard `for ... in` loop automatically catches this exception to cleanly exit the loop.

### Generators and `yield`
Writing custom iterators using complex classes is overly verbose. Both languages solve this with Generators -- functions that "pause" execution and emit values selectively.

Python uses the standard `def` keyword (unlike JS which requires `function*`). The interpreter recognizes that the function is a generator structurally because it contains the `yield` keyword rather than `return`.

When a generator function is invoked, it does not execute. Instead, it returns a generator object. Execution only begins when `next()` is called on that object, pausing immediately when it encounters `yield`, freezing local variable state.

### Generator Expressions
Python provides a highly optimized, inline syntax for constructing simple generators known as "Generator Expressions". Syntactically, they look identical to list comprehensions but use parentheses `()` instead of brackets `[]`. This provides lazy execution without requiring a formal function definition.

This is critical for memory optimization when processing millions of records where loading the entire payload into RAM via a standard list would trigger an `OutOfMemory` fault.

## Code Comparison

**JavaScript (Node.js)**
```javascript
// Generator definition requires the asterisk
function* countdown(start) {
    while (start > 0) {
        yield start;
        start -= 1;
    }
}

// Returns the iterator object
const counter = countdown(3);

console.log(counter.next()); // { value: 3, done: false }
console.log(counter.next()); // { value: 2, done: false }
console.log(counter.next()); // { value: 1, done: false }
console.log(counter.next()); // { value: undefined, done: true }

// Standard consumption
for (let num of countdown(3)) {
    console.log(num);
}
```

**Python**
```python
# Standard def keyword. The interpreter tracks the 'yield' presence
def countdown(start):
    while start > 0:
        yield start
        start -= 1

# Returns a generator object
counter = countdown(3)

# Manual execution using the built-in next() function
print(next(counter)) # 3
print(next(counter)) # 2
print(next(counter)) # 1

# Automatically catches StopIteration (Equivalent to done: true)
# print(next(counter)) -> raises StopIteration exception

# Standard usage pattern
for num in countdown(3):
    print(num)

# Generator Expressions (Memory efficient lazy evaluation)
# Will not process into lists until explicitly consumed
squares_generator = (x * x for x in range(1000000))

# Can be wrapped to immediately consume and load into memory 
# list_squares = list(squares_generator)
```

## Documentation
- [Python Tutorial: Iterators](https://docs.python.org/3/tutorial/classes.html#iterators)
- [Python Tutorial: Generators](https://docs.python.org/3/tutorial/classes.html#generators)
- [Python Glossary: generator](https://docs.python.org/3/glossary.html#term-generator)
