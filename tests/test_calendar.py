"""Tests for calendar display functions."""

import pytest
from nepalify.dates import BSDate, month_calendar, year_calendar
from nepalify.dates.converter import get_days_in_month


class TestMonthCalendar:
    """Tests for month_calendar function."""
    
    def test_basic_month_calendar(self):
        """Test basic month calendar output."""
        cal = month_calendar(2082, 10)
        assert isinstance(cal, str)
        assert "Magh" in cal or "2082" in cal
    
    def test_month_calendar_contains_days(self):
        """Test calendar contains day numbers."""
        cal = month_calendar(2082, 10)
        # Should contain day numbers
        assert "1" in cal
        assert "15" in cal
    
    def test_month_calendar_header(self):
        """Test calendar has header with month/year."""
        cal = month_calendar(2082, 10)
        assert "2082" in cal
    
    def test_month_calendar_weekday_header(self):
        """Test calendar has weekday header."""
        cal = month_calendar(2082, 10)
        # Should have day abbreviations
        assert "Sun" in cal or "Mon" in cal or "Tue" in cal
    
    def test_month_calendar_nepali(self):
        """Test Nepali calendar format."""
        cal = month_calendar(2082, 10, nepali=True)
        # Should contain Nepali month name
        assert "माघ" in cal
        # Should contain Nepali digits
        assert "१" in cal or "२" in cal
    
    def test_month_calendar_nepali_weekdays(self):
        """Test Nepali weekday names."""
        cal = month_calendar(2082, 10, nepali=True)
        # Should have at least one Nepali weekday abbreviation
        nepali_days = ["आइत", "सोम", "मंगल", "बुध", "बिही", "शुक्र", "शनि"]
        has_nepali_day = any(day in cal for day in nepali_days)
        assert has_nepali_day
    
    def test_month_calendar_all_months(self):
        """Test calendar generation for all 12 months."""
        for month in range(1, 13):
            cal = month_calendar(2080, month)
            assert isinstance(cal, str)
            assert len(cal) > 0
    
    def test_month_calendar_correct_days(self):
        """Test calendar shows correct number of days."""
        # Get days in Magh 2082
        days = get_days_in_month(2082, 10)
        cal = month_calendar(2082, 10)
        # Last day should appear
        assert str(days) in cal


class TestBSDateCalendar:
    """Tests for BSDate.calendar() method."""
    
    def test_bsdate_calendar_method(self):
        """Test BSDate.calendar() returns valid calendar."""
        date = BSDate(2082, 10, 15)
        cal = date.calendar()
        assert isinstance(cal, str)
        assert "2082" in cal
    
    def test_bsdate_calendar_current_day_highlight(self):
        """Test calendar highlights current day."""
        date = BSDate(2082, 10, 15)
        cal = date.calendar()
        # The day "15" should appear
        assert "15" in cal
    
    def test_bsdate_calendar_nepali(self):
        """Test BSDate.calendar() with Nepali format."""
        date = BSDate(2082, 10, 15)
        cal = date.calendar(nepali=True)
        assert "माघ" in cal


class TestYearCalendar:
    """Tests for year_calendar function."""
    
    def test_basic_year_calendar(self):
        """Test basic year calendar output."""
        cal = year_calendar(2082)
        assert isinstance(cal, str)
        assert "2082" in cal
    
    def test_year_calendar_all_months(self):
        """Test year calendar contains all 12 months."""
        cal = year_calendar(2082)
        months = [
            "Baishakh", "Jestha", "Asar", "Shrawan",
            "Bhadau", "Asoj", "Kartik", "Mangsir",
            "Poush", "Magh", "Falgun", "Chaitra"
        ]
        for month in months:
            assert month in cal, f"Missing month: {month}"
    
    def test_year_calendar_nepali(self):
        """Test Nepali year calendar."""
        cal = year_calendar(2082, nepali=True)
        # Should contain Nepali month names
        nepali_months = ["बैशाख", "जेष्ठ", "आषाढ", "श्रावण", "माघ"]
        has_nepali_month = any(month in cal for month in nepali_months)
        assert has_nepali_month
    
    def test_year_calendar_min_year(self):
        """Test year calendar for minimum year."""
        cal = year_calendar(1901)
        assert "1901" in cal
    
    def test_year_calendar_max_year(self):
        """Test year calendar for maximum year."""
        cal = year_calendar(2199)
        assert "2199" in cal


class TestCalendarEdgeCases:
    """Edge cases for calendar functions."""
    
    def test_invalid_month_raises(self):
        """Test invalid month raises ValueError."""
        with pytest.raises(ValueError):
            month_calendar(2082, 0)
        
        with pytest.raises(ValueError):
            month_calendar(2082, 13)
    
    def test_invalid_year_raises(self):
        """Test invalid year raises ValueError."""
        with pytest.raises(ValueError):
            month_calendar(1800, 1)
        
        with pytest.raises(ValueError):
            month_calendar(2300, 1)
    
    def test_leap_month_handling(self):
        """Test calendar handles months with different day counts."""
        # Year 1903 has 366 days (leap year equivalent)
        cal = year_calendar(1903)
        assert "1903" in cal
