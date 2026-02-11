"""Tests for Nepali ordinal number conversion."""

import pytest
from nepalify.numbers.ordinals import (
    to_nepali_ordinal,
    from_nepali_ordinal,
    ORDINALS_NEPALI,
)


class TestToNepaliOrdinal:
    """Tests for to_nepali_ordinal function."""

    # ── Integer inputs ──────────────────────────────────────────────────

    def test_first(self):
        assert to_nepali_ordinal(1) == "पहिलो"

    def test_second(self):
        assert to_nepali_ordinal(2) == "दोस्रो"

    def test_third(self):
        assert to_nepali_ordinal(3) == "तेस्रो"

    def test_fourth(self):
        assert to_nepali_ordinal(4) == "चौथो"

    def test_fifth_to_tenth(self):
        expected = {
            5: "पाँचौं",
            6: "छैठौं",
            7: "सातौं",
            8: "आठौं",
            9: "नवौं",
            10: "दशौं",
        }
        for num, nepali in expected.items():
            assert to_nepali_ordinal(num) == nepali, f"Failed for {num}"

    def test_teens(self):
        expected = {
            11: "एघारौं",
            12: "बाह्रौं",
            13: "तेह्रौं",
            14: "चौधौं",
            15: "पन्ध्रौं",
            16: "सोह्रौं",
            17: "सत्रौं",
            18: "अठारौं",
            19: "उन्नाइसौं",
        }
        for num, nepali in expected.items():
            assert to_nepali_ordinal(num) == nepali, f"Failed for {num}"

    def test_twentieth(self):
        assert to_nepali_ordinal(20) == "बीसौं"

    def test_fiftieth(self):
        assert to_nepali_ordinal(50) == "पचासौं"

    def test_hundredth(self):
        assert to_nepali_ordinal(100) == "सयौं"

    def test_all_mapped_values(self):
        """Ensure every mapped value round-trips correctly."""
        for num in ORDINALS_NEPALI:
            result = to_nepali_ordinal(num)
            assert result == ORDINALS_NEPALI[num]

    # ── English text inputs ─────────────────────────────────────────────

    def test_english_first(self):
        assert to_nepali_ordinal("first") == "पहिलो"

    def test_english_second(self):
        assert to_nepali_ordinal("second") == "दोस्रो"

    def test_english_third(self):
        assert to_nepali_ordinal("third") == "तेस्रो"

    def test_english_tenth(self):
        assert to_nepali_ordinal("tenth") == "दशौं"

    def test_english_twentieth(self):
        assert to_nepali_ordinal("twentieth") == "बीसौं"

    def test_english_case_insensitive(self):
        assert to_nepali_ordinal("First") == "पहिलो"
        assert to_nepali_ordinal("SECOND") == "दोस्रो"
        assert to_nepali_ordinal("Third") == "तेस्रो"

    # ── Abbreviated inputs ──────────────────────────────────────────────

    def test_abbreviated_1st(self):
        assert to_nepali_ordinal("1st") == "पहिलो"

    def test_abbreviated_2nd(self):
        assert to_nepali_ordinal("2nd") == "दोस्रो"

    def test_abbreviated_3rd(self):
        assert to_nepali_ordinal("3rd") == "तेस्रो"

    def test_abbreviated_10th(self):
        assert to_nepali_ordinal("10th") == "दशौं"

    def test_abbreviated_21st(self):
        assert to_nepali_ordinal("21st") == "एक्काइसौं"

    # ── String number inputs ────────────────────────────────────────────

    def test_string_number(self):
        """Plain number string should also work."""
        assert to_nepali_ordinal("1") == "पहिलो"
        assert to_nepali_ordinal("10") == "दशौं"

    # ── Edge cases / errors ─────────────────────────────────────────────

    def test_zero_raises(self):
        with pytest.raises(ValueError):
            to_nepali_ordinal(0)

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            to_nepali_ordinal(-1)

    def test_out_of_range_raises(self):
        with pytest.raises(ValueError):
            to_nepali_ordinal(101)

    def test_invalid_string_raises(self):
        with pytest.raises(ValueError):
            to_nepali_ordinal("hello")

    def test_wrong_type_raises(self):
        with pytest.raises(TypeError):
            to_nepali_ordinal(3.14)  # type: ignore

    def test_whitespace_stripped(self):
        assert to_nepali_ordinal("  first  ") == "पहिलो"


class TestFromNepaliOrdinal:
    """Tests for from_nepali_ordinal function."""

    def test_pahilo(self):
        assert from_nepali_ordinal("पहिलो") == 1

    def test_dosro(self):
        assert from_nepali_ordinal("दोस्रो") == 2

    def test_tesro(self):
        assert from_nepali_ordinal("तेस्रो") == 3

    def test_dashaun(self):
        assert from_nepali_ordinal("दशौं") == 10

    def test_bisaun(self):
        assert from_nepali_ordinal("बीसौं") == 20

    def test_sayaun(self):
        assert from_nepali_ordinal("सयौं") == 100

    def test_all_mapped_values(self):
        """Ensure every Nepali ordinal maps back to its integer."""
        for num, nepali in ORDINALS_NEPALI.items():
            assert from_nepali_ordinal(nepali) == num

    def test_whitespace_stripped(self):
        assert from_nepali_ordinal("  पहिलो  ") == 1

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            from_nepali_ordinal("nonsense")

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            from_nepali_ordinal("")


class TestRoundTrip:
    """Test that to_nepali_ordinal and from_nepali_ordinal are inverses."""

    def test_int_roundtrip(self):
        """int → Nepali → int should give the same number."""
        for i in range(1, 101):
            nepali = to_nepali_ordinal(i)
            assert from_nepali_ordinal(nepali) == i, f"Round-trip failed for {i}"

    def test_english_roundtrip(self):
        """English → Nepali → int should give the correct number."""
        words = {
            "first": 1, "second": 2, "third": 3,
            "fourth": 4, "fifth": 5, "tenth": 10,
        }
        for word, expected in words.items():
            nepali = to_nepali_ordinal(word)
            assert from_nepali_ordinal(nepali) == expected
