"""
Devanagari digit conversion utilities.

Unicode mappings:
- 0 → ० (U+0966)
- 1 → १ (U+0967)
- ...
- 9 → ९ (U+096F)
"""

from typing import Union

# Translation tables for efficient conversion
_EN_TO_NP = str.maketrans('0123456789', '०१२३४५६७८९')
_NP_TO_EN = str.maketrans('०१२३४५६७८९', '0123456789')


def to_devanagari(value: Union[str, int, float]) -> str:
    """
    Convert Arabic numerals to Devanagari numerals.
    
    Args:
        value: String, integer, or float containing digits to convert.
               Non-digit characters are preserved.
    
    Returns:
        String with Arabic digits (0-9) replaced by Devanagari (०-९).
    
    Examples:
        >>> to_devanagari("2024") → '२०२४'\n
        >>> to_devanagari(12345) → '१२३४५'\n
        >>> to_devanagari(3.14) → '३.१४'\n
        >>> to_devanagari("Price: Rs. 1,500") → 'Price: Rs. १,५००'
    """
    return str(value).translate(_EN_TO_NP)


def from_devanagari(value: str) -> str:
    """
    Convert Devanagari numerals to Arabic numerals.
    
    Args:
        value: String containing Devanagari digits to convert.
               Non-digit characters are preserved.
    
    Returns:
        String with Devanagari digits (०-९) replaced by Arabic (0-9).
    
    Examples:
        >>> from_devanagari("२०२४") → '2024'\n
        >>> from_devanagari("१२,३४५.६७") → '12,345.67'\n
        >>> from_devanagari("मूल्य: रु. १,५००") → 'मूल्य: रु. 1,500'
    """
    return str(value).translate(_NP_TO_EN)


def is_devanagari_digit(char: str) -> bool:
    """
    Check if a character is a Devanagari digit.
    
    Args:
        char: Single character to check.
    
    Returns:
        True if the character is a Devanagari digit (०-९).
    
    Examples:
        >>> is_devanagari_digit('५') → True\n
        >>> is_devanagari_digit('5') → False
    """
    return len(char) == 1 and '०' <= char <= '९'


def is_arabic_digit(char: str) -> bool:
    """
    Check if a character is an Arabic digit.
    
    Args:
        char: Single character to check.
    
    Returns:
        True if the character is an Arabic digit (0-9).
    
    Examples:
        >>> is_arabic_digit('5') → True\n
        >>> is_arabic_digit('५') → False
    """
    return len(char) == 1 and '0' <= char <= '9'
