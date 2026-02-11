"""
BSDateTime class - Bikram Sambat datetime with time and timezone support.

Similar to Python's datetime.datetime but for the BS calendar with Nepal Time.

Example:
    >>> from nepalify.dates import BSDateTime, NepaliTimeZone
    >>> 
    >>> # Current BS datetime in Nepal Time
    >>> now = BSDateTime.now(NepaliTimeZone())
    >>> print(now.strftime("%Y-%m-%d %H:%M:%S %A"))
    2082-10-24 11:15:30 Friday
    >>> 
    >>> # Format in Nepali
    >>> print(now.strftime("%Y-%m-%d %H:%M:%S %A", nepali=True))
    २०८२-१०-२४ ११:१५:३० शुक्रबार
"""

from __future__ import annotations
from datetime import datetime, date, time, timedelta, tzinfo as TzInfo
import time as _time
from typing import Optional, Union, Tuple


from nepalify.dates.converter import (
    ad_to_bs,
    bs_to_ad,
    get_days_in_month,
    is_valid_bs_date,
    BS_MIN_YEAR,
    BS_MAX_YEAR,
)
from nepalify.dates.bs_date import BSDate
from nepalify.dates.timezone import NepaliTimeZone, NPT

from nepalify.dates.format_codes import format_bs_datetime





class BSDateTime:
    """
    Bikram Sambat datetime with time and timezone support.
    
    Represents a datetime in the Nepali Bikram Sambat calendar with
    time components (hour, minute, second, microsecond) and optional
    timezone awareness.
    
    Attributes:
        year: BS year (1901-2199).
        month: BS month (1-12, where 1=Baisakh, 12=Chaitra).
        day: BS day (1-32 depending on month).
        hour: Hour (0-23).
        minute: Minute (0-59).
        second: Second (0-59).
        microsecond: Microsecond (0-999999).
        tzinfo: Timezone info (optional).
    
    Examples:
        >>> dt = BSDateTime(2080, 10, 24, 14, 30, 0)
        >>> print(dt)
        2080-10-24 14:30:00
        >>> 
        >>> # With timezone
        >>> dt = BSDateTime(2080, 10, 24, 14, 30, 0, tzinfo=NepaliTimeZone())
        >>> print(dt)
        2080-10-24 14:30:00+05:45
    """
    
    __slots__ = ('_year', '_month', '_day', '_hour', '_minute', 
                 '_second', '_microsecond', '_tzinfo')
    
    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tzinfo: Optional[TzInfo] = None
    ):
        """
        Create a BSDateTime instance.
        
        Args:
            year: BS year (1901-2199).
            month: BS month (1-12).
            day: BS day.
            hour: Hour (0-23), default 0.
            minute: Minute (0-59), default 0.
            second: Second (0-59), default 0.
            microsecond: Microsecond (0-999999), default 0.
            tzinfo: Timezone info, default None.
        
        Raises:
            ValueError: If any value is out of valid range.
        """
        # Validate BS date
        if not is_valid_bs_date(year, month, day):
            raise ValueError(
                f"Invalid BS date: {year}-{month}-{day}. "
                f"Supported range: {BS_MIN_YEAR}-{BS_MAX_YEAR}"
            )
        
        # Validate time components
        if not 0 <= hour <= 23:
            raise ValueError(f"Hour must be 0-23, got {hour}")
        if not 0 <= minute <= 59:
            raise ValueError(f"Minute must be 0-59, got {minute}")
        if not 0 <= second <= 59:
            raise ValueError(f"Second must be 0-59, got {second}")
        if not 0 <= microsecond <= 999999:
            raise ValueError(f"Microsecond must be 0-999999, got {microsecond}")
        
        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = tzinfo
    
    # Properties
    @property
    def year(self) -> int:
        """The BS year (1901-2199)."""
        return self._year
    
    @property
    def month(self) -> int:
        """The BS month (1-12)."""
        return self._month
    
    @property
    def day(self) -> int:
        """The BS day."""
        return self._day
    
    @property
    def hour(self) -> int:
        """The hour (0-23)."""
        return self._hour
    
    @property
    def minute(self) -> int:
        """The minute (0-59)."""
        return self._minute
    
    @property
    def second(self) -> int:
        """The second (0-59)."""
        return self._second
    
    @property
    def microsecond(self) -> int:
        """The microsecond (0-999999)."""
        return self._microsecond
    
    @property
    def tzinfo(self) -> Optional[TzInfo]:
        """The timezone info."""
        return self._tzinfo
    
    # Class methods for creation
    @classmethod
    def now(cls, tz: Optional[TzInfo] = None) -> BSDateTime:
        """
        Get current BS datetime.
        
        Args:
            tz: Timezone for the result. If None, uses local time.
        
        Returns:
            BSDateTime: Current datetime in BS.
        
        Examples:
            >>> now = BSDateTime.now()
            >>> now_npt = BSDateTime.now(NepaliTimeZone())
        """
        if tz is not None:
            current = datetime.now(tz)
        else:
            current = datetime.now()
        
        return cls.from_ad(current)
    
    @classmethod
    def today(cls) -> BSDateTime:
        """
        Get current BS date with time set to midnight.
        
        Returns:
            BSDateTime: Today's date at 00:00:00.
        """
        today_ad = date.today()
        bs_year, bs_month, bs_day = ad_to_bs(
            today_ad.year, today_ad.month, today_ad.day
        )
        return cls(bs_year, bs_month, bs_day)

    @classmethod
    def fromtimestamp(cls, timestamp: float, tz: Optional[TzInfo] = None) -> BSDateTime:
        """
        Create BSDateTime from POSIX timestamp.
        
        Args:
            timestamp: Seconds since Unix epoch.
            tz: Timezone for the result. Defaults to Nepal Time.
        
        Returns:
            BSDateTime: Datetime from timestamp.
        """
        if tz is None:
            tz = NepaliTimeZone()
        
        dt = datetime.fromtimestamp(timestamp, tz=tz)
        return cls.from_ad(dt)

    
    @classmethod
    def from_ad(cls, dt: Union[datetime, date]) -> BSDateTime:
        """
        Create BSDateTime from a Gregorian datetime or date.
        
        Args:
            dt: Python datetime.datetime or datetime.date object.
        
        Returns:
            BSDateTime: Equivalent BS datetime.
        
        Examples:
            >>> from datetime import datetime
            >>> ad_dt = datetime(2024, 2, 6, 14, 30, 0)
            >>> bs_dt = BSDateTime.from_ad(ad_dt)
            >>> print(bs_dt)
            2080-10-24 14:30:00
        """
        if isinstance(dt, datetime):
            bs_year, bs_month, bs_day = ad_to_bs(dt.year, dt.month, dt.day)
            return cls(
                bs_year, bs_month, bs_day,
                dt.hour, dt.minute, dt.second, dt.microsecond,
                dt.tzinfo
            )
        elif isinstance(dt, date):
            bs_year, bs_month, bs_day = ad_to_bs(dt.year, dt.month, dt.day)
            return cls(bs_year, bs_month, bs_day)
        else:
            raise TypeError(f"Expected datetime or date, got {type(dt).__name__}")
    
    @classmethod
    def fromgregorian(cls, dt: Union[datetime, date]) -> BSDateTime:
        """Alias for from_ad() for compatibility."""
        return cls.from_ad(dt)
    
    @classmethod
    def from_bs_date(cls, bs_date: BSDate) -> BSDateTime:
        """
        Create BSDateTime from a BSDate.
        
        Args:
            bs_date: BSDate object.
        
        Returns:
            BSDateTime: Datetime at midnight for the given date.
        """
        return cls(bs_date.year, bs_date.month, bs_date.day)
    
    @classmethod
    def combine(cls, bs_date: BSDate, t: time) -> BSDateTime:
        """
        Combine a BSDate and a time into a BSDateTime.
        
        Args:
            bs_date: BSDate object.
            t: datetime.time object.
        
        Returns:
            BSDateTime: Combined datetime.
        
        Examples:
            >>> from datetime import time
            >>> bs_date = BSDate(2080, 10, 24)
            >>> t = time(14, 30, 0)
            >>> bs_dt = BSDateTime.combine(bs_date, t)
        """
        return cls(
            bs_date.year, bs_date.month, bs_date.day,
            t.hour, t.minute, t.second, t.microsecond,
            t.tzinfo
        )
    
    # Conversion methods
    def to_ad(self) -> datetime:
        """
        Convert to Gregorian datetime.
        
        Returns:
            datetime: Python datetime.datetime object.
        
        Examples:
            >>> bs_dt = BSDateTime(2080, 10, 24, 14, 30, 0)
            >>> ad_dt = bs_dt.to_ad()
            >>> print(ad_dt)
            2024-02-06 14:30:00
        """
        ad_year, ad_month, ad_day = bs_to_ad(self._year, self._month, self._day)
        return datetime(
            ad_year, ad_month, ad_day,
            self._hour, self._minute, self._second, self._microsecond,
            self._tzinfo
        )
    
    def togregorian(self) -> datetime:
        """Alias for to_ad() for compatibility."""
        return self.to_ad()
    
    def to_date(self) -> BSDate:
        """
        Convert to BSDate (date only, no time).
        
        Returns:
            BSDate: Date component only.
        """
        return BSDate(self._year, self._month, self._day)
    
    def to_nepalidate(self) -> BSDate:
        """Alias for to_date() for nepali library compatibility."""
        return self.to_date()
    
    def to_time(self) -> time:
        """
        Get the time component.
        
        Returns:
            time: Time component with timezone.
        """
        return time(
            self._hour, self._minute, self._second, 
            self._microsecond, self._tzinfo
        )

    def timestamp(self) -> float:
        """
        Return POSIX timestamp.
        
        Returns:
            float: Seconds since Unix epoch.
        """
        return self.to_ad().timestamp()

    def timetuple(self) -> _time.struct_time:
        """
        Return time.struct_time for compatibility with time module.
        
        Returns:
            struct_time: Time tuple with BS year/month/day.
        """
        # Calculate day of year
        from nepalify.dates.converter import bs_date_to_ordinal
        
        ordinal = bs_date_to_ordinal(self._year, self._month, self._day)
        start_ordinal = bs_date_to_ordinal(self._year, 1, 1)
        day_of_year = ordinal - start_ordinal + 1
        
        # Convert Nepali weekday (0=Sun) to Python struct_time weekday (0=Mon)
        nepali_weekday = self.weekday()
        python_weekday = (nepali_weekday + 6) % 7
        
        return _time.struct_time((
            self._year, self._month, self._day,
            self._hour, self._minute, self._second,
            python_weekday, day_of_year, -1
        ))

    
    def date(self) -> BSDate:
        """Get the date component (alias for to_date)."""
        return self.to_date()
    
    def time(self) -> time:
        """Get the time component (alias for to_time)."""
        return self.to_time()
    
    # Weekday methods
    def weekday(self) -> int:
        """
        Return the day of the week.
        
        Returns:
            int: Day of week (0=Sunday, 1=Monday, ..., 6=Saturday).
            Note: Nepali convention starts week on Sunday.
        """
        ad_date = date(*bs_to_ad(self._year, self._month, self._day))
        # Python: Monday=0, Sunday=6
        # Nepali: Sunday=0, Saturday=6
        return (ad_date.weekday() + 1) % 7
    
    def isoweekday(self) -> int:
        """
        Return the ISO day of the week.
        
        Returns:
            int: ISO day of week (1=Monday, 7=Sunday).
        """
        ad_date = date(*bs_to_ad(self._year, self._month, self._day))
        return ad_date.isoweekday()
    
    # Formatting methods
    def strftime(self, fmt: str, style: str = 'formal') -> str:
        """
        Format the datetime as a string using format codes.
        
        Supported format codes:
            Standard (English): %Y, %y, %m, %d, %B, %b, %A, %a
                                %H, %I, %M, %S, %f, %p, %Z, %z
            Nepali (Devanagari): %K, %k, %n, %D, %N, %G, %g
                                 %h, %i, %s, %P
        
        Args:
            fmt: Format string.
            style: Month name style ('formal' or 'sanskrit') for %N.
        
        Returns:
            str: Formatted datetime string.
        
        Examples:
            >>> dt = BSDateTime(2080, 10, 24, 14, 30, 0)
            >>> dt.strftime("%Y-%m-%d %H:%M:%S")
            '2080-10-24 14:30:00'
            >>> dt.strftime("%K-%n-%D %h:%i %P")
            '२०८०-१०-२४ ०२:३० दिउँसो'
        """
        return format_bs_datetime(self, fmt, style=style)
    
    def isoformat(self, sep: str = 'T', timespec: str = 'auto') -> str:
        """
        Return the datetime in ISO format.
        
        Args:
            sep: Separator between date and time (default 'T').
            timespec: Time precision ('auto', 'hours', 'minutes', 
                     'seconds', 'milliseconds', 'microseconds').
        
        Returns:
            str: ISO formatted datetime string.
        """
        date_str = f"{self._year:04d}-{self._month:02d}-{self._day:02d}"
        
        if timespec == 'hours':
            time_str = f"{self._hour:02d}"
        elif timespec == 'minutes':
            time_str = f"{self._hour:02d}:{self._minute:02d}"
        elif timespec == 'seconds':
            time_str = f"{self._hour:02d}:{self._minute:02d}:{self._second:02d}"
        elif timespec == 'milliseconds':
            ms = self._microsecond // 1000
            time_str = f"{self._hour:02d}:{self._minute:02d}:{self._second:02d}.{ms:03d}"
        elif timespec == 'microseconds':
            time_str = f"{self._hour:02d}:{self._minute:02d}:{self._second:02d}.{self._microsecond:06d}"
        else:  # auto
            if self._microsecond:
                time_str = f"{self._hour:02d}:{self._minute:02d}:{self._second:02d}.{self._microsecond:06d}"
            elif self._second:
                time_str = f"{self._hour:02d}:{self._minute:02d}:{self._second:02d}"
            else:
                time_str = f"{self._hour:02d}:{self._minute:02d}:{self._second:02d}"
        
        result = f"{date_str}{sep}{time_str}"
        
        # Add timezone offset
        if self._tzinfo is not None:
            offset = self._tzinfo.utcoffset(None)
            if offset is not None:
                total_seconds = int(offset.total_seconds())
                sign = '+' if total_seconds >= 0 else '-'
                total_seconds = abs(total_seconds)
                hours, remainder = divmod(total_seconds, 3600)
                minutes = remainder // 60
                result += f"{sign}{hours:02d}:{minutes:02d}"
        
        return result
    
    def replace(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        second: Optional[int] = None,
        microsecond: Optional[int] = None,
        tzinfo: Union[TzInfo, None, type(NotImplemented)] = NotImplemented
    ) -> BSDateTime:
        """
        Return a datetime with the same value, except for specified fields.
        
        Args:
            year: New year value (optional).
            month: New month value (optional).
            day: New day value (optional).
            hour: New hour value (optional).
            minute: New minute value (optional).
            second: New second value (optional).
            microsecond: New microsecond value (optional).
            tzinfo: New timezone (optional, use None to remove).
        
        Returns:
            BSDateTime: New datetime with replaced values.
        """
        return BSDateTime(
            year if year is not None else self._year,
            month if month is not None else self._month,
            day if day is not None else self._day,
            hour if hour is not None else self._hour,
            minute if minute is not None else self._minute,
            second if second is not None else self._second,
            microsecond if microsecond is not None else self._microsecond,
            self._tzinfo if tzinfo is NotImplemented else tzinfo
        )
    
    def astimezone(self, tz: Optional[TzInfo] = None) -> BSDateTime:
        """
        Convert to a different timezone.
        
        If self is naive, it's assumed to be in local time.
        
        Args:
            tz: Target timezone. If None, converts to local time.
        
        Returns:
            BSDateTime: Datetime in the target timezone.
        """
        ad_dt = self.to_ad()
        
        if ad_dt.tzinfo is None:
            # Naive datetime - assume local time
            ad_dt = ad_dt.astimezone()
        
        if tz is None:
            converted = ad_dt.astimezone()
        else:
            converted = ad_dt.astimezone(tz)
        
        return BSDateTime.from_ad(converted)
    
    # Arithmetic operations
    def __add__(self, delta: timedelta) -> BSDateTime:
        """
        Add a timedelta to the datetime.
        
        Args:
            delta: timedelta to add.
        
        Returns:
            BSDateTime: New datetime.
        
        Examples:
            >>> dt = BSDateTime(2080, 10, 24, 14, 30)
            >>> dt + timedelta(hours=5)
            BSDateTime(2080, 10, 24, 19, 30, 0)
        """
        if not isinstance(delta, timedelta):
            return NotImplemented
        
        ad_dt = self.to_ad() + delta
        return BSDateTime.from_ad(ad_dt)
    
    def __radd__(self, delta: timedelta) -> BSDateTime:
        """Support delta + datetime."""
        return self.__add__(delta)
    
    def __sub__(
        self, 
        other: Union[timedelta, BSDateTime]
    ) -> Union[BSDateTime, timedelta]:
        """
        Subtract a timedelta or another BSDateTime.
        
        Args:
            other: timedelta to subtract, or BSDateTime for difference.
        
        Returns:
            BSDateTime if subtracting timedelta, timedelta if subtracting BSDateTime.
        
        Examples:
            >>> dt1 = BSDateTime(2080, 10, 24, 14, 30)
            >>> dt1 - timedelta(hours=2)
            BSDateTime(2080, 10, 24, 12, 30, 0)
            >>> dt2 = BSDateTime(2080, 10, 24, 12, 30)
            >>> dt1 - dt2
            datetime.timedelta(seconds=7200)
        """
        if isinstance(other, timedelta):
            return self.__add__(-other)
        elif isinstance(other, BSDateTime):
            return self.to_ad() - other.to_ad()
        return NotImplemented
    
    # Comparison operators
    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if isinstance(other, BSDateTime):
            return (
                self._year == other._year and
                self._month == other._month and
                self._day == other._day and
                self._hour == other._hour and
                self._minute == other._minute and
                self._second == other._second and
                self._microsecond == other._microsecond and
                self._tzinfo == other._tzinfo
            )
        return NotImplemented
    
    def __ne__(self, other: object) -> bool:
        """Check inequality."""
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    
    def __lt__(self, other: BSDateTime) -> bool:
        """Check if less than."""
        if not isinstance(other, BSDateTime):
            return NotImplemented
        return self.to_ad() < other.to_ad()
    
    def __le__(self, other: BSDateTime) -> bool:
        """Check if less than or equal."""
        if not isinstance(other, BSDateTime):
            return NotImplemented
        return self.to_ad() <= other.to_ad()
    
    def __gt__(self, other: BSDateTime) -> bool:
        """Check if greater than."""
        if not isinstance(other, BSDateTime):
            return NotImplemented
        return self.to_ad() > other.to_ad()
    
    def __ge__(self, other: BSDateTime) -> bool:
        """Check if greater than or equal."""
        if not isinstance(other, BSDateTime):
            return NotImplemented
        return self.to_ad() >= other.to_ad()
    
    def __hash__(self) -> int:
        """Return hash value."""
        return hash((
            self._year, self._month, self._day,
            self._hour, self._minute, self._second, self._microsecond,
            self._tzinfo
        ))
    
    def __repr__(self) -> str:
        """Return repr string."""
        parts = [
            f"BSDateTime({self._year}, {self._month}, {self._day}",
            f"{self._hour}, {self._minute}, {self._second}"
        ]
        if self._microsecond:
            parts.append(f", {self._microsecond}")
        if self._tzinfo:
            parts.append(f", tzinfo={self._tzinfo!r}")
        return f"{parts[0]}, {parts[1]}{''.join(parts[2:])})"
    
    def __str__(self) -> str:
        """Return string representation."""
        base = f"{self._year:04d}-{self._month:02d}-{self._day:02d} " \
               f"{self._hour:02d}:{self._minute:02d}:{self._second:02d}"
        
        if self._tzinfo is not None:
            offset = self._tzinfo.utcoffset(None)
            if offset is not None:
                total_seconds = int(offset.total_seconds())
                sign = '+' if total_seconds >= 0 else '-'
                total_seconds = abs(total_seconds)
                hours, remainder = divmod(total_seconds, 3600)
                minutes = remainder // 60
                base += f"{sign}{hours:02d}:{minutes:02d}"
        
        return base



    
    @classmethod
    def strptime(cls, date_string: str, fmt: str) -> BSDateTime:
        """
        Parse a string to a BSDateTime according to a format string.
        
        Args:
            date_string: String to parse.
            fmt: Format string.
        
        Returns:
            BSDateTime: Parsed datetime.
        """
        from nepalify.dates.parser import parse_bs_datetime
        return parse_bs_datetime(date_string, fmt)




__all__ = [
    "BSDateTime",
    "TIME_PERIODS_NEPALI",
]
