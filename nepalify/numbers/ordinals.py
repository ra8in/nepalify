"""
Nepali ordinal number conversion utilities.

Convert between integers, English ordinal text, and Nepali ordinal strings.
"""

from typing import Union, Dict


# ─── Nepali Ordinal Mappings (1-100) ───────────────────────────────────────────
# First few are unique forms, then a pattern of cardinal base + "औं" suffix.

ORDINALS_NEPALI: Dict[int, str] = {
    1: "पहिलो",
    2: "दोस्रो",
    3: "तेस्रो",
    4: "चौथो",
    5: "पाँचौं",
    6: "छैठौं",
    7: "सातौं",
    8: "आठौं",
    9: "नवौं",
    10: "दशौं",
    11: "एघारौं",
    12: "बाह्रौं",
    13: "तेह्रौं",
    14: "चौधौं",
    15: "पन्ध्रौं",
    16: "सोह्रौं",
    17: "सत्रौं",
    18: "अठारौं",
    19: "उन्नाइसौं",
    20: "बीसौं",
    21: "एक्काइसौं",
    22: "बाइसौं",
    23: "तेइसौं",
    24: "चौबीसौं",
    25: "पच्चीसौं",
    26: "छब्बीसौं",
    27: "सत्ताइसौं",
    28: "अठ्ठाइसौं",
    29: "उनन्तीसौं",
    30: "तीसौं",
    31: "एकतीसौं",
    32: "बत्तीसौं",
    33: "तेत्तीसौं",
    34: "चौँतीसौं",
    35: "पैँतीसौं",
    36: "छत्तीसौं",
    37: "सैँतीसौं",
    38: "अठतीसौं",
    39: "उनन्चालीसौं",
    40: "चालीसौं",
    41: "एकचालीसौं",
    42: "बयालीसौं",
    43: "त्रिचालीसौं",
    44: "चवालीसौं",
    45: "पैँतालीसौं",
    46: "छयालीसौं",
    47: "सत्चालीसौं",
    48: "अठचालीसौं",
    49: "उनन्पचासौं",
    50: "पचासौं",
    51: "एकाउन्नौं",
    52: "बाउन्नौं",
    53: "त्रिपन्नौं",
    54: "चउन्नौं",
    55: "पचपन्नौं",
    56: "छपन्नौं",
    57: "सन्ताउन्नौं",
    58: "अन्ठाउन्नौं",
    59: "उनन्साठीऔं",
    60: "साठीऔं",
    61: "एकसट्ठीऔं",
    62: "बयसट्ठीऔं",
    63: "त्रिसट्ठीऔं",
    64: "चौंसट्ठीऔं",
    65: "पैंसट्ठीऔं",
    66: "छयसट्ठीऔं",
    67: "सतसट्ठीऔं",
    68: "अठसट्ठीऔं",
    69: "उनन्सत्तरीऔं",
    70: "सत्तरीऔं",
    71: "एकहत्तरौं",
    72: "बहत्तरौं",
    73: "त्रिहत्तरौं",
    74: "चौहत्तरौं",
    75: "पचहत्तरौं",
    76: "छयहत्तरौं",
    77: "सतहत्तरौं",
    78: "अठहत्तरौं",
    79: "उनासीऔं",
    80: "असीऔं",
    81: "एकासीऔं",
    82: "बयासीऔं",
    83: "त्रियासीऔं",
    84: "चौरासीऔं",
    85: "पचासीऔं",
    86: "छयासीऔं",
    87: "सतासीऔं",
    88: "अठासीऔं",
    89: "उनान्नब्बेऔं",
    90: "नब्बेऔं",
    91: "एकानब्बेऔं",
    92: "बयानब्बेऔं",
    93: "त्रियानब्बेऔं",
    94: "चौरानब्बेऔं",
    95: "पंचानब्बेऔं",
    96: "छयानब्बेऔं",
    97: "सन्तानब्बेऔं",
    98: "अन्ठानब्बेऔं",
    99: "उनान्सयौं",
    100: "सयौं",
}

# Reverse lookup: Nepali ordinal → integer
_NEPALI_TO_INT: Dict[str, int] = {v: k for k, v in ORDINALS_NEPALI.items()}


# ─── English Ordinal Text Mappings ─────────────────────────────────────────────

ORDINALS_ENGLISH: Dict[str, int] = {
    # Full words
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
    "seventh": 7,
    "eighth": 8,
    "ninth": 9,
    "tenth": 10,
    "eleventh": 11,
    "twelfth": 12,
    "thirteenth": 13,
    "fourteenth": 14,
    "fifteenth": 15,
    "sixteenth": 16,
    "seventeenth": 17,
    "eighteenth": 18,
    "nineteenth": 19,
    "twentieth": 20,
    "twenty-first": 21,
    "twenty-second": 22,
    "twenty-third": 23,
    "twenty-fourth": 24,
    "twenty-fifth": 25,
    "thirtieth": 30,
    "fortieth": 40,
    "fiftieth": 50,
    "sixtieth": 60,
    "seventieth": 70,
    "eightieth": 80,
    "ninetieth": 90,
    "hundredth": 100,
    # Abbreviated forms
    "1st": 1,
    "2nd": 2,
    "3rd": 3,
    "4th": 4,
    "5th": 5,
    "6th": 6,
    "7th": 7,
    "8th": 8,
    "9th": 9,
    "10th": 10,
    "11th": 11,
    "12th": 12,
    "13th": 13,
    "14th": 14,
    "15th": 15,
    "16th": 16,
    "17th": 17,
    "18th": 18,
    "19th": 19,
    "20th": 20,
    "21st": 21,
    "22nd": 22,
    "23rd": 23,
    "24th": 24,
    "25th": 25,
    "26th": 26,
    "27th": 27,
    "28th": 28,
    "29th": 29,
    "30th": 30,
    "31st": 31,
    "32nd": 32,
    "40th": 40,
    "50th": 50,
    "60th": 60,
    "70th": 70,
    "80th": 80,
    "90th": 90,
    "100th": 100,
}

# Case-insensitive lookup
_ENGLISH_LOWER: Dict[str, int] = {k.lower(): v for k, v in ORDINALS_ENGLISH.items()}


# ─── Conversion Functions ──────────────────────────────────────────────────────

def to_nepali_ordinal(value: Union[int, str]) -> str:
    """
    Convert a number or English ordinal text to a Nepali ordinal string.

    Accepts:
    - Integers: 1, 2, 3, ...
    - English words: "first", "second", "third", ...
    - Abbreviated forms: "1st", "2nd", "3rd", ...

    Args:
        value: Integer or English ordinal text to convert.

    Returns:
        Nepali ordinal string (e.g., "पहिलो", "दोस्रो", "तेस्रो").

    Examples:
        >>> to_nepali_ordinal(1)
        'पहिलो'
        >>> to_nepali_ordinal(2)
        'दोस्रो'
        >>> to_nepali_ordinal("first")
        'पहिलो'
        >>> to_nepali_ordinal("1st")
        'पहिलो'
        >>> to_nepali_ordinal(10)
        'दशौं'

    Raises:
        ValueError: If the value cannot be converted to a Nepali ordinal.
        TypeError: If the value is not an int or str.
    """
    if isinstance(value, int):
        return _int_to_nepali_ordinal(value)
    elif isinstance(value, str):
        return _str_to_nepali_ordinal(value)
    else:
        raise TypeError(
            f"Expected int or str, got {type(value).__name__}"
        )


def from_nepali_ordinal(text: str) -> int:
    """
    Convert a Nepali ordinal string to its integer value.

    Args:
        text: Nepali ordinal string (e.g., "पहिलो", "दोस्रो").

    Returns:
        Integer value of the ordinal.

    Examples:
        >>> from_nepali_ordinal("पहिलो")
        1
        >>> from_nepali_ordinal("दोस्रो")
        2
        >>> from_nepali_ordinal("दशौं")
        10

    Raises:
        ValueError: If the text is not a recognized Nepali ordinal.
    """
    text = text.strip()
    result = _NEPALI_TO_INT.get(text)
    if result is None:
        raise ValueError(f"Unrecognized Nepali ordinal: '{text}'")
    return result


# ─── Internal Helpers ──────────────────────────────────────────────────────────

def _int_to_nepali_ordinal(n: int) -> str:
    """Convert integer to Nepali ordinal."""
    if n < 1:
        raise ValueError(f"Ordinal must be >= 1, got {n}")

    result = ORDINALS_NEPALI.get(n)
    if result is not None:
        return result

    raise ValueError(
        f"Ordinal {n} is out of supported range (1-{max(ORDINALS_NEPALI)})"
    )


def _str_to_nepali_ordinal(text: str) -> str:
    """Convert English ordinal text to Nepali ordinal."""
    text = text.strip().lower()

    # Try English ordinal text lookup
    num = _ENGLISH_LOWER.get(text)
    if num is not None:
        return ORDINALS_NEPALI[num]

    # Try parsing as a plain integer string
    try:
        n = int(text)
        return _int_to_nepali_ordinal(n)
    except ValueError:
        pass

    raise ValueError(
        f"Cannot convert '{text}' to Nepali ordinal. "
        f"Expected an integer, English ordinal word (e.g., 'first'), "
        f"or abbreviated form (e.g., '1st')."
    )
