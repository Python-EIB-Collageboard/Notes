# Classes

## Objective
Defining class blueprints, managing state initialization, distinguishing between class and instance scope, and utilizing inheritance.

## JavaScript Equivalent
JavaScript ES6 `class` syntax, which is syntactic sugar over prototypal inheritance. Python's class model is native and strictly object-oriented, determining method resolution intrinsically.

## Implementation Details

### Syntactic Structure and Initialization
Python uses the `class` keyword. The equivalent to JavaScript's `constructor()` is the `__init__()` dunder (double underscore) method. 

Crucially, Python requires an explicit reference to the instance object in all method signatures. By ironclad convention, this parameter is named `self`. While JavaScript implicitly injects `this` into method contexts, Python developers must manually declare `self` as the first parameter of any instance method, including `__init__`. When the method is invoked, Python automatically passes the instance reference.

### Instance vs. Class Attributes
A major point of divergence from JavaScript is the allocation of properties. 
- **Instance Attributes:** Declared inside `__init__` and bound to `self` (e.g., `self.name = name`). These are unique to the instantiated object.
- **Class Attributes:** Declared directly under the class block, outside any method. These are shared across all instances of the class. Mutating a class attribute alters the state for all instances simultaneously.

### Encapsulation and Access Modifiers
JavaScript implements true memory-level private fields using the `#` prefix. Python does not enforce strict access control. Instead, Python relies entirely on naming conventions:
- **Protected:** A single leading underscore (`_variable`) signals to other developers that the attribute is internal and should not wait be accessed directly.
- **Private (Name Mangling):** A double leading underscore (`__variable`) invokes the interpreter's name mangling algorithm, rewriting the attribute name internally to prevent accidental overriding in subclasses. It is not a true security barrier.

### Inheritance
Inheritance is implemented by passing the parent class as an argument to the child class definition: `class Child(Parent):`. To access parent methods from the child, Python uses the `super()` function, identical in purpose to JavaScript's `super`.

## Code Comparison

**JavaScript (Node.js)**
```javascript
class User {
    static count = 0; // Class variable

    constructor(username) {
        this.username = username; // Instance variable
        this._authenticated = false; // Protected convention
        this.#secret = "token"; // True private field
        User.count++;
    }

    login() {
        this._authenticated = true;
        console.log(`${this.username} logged in`);
    }
}

class Admin extends User {
    constructor(username, level) {
        super(username); // Call parent constructor
        this.level = level;
    }
}
```

**Python**
```python
class User:
    # Class Attribute (Shared among all instances)
    count = 0 

    def __init__(self, username):
        # Instance Attributes
        self.username = username 
        self._authenticated = False      # Protected by convention
        self.__secret = "token"          # Name-mangled (pseudo-private)
        
        # Accessing class attributes requires the class name
        User.count += 1

    # Instance method explicitly accepts 'self'
    def login(self):
        self._authenticated = True
        print(f"{self.username} logged in")

# Inheritance
class Admin(User):
    def __init__(self, username, level):
        # super() automatically resolves the parent class proxy
        super().__init__(username)
        self.level = level

# Instantiation (No 'new' keyword)
admin_user = Admin("root", "sysadmin")
admin_user.login()
```

## Documentation
- [Python Tutorial: Classes](https://docs.python.org/3/tutorial/classes.html)
- [Python Reference: Class definitions](https://docs.python.org/3/reference/compound_stmts.html#class-definitions)
