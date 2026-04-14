# Feature Request: State Persistence, Diagnostics, and Validation

## Context
Our application resets its state upon termination. Today, we must implement file-based persistence using the standard library. Additionally, we will replace naive prints with formalized logging and introduce automated testing to guarantee the integrity of our `DataStore` abstraction. This mimics a transition from standard `fs` writing and `console.log` in Node to a robust production-style layout.

## Technical Requirements
1. **JSON Serialization:**
   - Import Python's built-in `json` module.
   - Refactor `DataStore` to save its state to a local `data.json` file whenever a state-altering command (Create, Update, Delete) is executed.
   - Refactor `DataStore.__init__()` to load data from `data.json` if it exists, or dynamically create an empty data structure within the file if it does not.

2. **Diagnostic Logging:**
   - Import the standard library `logging` module.
   - Replace internal debug-level `print()` statements within `DataStore` with appropriate log levels (e.g., `logging.info("Item created")`, `logging.error("File not found")`). Note that input and output prompts within `AppController` should still use `print()` and `input()`.

3. **Unit Validation with Pytest:**
   - Install `pytest` via `pip` and update your `requirements.txt`.
   - Create a test file (e.g., `test_datastore.py`).
   - Write unit tests that directly instantiate `DataStore` and validate the logic of its CRUD instance methods. Bypass the `AppController` UI layer entirely.
   - Include test cases for expected operation logic.

## Definition of Done
- State persists across separate executions of `app.py` via `data.json`.
- The application initializes smoothly even if `data.json` has not yet been generated.
- Standard library `logging` traces CRUD operations.
- `pytest` executes successfully against the `DataStore` methods.
- Code changes are pushed to the target repository.
