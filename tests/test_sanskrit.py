"""Tests for Sanskrit month name support."""

from nepalify import BSDate, BSDateTime, get_month_name, parse
from nepalify.text import MONTHS_NEPALI, MONTHS_NEPALI_SANSKRIT


class TestSanskritMonthNames:
    """Test Sanskrit month name support."""
    
    def test_formal_month_name_default(self):
        """Test default returns formal name."""
        assert get_month_name(2) == "जेठ"
        assert get_month_name(2, style='formal') == "जेठ"
    
    def test_sanskrit_month_name(self):
        """Test style='sanskrit' returns Sanskrit name."""
        assert get_month_name(2, style='sanskrit') == "ज्येष्ठ"
    
    def test_all_sanskrit_months(self):
        """Test all 12 Sanskrit month names."""
        expected = [
            "वैशाख", "ज्येष्ठ", "आषाढ", "श्रावण",
            "भाद्र", "आश्विन", "कार्तिक", "मार्ग",
            "पौष", "माघ", "फाल्गुन", "चैत्र"
        ]
        for i, name in enumerate(expected, 1):
            assert get_month_name(i, style='sanskrit') == name
    
    def test_constants_length(self):
        """Test that constants have correct length."""
        assert len(MONTHS_NEPALI_SANSKRIT) == 12
    
    def test_bs_date_strftime_sanskrit(self):
        """Test BSDate.strftime with Sanskrit style."""
        date = BSDate(2080, 2, 15)
        # Old: date.strftime("%B %d, %Y", nepali=True, style='sanskrit')
        # New: Use %N (Nepali month) which respects style
        result = date.strftime("%N %D, %K", style='sanskrit')
        assert "ज्येष्ठ" in result
        
    def test_bs_datetime_strftime_sanskrit(self):
        """Test BSDateTime.strftime with Sanskrit style."""
        dt = BSDateTime(2080, 2, 15, 14, 30)
        result = dt.strftime("%N %D, %K", style='sanskrit')
        assert "ज्येष्ठ" in result
    
    def test_parse_formal_nepali(self):
        """Test parser accepts formal Nepali month names."""
        result = parse("जेठ 15, 2080")
        assert result.month == 2
    
    def test_parse_sanskrit_nepali(self):
        """Test parser accepts Sanskrit Nepali month names."""
        result = parse("ज्येष्ठ 15, 2080")
        assert result.month == 2
    
    def test_parse_both_same_result(self):
        """Test parser gives same result for formal and Sanskrit."""
        formal = parse("जेठ 15, 2080")
        sanskrit = parse("ज्येष्ठ 15, 2080")
        assert formal == sanskrit
    
    def test_parse_english(self):
        """Test parser accepts English month names."""
        result = parse("Jestha 15, 2080")
        assert result == BSDate(2080, 2, 15)
        
        result2 = parse("Asar 10, 2080")
        assert result2 == BSDate(2080, 3, 10)
    
    def test_key_differences(self):
        """Test months with notable differences between formal and Sanskrit."""
        differences = {
            2: ("जेठ", "ज्येष्ठ"),      # Jestha
            3: ("असार", "आषाढ"),       # Ashadh
            4: ("साउन", "श्रावण"),     # Shrawan
            5: ("भदौ", "भाद्र"),       # Bhadra
            6: ("असोज", "आश्विन"),     # Ashwin
            8: ("मंसिर", "मार्ग"),     # Mangsir
            11: ("फागुन", "फाल्गुन"),  # Falgun
            12: ("चैत", "चैत्र"),       # Chaitra
        }
        
        for month, (formal, sanskrit) in differences.items():
            assert get_month_name(month, style='formal') == formal
            assert get_month_name(month, style='sanskrit') == sanskrit
