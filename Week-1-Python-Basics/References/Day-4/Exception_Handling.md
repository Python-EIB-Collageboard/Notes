# Exception Handling

## Objective
Strategic interception of runtime errors, custom exception generation, and deterministic resource teardown.

## JavaScript Equivalent
JavaScript execution leverages the `try...catch...finally` block for error interception, catching all thrown values indiscriminately. Developers use the `throw` keyword, typically instantiating native `Error` objects, to signal faults.

## Implementation Details

### The Python Paradigm: `try...except...else...finally`
Python utilizes a structurally similar pattern to JavaScript with two significant differences: explicit exception targeting and the `else` block.
- `try`: The bounded logic block verified for exceptions.
- `except`: Intercepts specific exception types. Python allows multiple cascading `except` blocks, catching different errors explicitly.
- `else`: Executes strictly and only if the `try` block completes successfully. JavaScript has no native parallel for this conceptual separation of logic.
- `finally`: Executes unconditionally, serving as a determinist resource teardown mechanism.

### Specificity in Exception Targeting
In JavaScript, `catch(err)` absorbs every error, requiring developers to manually write control flow inside the block (e.g., `if (err instanceof TypeError)`) to react appropriately.

Python natively targets exceptions in the block definition itself. Using a generic `except:` or `except Exception:` without logging the failure is considered a rigorous anti-pattern ("swallowing exceptions"). Engineers should catch strictly the granular errors expected.

### Catching vs Generating Errors
The JavaScript `throw` maps functionally to Python's `raise`. Python exceptions are standard classes that inherit from the root `BaseException` object (typically subclassing the `Exception` object). When intercepting an exception, engineers can bind the specific exception object to a local variable using the `as` keyword (e.g., `except TypeError as e`) to inspect its `.args` property or stack context.

### Bubbling
Identical to JavaScript, an unhandled exception in Python bubbles up the call stack until it encounters a boundary or crashes the interpreter process.

## Code Comparison

**JavaScript (Node.js)**
```javascript
function decodeConfig(jsonString) {
    if (typeof jsonString !== "string") {
        throw new TypeError("Config must be a string");
    }
    return JSON.parse(jsonString);
}


try {
    const config = decodeConfig("{ invalid JSON }");
    // Mixed logic pattern -- execution here implies the try succeeded
    console.log("Config loaded:", config);
} catch (error) {
    if (error instanceof TypeError) {
        console.error("Developer passed bad type:", error.message);
    } else if (error instanceof SyntaxError) {
        console.error("Payload was malformed:", error.message);
    } else {
        throw error; // Bubble unanticipated errors
    }
} finally {
    console.log("Cleanup executed");
}
```

**Python**
```python
import json

def decode_config(json_string):
    if not isinstance(json_string, str):
        # Triggers the exception instance
        raise TypeError("Config must be a string")
    return json.loads(json_string)


try:
    config = decode_config("{ invalid JSON }")
except TypeError as error:
    # Explicitly targeted type validation error
    print(f"Developer passed bad type: {error}")
except json.JSONDecodeError as error:
    # Explicitly targeted payload parsing error
    print(f"Payload was malformed: {error.msg}")
else:
    # Logic separation -- this ONLY runs if NO exceptions occurred.
    # Prevents accidental catching of errors raised within this success block.
    print(f"Config loaded: {config}")
finally:
    # Deterministic teardown, runs unconditionally
    print("Cleanup executed")
```

## Documentation
- [Python Tutorial: Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Python Built-in Exceptions Hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)
