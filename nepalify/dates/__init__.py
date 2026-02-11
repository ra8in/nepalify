"""
Nepalify Dates Module

Classes and functions for:
- AD ↔ BS (Bikram Sambat) date conversion
- BSDate class with datetime-like API
- BSDateTime class with time and timezone support
- Nepal timezone (UTC+05:45)
- Monthly and yearly calendar generation
- Date parsing with auto-format detection
"""

from nepalify.dates.bs_date import BSDate
from nepalify.dates.bs_datetime import BSDateTime
from nepalify.dates.converter import (
    ad_to_bs,
    bs_to_ad,
    get_days_in_month,
    get_days_in_year,
    is_valid_bs_date,
    BS_MIN_YEAR,
    BS_MAX_YEAR,
)
from nepalify.dates.timezone import (
    NepaliTimeZone,
    NPT,
    NEPAL_TIMEZONE,
    NPT_OFFSET,
    now,
    utc_now,
    nepali_now,
    to_nepali_timezone,
    to_utc_timezone,
    from_utc,
    get_local_timezone,
)
from nepalify.dates.calendar import (
    month_calendar,
    year_calendar,
)
from nepalify.dates.parser import (
    parse,
    parse_date,
    parse_datetime,
)

__all__ = [
    # Date classes
    "BSDate",
    "BSDateTime",
    # Conversion functions
    "ad_to_bs",
    "bs_to_ad",
    "get_days_in_month",
    "get_days_in_year",
    "is_valid_bs_date",
    # Constants
    "BS_MIN_YEAR",
    "BS_MAX_YEAR",
    # Timezone
    "NepaliTimeZone",
    "NPT",
    "NEPAL_TIMEZONE",
    "NPT_OFFSET",
    "now",
    "utc_now",
    "nepali_now",
    "to_nepali_timezone",
    "to_utc_timezone",
    "from_utc",
    "get_local_timezone",
    # Calendar
    "month_calendar",
    "year_calendar",
    # Parsing
    "parse",
    "parse_date",
    "parse_datetime",
]

