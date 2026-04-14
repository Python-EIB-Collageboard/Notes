# Objects

## Objective
Mechanics of instantiating classes, dynamically binding attributes, and understanding Python's underlying data model via dunder methods.

## JavaScript Equivalent
JavaScript objects (instantiated via the `new` keyword) and prototype chain mechanics.

## Implementation Details

### Instantiation
Unlike JavaScript, Python does not employ a `new` keyword to create an object from a class. The class boundary itself acts as a callable function. Passing arguments directly to the class name routes them to the object's `__init__` constructor.

### Memory and Dynamic Assignment
In both languages, objects act essentially as dynamically resizable hash maps in memory. Python objects maintain an internal dictionary named `__dict__` that continuously tracks the instance's unique attributes. 

Because of this, Python developers can dynamically bind new attributes to an object arbitrary times at runtime, exactly as JavaScript engineers inject new properties onto an object. However, while functionally valid, aggressively mutating the shape of an object outside its constructor is considered a poor architectural pattern as it obscures the object's intended interface.

### The Data Model and Dunder Methods
Where JavaScript uses specific prototype methods (like `.toString()` or symbols like `[Symbol.toPrimitive]`) to hook into language operations, Python leverages a comprehensive internal protocol known as "dunder" (Double Under) or "magic" methods.

These methods override built-in operations. When a developer writes `print(obj)`, Python does not arbitrarily stringify the properties. It implicitly searches for and executes the object's `__str__()` method. When an engineer writes `obj1 == obj2`, Python executes `obj1.__eq__(obj2)`. 

Mastering Python object behavior requires understanding this meta-protocol.

Common dunder methods:
- `__str__(self)`: Human-readable string representation (triggered by `str()` or `print()`).
- `__repr__(self)`: Unambiguous string representing the raw state, ideally executable (triggered by `repr()`).
- `__eq__(self, other)`: Overrides the `==` equality operator check.
- `__len__(self)`: Allows the use of `len(obj)`.

## Code Comparison

**JavaScript (Node.js)**
```javascript
class Vector {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    // Equivalent to __str__
    toString() {
        return `Vector(${this.x}, ${this.y})`;
    }
}

// Javascript requires 'new'
const v1 = new Vector(10, 20);

// Dynamic attribute assignment
v1.z = 30; 
```

**Python**
```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Dunder method overriding the string representation
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
        
    # Dunder method overriding the explicit equality check
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

# Instantiation does not use 'new'
v1 = Vector(10, 20)
v2 = Vector(10, 20)

# Triggers __str__
print(v1) # Vector(10, 20)

# Triggers __eq__
print(v1 == v2) # True. Without __eq__, this compares memory addresses and returns False.

# Dynamic assignment is possible but typically avoided
v1.z = 30
```

## Documentation
- [Python Reference: Data model](https://docs.python.org/3/reference/datamodel.html)
- [Python Tutorial: Classes](https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes)
