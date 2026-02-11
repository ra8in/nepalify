"""
Nepalify Text Module

Functions for:
- Text localization (Nepali month/day names)
- Convert English text elements to Nepali
"""

from nepalify.text.constants import (
    MONTHS_NEPALI,
    MONTHS_NEPALI_SANSKRIT,
    MONTHS_ENGLISH,
    MONTHS_ENGLISH_SHORT,
    DAYS_NEPALI,
    DAYS_NEPALI_SHORT,
    DAYS_ENGLISH,
    DAYS_ENGLISH_SHORT,
    GREGORIAN_MONTHS_NEPALI,
)
from nepalify.text.localization import (
    convert_to_nepali,
    get_month_name,
    get_day_name,
)

__all__ = [
    # Constants
    "MONTHS_NEPALI",
    "MONTHS_NEPALI_SANSKRIT",
    "MONTHS_ENGLISH",
    "MONTHS_ENGLISH_SHORT",
    "DAYS_NEPALI",
    "DAYS_NEPALI_SHORT",
    "DAYS_ENGLISH",
    "DAYS_ENGLISH_SHORT",
    "GREGORIAN_MONTHS_NEPALI",
    # Functions
    "convert_to_nepali",
    "get_month_name",
    "get_day_name",
]
