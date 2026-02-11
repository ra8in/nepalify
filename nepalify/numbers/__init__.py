"""
Nepalify Numbers Module

Functions for:
- Devanagari digit conversion
- Indian/Nepali number formatting (3-2-2 grouping)
- Number to Nepali words conversion
- Ordinal number conversion (1 → पहिलो, "first" → पहिलो)
"""

from nepalify.numbers.devanagari import to_devanagari, from_devanagari
from nepalify.numbers.formatting import format_number, to_words_nepali
from nepalify.numbers.ordinals import to_nepali_ordinal, from_nepali_ordinal

__all__ = [
    "to_devanagari",
    "from_devanagari",
    "format_number",
    "to_words_nepali",
    "to_nepali_ordinal",
    "from_nepali_ordinal",
]
