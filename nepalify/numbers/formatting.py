"""
Number formatting utilities.

Supports:
- Indian/Nepali numbering system (3-2-2 grouping)
- Number to Nepali words conversion
"""

from typing import Union
from nepalify.numbers.devanagari import to_devanagari


def format_number(
    number: Union[int, float, str],
    use_devanagari: bool = False,
    delimiter: str = ","
) -> str:
    """
    Format a number using the Indian/Nepali numbering system.
    
    Uses the 3-2-2 grouping pattern (first 3 digits from right, then groups of 2).
    
    Args:
        number: Number to format. Can be int, float, or string.
                Existing commas in strings are automatically stripped.
        use_devanagari: If True, convert digits to Devanagari numerals.
        delimiter: Character to use as thousands separator (default: comma).
    
    Returns:
        Formatted number string with Indian/Nepali grouping.
    
    Examples:
        format_number(1234567)→
        '12,34,567'\n
        format_number(1234567890)→
        '1,23,45,67,890'\n\n
        format_number(1234567, use_devanagari=True)→
        '१२,३४,५६७'\n
        format_number(-1234567.89)→
        '-12,34,567.89'\n
        format_number("2,553,871")  # Western format → Nepali
        '25,53,871'
    """
    # Convert to string and strip existing commas
    num_str = str(number).replace(',', '')
    
    # Handle negative numbers
    is_negative = num_str.startswith('-')
    if is_negative:
        num_str = num_str[1:]
    
    # Separate integer and decimal parts
    if '.' in num_str:
        integer_part, decimal_part = num_str.split('.', 1)
    else:
        integer_part = num_str
        decimal_part = None
    
    # Apply Indian/Nepali grouping: first 3 digits from right, then 2 digits each
    if len(integer_part) <= 3:
        formatted = integer_part
    else:
        # Take last 3 digits
        result = [integer_part[-3:]]
        remaining = integer_part[:-3]
        
        # Group remaining digits in pairs of 2 from right to left
        while len(remaining) > 2:
            result.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        
        # Add any remaining digits (1 or 2)
        if remaining:
            result.insert(0, remaining)
        
        formatted = delimiter.join(result)
    
    # Rejoin with decimal part if present
    if decimal_part is not None:
        formatted = f"{formatted}.{decimal_part}"
    
    # Add negative sign back
    if is_negative:
        formatted = f"-{formatted}"
    
    # Convert to Devanagari if requested
    if use_devanagari:
        formatted = to_devanagari(formatted)
    
    return formatted


# Nepali number words
_ONES = [
    '', 'एक', 'दुई', 'तीन', 'चार', 'पाँच', 'छ', 'सात', 'आठ', 'नौ',
    'दश', 'एघार', 'बाह्र', 'तेह्र', 'चौध', 'पन्ध्र', 'सोह्र', 'सत्र', 'अठार', 'उन्नाइस',
    'बीस', 'एक्काइस', 'बाइस', 'तेइस', 'चौबीस', 'पच्चीस', 'छब्बीस', 'सत्ताइस', 'अठ्ठाइस', 'उनन्तीस',
    'तीस', 'एकतीस', 'बत्तीस', 'तेत्तीस', 'चौँतीस', 'पैँतीस', 'छत्तीस', 'सैँतीस', 'अठतीस', 'उनन्चालीस',
    'चालीस', 'एकचालीस', 'बयालीस', 'त्रिचालीस', 'चवालीस', 'पैँतालीस', 'छयालीस', 'सत्चालीस', 'अठचालीस', 'उनन्पचास',
    'पचास', 'एकाउन्न', 'बाउन्न', 'त्रिपन्न', 'चउन्न', 'पचपन्न', 'छपन्न', 'सन्ताउन्न', 'अन्ठाउन्न', 'उनन्साठी',
    'साठी', 'एकसट्ठी', 'बयसट्ठी', 'त्रिसट्ठी', 'चौंसट्ठी', 'पैंसट्ठी', 'छयसट्ठी', 'सतसट्ठी', 'अठसट्ठी', 'उनन्सत्तरी',
    'सत्तरी', 'एकहत्तर', 'बहत्तर', 'त्रिहत्तर', 'चौहत्तर', 'पचहत्तर', 'छयहत्तर', 'सतहत्तर', 'अठहत्तर', 'उनासी',
    'असी', 'एकासी', 'बयासी', 'त्रियासी', 'चौरासी', 'पचासी', 'छयासी', 'सतासी', 'अठासी', 'उनान्नब्बे',
    'नब्बे', 'एकानब्बे', 'बयानब्बे', 'त्रियानब्बे', 'चौरानब्बे', 'पंचानब्बे', 'छयानब्बे', 'सन्तानब्बे', 'अन्ठानब्बे', 'उनान्सय'
]

_HUNDRED = 'सय'
_THOUSAND = 'हजार'
_LAKH = 'लाख'
_CRORE = 'करोड'
_ARAB = 'अर्ब'
_KHARAB = 'खर्ब'


def _convert_two_digits(n: int) -> str:
    """Convert a number 0-99 to Nepali words."""
    if n < 100:
        return _ONES[n]
    return ''


def _convert_three_digits(n: int) -> str:
    """Convert a number 0-999 to Nepali words."""
    if n == 0:
        return ''
    
    result = []
    
    # Hundreds place
    if n >= 100:
        hundreds = n // 100
        result.append(_ONES[hundreds])
        result.append(_HUNDRED)
        n %= 100
    
    # Remaining two digits
    if n > 0:
        result.append(_ONES[n])
    
    return ' '.join(result)


def to_words_nepali(number: int) -> str:
    """
    Convert a number to Nepali words.
    
    Supports the Indian/Nepali numbering system:
    - हजार (thousand)
    - लाख (lakh = 100,000)
    - करोड (crore = 10,000,000)
    - अर्ब (arab = 1,000,000,000)
    - खर्ब (kharab = 100,000,000,000)
    
    Args:
        number: Integer to convert (must be non-negative).
    
    Returns:
        Nepali word representation of the number.
    
    Examples:
        to_words_nepali(0)
        'शुन्य'\n
        to_words_nepali(15)
        'पन्ध्र'\n
        to_words_nepali(100)
        'एक सय'\n
        to_words_nepali(1234)
        'एक हजार दुई सय चौँतीस'\n
        to_words_nepali(100000)
        'एक लाख'\n
        to_words_nepali(10000000)
        'एक करोड'
    
    Raises:
        ValueError: If number is negative.
    """
    if number < 0:
        raise ValueError("Negative numbers are not supported")
    
    if number == 0:
        return 'शुन्य'
    
    if number < 100:
        return _ONES[number]
    
    parts = []
    
    # Kharab (10^11)
    if number >= 10**11:
        kharab = number // 10**11
        parts.append(_convert_two_digits(kharab))
        parts.append(_KHARAB)
        number %= 10**11
    
    # Arab (10^9)
    if number >= 10**9:
        arab = number // 10**9
        parts.append(_convert_two_digits(arab))
        parts.append(_ARAB)
        number %= 10**9
    
    # Crore (10^7)
    if number >= 10**7:
        crore = number // 10**7
        parts.append(_convert_two_digits(crore))
        parts.append(_CRORE)
        number %= 10**7
    
    # Lakh (10^5)
    if number >= 10**5:
        lakh = number // 10**5
        parts.append(_convert_two_digits(lakh))
        parts.append(_LAKH)
        number %= 10**5
    
    # Thousand (10^3)
    if number >= 10**3:
        thousand = number // 10**3
        parts.append(_convert_two_digits(thousand))
        parts.append(_THOUSAND)
        number %= 10**3
    
    # Remaining (0-999)
    if number > 0:
        parts.append(_convert_three_digits(number))
    
    return ' '.join(parts)
