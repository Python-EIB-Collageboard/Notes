# File Handling

## Objective
Synchronous file system interactions, automated resource leak prevention, and object streams utilizing native built-ins.

## JavaScript Equivalent
JavaScript manages file I/O through the `fs` core module via synchronous blocks (`fs.readFileSync`), callbacks, or promises. Python utilizes built-in functions to interface with the operating system directly, without requiring imports.

## Implementation Details

### The `open()` Function and Modes
Python accesses files by instantiating a stream object via the standard `open(file, mode)` function. Crucially, the target `mode` determines permissions and behavioral characteristics:
- `'r'` (Read): Default mode. Fails with `FileNotFoundError` if the file doesn't exist.
- `'w'` (Write): Opens a file exclusively for writing. Overwrites the file entirely if it exists; creates it if it doesn't.
- `'a'` (Append): Opens a file to append data to the end without truncating the existing payload.
- `'r+'` (Read and Write): Opens the file without truncation, allowing updates in place.
- Append a `'b'` to any mode (e.g., `'rb'`, `'wb'`) to operate in binary mode rather than standard text encoding (utf-8).

### The Peril of Open Resource Handles
Node.js relies entirely on garbage collection and event loops. When allocating a file stream asynchronously, it inherently detaches.

In Python, file handles are operating-system resources that remain allocated indefinitely until formally terminated via `.close()`. A program that repeatedly opens files without closing them will inevitably trigger `OSError: [Errno 24] Too many open files`.

### Context Managers (`with` statement)
JavaScript relies on developers explicitly using `finally` blocks to verify stream closure. Python mitigates this entirely using the `with` statement, known as a Context Manager. 

A Context Manager formally bounds an execution block. It guarantees that the `.__exit__()` method of an object (in this case, the file's `close` method) runs when the block concludes, even if a `RuntimeError` or early `return` violently terminates the block's execution. It is considered an extreme anti-pattern to manually call `.close()` in Python rather than wrapping the operation in a `with` statement.

### Modern File Paths
While Python maintains the traditional `os.path` module (analogous to Node's `path`), modern Python relies on the `pathlib` module, which abstracts file routes into object-oriented models rather than manipulating bare strings.

## Code Comparison

**JavaScript (Node.js)**
```javascript
const fs = require('fs');
const path = require('path');

const targetFile = path.join(__dirname, 'output.txt');

// Naive Synchronous Write (requires manual error verification in older iterations)
fs.writeFileSync(targetFile, 'Initialization data', 'utf8');

// Reading and explicit teardown checks
let fileDescriptor;
try {
    fileDescriptor = fs.openSync(targetFile, 'r');
    const buffer = fs.readFileSync(fileDescriptor, 'utf8');
    
    // Breaking by line
    const lines = buffer.split('\n');
    lines.forEach(line => console.log(line));
} catch (err) {
    console.error("I/O Failure:", err.message);
} finally {
    if (fileDescriptor !== undefined) {
        fs.closeSync(fileDescriptor);
    }
}
```

**Python**
```python
from pathlib import Path

# Object-oriented path resolution
target_file = Path.cwd() / "output.txt"

# Synchronous Write utilizing the 'with' context manager
with open(target_file, mode="w", encoding="utf-8") as file_stream:
    file_stream.write("Initialization data\n")
    file_stream.write("Secondary metrics\n")

# Reading -- the file is automatically and safely closed at the block conclusion
try:
    with open(target_file, mode="r", encoding="utf-8") as file_stream:
        # File streams are intrinsically iterable by line in Python
        for line in file_stream:
            # .strip() removes trailing newline characters
            print(line.strip())
            
        # Alternatively, file_stream.read() returns the entire file string
        # file_stream.readlines() returns an array of line strings
except FileNotFoundError as err:
    print(f"I/O Failure: {err}")
```

## Documentation
- [Python Tutorial: Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
- [Python Reference: The 'with' statement](https://docs.python.org/3/reference/compound_stmts.html#with)
- [Python Standard Library: pathlib](https://docs.python.org/3/library/pathlib.html)
