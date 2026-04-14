# Feature Request: OOP Refactoring and Architectural Expansion

## Context
Currently, our `app.py` manages both presentation (console input/output) and data operations procedurally. As we move towards more complex applications, we must segregate our concerns. In Node.js, we would abstract business logic using classes or prototype functions. Here, we will refactor our app into a class-based architecture. This specific separation (UI vs. Data Layer) paves the way for integrating a separate web server (Flask) and a separate persistent data store (DynamoDB) in upcoming weeks.

## Technical Requirements
1. **Data Store Abstraction:**
   - Create a `DataStore` class (e.g., in a separate module or directly in `app.py`).
   - Define an `__init__()` method that initializes the collection holding your records.
   - Move the CRUD logic (Create, Read, Update, Delete) out of the global scope and encapsulate them as instance methods on the `DataStore` class.

2. **Application Controller Abstraction:**
   - Create an `AppController` class.
   - Define an `__init__()` method that initializes standard configuration and instantiates the `DataStore` as an instance property (`self.db = DataStore()`).
   - Abstract the `while True:` loop and the input routing logic into an execution method on `AppController` (e.g., `run()`).

3. **Execution Context:**
   - Ensure the application properly routes commands from the `AppController` to the `DataStore` instance.
   - Use the `if __name__ == "__main__":` idiom to initialize and run the `AppController` if the file is executed directly.

## Definition of Done
- Procedural data dictionaries and standard functions are entirely refactored into the `DataStore` and `AppController` classes.
- Proper instance variables (`self`) and method definitions are utilized.
- Operations from the terminal function exactly as they did in Day 2, proving the refactor is functionally identical.
- Code changes are pushed to the target repository.
