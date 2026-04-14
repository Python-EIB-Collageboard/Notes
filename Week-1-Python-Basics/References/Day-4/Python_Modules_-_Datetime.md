# Python Modules -- Datetime

## Objective
Precise manipulation, arithmetic, and formatting of chronological data using the `datetime` module.

## JavaScript Equivalent
JavaScript relies on the singular `Date` object, representing milliseconds since the Unix epoch, notoriously burdened by legacy behaviors. Because of its limitations, JavaScript environments often depend on heavy external libraries like Moment.js or date-fns. Python separates temporal logic natively.

## Implementation Details

### The Four Primary Classes
Python's approach is structurally explicit. Rather than overloading a single class, the `datetime` module exports distinct classes tailored to specific temporal use cases:
- `date`: Represents an idealized calendar date (Year, Month, Day) assuming the Gregorian calendar.
- `time`: Represents purely idealized time (Hour, Minute, Second, Microsecond), decoupled from any specific calendar day.
- `datetime`: A combination of a date and time.
- `timedelta`: Represents a duration or difference between two `date`, `time`, or `datetime` instances.

### Strings to Dates and Dates to Strings
JavaScript standardizes on standard ISO string formatting via `Date.parse()` and `.toISOString()`. Python provides robust string conversion functions:
- `strftime` (Format Time): Converts a `datetime` object into a custom-formatted string using format codes.
- `strptime` (Parse Time): Converts a custom-formatted string into a `datetime` object.

A `datetime` object can also natively be converted to an ISO standard using `.isoformat()`.

### Timezone Naive vs Timezone Aware
A crucial Python concept is whether a `datetime` object is "Naive" or "Aware." 
- **Naive:** Does not contain timezone information. Operations assume they refer to the same timezone. `datetime.now()` returns a naive datetime.
- **Aware:** Contains explicit `tzinfo` indicating its timezone. Crucial for comparing timestamps from different locales.

To create aware datetimes natively, developers use the `timezone` class from the `datetime` module (e.g., `timezone.utc`).

## Code Comparison

**JavaScript (Node.js)**
```javascript
// Current timestamp
const now = new Date();

// Duration arithmetic (manual ms calculation)
const tomorrow = new Date(now.getTime() + (24 * 60 * 60 * 1000));

// Explicit Date initialization
const specificDate = new Date(2023, 11, 25, 12, 0, 0); // Note: Month is 0-indexed in JS

// Formatting (Often requires Intl.DateTimeFormat or a library)
const isoString = now.toISOString();
```

**Python**
```python
from datetime import datetime, date, time, timedelta, timezone

# Distinct object types
current_date = date.today()
current_time = datetime.now().time()
now = datetime.now() # Naive current datetime

# Duration arithmetic using timedelta
tomorrow = now + timedelta(days=1, hours=2)
time_difference = tomorrow - now # Resolves to a timedelta object
print(time_difference.days) # 1

# Explicit initialization (Months are 1-indexed, mathematically logical)
specific = datetime(year=2023, month=12, day=25, hour=12)

# Timezone aware datetime
utc_now = datetime.now(tz=timezone.utc)

# String Parsing (strptime) and Formatting (strftime)
# %Y = 4-digit year, %m = 2-digit month, %d = 2-digit day
date_str = "2023-12-01 15:30"
parsed_dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")

formatted_str = parsed_dt.strftime("%B %d, %Y") # "December 01, 2023"
iso_str = parsed_dt.isoformat()
```

## Documentation
- [Python Standard Library: datetime](https://docs.python.org/3/library/datetime.html)
- [strftime() and strptime() Format Codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)
