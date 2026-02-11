"""
Nepalify - Python Library for Nepali Date, Number, and Text Formatting

A comprehensive library for:
- Devanagari digit conversion
- Indian/Nepali number formatting (3-2-2 grouping)
- AD ↔ BS (Bikram Sambat) date conversion
- Date/DateTime formatting with Nepali locale
- Nepal timezone (UTC+05:45) support
- Text localization (months, days, numbers)
"""

from .version import __version__

# Number formatting
from nepalify.numbers import (
    to_devanagari,
    from_devanagari,
    format_number,
    to_words_nepali,
)

# Date conversion, datetime, and timezone
from nepalify.dates import (
    # Date/DateTime classes
    BSDate,
    BSDateTime,
    # Conversion functions
    ad_to_bs,
    bs_to_ad,
    get_days_in_month,
    is_valid_bs_date,
    # Timezone
    NepaliTimeZone,
    NPT,
    now,
    utc_now,
    nepali_now,
    to_nepali_timezone,
    to_utc_timezone,
    # Calendar
    month_calendar,
    year_calendar,
    # Parsing
    parse,
    parse_date,
    parse_datetime,
)

# Text localization
from nepalify.text import (
    convert_to_nepali,
    get_month_name,
    get_day_name,
    MONTHS_NEPALI,
    MONTHS_ENGLISH,
    DAYS_NEPALI,
    DAYS_ENGLISH,
)

__all__ = [
    # Version
    "__version__",
    # Numbers
    "to_devanagari",
    "from_devanagari",
    "format_number",
    "to_words_nepali",
    # Date/DateTime Classes
    "BSDate",
    "BSDateTime",
    # Conversion
    "ad_to_bs",
    "bs_to_ad",
    "get_days_in_month",
    "is_valid_bs_date",
    # Timezone
    "NepaliTimeZone",
    "NPT",
    "now",
    "utc_now",
    "nepali_now",
    "to_nepali_timezone",
    "to_utc_timezone",
    # Calendar
    "month_calendar",
    "year_calendar",
    # Parsing
    "parse",
    "parse_date",
    "parse_datetime",
    # Text
    "convert_to_nepali",
    "get_month_name",
    "get_day_name",
    "MONTHS_NEPALI",
    "MONTHS_ENGLISH",
    "DAYS_NEPALI",
    "DAYS_ENGLISH",
]

