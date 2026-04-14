# Python Modules -- Regex

## Objective
Advanced pattern matching, text substitution, and extraction utilizing the `re` module.

## JavaScript Equivalent
JavaScript engineers typically use literal regex syntax (e.g., `/pattern/gi`) coupled with `String.prototype` methods (`match()`, `replace()`, `search()`) or the `RegExp` object. Python lacks literal regex syntax and integrates all regex operations through the `re` module.

## Implementation Details

### Raw Strings vs String Literals
Because Python has no native regex literal, patterns must be supplied as standard strings. However, standard strings evaluate escape characters (like `\n` or `\b`). A regex engine also relies heavily on identical escape characters.

To prevent Python from evaluating the escape characters before the regex engine receives the string, developers must use **raw strings**, prefixed with `r` (e.g., `r"\bword\b"`). Without the `r` prefix, an engineer would have to double-escape characters (e.g., `"\\bword\\b"`).

### Core Regex Functions
Python's `re` module separates operations into distinct functions rather than prototype methods:
- `re.search(pattern, string)`: Scans through the string looking for the first location where the pattern produces a match. Returns a single Match object or `None`.
- `re.match(pattern, string)`: Strictly matches only at the *beginning* of the string. Returns a Match object or `None`.
- `re.findall(pattern, string)`: Returns all non-overlapping matches of pattern in string as a list of strings.
- `re.finditer(pattern, string)`: Returns an iterator yielding Match objects over all non-overlapping matches. Efficient for large datasets.
- `re.sub(pattern, replacement, string)`: Replaces occurrences of the pattern. Analogous to `String.replace()`.

### Match Objects and the `group` Method
When `search` or `match` succeeds, they return a Match object. To extract the actual matched string, developers call the `.group()` method on the object. Passing integer arguments (e.g., `.group(1)`) extracts specific regex capture groups.

### Compilation
JavaScript compiles regex literals on script load. In Python, calling `re.match()` repeatedly on the same string implicitly compiles and caches the pattern. However, for critical loops, it is vastly more performant to pre-compile the regex into a pattern object using `re.compile()`.

## Code Comparison

**JavaScript (Node.js)**
```javascript
const text = "Error 404: resource id 8990 not found.";
const numRegex = /\d+/g; // global flag

// Find all matches
const allMatches = text.match(numRegex); // ['404', '8990']

// Test if pattern exists
const hasNumber = numRegex.test(text); // true

// Replace with a function
const redacted = text.replace(numRegex, (match) => {
    return "[redacted]";
});
```

**Python**
```python
import re

text = "Error 404: resource id 8990 not found."
# Raw string enforced for regex
num_pattern = r"\d+"

# Find all matches
all_matches = re.findall(num_pattern, text) # ['404', '8990']

# Test if pattern exists (search returns None if no match)
has_number = re.search(num_pattern, text) is not None

# Compiling for performance in loops
compiled_pattern = re.compile(num_pattern)
loop_matches = compiled_pattern.findall(text)

# Replace with a function
def censor(match_obj):
    return "[redacted]"

redacted = re.sub(num_pattern, censor, text)

# Extracting groups
parsed = re.search(r"Error (\d+): (.+)", text)
error_code = parsed.group(1) # '404'
error_msg = parsed.group(2)  # 'resource id 8990 not found.'
```

## Documentation
- [Python Standard Library: re](https://docs.python.org/3/library/re.html)
- [Python Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html)
