"""
Nepal Timezone Support.

Provides timezone utilities for Nepal Standard Time (NPT) which is UTC+05:45.
Nepal does not observe daylight saving time.

Example:
    >>> from nepalify.dates.timezone import NepaliTimeZone, nepali_now
    >>> import datetime
    >>> 
    >>> # Create datetime with Nepal timezone
    >>> dt = datetime.datetime(2024, 2, 7, 11, 0, tzinfo=NepaliTimeZone())
    >>> print(dt)  # 2024-02-07 11:00:00+05:45
    >>> 
    >>> # Get current Nepal time
    >>> now = nepali_now()
    >>> print(now)
"""

import datetime
from typing import Optional, Union

# Constants
NEPAL_TIMEZONE = "Asia/Kathmandu"
NPT_OFFSET = datetime.timedelta(hours=5, minutes=45)


class NepaliTimeZone(datetime.tzinfo):
    """
    Nepal Standard Time timezone implementation.
    
    NepaliTimeZone represents "Asia/Kathmandu" with a fixed UTC offset of +05:45.
    Nepal does not observe daylight saving time (DST).
    
    This class implements Python's tzinfo interface, making it compatible
    with standard datetime operations.
    
    Attributes:
        offset: Fixed timedelta of +5 hours 45 minutes.
    
    Examples:
        >>> import datetime
        >>> from nepalify.dates.timezone import NepaliTimeZone
        >>> 
        >>> # Create timezone-aware datetime
        >>> npt = NepaliTimeZone()
        >>> dt = datetime.datetime(2024, 2, 7, 11, 30, tzinfo=npt)
        >>> print(dt)
        2024-02-07 11:30:00+05:45
        >>> 
        >>> # Check offset
        >>> print(npt.utcoffset(None))
        5:45:00
    """
    
    __slots__ = ()
    
    def utcoffset(self, dt: Optional[datetime.datetime]) -> datetime.timedelta:
        """
        Return the UTC offset for Nepal Time.
        
        Nepal Time is always UTC+05:45 (no DST).
        
        Args:
            dt: Datetime object (unused, as NPT has fixed offset).
        
        Returns:
            timedelta: Fixed offset of 5 hours 45 minutes.
        """
        return NPT_OFFSET
    
    def dst(self, dt: Optional[datetime.datetime]) -> datetime.timedelta:
        """
        Return the daylight saving time offset.
        
        Nepal does not observe DST, so this always returns zero.
        
        Args:
            dt: Datetime object (unused).
        
        Returns:
            timedelta: Zero (no DST adjustment).
        """
        return datetime.timedelta(0)
    
    def tzname(self, dt: Optional[datetime.datetime]) -> str:
        """
        Return the timezone name.
        
        Args:
            dt: Datetime object (unused).
        
        Returns:
            str: "Asia/Kathmandu"
        """
        return NEPAL_TIMEZONE
    
    def __repr__(self) -> str:
        """Return representation string."""
        return f"NepaliTimeZone('{NEPAL_TIMEZONE}', UTC+05:45)"
    
    def __str__(self) -> str:
        """Return string representation."""
        return NEPAL_TIMEZONE
    
    def __eq__(self, other: object) -> bool:
        """Check equality with another timezone."""
        if isinstance(other, NepaliTimeZone):
            return True
        if isinstance(other, datetime.tzinfo):
            try:
                return other.utcoffset(None) == NPT_OFFSET
            except Exception:
                return False
        return False
    
    def __hash__(self) -> int:
        """Return hash value."""
        return hash(("NepaliTimeZone", NPT_OFFSET))


# Singleton instance for convenience
NPT = NepaliTimeZone()


def get_local_timezone() -> Optional[datetime.tzinfo]:
    """
    Get the current system's local timezone.
    
    Returns:
        tzinfo: Local timezone or None if unavailable.
    
    Examples:
        >>> tz = get_local_timezone()
        >>> print(tz)
    """
    return datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo


def now() -> datetime.datetime:
    """
    Get current datetime with system's local timezone.
    
    Unlike datetime.now(), this includes timezone information.
    
    Returns:
        datetime: Current datetime with local timezone.
    
    Examples:
        >>> from nepalify.dates.timezone import now
        >>> current = now()
        >>> print(current.tzinfo is not None)
        True
    """
    return datetime.datetime.now(datetime.timezone.utc).astimezone()


def utc_now() -> datetime.datetime:
    """
    Get current UTC datetime.
    
    Returns:
        datetime: Current UTC datetime with timezone info.
    
    Examples:
        >>> from nepalify.dates.timezone import utc_now
        >>> utc = utc_now()
        >>> print(utc.tzname())
        UTC
    """
    return datetime.datetime.now(datetime.timezone.utc)


def nepali_now() -> datetime.datetime:
    """
    Get current datetime in Nepal Time (NPT).
    
    Returns:
        datetime: Current datetime in Nepal timezone (UTC+05:45).
    
    Examples:
        >>> from nepalify.dates.timezone import nepali_now
        >>> npt = nepali_now()
        >>> print(npt.tzname())
        Asia/Kathmandu
    """
    return datetime.datetime.now(NepaliTimeZone())


def to_nepali_timezone(dt: datetime.datetime) -> datetime.datetime:
    """
    Convert a datetime to Nepal timezone.
    
    If the datetime is naive (no timezone), it's assumed to be in
    the local system timezone before conversion.
    
    Args:
        dt: Datetime object to convert.
    
    Returns:
        datetime: Datetime in Nepal timezone (UTC+05:45).
    
    Raises:
        TypeError: If dt is not a datetime object.
    
    Examples:
        >>> import datetime
        >>> from nepalify.dates.timezone import to_nepali_timezone
        >>> 
        >>> # Convert UTC time to NPT
        >>> utc_dt = datetime.datetime(2024, 2, 7, 5, 15, 
        ...                            tzinfo=datetime.timezone.utc)
        >>> npt_dt = to_nepali_timezone(utc_dt)
        >>> print(npt_dt)
        2024-02-07 11:00:00+05:45
    """
    if not isinstance(dt, datetime.datetime):
        raise TypeError(f"Expected datetime.datetime, got {type(dt).__name__}")
    
    # Handle naive datetime - assume local timezone
    if dt.tzinfo is None:
        local_tz = get_local_timezone()
        dt = dt.replace(tzinfo=local_tz)
    
    return dt.astimezone(NepaliTimeZone())


def to_utc_timezone(dt: datetime.datetime) -> datetime.datetime:
    """
    Convert a datetime to UTC timezone.
    
    If the datetime is naive (no timezone), it's assumed to be in
    the local system timezone before conversion.
    
    Args:
        dt: Datetime object to convert.
    
    Returns:
        datetime: Datetime in UTC timezone.
    
    Raises:
        TypeError: If dt is not a datetime object.
    
    Examples:
        >>> import datetime
        >>> from nepalify.dates.timezone import to_utc_timezone, NepaliTimeZone
        >>> 
        >>> # Convert NPT time to UTC
        >>> npt_dt = datetime.datetime(2024, 2, 7, 11, 0, 
        ...                            tzinfo=NepaliTimeZone())
        >>> utc_dt = to_utc_timezone(npt_dt)
        >>> print(utc_dt)
        2024-02-07 05:15:00+00:00
    """
    if not isinstance(dt, datetime.datetime):
        raise TypeError(f"Expected datetime.datetime, got {type(dt).__name__}")
    
    # Handle naive datetime - assume local timezone
    if dt.tzinfo is None:
        local_tz = get_local_timezone()
        dt = dt.replace(tzinfo=local_tz)
    
    return dt.astimezone(datetime.timezone.utc)


def from_utc(
    dt: datetime.datetime, 
    target_tz: Optional[datetime.tzinfo] = None
) -> datetime.datetime:
    """
    Convert UTC datetime to target timezone (default: NPT).
    
    Args:
        dt: UTC datetime object.
        target_tz: Target timezone (default: NepaliTimeZone).
    
    Returns:
        datetime: Datetime in target timezone.
    
    Examples:
        >>> import datetime
        >>> from nepalify.dates.timezone import from_utc
        >>> 
        >>> utc = datetime.datetime(2024, 2, 7, 5, 15, 
        ...                         tzinfo=datetime.timezone.utc)
        >>> npt = from_utc(utc)
        >>> print(npt)
        2024-02-07 11:00:00+05:45
    """
    if target_tz is None:
        target_tz = NepaliTimeZone()
    
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    
    return dt.astimezone(target_tz)


__all__ = [
    # Constants
    "NEPAL_TIMEZONE",
    "NPT_OFFSET",
    "NPT",
    # Classes
    "NepaliTimeZone",
    # Functions
    "get_local_timezone",
    "now",
    "utc_now",
    "nepali_now",
    "to_nepali_timezone",
    "to_utc_timezone",
    "from_utc",
]
