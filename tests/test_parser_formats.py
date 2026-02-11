"""Tests for enhanced parser with format codes."""

import pytest
from nepalify.dates import BSDateTime, BSDate
from nepalify.dates.parser import parse_bs_datetime
from nepalify.dates.timezone import NepaliTimeZone

class TestParserFormats:
    """Test parse_bs_datetime and BSDateTime.strptime with format codes."""
    
    def test_standard_iso(self):
        """Test %Y-%m-%d %H:%M:%S"""
        dt = BSDateTime.strptime("2080-10-24 14:30:00", "%Y-%m-%d %H:%M:%S")
        assert dt.year == 2080
        assert dt.month == 10
        assert dt.day == 24
        assert dt.hour == 14
        assert dt.minute == 30
        assert dt.second == 0
    
    def test_nepali_digits(self):
        """Test %K-%n-%D (Nepali digits)"""
        # २०८०-१०-२४
        dt = BSDateTime.strptime("२०८०-१०-२४", "%K-%n-%D")
        assert dt.year == 2080
        assert dt.month == 10
        assert dt.day == 24
    
    def test_mixed_format(self):
        """Test mixed codes"""
        # 2080/10/24
        dt = BSDateTime.strptime("2080/10/24", "%Y/%m/%d")
        assert dt.year == 2080
    
    def test_time_only_defaults(self):
        """Test parsing time only (should error if date missing? or default?)"""
        # Current implementation passes 'pass' if date missing -> defaults to 0 -> invalid date error likely
        with pytest.raises(Exception): # ValueError or similar
             BSDateTime.strptime("14:30", "%H:%M")

    def test_partial_year_k(self):
        """Test %k (short Nepali year)"""
        # ८०-१०-२४ (80-10-24)
        dt = BSDateTime.strptime("८०-१०-२४", "%k-%n-%D")
        assert dt.year == 2080
        assert dt.month == 10
    
    def test_am_pm(self):
        """Test %p (AM/PM)"""
        dt = BSDateTime.strptime("2080-10-24 02:30 PM", "%Y-%m-%d %I:%M %p")
        assert dt.hour == 14
        assert dt.minute == 30
        
        dt = BSDateTime.strptime("2080-10-24 02:30 AM", "%Y-%m-%d %I:%M %p")
        assert dt.hour == 2
