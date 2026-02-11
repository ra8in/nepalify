"""
Bikram Sambat Calendar Generation.

Generate formatted monthly and yearly calendars for the BS calendar system.

Example:
    >>> from nepalify.dates import BSDate
    >>> from nepalify.dates.calendar import month_calendar
    >>> 
    >>> # Print calendar for Baisakh 2078
    >>> print(month_calendar(2078, 1))
    Baishakh 2078
    Sun Mon Tue Wed Thu Fri Sat
      1   2   3   4   5   6   7
      8   9  10  11  12  13  14
     15  16  17  18  19  20  21
     22  23  24  25  26  27  28
     29  30  31
    >>> 
    >>> # Print in Nepali
    >>> print(month_calendar(2078, 1, nepali=True))
    बैशाख २०७८
    आइत सोम मंगल बुध बिही शुक्र शनि
      १   २   ३   ४   ५   ६   ७
      ८   ९  १०  ११  १२  १३  १४
     १५  १६  १७  १८  १९  २०  २१
     २२  २३  २४  २५  २६  २७  २८
     २९  ३०  ३१
"""

from typing import List, Optional

from nepalify.dates.converter import get_days_in_month, is_valid_bs_date
from nepalify.dates.bs_date import BSDate
from nepalify.text.constants import (
    MONTHS_NEPALI,
    MONTHS_ENGLISH,
    DAYS_NEPALI_SHORT,
    DAYS_ENGLISH_SHORT,
)
from nepalify.numbers.devanagari import to_devanagari


def month_calendar(
    year: int,
    month: int,
    nepali: bool = False,
    first_weekday: int = 0,
    highlight_today: bool = False
) -> str:
    """
    Generate a formatted calendar for a BS month.
    
    Args:
        year: BS year (1901-2199).
        month: BS month (1-12).
        nepali: Use Nepali numerals and names if True.
        first_weekday: First day of week (0=Sunday, default).
        highlight_today: Mark today's date with brackets.
    
    Returns:
        str: Formatted calendar string.
    
    Raises:
        ValueError: If year or month is invalid.
    
    Examples:
        >>> print(month_calendar(2078, 1))
        Baishakh 2078
        Sun Mon Tue Wed Thu Fri Sat
          1   2   3   4   5   6   7
          8   9  10  11  12  13  14
         15  16  17  18  19  20  21
         22  23  24  25  26  27  28
         29  30  31
        
        >>> print(month_calendar(2080, 10, nepali=True))
        माघ २०८०
        आइत सोम मंगल बुध बिही शुक्र शनि
        ...
    """
    # Validate inputs
    if not is_valid_bs_date(year, month, 1):
        raise ValueError(f"Invalid BS year/month: {year}/{month}")
    
    # Get month info
    days_in_month = get_days_in_month(year, month)
    first_day = BSDate(year, month, 1)
    first_weekday_of_month = first_day.weekday()
    
    # Get today for highlighting
    today = None
    if highlight_today:
        today = BSDate.today()
    
    # Build header
    if nepali:
        month_name = MONTHS_NEPALI[month - 1]
        year_str = to_devanagari(str(year))
        header = f"{month_name} {year_str}"
        # Rotate day names based on first_weekday
        day_names = DAYS_NEPALI_SHORT[first_weekday:] + DAYS_NEPALI_SHORT[:first_weekday]
    else:
        month_name = MONTHS_ENGLISH[month - 1]
        header = f"{month_name} {year}"
        day_names = DAYS_ENGLISH_SHORT[first_weekday:] + DAYS_ENGLISH_SHORT[:first_weekday]
    
    # Calculate header width
    day_width = 4 if nepali else 4
    week_width = 7 * day_width - 1
    
    lines = []
    
    # Center the month/year header
    lines.append(header.center(week_width))
    
    # Day names header
    if nepali:
        # Nepali day names may have varying widths
        day_header = " ".join(d.ljust(3) for d in day_names)
    else:
        day_header = " ".join(d.ljust(3) for d in day_names)
    lines.append(day_header)
    
    # Calculate starting position
    start_pos = (first_weekday_of_month - first_weekday) % 7
    
    # Build week rows
    week = ['   '] * start_pos  # Leading empty cells
    
    for day in range(1, days_in_month + 1):
        # Check if this is today
        is_today = (highlight_today and today and 
                    today.year == year and today.month == month and today.day == day)
        
        if nepali:
            day_str = to_devanagari(str(day))
            if is_today:
                cell = f"[{day_str}]".rjust(4)
            else:
                cell = day_str.rjust(3)
        else:
            if is_today:
                cell = f"[{day}]".rjust(4)
            else:
                cell = str(day).rjust(3)
        
        week.append(cell)
        
        if len(week) == 7:
            lines.append(" ".join(week))
            week = []
    
    # Add remaining days in last week
    if week:
        lines.append(" ".join(week))
    
    return "\n".join(lines)


def year_calendar(
    year: int,
    nepali: bool = False,
    columns: int = 3,
    highlight_today: bool = False
) -> str:
    """
    Generate calendar for an entire BS year.
    
    Args:
        year: BS year (1901-2199).
        nepali: Use Nepali numerals and names if True.
        columns: Number of months per row (default 3).
        highlight_today: Mark today's date.
    
    Returns:
        str: Formatted year calendar.
    
    Examples:
        >>> print(year_calendar(2080, columns=4))
        # Shows all 12 months in 3 rows of 4 columns
    """
    from nepalify.dates.converter import BS_MIN_YEAR, BS_MAX_YEAR
    
    if not BS_MIN_YEAR <= year <= BS_MAX_YEAR:
        raise ValueError(f"Year must be {BS_MIN_YEAR}-{BS_MAX_YEAR}, got {year}")
    
    # Generate each month's calendar
    month_calendars = []
    for month in range(1, 13):
        cal = month_calendar(year, month, nepali, highlight_today=highlight_today)
        month_calendars.append(cal.split('\n'))
    
    # Combine months into rows
    result_lines = []
    year_header = to_devanagari(str(year)) if nepali else str(year)
    result_lines.append(f"{'=' * 20} {year_header} {'=' * 20}")
    result_lines.append("")
    
    for row_start in range(0, 12, columns):
        row_months = month_calendars[row_start:row_start + columns]
        
        # Get max lines in this row
        max_lines = max(len(m) for m in row_months)
        
        # Pad shorter months
        for m in row_months:
            while len(m) < max_lines:
                m.append(" " * len(m[0]) if m else "")
        
        # Combine line by line
        separator = "   "
        for i in range(max_lines):
            row_line = separator.join(
                m[i].ljust(25) if i < len(m) else " " * 25 
                for m in row_months
            )
            result_lines.append(row_line)
        
        result_lines.append("")  # Blank line between rows
    
    return "\n".join(result_lines)


def _add_calendar_method_to_bsdate():
    """
    Add calendar() method to BSDate class.
    
    This is called at module import to extend BSDate functionality.
    """
    def calendar(self, nepali: bool = False, highlight_today: bool = True) -> str:
        """
        Generate a formatted calendar for this date's month.
        
        Args:
            nepali: Use Nepali numerals and names.
            highlight_today: Mark today's date.
        
        Returns:
            str: Formatted calendar string.
        
        Examples:
            >>> date = BSDate(2078, 1, 15)
            >>> print(date.calendar())
            Baishakh 2078
            Sun Mon Tue Wed Thu Fri Sat
            ...
        """
        return month_calendar(self.year, self.month, nepali, highlight_today=highlight_today)
    
    BSDate.calendar = calendar


# Add the calendar method to BSDate when this module is imported
_add_calendar_method_to_bsdate()


__all__ = [
    "month_calendar",
    "year_calendar",
]
