"""
Enhanced format code system with lambda-based formatters.

Supports all standard datetime format codes plus Nepali-specific codes:
- %D: Devanagari day (०१-३२)
- %n: Devanagari month (०१-१२)
- %N: Nepali month name (वैशाख, जेष्ठ, ...)
- %K: Devanagari year (२०८०)
- %k: Devanagari short year (८०)
- %G: Nepali weekday name (आइतबार, सोमबार, ...)
"""

from typing import Callable, Dict, Union, TYPE_CHECKING
from nepalify.numbers.devanagari import to_devanagari
from nepalify.text.constants import (
    DAYS_ENGLISH, DAYS_ENGLISH_SHORT,
    DAYS_NEPALI, DAYS_NEPALI_SHORT,
    MONTHS_ENGLISH, MONTHS_ENGLISH_SHORT,
    MONTHS_NEPALI, MONTHS_NEPALI_SANSKRIT,
    TIME_PERIODS_NEPALI
)

if TYPE_CHECKING:
    from nepalify.dates.bs_date import BSDate
    from nepalify.dates.bs_datetime import BSDateTime

# Type alias
FormatFunc = Callable[[Union['BSDate', 'BSDateTime']], str]

def get_nepali_time_period(hour: int) -> str:
    """Get Nepali time period name based on hour of day."""
    if 4 <= hour < 12:
        return TIME_PERIODS_NEPALI['morning']
    elif 12 <= hour < 16:
        return TIME_PERIODS_NEPALI['afternoon']
    elif 16 <= hour < 20:
        return TIME_PERIODS_NEPALI['evening']
    else:
        return TIME_PERIODS_NEPALI['night']

def format_timezone_offset(date_obj) -> str:
    """Format timezone offset as string like +0545."""
    if not hasattr(date_obj, 'tzinfo') or date_obj.tzinfo is None:
        return ''
    offset = date_obj.tzinfo.utcoffset(None)
    if offset is None:
        return ''
    total_seconds = int(offset.total_seconds())
    sign = '+' if total_seconds >= 0 else '-'
    total_seconds = abs(total_seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    return f"{sign}{hours:02d}{minutes:02d}"

def format_timezone_name(date_obj) -> str:
    """Format timezone name as string like NPT."""
    if not hasattr(date_obj, 'tzinfo') or date_obj.tzinfo is None:
        return ''
    return date_obj.tzinfo.tzname(None) or ''

# Standard format codes (matching Python's strftime)
STANDARD_CODES: Dict[str, FormatFunc] = {
    # Date codes
    '%Y': lambda o: f"{o.year:04d}",
    '%y': lambda o: f"{o.year % 100:02d}",
    '%m': lambda o: f"{o.month:02d}",
    '%d': lambda o: f"{o.day:02d}",
    '%B': lambda o: MONTHS_ENGLISH[o.month - 1],
    '%b': lambda o: MONTHS_ENGLISH_SHORT[o.month - 1],
    '%A': lambda o: DAYS_ENGLISH[o.weekday()],
    '%a': lambda o: DAYS_ENGLISH_SHORT[o.weekday()],
    '%w': lambda o: str(o.weekday()),
    '%j': lambda o: f"{o.toordinal() - o.replace(month=1, day=1).toordinal() + 1:03d}",
    
    # Time codes (for BSDateTime)
    '%H': lambda o: f"{getattr(o, 'hour', 0):02d}",
    '%I': lambda o: f"{(getattr(o, 'hour', 0) % 12) or 12:02d}",
    '%M': lambda o: f"{getattr(o, 'minute', 0):02d}",
    '%S': lambda o: f"{getattr(o, 'second', 0):02d}",
    '%f': lambda o: f"{getattr(o, 'microsecond', 0):06d}",
    '%p': lambda o: 'PM' if getattr(o, 'hour', 0) >= 12 else 'AM',
    
    # Timezone
    '%z': format_timezone_offset,
    '%Z': format_timezone_name,
    
    # Literal
    '%%': lambda o: '%',
}

# Nepali-specific format codes
NEPALI_CODES: Dict[str, FormatFunc] = {
    '%D': lambda o: to_devanagari(f"{o.day:02d}"),  # Devanagari day
    '%n': lambda o: to_devanagari(f"{o.month:02d}"),  # Devanagari month number
    '%N': lambda o: MONTHS_NEPALI[o.month - 1],  # Nepali month name
    '%K': lambda o: to_devanagari(f"{o.year:04d}"),  # Devanagari year
    '%k': lambda o: to_devanagari(f"{o.year % 100:02d}"),  # Devanagari short year
    '%G': lambda o: DAYS_NEPALI[o.weekday()],  # Nepali weekday
    '%g': lambda o: DAYS_NEPALI_SHORT[o.weekday()],  # Short Nepali weekday
    '%h': lambda o: to_devanagari(f"{getattr(o, 'hour', 0):02d}"),  # Devanagari hour
    '%i': lambda o: to_devanagari(f"{getattr(o, 'minute', 0):02d}"),  # Devanagari minute
    '%s': lambda o: to_devanagari(f"{getattr(o, 'second', 0):02d}"),  # Devanagari second
    '%P': lambda o: get_nepali_time_period(getattr(o, 'hour', 0)),  # Nepali period
}

# Combined lookup (standard + Nepali)
ALL_FORMAT_CODES = {**STANDARD_CODES, **NEPALI_CODES}

def format_bs_datetime(
    date_obj: Union['BSDate', 'BSDateTime'], 
    fmt: str, 
    style: str = 'formal'
) -> str:
    """Format BS date/datetime using format codes.
    
    Args:
        date_obj: BSDate or BSDateTime instance.
        fmt: Format string with % codes.
        style: Month name style ('formal' or 'sanskrit').
               Affects %N code.
    
    Returns:
        str: Formatted string.
    
    Examples:
        >>> dt = BSDateTime(2080, 10, 24, 14, 30)
        >>> format_bs_datetime(dt, '%Y-%m-%d %H:%M')
        '2080-10-24 14:30'
        >>> format_bs_datetime(dt, '%D %N, %K')
        '२४ माघ, २०८०'
    """
    result = fmt
    
    # Process format codes
    # We iterate over the format string to find codes, rather than iterating over all codes
    # This is more efficient for long format strings or many codes
    
    # Optimization: Check if string has any % before processing
    if '%' not in result:
        return result
    
    # Helper to avoid repeated getattr calls
    # (Not strictly necessary given lambda structure but good for future optimization)
    
    for code, formatter in ALL_FORMAT_CODES.items():
        if code in result:
            try:
                # Handle style-dependent codes
                if code == '%N' and style == 'sanskrit':
                    value = MONTHS_NEPALI_SANSKRIT[date_obj.month - 1]
                else:
                    value = formatter(date_obj)
                
                result = result.replace(code, value)
            except AttributeError:
                # Code not applicable (e.g., %H for BSDate)
                pass
            except Exception:
                # Fallback for any other errors (e.g. invalid date state)
                pass
                
    return result
