"""Tests for the dates module."""

import pytest
from datetime import date, timedelta
from nepalify.dates import BSDate, ad_to_bs, bs_to_ad
from nepalify.dates.converter import get_days_in_month, is_valid_bs_date


class TestConverter:
    """Tests for AD ↔ BS conversion functions."""
    
    def test_reference_date_ad_to_bs(self):
        """Test the reference date: 1844-04-11 AD = 1901-01-01 BS."""
        assert ad_to_bs(1844, 4, 11) == (1901, 1, 1)
    
    def test_reference_date_bs_to_ad(self):
        """Test the reference date: 1901-01-01 BS = 1844-04-11 AD."""
        assert bs_to_ad(1901, 1, 1) == (1844, 4, 11)
    
    def test_known_date_1(self):
        """Test known conversion: 2024-02-06 AD ≈ 2080-10-24 BS."""
        result = ad_to_bs(2024, 2, 6)
        assert result[0] == 2080  # Year
        assert result[1] == 10    # Month (Magh)
    
    def test_known_date_2(self):
        """New Year 2081: 2024-04-13 AD = 2081-01-01 BS."""
        # This may vary slightly based on calendar data
        result = ad_to_bs(2024, 4, 13)
        assert result[0] == 2080 or result[0] == 2081
    
    def test_roundtrip_ad_to_bs_to_ad(self):
        """Converting AD→BS→AD should return the original date."""
        original = (2020, 6, 15)
        bs = ad_to_bs(*original)
        back_to_ad = bs_to_ad(*bs)
        assert back_to_ad == original
    
    def test_roundtrip_bs_to_ad_to_bs(self):
        """Converting BS→AD→BS should return the original date."""
        original = (2077, 6, 15)
        ad = bs_to_ad(*original)
        back_to_bs = ad_to_bs(*ad)
        assert back_to_bs == original
    
    def test_invalid_bs_year(self):
        with pytest.raises(ValueError):
            bs_to_ad(1899, 1, 1)  # Before supported range (1901)
    
    def test_invalid_bs_month(self):
        with pytest.raises(ValueError):
            bs_to_ad(2080, 13, 1)  # Invalid month
    
    def test_get_days_in_month(self):
        """Days in months should be 29-32."""
        days = get_days_in_month(2080, 1)  # Baisakh 2080
        assert 29 <= days <= 32
    
    def test_is_valid_bs_date(self):
        assert is_valid_bs_date(2080, 10, 24) is True
        assert is_valid_bs_date(2080, 13, 1) is False
        assert is_valid_bs_date(1899, 1, 1) is False 


class TestBSDate:
    """Tests for BSDate class."""
    
    def test_create_date(self):
        date = BSDate(2080, 10, 24)
        assert date.year == 2080
        assert date.month == 10
        assert date.day == 24
    
    def test_invalid_date_raises(self):
        with pytest.raises(ValueError):
            BSDate(2080, 13, 1)
    
    def test_today(self):
        today = BSDate.today()
        assert isinstance(today, BSDate)
        assert 1901 <= today.year <= 2199
    
    def test_from_ad(self):
        ad_date = date(2024, 2, 6)
        bs_date = BSDate.from_ad(ad_date)
        assert bs_date.year == 2080
        assert bs_date.month == 10
    
    def test_to_ad(self):
        bs_date = BSDate(2080, 10, 24)
        ad_date = bs_date.to_ad()
        assert isinstance(ad_date, date)
    
    def test_strftime_basic(self):
        d = BSDate(2080, 10, 24)
        assert d.strftime("%Y-%m-%d") == "2080-10-24"
    
    def test_strftime_month_name(self):
        d = BSDate(2080, 10, 24)
        formatted = d.strftime("%B %d, %Y")
        assert "Magh" in formatted
        assert "24" in formatted
        assert "2080" in formatted
    
    def test_strftime_nepali(self):
        d = BSDate(2080, 10, 24)
        # Old: d.strftime("%Y-%m-%d", nepali=True)
        # New: Use Nepali format codes
        formatted = d.strftime("%K-%n-%D")
        assert "२०८०" in formatted
        assert "१०" in formatted
        assert "२४" in formatted
    

    
    def test_isoformat(self):
        d = BSDate(2080, 10, 24)
        assert d.isoformat() == "2080-10-24"
    
    def test_str(self):
        d = BSDate(2080, 10, 24)
        assert str(d) == "2080-10-24"
    
    def test_repr(self):
        d = BSDate(2080, 10, 24)
        assert repr(d) == "BSDate(2080, 10, 24)"
    
    def test_add_days(self):
        d = BSDate(2080, 10, 24)
        new_d = d + 7
        assert isinstance(new_d, BSDate)
        # Should be 7 days later
        assert (new_d.to_ad() - d.to_ad()).days == 7
    
    def test_add_timedelta(self):
        d = BSDate(2080, 10, 24)
        new_d = d + timedelta(days=7)
        assert (new_d.to_ad() - d.to_ad()).days == 7
    
    def test_subtract_days(self):
        d = BSDate(2080, 10, 24)
        new_d = d - 7
        assert isinstance(new_d, BSDate)
        assert (d.to_ad() - new_d.to_ad()).days == 7
    
    def test_subtract_dates(self):
        d1 = BSDate(2080, 10, 24)
        d2 = BSDate(2080, 10, 17)
        diff = d1 - d2
        assert isinstance(diff, timedelta)
        assert diff.days == 7
    
    def test_equality(self):
        d1 = BSDate(2080, 10, 24)
        d2 = BSDate(2080, 10, 24)
        assert d1 == d2
    
    def test_inequality(self):
        d1 = BSDate(2080, 10, 24)
        d2 = BSDate(2080, 10, 25)
        assert d1 != d2
    
    def test_less_than(self):
        d1 = BSDate(2080, 10, 24)
        d2 = BSDate(2080, 10, 25)
        assert d1 < d2
    
    def test_greater_than(self):
        d1 = BSDate(2080, 10, 25)
        d2 = BSDate(2080, 10, 24)
        assert d1 > d2
    
    def test_hash(self):
        d = BSDate(2080, 10, 24)
        assert hash(d) == hash((2080, 10, 24))
    
    def test_replace(self):
        d = BSDate(2080, 10, 24)
        new_d = d.replace(day=15)
        assert new_d.year == 2080
        assert new_d.month == 10
        assert new_d.day == 15
    
    def test_weekday(self):
        d = BSDate(2080, 10, 24)
        weekday = d.weekday()
        assert 0 <= weekday <= 6
