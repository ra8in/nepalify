"""
Nepalify Numbers Module

Functions for:
- Devanagari digit conversion
- Indian/Nepali number formatting (3-2-2 grouping)
- Number to Nepali words conversion
"""

from nepalify.numbers.devanagari import to_devanagari, from_devanagari
from nepalify.numbers.formatting import format_number, to_words_nepali

__all__ = [
    "to_devanagari",
    "from_devanagari",
    "format_number",
    "to_words_nepali",
]
