"""
BSDate class - Bikram Sambat date with datetime-like API.

Similar to Python's datetime.date but for the BS calendar.
"""

from __future__ import annotations
from datetime import date, timedelta
from typing import Optional, Union

from nepalify.dates.converter import (
    ad_to_bs,
    bs_to_ad,
    get_days_in_month,
    is_valid_bs_date,
    bs_date_to_ordinal,
    ordinal_to_bs_date,
    get_max_ordinal,
    BS_MIN_YEAR,
    BS_MAX_YEAR,
)

from nepalify.dates.format_codes import format_bs_datetime


class BSDate:
    """
    Bikram Sambat date class with datetime-like API.
    
    Represents a date in the Nepali Bikram Sambat calendar.
    Provides conversion to/from Gregorian dates, formatting,
    and date arithmetic.
    
    Attributes:
        year: BS year (2000-2100).
        month: BS month (1-12, where 1=Baisakh, 12=Chaitra).
        day: BS day (1-32 depending on month).
    
    Examples:
        >>> date = BSDate(2080, 10, 24)
        >>> date.year, date.month, date.day
        (2080, 10, 24)
        >>> date.strftime("%Y-%m-%d")
        '2080-10-24'
        >>> date.to_ad()
        datetime.date(2024, 2, 6)
    """
    
    __slots__ = ('_year', '_month', '_day')
    
    def __init__(self, year: int, month: int, day: int):
        """
        Create a BSDate instance.
        
        Args:
            year: BS year (1901-2199).
            month: BS month (1-12).
            day: BS day.
        
        Raises:
            ValueError: If the date is invalid.
        """
        if not is_valid_bs_date(year, month, day):
            raise ValueError(
                f"Invalid BS date: {year}-{month}-{day}. "
                f"Supported range: {BS_MIN_YEAR}-{BS_MAX_YEAR}"
            )
        
        self._year = year
        self._month = month
        self._day = day
    
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
    
    @classmethod
    def today(cls) -> BSDate:
        """
        Return the current date in BS.
        
        Returns:
            BSDate object representing today.
        
        Examples:
            >>> today = BSDate.today()
            >>> print(today)
            2080-10-24
        """
        today_ad = date.today()
        bs_year, bs_month, bs_day = ad_to_bs(
            today_ad.year, today_ad.month, today_ad.day
        )
        return cls(bs_year, bs_month, bs_day)
    
    @classmethod
    def from_ad(cls, ad_date: date) -> BSDate:
        """
        Create a BSDate from a Gregorian date.
        
        Args:
            ad_date: Python datetime.date object.
        
        Returns:
            Equivalent BSDate.
        
        Examples:
            >>> from datetime import date
            >>> bs = BSDate.from_ad(date(2024, 2, 6))
            >>> print(bs)
            2080-10-24
        """
        bs_year, bs_month, bs_day = ad_to_bs(
            ad_date.year, ad_date.month, ad_date.day
        )
        return cls(bs_year, bs_month, bs_day)
    
    @classmethod
    def fromgregorian(cls, ad_date: date) -> BSDate:
        """Alias for from_ad() for compatibility."""
        return cls.from_ad(ad_date)
    
    def to_ad(self) -> date:
        """
        Convert to a Gregorian date.
        
        Returns:
            Python datetime.date object.
        
        Examples:
            >>> bs = BSDate(2080, 10, 24)
            >>> bs.to_ad()
            datetime.date(2024, 2, 6)
        """
        ad_year, ad_month, ad_day = bs_to_ad(self._year, self._month, self._day)
        return date(ad_year, ad_month, ad_day)
    
    def togregorian(self) -> date:
        """Alias for to_ad() for compatibility."""
        return self.to_ad()
    
    def toordinal(self) -> int:
        """Return proleptic ordinal (days since BS 1901-01-01).
        
        This is the fast way to do date arithmetic. Use ordinals for:
        - Adding/subtracting days
        - Comparing dates
        - Calculating differences
        
        Returns:
            int: Number of days since BS 1901-01-01 (which is ordinal 1).
        
        Examples:
            >>> BSDate(1901, 1, 1).toordinal()
            1
            >>> BSDate(1901, 1, 2).toordinal()
            2
            >>> BSDate(2080, 10, 24).toordinal()
            65532
        """
        return bs_date_to_ordinal(self._year, self._month, self._day)
    
    @classmethod
    def fromordinal(cls, ordinal: int) -> BSDate:
        """Create BSDate from ordinal.
        
        Inverse of toordinal(). Fast way to construct dates from arithmetic.
        
        Args:
            ordinal: Days since BS 1901-01-01 (1 = first day of 1901).
        
        Returns:
            BSDate: Date object for that ordinal.
        
        Examples:
            >>> BSDate.fromordinal(1)
            BSDate(1901, 1, 1)
            >>> BSDate.fromordinal(2)
            BSDate(1901, 1, 2)
        
        Raises:
            ValueError: If ordinal is outside valid range.
        """
        year, month, day = ordinal_to_bs_date(ordinal)
        return cls(year, month, day)
    
    def weekday(self) -> int:
        """
        Return the day of the week.
        
        Returns:
            Day of week (0=Sunday, 1=Monday, ..., 6=Saturday).
            Note: This differs from Python's datetime.weekday() 
            which uses 0=Monday.
        
        Examples:
            >>> BSDate(2080, 10, 24).weekday()
            2  # Tuesday
        """
        # Get AD date and calculate weekday
        ad_date = self.to_ad()
        # Python's weekday: Monday=0, Sunday=6
        # We want: Sunday=0, Saturday=6
        return (ad_date.weekday() + 1) % 7
    
    def isoweekday(self) -> int:
        """
        Return the ISO day of the week.
        
        Returns:
            ISO day of week (1=Monday, 7=Sunday).
        """
        return self.to_ad().isoweekday()
    
    def strftime(self, fmt: str, style: str = 'formal') -> str:
        """
        Format the date as a string using format codes.
        
        Supported format codes:
            Standard (English): %Y, %y, %m, %d, %B, %b, %A, %a
            Nepali (Devanagari): %K, %k, %n, %D, %N, %G, %g
        
        Args:
            fmt: Format string.
            style: Month name style ('formal' or 'sanskrit') for %N.
        
        Returns:
            Formatted date string.
        
        Examples:
            >>> date = BSDate(2080, 10, 24)
            >>> date.strftime("%Y-%m-%d")
            '2080-10-24'
            >>> date.strftime("%K-%n-%D")
            '२०८०-१०-२४'
            >>> date.strftime("%D %N, %K")
            '२४ माघ, २०८०'
        """
        return format_bs_datetime(self, fmt, style=style)
    
    def isoformat(self) -> str:
        """
        Return the date in ISO format (YYYY-MM-DD).
        
        Returns:
            ISO formatted date string.
        """
        return f"{self._year:04d}-{self._month:02d}-{self._day:02d}"
    
    def replace(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None
    ) -> BSDate:
        """
        Return a date with the same value, except for specified fields.
        
        Args:
            year: New year value (optional).
            month: New month value (optional).
            day: New day value (optional).
        
        Returns:
            New BSDate with replaced values.
        """
        return BSDate(
            year if year is not None else self._year,
            month if month is not None else self._month,
            day if day is not None else self._day
        )
    
    def __add__(self, days: Union[int, timedelta]) -> BSDate:
        """Add days to the date using fast ordinal arithmetic.
        
        Args:
            days: Number of days to add (int or timedelta).
        
        Returns:
            New BSDate.
        
        Examples:
            >>> date = BSDate(2080, 10, 24)
            >>> date + 7
            BSDate(2080, 11, 1)
            >>> date + timedelta(days=30)
            BSDate(2080, 11, 24)
        """
        if isinstance(days, timedelta):
            days = days.days
        elif not isinstance(days, int):
            return NotImplemented
        
        # Fast ordinal-based arithmetic
        new_ordinal = self.toordinal() + days
        return BSDate.fromordinal(new_ordinal)
    
    def __radd__(self, days: Union[int, timedelta]) -> BSDate:
        """Support days + date."""
        return self.__add__(days)
    
    def __sub__(self, other: Union[int, timedelta, BSDate]) -> Union[BSDate, timedelta]:
        """Subtract days or another BSDate using fast ordinal arithmetic.
        
        Args:
            other: Days to subtract (int/timedelta) or BSDate.
        
        Returns:
            New BSDate if subtracting days, or timedelta (day difference) if BSDate.
        
        Examples:
            >>> date1 = BSDate(2080, 10, 24)
            >>> date1 - 7
            BSDate(2080, 10, 17)
            >>> date2 = BSDate(2080, 10, 17)
            >>> date1 - date2
            datetime.timedelta(days=7)
        """
        if isinstance(other, BSDate):
            # Return timedelta for compatibility with datetime API
            days_diff = self.toordinal() - other.toordinal()
            return timedelta(days=days_diff)
        
        if isinstance(other, timedelta):
            return self.__add__(-other.days)
        
        if isinstance(other, int):
            return self.__add__(-other)
        
        return NotImplemented
    
    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if isinstance(other, BSDate):
            return (
                self._year == other._year and
                self._month == other._month and
                self._day == other._day
            )
        return NotImplemented
    
    def __ne__(self, other: object) -> bool:
        """Check inequality."""
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    
    def __lt__(self, other: BSDate) -> bool:
        """Check if less than using fast ordinal comparison."""
        if not isinstance(other, BSDate):
            return NotImplemented
        return self.toordinal() < other.toordinal()
    
    def __le__(self, other: BSDate) -> bool:
        """Check if less than or equal using fast ordinal comparison."""
        if not isinstance(other, BSDate):
            return NotImplemented
        return self.toordinal() <= other.toordinal()
    
    def __gt__(self, other: BSDate) -> bool:
        """Check if greater than using fast ordinal comparison."""
        if not isinstance(other, BSDate):
            return NotImplemented
        return self.toordinal() > other.toordinal()
    
    def __ge__(self, other: BSDate) -> bool:
        """Check if greater than or equal using fast ordinal comparison."""
        if not isinstance(other, BSDate):
            return NotImplemented
        return self.toordinal() >= other.toordinal()
    
    def __hash__(self) -> int:
        """Return hash value."""
        return hash((self._year, self._month, self._day))
    
    def __repr__(self) -> str:
        """Return repr string."""
        return f"BSDate({self._year}, {self._month}, {self._day})"
    
    def __str__(self) -> str:
        """Return string representation."""
        return self.isoformat()
