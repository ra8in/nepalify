"""
Text localization utilities.

Convert English text elements to Nepali Devanagari.
"""

import re
from typing import Union

from nepalify.numbers.devanagari import to_devanagari
from nepalify.text.constants import (
    MONTHS_NEPALI,
    MONTHS_ENGLISH,
    DAYS_NEPALI,
    DAYS_ENGLISH,
    GREGORIAN_MONTHS_NEPALI,
    GREGORIAN_MONTHS_ENGLISH,
)


def get_month_name(
    month: int,
    nepali: bool = True,
    abbreviated: bool = False,
    style: str = 'formal'
) -> str:
    """
    Get the BS month name.
    
    Args:
        month: Month number (1-12, where 1=Baisakh, 12=Chaitra).
        nepali: If True, return Nepali name; otherwise English.
        abbreviated: If True, return abbreviated form (English only).
        style: 'formal' for colloquial names (जेठ), 
               'sanskrit' for traditional names (ज्येष्ठ).
               Only applies when nepali=True.
    
    Returns:
        Month name string.
    
    Examples:
        >>> get_month_name(1)
        'बैशाख'
        >>> get_month_name(1, nepali=False)
        'Baisakh'
        >>> get_month_name(2)
        'जेठ'
        >>> get_month_name(2, style='sanskrit')
        'ज्येष्ठ'
        >>> get_month_name(10)
        'माघ'
    
    Raises:
        ValueError: If month is not in range 1-12.
    """
    if not 1 <= month <= 12:
        raise ValueError(f"Month must be 1-12, got {month}")
    
    if nepali:
        if style == 'sanskrit':
            from nepalify.text.constants import MONTHS_NEPALI_SANSKRIT
            return MONTHS_NEPALI_SANSKRIT[month - 1]
        else:  # 'formal' (default)
            return MONTHS_NEPALI[month - 1]
    elif abbreviated:
        from nepalify.text.constants import MONTHS_ENGLISH_SHORT
        return MONTHS_ENGLISH_SHORT[month - 1]
    else:
        return MONTHS_ENGLISH[month - 1]


def get_day_name(
    weekday: int,
    nepali: bool = True,
    abbreviated: bool = False
) -> str:
    """
    Get the day of week name.
    
    Args:
        weekday: Day of week (0-6, where 0=Sunday, 6=Saturday).
        nepali: If True, return Nepali name; otherwise English.
        abbreviated: If True, return abbreviated form.
    
    Returns:
        Day name string.
    
    Examples:
        >>> get_day_name(0)
        'आइतबार'
        >>> get_day_name(0, nepali=False)
        'Sunday'
        >>> get_day_name(5)
        'शुक्रबार'
    
    Raises:
        ValueError: If weekday is not in range 0-6.
    """
    if not 0 <= weekday <= 6:
        raise ValueError(f"Weekday must be 0-6, got {weekday}")
    
    if nepali:
        if abbreviated:
            from nepalify.text.constants import DAYS_NEPALI_SHORT
            return DAYS_NEPALI_SHORT[weekday]
        return DAYS_NEPALI[weekday]
    else:
        if abbreviated:
            from nepalify.text.constants import DAYS_ENGLISH_SHORT
            return DAYS_ENGLISH_SHORT[weekday]
        return DAYS_ENGLISH[weekday]


# Build lookup dictionaries for conversion
_DAY_MAP = {day.lower(): DAYS_NEPALI[i] for i, day in enumerate(DAYS_ENGLISH)}
_MONTH_MAP = {month.lower(): MONTHS_NEPALI[i] for i, month in enumerate(MONTHS_ENGLISH)}
_GREGORIAN_MONTH_MAP = {
    month.lower(): GREGORIAN_MONTHS_NEPALI[i] 
    for i, month in enumerate(GREGORIAN_MONTHS_ENGLISH)
}


def convert_to_nepali(
    text: Union[str, int, float],
    convert_digits: bool = True,
    convert_days: bool = True,
    convert_bs_months: bool = True,
    convert_gregorian_months: bool = True
) -> str:
    """
    Convert English text elements to Nepali Devanagari.
    
    Converts:
    - Digits (0-9) to Devanagari (०-९)
    - Day names (Sunday-Saturday) to Nepali
    - BS month names (Baisakh-Chaitra) to Nepali
    - Gregorian month names (January-December) to Nepali
    
    Args:
        text: Text to convert (string or number).
        convert_digits: Convert Arabic digits to Devanagari.
        convert_days: Convert English day names to Nepali.
        convert_bs_months: Convert BS month names to Nepali.
        convert_gregorian_months: Convert Gregorian month names to Nepali.
    
    Returns:
        Text with English elements converted to Nepali.
    
    Examples:
        >>> convert_to_nepali("15 Magh 2080")
        '१५ माघ २०८०'
        >>> convert_to_nepali("Sunday, January 15")
        'आइतबार, जनवरी १५'
        >>> convert_to_nepali(2024)
        '२०२४'
    """
    result = str(text)
    
    # Replace day names (case-insensitive, whole words only)
    if convert_days:
        for eng, nep in _DAY_MAP.items():
            result = re.sub(rf'\b{eng}\b', nep, result, flags=re.IGNORECASE)
    
    # Replace BS month names
    if convert_bs_months:
        for eng, nep in _MONTH_MAP.items():
            result = re.sub(rf'\b{eng}\b', nep, result, flags=re.IGNORECASE)
    
    # Replace Gregorian month names
    if convert_gregorian_months:
        for eng, nep in _GREGORIAN_MONTH_MAP.items():
            result = re.sub(rf'\b{eng}\b', nep, result, flags=re.IGNORECASE)
    
    # Replace digits last (to not interfere with word replacements)
    if convert_digits:
        result = to_devanagari(result)
    
    return result
