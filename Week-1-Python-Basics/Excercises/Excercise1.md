# Feature Request: Application Scaffolding and REPL Initialization

## Context
As we transition from Node.js to Python, our first goal is establishing the execution environment and a core event loop. In Node.js, we would use `npm init` and structural files like `package.json`. In Python, we rely on virtual environments and dependency requirement files. We need to scaffold a new console application (e.g., Task Tracker, Library System, or a domain of your choice) and build its primary event loop to accept continuous user input.

## Technical Requirements
1. **Repository Scaffolding:**
   - Initialize a local project structure.
   - Configure a standard `.gitignore` file for Python projects.
   - Establish a virtual environment (`venv`).
   - Create a `requirements.txt` file.

2. **Application Entry Point:**
   - Create the main execution script named `app.py`.
   - Implement a Continuous REPL (Read-Eval-Print Loop) using a `while True:` structure.
   - Use Python's built-in `input()` function to prompt the user for commands.

3. **Core Primitives & Conditionals:**
   - Prompt the user with a menu of standard CRUD operations (Create, Read, Update, Delete, Exit).
   - Use string evaluation and conditional statements (`if/elif/else`) to route the user's input.
   - For now, merely print a confirmation message (e.g., "You selected Create...") using primitive types. Do not implement state persistence yet.
   - Provide a mechanism to cleanly break the loop when the user inputs 'Exit'.

## Definition of Done
- A functional Python virtual environment is active.
- `app.py` runs successfully from the terminal.
- The REPL accepts input, properly routes commands using string comparisons, and handles termination cleanly.
- Code is pushed to the organizational GitHub repository.
