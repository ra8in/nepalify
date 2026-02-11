"""Tests for the text module."""

import pytest
from nepalify.text import (
    convert_to_nepali,
    get_month_name,
    get_day_name,
    MONTHS_NEPALI,
    MONTHS_ENGLISH,
    DAYS_NEPALI,
    DAYS_ENGLISH,
)


class TestGetMonthName:
    """Tests for get_month_name function."""
    
    def test_nepali_month(self):
        assert get_month_name(1) == "बैशाख"
        assert get_month_name(10) == "माघ"
    
    def test_english_month(self):
        assert get_month_name(1, nepali=False) == "Baishakh"
        assert get_month_name(10, nepali=False) == "Magh"
    
    def test_abbreviated(self):
        assert get_month_name(1, nepali=False, abbreviated=True) == "Bai"
    
    def test_invalid_month(self):
        with pytest.raises(ValueError):
            get_month_name(0)
        with pytest.raises(ValueError):
            get_month_name(13)


class TestGetDayName:
    """Tests for get_day_name function."""
    
    def test_nepali_day(self):
        assert get_day_name(0) == "आइतबार"  # Sunday
        assert get_day_name(5) == "शुक्रबार"  # Friday
    
    def test_english_day(self):
        assert get_day_name(0, nepali=False) == "Sunday"
        assert get_day_name(5, nepali=False) == "Friday"
    
    def test_abbreviated(self):
        assert get_day_name(0, nepali=False, abbreviated=True) == "Sun"
        assert get_day_name(0, nepali=True, abbreviated=True) == "आइत"
    
    def test_invalid_day(self):
        with pytest.raises(ValueError):
            get_day_name(-1)
        with pytest.raises(ValueError):
            get_day_name(7)


class TestConvertToNepali:
    """Tests for convert_to_nepali function."""
    
    def test_convert_digits(self):
        assert convert_to_nepali("2024") == "२०२४"
    
    def test_convert_number(self):
        assert convert_to_nepali(123) == "१२३"
    
    def test_convert_day(self):
        result = convert_to_nepali("Sunday")
        assert "आइतबार" in result
    
    def test_convert_day_lowercase(self):
        result = convert_to_nepali("sunday")
        assert "आइतबार" in result
    
    def test_convert_bs_month(self):
        result = convert_to_nepali("Magh")
        assert "माघ" in result
    
    def test_convert_gregorian_month(self):
        result = convert_to_nepali("January")
        assert "जनवरी" in result
    
    def test_convert_mixed(self):
        result = convert_to_nepali("15 Magh 2080")
        assert "१५" in result
        assert "माघ" in result
        assert "२०८०" in result
    
    def test_convert_full_date(self):
        result = convert_to_nepali("Sunday, 15 January 2024")
        assert "आइतबार" in result
        assert "जनवरी" in result
        assert "१५" in result
        assert "२०२४" in result
    
    def test_selective_conversion(self):
        # Only convert digits
        result = convert_to_nepali(
            "Sunday 15",
            convert_days=False,
            convert_bs_months=False,
            convert_gregorian_months=False
        )
        assert "Sunday" in result
        assert "१५" in result


class TestConstants:
    """Tests for constant arrays."""
    
    def test_months_nepali_length(self):
        assert len(MONTHS_NEPALI) == 12
    
    def test_months_english_length(self):
        assert len(MONTHS_ENGLISH) == 12
    
    def test_days_nepali_length(self):
        assert len(DAYS_NEPALI) == 7
    
    def test_days_english_length(self):
        assert len(DAYS_ENGLISH) == 7
    
    def test_month_names_valid(self):
        assert MONTHS_NEPALI[0] == "बैशाख"
        assert MONTHS_ENGLISH[0] == "Baishakh"
    
    def test_day_names_valid(self):
        assert DAYS_NEPALI[0] == "आइतबार"
        assert DAYS_ENGLISH[0] == "Sunday"
