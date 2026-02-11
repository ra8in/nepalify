"""Tests for date/datetime parsing module."""

import pytest
from nepalify.dates import BSDate, BSDateTime
from nepalify.dates import parse, parse_date, parse_datetime


class TestParse:
    """Tests for the auto-detect parse function."""
    
    def test_iso_date(self):
        """Test parsing ISO format date."""
        result = parse("2079-02-15")
        assert isinstance(result, BSDate)
        assert result.year == 2079
        assert result.month == 2
        assert result.day == 15
    
    def test_iso_date_slash(self):
        """Test parsing ISO format with slashes."""
        result = parse("2079/02/15")
        assert isinstance(result, BSDate)
        assert result.year == 2079
        assert result.month == 2
        assert result.day == 15
    
    def test_nepali_digits(self):
        """Test parsing Nepali (Devanagari) digits."""
        result = parse("२०७८-०१-१८")
        assert isinstance(result, BSDate)
        assert result.year == 2078
        assert result.month == 1
        assert result.day == 18
    
    def test_named_month_english(self):
        """Test parsing named month format (English)."""
        result = parse("Jestha 15, 2079")
        assert isinstance(result, BSDate)
        assert result.year == 2079
        assert result.month == 2  # Jestha is month 2
        assert result.day == 15
    
    def test_named_month_day_first(self):
        """Test parsing day-first named month format."""
        result = parse("15 Magh 2080")
        assert isinstance(result, BSDate)
        assert result.year == 2080
        assert result.month == 10  # Magh is month 10
        assert result.day == 15
    
    def test_named_month_short(self):
        """Test parsing abbreviated month name."""
        result = parse("Jes 15, 2079")
        assert isinstance(result, BSDate)
        assert result.month == 2  # Jestha
    
    def test_all_month_names(self):
        """Test parsing all English month names."""
        months = [
            ("Baishakh", 1), ("Jestha", 2), ("Asar", 3), ("Shrawan", 4),
            ("Bhadau", 5), ("Asoj", 6), ("Kartik", 7), ("Mangsir", 8),
            ("Poush", 9), ("Magh", 10), ("Falgun", 11), ("Chaitra", 12)
        ]
        for month_name, month_num in months:
            result = parse(f"{month_name} 1, 2080")
            assert result.month == month_num, f"Failed for {month_name}"
    
    def test_datetime_with_time(self):
        """Test parsing datetime with time."""
        result = parse("2079-02-15 15:23")
        assert isinstance(result, BSDateTime)
        assert result.year == 2079
        assert result.hour == 15
        assert result.minute == 23
    
    def test_datetime_with_seconds(self):
        """Test parsing datetime with seconds."""
        result = parse("2079-02-15 15:23:45")
        assert isinstance(result, BSDateTime)
        assert result.second == 45
    
    def test_datetime_am_pm(self):
        """Test parsing datetime with AM/PM."""
        result = parse("2079-02-15 5:23 AM")
        assert isinstance(result, BSDateTime)
        assert result.hour == 5
        
        result_pm = parse("2079-02-15 5:23 PM")
        assert result_pm.hour == 17  # 5 PM = 17:00
    
    def test_datetime_noon(self):
        """Test parsing noon with AM/PM."""
        result = parse("2079-02-15 12:00 PM")
        assert result.hour == 12
    
    def test_datetime_midnight(self):
        """Test parsing midnight with AM/PM."""
        result = parse("2079-02-15 12:00 AM")
        assert result.hour == 0
    
    def test_invalid_format_raises(self):
        """Test that invalid format raises ValueError."""
        with pytest.raises(ValueError):
            parse("invalid date format")
    
    def test_invalid_date_raises(self):
        """Test that invalid date values raise ValueError."""
        with pytest.raises(ValueError):
            parse("2080-13-01")  # Invalid month
    
    def test_whitespace_handling(self):
        """Test that leading/trailing whitespace is handled."""
        result = parse("  2079-02-15  ")
        assert result.year == 2079


class TestParseDate:
    """Tests for parse_date function."""
    
    def test_date_from_date_string(self):
        """Test parse_date with date string."""
        result = parse_date("2079-02-15")
        assert isinstance(result, BSDate)
        assert result.year == 2079
    
    def test_date_from_datetime_string(self):
        """Test parse_date extracts date from datetime."""
        result = parse_date("2079-02-15 15:23")
        assert isinstance(result, BSDate)
        assert result.year == 2079
        assert result.month == 2
        assert result.day == 15
        # Should not have hour attribute
        assert not hasattr(result, 'hour')


class TestParseDatetime:
    """Tests for parse_datetime function."""
    
    def test_datetime_from_datetime_string(self):
        """Test parse_datetime with datetime string."""
        result = parse_datetime("2079-02-15 15:23")
        assert isinstance(result, BSDateTime)
        assert result.hour == 15
    
    def test_datetime_from_date_string(self):
        """Test parse_datetime adds midnight time."""
        result = parse_datetime("2079-02-15")
        assert isinstance(result, BSDateTime)
        assert result.year == 2079
        assert result.hour == 0
        assert result.minute == 0
        assert result.second == 0


class TestParseEdgeCases:
    """Edge cases for parsing."""
    
    def test_min_year(self):
        """Test parsing minimum year."""
        result = parse("1901-01-01")
        assert result.year == 1901
    
    def test_max_year(self):
        """Test parsing maximum year."""
        result = parse("2199-01-01")
        assert result.year == 2199
    
    def test_single_digit_day_month(self):
        """Test parsing single digit day/month."""
        result = parse("2079-2-5")
        assert result.month == 2
        assert result.day == 5
    
    def test_mixed_separators(self):
        """Test parsing dates with mixed separators fails gracefully."""
        # Standard separators should work
        result = parse("2079-02-15")
        assert result.year == 2079
        
        result2 = parse("2079/02/15")
        assert result2.year == 2079
