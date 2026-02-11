"""
AD ↔ BS (Bikram Sambat) date conversion algorithms.

Reference date: 1901-01-01 BS = 1844-04-11 AD
Supported range: 1901 BS - 2199 BS
"""

import json
import bisect
from functools import lru_cache
from datetime import date, timedelta
from pathlib import Path
from typing import Tuple, Dict, List

# Load BS calendar data
_DATA_PATH = Path(__file__).parent / "data" / "bs_calendar.json"
_BS_CALENDAR: Dict[str, List[int]] = {}


def _load_calendar_data() -> Dict[str, List[int]]:
    """Load BS calendar data from JSON file."""
    global _BS_CALENDAR
    if not _BS_CALENDAR:
        with open(_DATA_PATH, 'r', encoding='utf-8') as f:
            _BS_CALENDAR = json.load(f)
    return _BS_CALENDAR


def get_days_in_month(year: int, month: int) -> int:
    """
    Get the number of days in a BS month.
    
    Args:
        year: BS year (1901-2199).
        month: BS month (1-12).
    
    Returns:
        Number of days in the month.
    
    Raises:
        ValueError: If year or month is out of range.
    """
    calendar = _load_calendar_data()
    year_str = str(year)
    
    if year_str not in calendar:
        raise ValueError(f"BS year {year} not in supported range (1901-2199)")
    if not 1 <= month <= 12:
        raise ValueError(f"Month must be 1-12, got {month}")
    
    return calendar[year_str][month - 1]


def get_days_in_year(year: int) -> int:
    """
    Get the total number of days in a BS year.
    
    Args:
        year: BS year (1901-2199).
    
    Returns:
        Total number of days in the year.
    """
    calendar = _load_calendar_data()
    year_str = str(year)
    
    if year_str not in calendar:
        raise ValueError(f"BS year {year} not in supported range (1901-2199)")
    
    return sum(calendar[year_str])


# Reference date for conversions
_REF_BS = (1901, 1, 1)  # BS date
_REF_AD = date(1844, 4, 11)  # Equivalent AD date (Corrected for 2000+ alignment)

# BS year range
BS_MIN_YEAR = 1901
BS_MAX_YEAR = 2199


# ============================================================================
# Ordinal-Based Date System
# ============================================================================
# Pre-computed lookup tables for O(1) date lookups and fast arithmetic

_CUMULATIVE_DAYS_BY_YEAR: List[int] = []  # Total days before each year
_CUMULATIVE_DAYS_BY_MONTH: Dict[int, List[int]] = {}  # Days before each month per year
_MAX_ORDINAL: int = 0  # Maximum valid ordinal

_ORDINAL_INITIALIZED = False


def _initialize_calendar_lookup_tables() -> None:
    """Initialize pre-computed lookup tables for O(1) date lookups.
    
    Called automatically when ordinal functions are first used.
    Pre-computes cumulative days for fast year/month/day lookups.
    """
    global _CUMULATIVE_DAYS_BY_YEAR, _CUMULATIVE_DAYS_BY_MONTH, _MAX_ORDINAL, _ORDINAL_INITIALIZED
    
    if _ORDINAL_INITIALIZED:
        return
    
    calendar = _load_calendar_data()
    cumulative_days = 0
    
    for year in range(BS_MIN_YEAR, BS_MAX_YEAR + 1):
        year_str = str(year)
        if year_str not in calendar:
            break
            
        _CUMULATIVE_DAYS_BY_YEAR.append(cumulative_days)
        
        # Pre-compute cumulative days for each month in this year
        month_cumulative = [0]  # Days before month 1 = 0
        for month in range(1, 13):
            month_cumulative.append(
                month_cumulative[-1] + calendar[year_str][month - 1]
            )
        _CUMULATIVE_DAYS_BY_MONTH[year] = month_cumulative
        
        cumulative_days += sum(calendar[year_str])
    
    _MAX_ORDINAL = cumulative_days
    _ORDINAL_INITIALIZED = True


def bs_date_to_ordinal(year: int, month: int, day: int) -> int:
    """Convert BS date components to ordinal number.
    
    Ordinal is the number of days since BS 1901-01-01 (which is ordinal 1).
    This enables fast date arithmetic: just add/subtract integers.
    
    Args:
        year: BS year (1901-2199)
        month: BS month (1-12)
        day: BS day (1-32)
    
    Returns:
        int: Days since epoch (1901-01-01 = 1)
    
    Examples:
        >>> bs_date_to_ordinal(1901, 1, 1)
        1
        >>> bs_date_to_ordinal(1901, 1, 2)
        2
        >>> bs_date_to_ordinal(2080, 10, 24)
        65532
    
    Raises:
        ValueError: If date is outside supported range.
    """
    _initialize_calendar_lookup_tables()
    
    if not BS_MIN_YEAR <= year <= BS_MAX_YEAR:
        raise ValueError(f"Year {year} outside supported range ({BS_MIN_YEAR}-{BS_MAX_YEAR})")
    if not 1 <= month <= 12:
        raise ValueError(f"Month {month} must be 1-12")
    if year not in _CUMULATIVE_DAYS_BY_MONTH:
        raise ValueError(f"Year {year} not in calendar data")
    
    year_index = year - BS_MIN_YEAR
    return (
        _CUMULATIVE_DAYS_BY_YEAR[year_index] + 
        _CUMULATIVE_DAYS_BY_MONTH[year][month - 1] + 
        day
    )


def ordinal_to_bs_date(ordinal: int) -> Tuple[int, int, int]:
    """Convert ordinal number back to BS date components.
    
    Inverse of bs_date_to_ordinal(). Uses binary search for efficiency.
    
    Args:
        ordinal: Days since BS 1901-01-01 (1 = 1901-01-01)
    
    Returns:
        Tuple of (year, month, day)
    
    Examples:
        >>> ordinal_to_bs_date(1)
        (1901, 1, 1)
        >>> ordinal_to_bs_date(2)
        (1901, 1, 2)
        >>> ordinal_to_bs_date(65532)
        (2080, 10, 24)
    
    Raises:
        ValueError: If ordinal is outside supported range.
    """
    import bisect
    
    _initialize_calendar_lookup_tables()
    
    if ordinal < 1:
        raise ValueError(f"Ordinal {ordinal} must be >= 1")
    if ordinal > _MAX_ORDINAL:
        raise ValueError(f"Ordinal {ordinal} exceeds maximum ({_MAX_ORDINAL})")
    
    # Binary search for year
    year_index = bisect.bisect_right(_CUMULATIVE_DAYS_BY_YEAR, ordinal - 1) - 1
    if year_index < 0:
        year_index = 0
    year = BS_MIN_YEAR + year_index
    
    # Calculate remaining days in that year
    remaining_days = ordinal - _CUMULATIVE_DAYS_BY_YEAR[year_index]
    
    # Binary search for month
    month_lookup = _CUMULATIVE_DAYS_BY_MONTH[year]
    month = bisect.bisect_right(month_lookup, remaining_days - 1)
    if month < 1:
        month = 1
    if month > 12:
        month = 12
    
    # Calculate day
    day = remaining_days - month_lookup[month - 1]
    
    return year, month, day


def get_max_ordinal() -> int:
    """Get the maximum valid ordinal value.
    
    Returns:
        int: Maximum ordinal (last day of BS 2199)
    """
    _initialize_calendar_lookup_tables()
    return _MAX_ORDINAL


@lru_cache(maxsize=1024)
def ad_to_bs(year: int, month: int, day: int) -> Tuple[int, int, int]:
    """
    Convert a Gregorian (AD) date to Bikram Sambat (BS).
    
    Args:
        year: Gregorian year.
        month: Gregorian month (1-12).
        day: Gregorian day.
    
    Returns:
        Tuple of (bs_year, bs_month, bs_day).
    
    Raises:
        ValueError: If the date is outside the supported range.
    """
    try:
        target_ad = date(year, month, day)
    except ValueError as e:
        raise ValueError(f"Invalid AD date: {year}-{month}-{day}") from e

    # Calculate ordinal difference
    # BS 1901-01-01 is ordinal 1
    # AD 1844-04-11 is reference for BS 1901-01-01
    
    ref_ad_ordinal = _REF_AD.toordinal()
    target_ad_ordinal = target_ad.toordinal()
    
    # bs_ordinal = (target - ref) + 1
    bs_ordinal = target_ad_ordinal - ref_ad_ordinal + 1
    
    if bs_ordinal < 1:
         raise ValueError(
            f"Date {year}-{month}-{day} is before the supported range "
            f"(starts at {_REF_AD})"
        )
        
    try:
        return ordinal_to_bs_date(bs_ordinal)
    except ValueError:
         raise ValueError(
            f"Date {year}-{month}-{day} is beyond the supported range "
            f"(BS 1901-2199)"
        )



@lru_cache(maxsize=1024)
def bs_to_ad(year: int, month: int, day: int) -> Tuple[int, int, int]:
    """
    Convert a Bikram Sambat (BS) date to Gregorian (AD).
    
    Args:
        year: BS year (1901-2199).
        month: BS month (1-12).
        day: BS day.
    
    Returns:
        Tuple of (ad_year, ad_month, ad_day).
    
    Raises:
        ValueError: If the date is outside the supported range or invalid.
    """
    # Get ordinal (validates input)
    bs_ordinal = bs_date_to_ordinal(year, month, day)
    
    # Calculate AD date
    # bs_ordinal 1 = _REF_AD
    # ad_ordinal = ref_ad_ordinal + bs_ordinal - 1
    
    ref_ad_ordinal = _REF_AD.toordinal()
    ad_ordinal = ref_ad_ordinal + bs_ordinal - 1
    
    ad_date = date.fromordinal(ad_ordinal)
    
    return (ad_date.year, ad_date.month, ad_date.day)



def is_valid_bs_date(year: int, month: int, day: int) -> bool:
    """
    Check if a BS date is valid.
    
    Args:
        year: BS year.
        month: BS month.
        day: BS day.
    
    Returns:
        True if the date is valid, False otherwise.
    """
    try:
        calendar = _load_calendar_data()
        year_str = str(year)
        
        if year_str not in calendar:
            return False
        if not 1 <= month <= 12:
            return False
        
        days_in_month = calendar[year_str][month - 1]
        return 1 <= day <= days_in_month
    except Exception:
        return False
