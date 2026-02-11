# Nepalify

[![PyPI](https://img.shields.io/pypi/v/nepalify?color=orange&label=PyPI)](https://pypi.org/project/nepalify/) ![License](https://img.shields.io/badge/License-MIT-yellow) ![Python](https://img.shields.io/badge/python-3.8+-blue)

A comprehensive Python library for:
- **High Performance:** Ultra-fast O(1) date conversions (sub-microsecond)
- **Date Conversion:** Bidirectional AD ↔ BS (Bikram Sambat) conversion
- **DateTime Support:** Full datetime with time components, timezone, and timestamp support
- **Nepal Timezone:** UTC+05:45 timezone support
- **Advanced Formatting:** Full `strftime`/`strptime` support with Nepali codes
- **BS Calendar:** Monthly and yearly calendar display
- **Number Formatting:** Devanagari digits and Indian/Nepali 3-2-2 grouping
- **Text Localization:** Nepali month/day names and text conversion

## Installation

```bash
pip install nepalify
```

## Quick Start

```python
from nepalify import BSDate, BSDateTime, NepaliTimeZone, format_number, to_devanagari

# Current BS date and time
today = BSDate.today()
print(today.strftime("%K-%n-%D"))   # २०८२-१०-२४

# BS DateTime with timezone
now = BSDateTime.now(NepaliTimeZone())
print(now.strftime("%K-%n-%D %h:%i:%s"))  # २०८२-१०-२४ ११:२५:३०

# Display calendar
print(today.calendar())

# Number formatting
print(format_number(1234567))       # 12,34,567
print(to_devanagari("2024"))        # २०२४
```

## Features



### Date Conversion

```python
from nepalify import BSDate, ad_to_bs, bs_to_ad

# Create BS date
bs_date = BSDate(2080, 10, 24)

# Convert AD to BS
bs_tuple = ad_to_bs(2024, 2, 6)     # (2080, 10, 24)

# Convert BS to AD
ad_tuple = bs_to_ad(2080, 10, 24)   # (2024, 2, 6)

# BSDate API (datetime-like)
today = BSDate.today()
print(today.year, today.month, today.day)
print(today.weekday())              # 0=Sunday, 6=Saturday

# Date arithmetic
tomorrow = today + 1
next_week = today + 7
```

### BSDateTime (with Time Support)

```python
from nepalify import BSDateTime, NepaliTimeZone
from datetime import timedelta

# Create BS datetime
dt = BSDateTime(2080, 10, 24, 14, 30, 0)
print(dt)  # 2080-10-24 14:30:00

# Current BS datetime
now = BSDateTime.now()
now_npt = BSDateTime.now(NepaliTimeZone())
print(now_npt)  # 2082-10-24 11:25:30+05:45

# Convert from AD datetime
from datetime import datetime
ad_dt = datetime(2024, 2, 6, 14, 30)
bs_dt = BSDateTime.from_ad(ad_dt)

# Convert to AD datetime
back_to_ad = bs_dt.to_ad()

# Datetime arithmetic
new_dt = dt + timedelta(hours=5, minutes=30)
diff = dt - BSDateTime(2080, 10, 20, 10, 0)  # Returns timedelta

# Format with time codes
dt.strftime("%Y-%m-%d %H:%M:%S")        # 2080-10-24 14:30:00
dt.strftime("%I:%M %p")                  # 02:30 PM
dt.strftime("%h:%i %P")                  # ०२:३० दिउँसो
```

### Nepal Timezone (UTC+05:45)

```python
from nepalify import NepaliTimeZone, NPT, nepali_now, to_nepali_timezone
import datetime

# Get current Nepal time
npt_now = nepali_now()
print(npt_now)  # 2026-02-07 11:25:30+05:45

# Create timezone-aware datetime
dt = datetime.datetime(2024, 2, 7, 11, 0, tzinfo=NepaliTimeZone())

# Convert from UTC to NPT
utc_dt = datetime.datetime(2024, 2, 7, 5, 15, tzinfo=datetime.timezone.utc)
npt_dt = to_nepali_timezone(utc_dt)
print(npt_dt)  # 2024-02-07 11:00:00+05:45

# Use NPT singleton
from nepalify import NPT
dt = datetime.datetime.now(NPT)
```

### Date Formatting

```python
from nepalify import BSDate, BSDateTime

date = BSDate(2080, 10, 24)
dt = BSDateTime(2080, 10, 24, 14, 30, 0)

# Format with various codes
date.strftime("%Y-%m-%d")           # 2080-10-24
date.strftime("%B %d, %Y")          # Magh 24, 2080
date.strftime("%A, %B %d")          # Wednesday, Magh 24

# Nepali locale (New Format Codes)
date.strftime("%K-%n-%D")           # २०८०-१०-२४
date.strftime("%N %D, %K")          # माघ २४, २०८०
date.strftime("%N %D, %K", style='sanskrit') # माघ २४, २०८० (Sanskrit month names)
dt.strftime("%h:%i %P")             # ०२:३० दिउँसो

# Nepali time periods (%P)
# बिहान (morning), दिउँसो (afternoon), बेलुका (evening), राति (night)
```

### Monthly Calendar

```python
from nepalify import BSDate, month_calendar, year_calendar

# Get calendar for a month
print(month_calendar(2082, 10))
# Output:
#          Magh 2082
# Sun Mon Tue Wed Thu Fri Sat
#               1   2   3
#   4   5   6   7   8   9  10
#  11  12  13  14  15  16  17
#  18  19  20  21  22  23  24
#  25  26  27  28  29

# Calendar from BSDate (highlights today)
today = BSDate.today()
print(today.calendar())

# Nepali calendar
print(month_calendar(2082, 10, nepali=True))
# Output:
#          माघ २०८२
# आइत सोम मंगल बुध बिही शुक्र शनि
#               १   २   ३
#   ४   ५   ६   ७   ८   ९  १०
# ...

# Full year calendar
print(year_calendar(2082))
```

### Date Parsing

```python
from nepalify import parse, parse_date, parse_datetime

# Auto-detect format
parse("2079-02-15")                 # BSDate(2079, 2, 15)
parse("२०७८-०१-१८")                # BSDate(2078, 1, 18)

# Parse using format codes (New in v2.0)
BSDateTime.strptime("2080-10-24", "%Y-%m-%d")
BSDateTime.strptime("२०८०-१०-२४", "%K-%n-%D")
BSDateTime.strptime("Magh 24, 2080", "%B %d, %Y")
```

### Number Formatting

```python
from nepalify import to_devanagari, from_devanagari, format_number

# Devanagari conversion
to_devanagari("12345")              # १२३४५
from_devanagari("१२३४५")            # 12345

# Indian/Nepali numbering (3-2-2 grouping)
format_number(1234567890)           # 1,23,45,67,890
format_number(1234567, use_devanagari=True)  # १२,३४,५६७
```

### Text Localization

```python
from nepalify import convert_to_nepali, get_month_name, get_day_name

# Convert mixed text
convert_to_nepali("15 Magh 2080")   # १५ माघ २०८०
convert_to_nepali("Sunday")         # आइतबार

# Get month/day names
get_month_name(10)                  # माघ
get_month_name(10, nepali=False)    # Magh
get_day_name(0)                     # आइतबार
get_day_name(0, nepali=False)       # Sunday
```

## Supported BS Date Range

- **Minimum:** 1901-01-01 BS (1844-04-13 AD)
- **Maximum:** 2199-12-30 BS (2143-04-14 AD)

## Performance

`nepalify` is optimized for high-throughput applications, featuring:
- **O(1) Conversions:** Ordinal-based arithmetic avoids costly iteration.
- **Caching:** Frequently used conversions and regex patterns are cached.
- **Lazy Evaluation:** Format codes are processed only when needed.

| Operation | Time per Op |
|-----------|-------------|
| BS to AD | ~0.11 µs |
| AD to BS | ~0.06 µs |
| Date Add | ~1.01 µs |



## Format Codes Reference

### Date Codes
| Code | Description | Example |
|------|-------------|---------|
| `%Y` | Year (English) | 2080 |
| `%y` | Year short (English) | 80 |
| `%K` | Year (Nepali) | २०८० |
| `%k` | Year short (Nepali) | ८० |
| `%m` | Month (English) | 10 |
| `%n` | Month (Nepali) | १० |
| `%B` | Month Name (English) | Magh |
| `%b` | Month Name Short | Mag |
| `%N` | Month Name (Nepali) | माघ |
| `%d` | Day (English) | 24 |
| `%D` | Day (Nepali) | २४ |
| `%A` | Weekday (English) | Tuesday |
| `%a` | Weekday Short | Tue |
| `%G` | Weekday (Nepali) | मंगलबार |
| `%g` | Weekday Short (Nep) | मंगल |

### Time Codes
| Code | Description | Example |
|------|-------------|---------|
| `%H` | Hour (24-hour) | 14 |
| `%I` | Hour (12-hour) | 02 |
| `%h` | Hour (Nepali) | १४ |
| `%M` | Minute | 30 |
| `%i` | Minute (Nepali) | ३० |
| `%S` | Second | 00 |
| `%s` | Second (Nepali) | ०० |
| `%f` | Microsecond | 000000 |
| `%p` | AM/PM | PM |
| `%P` | Nepali Period | दिउँसो |
| `%z` | UTC offset | +0545 |
| `%Z` | Timezone name | NPT |

## License

MIT License

Copyright (c) 2024 Rabin Katel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

