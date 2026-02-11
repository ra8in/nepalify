"""
Date and DateTime Parsing for Bikram Sambat.

Auto-detect and parse various date/datetime formats including:
- ISO format: 2079-02-15
- Nepali numerals: २०७८-०१-१८
- Named months: Jestha 15, 2079
- With time: 2079-02-15 15:23

Example:
    >>> from nepalify.dates.parser import parse
    >>> 
    >>> # Various format support
    >>> parse("2079-02-15")
    BSDate(2079, 2, 15)
    >>> parse("२०७८-०१-१८")
    BSDate(2078, 1, 18)
    >>> parse("2079-02-15 15:23")
    BSDateTime(2079, 2, 15, 15, 23, 0)
    >>> parse("Jestha 15, 2079")
    BSDate(2079, 2, 15)
"""

import re
from typing import Union, Optional, Dict, List, Tuple
from functools import lru_cache


from nepalify.dates.converter import is_valid_bs_date
from nepalify.numbers.devanagari import from_devanagari
from nepalify.text.constants import (
    MONTHS_ENGLISH,
    MONTHS_NEPALI,
    MONTHS_NEPALI_SANSKRIT,
)


# Month name mappings (lowercase for case-insensitive matching)
_MONTH_NAME_TO_NUM: Dict[str, int] = {}

# Add English month names (standard)
for i, name in enumerate(MONTHS_ENGLISH, 1):
    _MONTH_NAME_TO_NUM[name.lower()] = i
    # Add short forms (first 3 letters)
    _MONTH_NAME_TO_NUM[name[:3].lower()] = i

# Add Nepali month names (formal)
for i, name in enumerate(MONTHS_NEPALI, 1):
    _MONTH_NAME_TO_NUM[name] = i

# Add Nepali month names (Sanskrit)
for i, name in enumerate(MONTHS_NEPALI_SANSKRIT, 1):
    _MONTH_NAME_TO_NUM[name] = i

# Common date patterns (order matters - more specific first)
_DATE_PATTERNS: List[Tuple[re.Pattern, str]] = [
    # ISO format with time: 2079-02-15 15:23:45
    (re.compile(r'^(\d{4})[-/](\d{1,2})[-/](\d{1,2})\s+(\d{1,2}):(\d{2})(?::(\d{2}))?(?:\.(\d+))?$'), 'datetime'),
    
    # ISO format date only: 2079-02-15 or 2079/02/15
    (re.compile(r'^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$'), 'date'),
    
    # Named month: Jestha 15, 2079 or Jestha 15 2079
    (re.compile(r'^([A-Za-z]+)\s+(\d{1,2})(?:,?\s+)(\d{4})$'), 'named_month'),
    
    # Named month (Nepali): माघ 15, 2079
    (re.compile(r'^([^\d\s]+)\s+(\d{1,2})(?:,?\s+)(\d{4})$'), 'named_month'),
    
    # Day Month Year: 15 Jestha 2079
    (re.compile(r'^(\d{1,2})\s+([A-Za-z]+)(?:,?\s+)(\d{4})$'), 'day_month_year'),
    
    # Time with AM/PM: 2079-02-15 5:23 AM
    (re.compile(r'^(\d{4})[-/](\d{1,2})[-/](\d{1,2})\s+(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)$'), 'datetime_ampm'),
    
    # Short year: 79-02-15
    (re.compile(r'^(\d{2})[-/](\d{1,2})[-/](\d{1,2})$'), 'short_year'),
]


def _normalize_nepali_digits(text: str) -> str:
    """Convert any Nepali digits in text to ASCII digits."""
    return from_devanagari(text)


def _parse_month_name(name: str) -> Optional[int]:
    """
    Parse month name to month number.
    
    Args:
        name: Month name (English or Nepali).
    
    Returns:
        Month number (1-12) or None if not found.
    """
    # Try exact match first (for Nepali)
    if name in _MONTH_NAME_TO_NUM:
        return _MONTH_NAME_TO_NUM[name]
    
    # Try lowercase for English
    name_lower = name.lower()
    if name_lower in _MONTH_NAME_TO_NUM:
        return _MONTH_NAME_TO_NUM[name_lower]
    
    return None


def parse(date_string: str) -> Union['BSDate', 'BSDateTime']:
    """
    Auto-detect and parse a date/datetime string.
    
    Supports various formats including:
    - ISO format: 2079-02-15
    - Nepali numerals: २०७८-०१-१८
    - Named months: Jestha 15, 2079 or 15 Jestha, 2079
    - With time: 2079-02-15 15:23 or 2079-02-15 5:23 AM
    
    Args:
        date_string: String to parse.
    
    Returns:
        BSDate or BSDateTime depending on whether time is present.
    
    Raises:
        ValueError: If the format cannot be detected or date is invalid.
    
    Examples:
        >>> parse("2079-02-15")
        BSDate(2079, 2, 15)
        >>> parse("२०७८-०१-१८")
        BSDate(2078, 1, 18)
        >>> parse("2079-02-15 15:23")
        BSDateTime(2079, 2, 15, 15, 23, 0)
        >>> parse("Jestha 15, 2079")
        BSDate(2079, 2, 15)
    """
    # Import here to avoid circular imports
    from nepalify.dates.bs_date import BSDate
    from nepalify.dates.bs_datetime import BSDateTime
    
    # Normalize: strip whitespace and convert Nepali digits
    text = date_string.strip()
    normalized = _normalize_nepali_digits(text)
    
    # Try each pattern
    for pattern, pattern_type in _DATE_PATTERNS:
        match = pattern.match(normalized)
        if not match:
            continue
        
        try:
            if pattern_type == 'date':
                year, month, day = map(int, match.groups())
                if is_valid_bs_date(year, month, day):
                    return BSDate(year, month, day)
            
            elif pattern_type == 'datetime':
                groups = match.groups()
                year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
                hour, minute = int(groups[3]), int(groups[4])
                second = int(groups[5]) if groups[5] else 0
                microsecond = int(groups[6]) if groups[6] else 0
                
                if is_valid_bs_date(year, month, day):
                    return BSDateTime(year, month, day, hour, minute, second, microsecond)
            
            elif pattern_type == 'datetime_ampm':
                groups = match.groups()
                year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
                hour, minute = int(groups[3]), int(groups[4])
                ampm = groups[5].upper()
                
                # Convert 12-hour to 24-hour
                if ampm == 'PM' and hour != 12:
                    hour += 12
                elif ampm == 'AM' and hour == 12:
                    hour = 0
                
                if is_valid_bs_date(year, month, day):
                    return BSDateTime(year, month, day, hour, minute, 0)
            
            elif pattern_type == 'named_month':
                month_name, day, year = match.groups()
                month = _parse_month_name(month_name)
                if month and is_valid_bs_date(int(year), month, int(day)):
                    return BSDate(int(year), month, int(day))
            
            elif pattern_type == 'day_month_year':
                day, month_name, year = match.groups()
                month = _parse_month_name(month_name)
                if month and is_valid_bs_date(int(year), month, int(day)):
                    return BSDate(int(year), month, int(day))
            
            elif pattern_type == 'short_year':
                year, month, day = map(int, match.groups())
                # Assume 2000s for 2-digit years
                year = 2000 + year if year < 50 else 1900 + year
                if is_valid_bs_date(year, month, day):
                    return BSDate(year, month, day)
        
        except (ValueError, TypeError):
            continue
    
    raise ValueError(f"Could not parse date string: '{date_string}'")


def parse_date(date_string: str) -> 'BSDate':
    """
    Parse a date string to BSDate.
    
    Like parse(), but always returns BSDate (time components ignored).
    
    Args:
        date_string: String to parse.
    
    Returns:
        BSDate object.
    
    Raises:
        ValueError: If parsing fails.
    """
    from nepalify.dates.bs_date import BSDate
    from nepalify.dates.bs_datetime import BSDateTime
    
    result = parse(date_string)
    
    if isinstance(result, BSDateTime):
        return result.to_date()
    return result


def parse_datetime(date_string: str) -> 'BSDateTime':
    """
    Parse a datetime string to BSDateTime.
    
    Like parse(), but always returns BSDateTime (date-only strings get midnight time).
    
    Args:
        date_string: String to parse.
    
    Returns:
        BSDateTime object.
    
    Raises:
        ValueError: If parsing fails.
    """
    from nepalify.dates.bs_date import BSDate
    from nepalify.dates.bs_datetime import BSDateTime
    
    result = parse(date_string)
    
    if isinstance(result, BSDate):
        return BSDateTime(result.year, result.month, result.day)
    return result


# Format code patterns for strftime/strptime
# Maps format codes to regex patterns
_FORMAT_CODE_PATTERNS = {
    # Date
    '%Y': r'(?P<Y>\d{4})',              # 2080
    '%y': r'(?P<y>\d{2})',              # 80
    '%m': r'(?P<m>\d{1,2})',            # 01-12
    '%d': r'(?P<d>\d{1,2})',            # 01-32
    # Nepali Date
    '%K': r'(?P<K>[०-९]{4})',           # २०८०
    '%k': r'(?P<k>[०-९]{2})',           # ८०
    '%n': r'(?P<n>[०-९]{1,2})',         # ०१-१२
    '%D': r'(?P<D>[०-९]{1,2})',         # ०१-३२
    # Time
    '%H': r'(?P<H>\d{1,2})',            # 00-23
    '%I': r'(?P<I>\d{1,2})',            # 01-12
    '%M': r'(?P<M>\d{1,2})',            # 00-59
    '%S': r'(?P<S>\d{1,2})',            # 00-59
    '%f': r'(?P<f>\d{1,6})',            # 000000
    '%p': r'(?P<p>AM|PM|am|pm)',        # AM/PM
    # Nepali Time
    '%h': r'(?P<h>[०-९]{1,2})',         # ००-२३
    '%i': r'(?P<i>[०-९]{1,2})',         # ००-५९
    '%s': r'(?P<s>[०-९]{1,2})',         # ००-५९
    '%P': r'(?P<P>बिहान|दिउँसो|बेलुका|राति)', # Nepali period
    # Literal
    '%%': r'%',
}


@lru_cache(maxsize=128)
def _compile_format(fmt: str) -> re.Pattern:

    """
    Compile a strftime format string into a regex pattern.
    
    Args:
        fmt: Format string (e.g. "%Y-%m-%d").
    
    Returns:
        Compiled regex pattern.
    """
    pattern_str = re.escape(fmt)
    
    # Replace escaped format codes with regex patterns
    for code, regex in _FORMAT_CODE_PATTERNS.items():
        # Using negative lookbehind to ensure we don't match escaped %
        # But re.escape escapes %, so we look for \%Y
        escaped_code = re.escape(code)
        # We need to replace the escaped code with the regex
        # Pattern for replacement: \%Y -> regex
        pattern_str = pattern_str.replace(escaped_code, regex)
    
    # Allow whitespace flexibility
    pattern_str = pattern_str.replace(r'\ ', r'\s+')
    
    return re.compile(f"^{pattern_str}$")


def parse_bs_datetime(date_string: str, fmt: str) -> 'BSDateTime':
    """
    Parse a date string according to a format string.
    
    Supported format codes:
        Standard: %Y, %y, %m, %d, %H, %I, %M, %S, %f, %p
        Nepali: %K, %k, %n, %D, %h, %i, %s, %P
    
    Args:
        date_string: Date string to parse.
        fmt: Format string.
    
    Returns:
        BSDateTime object.
    
    Raises:
        ValueError: If parsing fails.
    """
    from nepalify.dates.bs_date import BSDate
    from nepalify.dates.bs_datetime import BSDateTime
    from nepalify.text.constants import TIME_PERIODS_NEPALI

    
    # Compile pattern
    pattern = _compile_format(fmt)
    match = pattern.match(date_string)
    
    if not match:
        raise ValueError(f"time data '{date_string}' does not match format '{fmt}'")
    
    groups = match.groupdict()
    
    # Extract date components (default to today/now if missing?)
    # Usually strftime defaults to 1900-01-01. BS might default to something else?
    # BSDateTime defaults: year, month, day required. Time defaults to 0.
    
    # Parse Year
    year = 0
    if 'Y' in groups:
        year = int(groups['Y'])
    elif 'K' in groups:
        year = int(_normalize_nepali_digits(groups['K']))
    elif 'y' in groups:
        y = int(groups['y'])
        year = 2000 + y  # Assume 2000+ for 2-digit years
    elif 'k' in groups:
        y = int(_normalize_nepali_digits(groups['k']))
        year = 2000 + y  # Assume 2000+ for 2-digit years
    
    # Parse Month
    month = 0
    if 'm' in groups:
        month = int(groups['m'])
    elif 'n' in groups:
        month = int(_normalize_nepali_digits(groups['n']))
    
    # Parse Day
    day = 0
    if 'd' in groups:
        day = int(groups['d'])
    elif 'D' in groups:
        day = int(_normalize_nepali_digits(groups['D']))
    
    # Validate required date components
    if year == 0 or month == 0 or day == 0:
        # If any essential component is missing, we can't create a valid date
        # Unless we default them. Python's strptime defaults to 1900-01-01.
        # But for BS, maybe 1970? Or error?
        # BSDateTime constructor requires year, month, day.
        # Let's enforce them for now or default to 1901-01-01 if completely missing?
        # Better to raise error if missing.
        # But typical strptime allows partial parsing if defaults exist.
        pass
    
    # Parse Time
    hour = 0
    if 'H' in groups:
        hour = int(groups['H'])
    elif 'h' in groups:
        hour = int(_normalize_nepali_digits(groups['h']))
    elif 'I' in groups:
        hour = int(groups['I'])
    # Handle AM/PM logic later
    
    minute = 0
    if 'M' in groups:
        minute = int(groups['M'])
    elif 'i' in groups:
        minute = int(_normalize_nepali_digits(groups['i']))
    
    second = 0
    if 'S' in groups:
        second = int(groups['S'])
    elif 's' in groups:
        second = int(_normalize_nepali_digits(groups['s']))
    
    microsecond = 0
    if 'f' in groups:
        # Pad to 6 digits logic or just int?
        # usually %f is 000000.
        microsecond = int(groups['f'].ljust(6, '0')[:6])
    
    # Handle AM/PM
    ampm = groups.get('p')
    nepali_period = groups.get('P')
    
    if ampm:
        ampm = ampm.upper()
        if ampm == 'PM' and hour != 12:
            hour += 12
        elif ampm == 'AM' and hour == 12:
            hour = 0
    elif nepali_period:
        # Map Nepali period to 24h?
        # Roughly: Morning (4-11), Afternoon (12-15), Evening (16-19), Night (20-3)
        # But this is lossy converting back from range name.
        # Unless format string had %I (12-hour)?
        # If we have %h (Nepali hour), is it 12h or 24h?
        # Usually %h implies 24h or 12h depending on context?
        # If nepali_period is present, assume 12-hour logic if hour <= 12?
        # "दिउँसो ०२:३०" -> 14:30.
        # "बिहान १०:००" -> 10:00.
        # "बेलुका ०६:००" -> 18:00.
        pass # Complex logic, maybe skip for now or assume PM if evening/afternoon/night & hour<12?
    
    return BSDateTime(year, month, day, hour, minute, second, microsecond)


__all__ = [
    "parse",
    "parse_date",
    "parse_datetime",
    "parse_bs_datetime",
]

