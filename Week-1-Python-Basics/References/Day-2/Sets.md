# Sets

## Objective
Python's mutable, unordered collection of unique elements and its mathematical operations.

## JavaScript Equivalent
JavaScript `Set`. While JS Sets perform similar uniqueness constraints, Python Sets include mathematically robust builtin operators for intersection, union, and difference, moving them beyond mere de-duplication stores.

## Implementation Details

### Uniqueness and Setup
Sets automatically enforce uniqueness and disregard insertion order. They require hashable elements. Sets are defined with curly braces `{}` containing elements (as opposed to key-value pairs), but an empty set must be instantiated natively via `set()` as `{}` reserves dictionary instantiation.

```python
# Initializing
valid_ids = {101, 102, 102, 103} 
print(valid_ids) # {101, 102, 103}

empty_set = set() # Correct
empty_dic = {}    # Dict, not a Set
```

### Mathematical Operators
Python overrides binary operators to perform pure set theory math. These operators return a new Set with the evaluated results.

```python
admin_roles = {"read", "write", "delete"}
guest_roles = {"read"}

# Union (|) - Combine distinct elements
print(admin_roles | guest_roles) # {'read', 'write', 'delete'}

# Intersection (&) - Common elements
print(admin_roles & guest_roles) # {'read'}

# Difference (-) - Elements in set 1, not in set 2
print(admin_roles - guest_roles) # {'write', 'delete'}

# Symmetric Difference (^) - Elements in either set, but not both
print(admin_roles ^ guest_roles) # {'write', 'delete'}
```

### O(1) Membership Testing
Like JS, the explicit focus of a set is checking membership operations. The Python `in` operator evaluates in `O(1)` time utilizing the hash.

```python
user_id = 100
banned_ids = {100, 200, 300}

# Lightning fast check compared to Lists
if user_id in banned_ids:
    print("Denied")
```

## Code Comparison

**JavaScript (Node.js)**
```javascript
const nodeIds = new Set([1, 2, 3]);
nodeIds.add(4);

// Checking existence
if (nodeIds.has(2)) {
    console.log("Exists");
}

// Intersections require iteration manually
const setA = new Set([1, 2]);
const setB = new Set([2, 3]);
const intersection = new Set([...setA].filter(x => setB.has(x)));
```

**Python**
```python
node_ids = {1, 2, 3}
node_ids.add(4)

# Checking existence
if 2 in node_ids:
    print("Exists")

# Intersections are built into operators
set_a = {1, 2}
set_b = {2, 3}
intersection = set_a & set_b
```

## Documentation
- [Python Built-in Types: Set Types — set, frozenset](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
