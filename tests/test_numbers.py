"""Tests for the numbers module."""

import pytest
from nepalify.numbers import to_devanagari, from_devanagari, format_number, to_words_nepali


class TestDevanagariConversion:
    """Tests for Devanagari digit conversion."""
    
    def test_to_devanagari_string(self):
        assert to_devanagari("0123456789") == "०१२३४५६७८९"
    
    def test_to_devanagari_integer(self):
        assert to_devanagari(2024) == "२०२४"
    
    def test_to_devanagari_float(self):
        assert to_devanagari(3.14) == "३.१४"
    
    def test_to_devanagari_mixed(self):
        assert to_devanagari("Price: Rs. 1,500") == "Price: Rs. १,५००"
    
    def test_to_devanagari_empty(self):
        assert to_devanagari("") == ""
    
    def test_from_devanagari_string(self):
        assert from_devanagari("०१२३४५६७८९") == "0123456789"
    
    def test_from_devanagari_mixed(self):
        assert from_devanagari("१२,३४५.६७") == "12,345.67"
    
    def test_roundtrip(self):
        original = "12345"
        assert from_devanagari(to_devanagari(original)) == original


class TestFormatNumber:
    """Tests for Indian/Nepali number formatting."""
    
    def test_small_number(self):
        assert format_number(123) == "123"
    
    def test_four_digits(self):
        assert format_number(1234) == "1,234"
    
    def test_five_digits(self):
        assert format_number(12345) == "12,345"
    
    def test_six_digits(self):
        """One lakh."""
        assert format_number(100000) == "1,00,000"
    
    def test_seven_digits(self):
        """Ten lakhs."""
        assert format_number(1234567) == "12,34,567"
    
    def test_eight_digits(self):
        """One crore."""
        assert format_number(10000000) == "1,00,00,000"
    
    def test_ten_digits(self):
        assert format_number(1234567890) == "1,23,45,67,890"
    
    def test_negative_number(self):
        assert format_number(-1234567) == "-12,34,567"
    
    def test_float_number(self):
        assert format_number(1234567.89) == "12,34,567.89"
    
    def test_string_input(self):
        assert format_number("1234567") == "12,34,567"
    
    def test_western_format_input(self):
        """Should handle western format and convert to Indian."""
        assert format_number("2,553,871") == "25,53,871"
    
    def test_with_devanagari(self):
        assert format_number(1234567, use_devanagari=True) == "१२,३४,५६७"


class TestToWordsNepali:
    """Tests for number to Nepali words conversion."""
    
    def test_zero(self):
        assert to_words_nepali(0) == "शुन्य"
    
    def test_single_digit(self):
        assert to_words_nepali(5) == "पाँच"
    
    def test_teens(self):
        assert to_words_nepali(15) == "पन्ध्र"
    
    def test_hundred(self):
        assert to_words_nepali(100) == "एक सय"
    
    def test_thousand(self):
        assert to_words_nepali(1000) == "एक हजार"
    
    def test_lakh(self):
        assert to_words_nepali(100000) == "एक लाख"
    
    def test_crore(self):
        assert to_words_nepali(10000000) == "एक करोड"

    def test_arab(self):
        assert to_words_nepali(1000000000) == "एक अर्ब"

    def test_kharab(self):
        assert to_words_nepali(100000000000) == "एक खर्ब"
    
    def test_negative_raises(self):
        with pytest.raises(ValueError):
            to_words_nepali(-1)
