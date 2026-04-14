# Binary Type

## Objective
Python's binary types (`bytes`, `bytearray`, `memoryview`), their role in I/O and network operations, and their relationship to the `str` type.

## JavaScript Equivalent
JavaScript uses `Buffer` (Node.js) and `ArrayBuffer`/`TypedArray` (browser and Node.js) for raw binary data. Python provides `bytes` (immutable), `bytearray` (mutable), and `memoryview` (zero-copy view). The separation between text (`str`) and binary (`bytes`) in Python is strict and explicit -- there is no implicit coercion between the two.

## Implementation Details

### `bytes` -- Immutable Binary Sequence
A `bytes` object is an immutable sequence of integers in the range 0-255. It is the Python analog of Node.js `Buffer` for read-only binary data.

```python
# Literal syntax: b prefix
b1 = b"hello"
b2 = b'\x48\x65\x6c\x6c\x6f'  # same as b"Hello" in hex escapes
b3 = bytes(5)                   # b'\x00\x00\x00\x00\x00' -- 5 zero bytes
b4 = bytes([72, 101, 108, 108, 111])  # from integer sequence

type(b1)   # <class 'bytes'>
len(b1)    # 5

b1[0]      # 72  -- indexing returns an int (not a bytes of length 1)
b1[1:3]    # b'el' -- slicing returns bytes
```

Unlike `str`, indexing a `bytes` object returns an integer, not a single-byte sequence.

### Encoding and Decoding -- `str` <--> `bytes`
The bridge between `str` and `bytes` is explicit encoding. Python 3 enforces this; there is no implicit conversion.

```python
# str -> bytes
encoded = "hello".encode("utf-8")        # b'hello'
encoded_latin = "cafe\u0301".encode("utf-8")  # multi-byte UTF-8

# bytes -> str
decoded = b"hello".decode("utf-8")       # "hello"
decoded_err = b'\xff\xfe'.decode("utf-16")

# Specifying error handling
b'\x80abc'.decode("utf-8", errors="replace")   # '\ufffdabc'
b'\x80abc'.decode("utf-8", errors="ignore")    # 'abc'
```

Forgetting to encode/decode is the most common source of `TypeError` when working with files, sockets, or HTTP requests: `TypeError: a bytes-like object is required, not 'str'`.

### `bytearray` -- Mutable Binary Sequence
`bytearray` is the mutable counterpart to `bytes`. It supports in-place modification.

```python
ba = bytearray(b"hello")
ba[0] = 72           # modify in-place (H = 72)
ba.append(33)        # append byte value 33 ('!')
ba.extend(b" world") # extend with another bytes-like object

bytes(ba)            # b'Hello! world' -- convert back to immutable bytes
```

Use `bytearray` when building binary payloads incrementally (e.g., constructing protocol frames, reading from a socket into a growing buffer).

### `memoryview` -- Zero-Copy View
`memoryview` exposes the internal memory buffer of a `bytes` or `bytearray` object without copying it. Used for performance in I/O-heavy operations.

```python
data = bytearray(b"hello world")
mv = memoryview(data)

mv[0:5]               # <memory at 0x...>
bytes(mv[0:5])        # b"hello" -- no copy of the underlying data until cast
mv[0:5].tobytes()     # b"hello"
```

Pass a `memoryview` slice to socket `send()` or file `write()` to avoid intermediate copies when handling large binary buffers.

### File I/O in Binary Mode
Files opened in binary mode (`"rb"`, `"wb"`) return and accept `bytes` objects, not strings. Text mode (`"r"`, `"w"`) handles encoding transparently.

```python
# Binary read
with open("image.png", "rb") as f:
    data = f.read()   # data is bytes

# Binary write
with open("output.bin", "wb") as f:
    f.write(b'\x89PNG\r\n\x1a\n')
```

File I/O in text mode and binary mode is covered in depth in Day 4 (File Handling).

### Bytes Literals
| Literal Form | Description |
|---|---|
| `b"text"` | ASCII characters, max value 127 |
| `b'\x41'` | Hex escape -- single byte |
| `b'\n'` | Standard escape sequences |
| `b'\101'` | Octal escape |

Only ASCII characters are allowed in `bytes` literals. Non-ASCII values must use escape sequences.

## Code Comparison

**JavaScript (Node.js)**
```javascript
// Create a Buffer
const buf1 = Buffer.from("hello", "utf-8");    // from string
const buf2 = Buffer.alloc(5);                  // 5 zero bytes
const buf3 = Buffer.from([72, 101, 108, 108, 111]); // from integers

buf1[0];         // 72 (integer)
buf1.length;     // 5
buf1.toString("utf-8");  // "hello"

// Slicing (returns a view, not a copy)
buf1.slice(0, 3);   // <Buffer 68 65 6c>

// Mutable in-place
buf2[0] = 65;    // modify byte
```

**Python**
```python
# bytes -- immutable
b1 = "hello".encode("utf-8")   # b'hello'
b2 = bytes(5)                   # b'\x00\x00\x00\x00\x00'
b3 = bytes([72, 101, 108, 108, 111])  # b'Hello'

b1[0]           # 72 (integer)
len(b1)         # 5
b1.decode("utf-8")  # "hello"

b1[0:3]         # b'hel' -- new bytes object (copy)

# bytearray -- mutable
ba = bytearray(b2)
ba[0] = 65      # modify in-place

# memoryview -- zero-copy view
mv = memoryview(b1)
mv[0:3].tobytes()  # b'hel' -- no intermediate copy
```

Key differences:
- Python's `bytes` is immutable; `Buffer` in Node.js is mutable
- Python has a distinct mutable type (`bytearray`) for in-place modification
- The `str` / `bytes` boundary in Python 3 is strict; Node.js `Buffer` interoperates more loosely with strings

## Documentation
- [Python Built-in Types: Binary Sequence Types](https://docs.python.org/3/library/stdtypes.html#binary-sequence-types-bytes-bytearray-memoryview)
- [Python `codecs` -- Codec Registry and Base Classes](https://docs.python.org/3/library/codecs.html)
