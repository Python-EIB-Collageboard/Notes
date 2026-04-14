# While Loops

## Objective
Python's syntax for indefinite execution and specific loop behavior.

## JavaScript Equivalent
JavaScript `while` and `do...while` loops. Python matches the standard `while` evaluation cycle but intentionally omits a `do...while` structure, requiring a different approach for post-evaluation loops.

## Implementation Details

### Standard Execution Flow
Like JS, the `while` loop checks its condition prior to starting the block. `break` instantly terminates the loop context, and `continue` jumps instantly to the next evaluation stage.

```python
count = 0
while count < 3:
    print(count)
    count += 1 # Python lacks the `++` post-increment operator
```

### Simulating do...while
Because Python lacks `do...while`, running an operation *at least once* before evaluating typically utilizes a `while True:` structure with an internal breakout.

```python
# Simulating a JavaScript do...while
while True:
    response = fetch_data()
    if response.is_valid():
        break
```

### The `else` Block in Loops
Python includes a unique feature allowing an `else` clause at the end of a `while` loop. The `else` block executes *only* if the loop condition resolves normally to False. If the loop is terminated early via a `break` statement, the `else` block is explicitly skipped. 

```python
retry_count = 0
while retry_count < 3:
    if attempt_connection():
        print("Connected!")
        break
    retry_count += 1
else:
    # Executed ONLY if the loop finishes all 3 attempts without a 'break'
    print("Connection failed after 3 attempts.")
```

## Code Comparison

**JavaScript (Node.js)**
```javascript
let i = 0;
while (i < 5) {
    if (i === 3) break;
    i++;
}

// Do-while equivalent
let result;
do {
    result = poll();
} while (!result);
```

**Python**
```python
i = 0
while i < 5:
    if i == 3:
        break
    i += 1

# Do-while equivalent
while True:
    result = poll()
    if result:
        break
```

## Documentation
- [Python Compound Statements: The while statement](https://docs.python.org/3/reference/compound_stmts.html#the-while-statement)
