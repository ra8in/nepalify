"""
Nepali language constants.

BS Month Names, Day Names, and related constants.
"""

from typing import List

# BS Month Names - Formal/Colloquial (1-indexed: Baisakh=1, Chaitra=12)
MONTHS_NEPALI: List[str] = [
    "बैशाख",    # 1 - Baisakh (Apr-May)
    "जेठ",      # 2 - Jestha (May-Jun)
    "असार",     # 3 - Ashadh (Jun-Jul)
    "साउन",     # 4 - Shrawan (Jul-Aug)
    "भदौ",      # 5 - Bhadra (Aug-Sep)
    "असोज",     # 6 - Ashwin (Sep-Oct)
    "कार्तिक",   # 7 - Kartik (Oct-Nov)
    "मंसिर",    # 8 - Mangsir (Nov-Dec)
    "पुष",      # 9 - Poush (Dec-Jan)
    "माघ",      # 10 - Magh (Jan-Feb)
    "फागुन",    # 11 - Falgun (Feb-Mar)
    "चैत",      # 12 - Chaitra (Mar-Apr)
]

# BS Month Names - Sanskrit/Traditional
MONTHS_NEPALI_SANSKRIT: List[str] = [
    "वैशाख",    # 1 - Vaisakha (Apr-May)
    "ज्येष्ठ",   # 2 - Jyeshtha (May-Jun)
    "आषाढ",     # 3 - Asadha (Jun-Jul)
    "श्रावण",    # 4 - Shravana (Jul-Aug)
    "भाद्र",     # 5 - Bhadrapada (Aug-Sep)
    "आश्विन",    # 6 - Ashvin (Sep-Oct)
    "कार्तिक",   # 7 - Kartika (Oct-Nov)
    "मार्ग",     # 8 - Margashirsha (Nov-Dec)
    "पौष",      # 9 - Pausha (Dec-Jan)
    "माघ",      # 10 - Magha (Jan-Feb)
    "फाल्गुन",   # 11 - Phalguna (Feb-Mar)
    "चैत्र",     # 12 - Chaitra (Mar-Apr)
]

MONTHS_ENGLISH: List[str] = [
    "Baishakh",
    "Jestha",
    "Asar",
    "Shrawan",
    "Bhadau",
    "Asoj",
    "Kartik",
    "Mangsir",
    "Poush",
    "Magh",
    "Falgun",
    "Chaitra",
]

MONTHS_ENGLISH_SHORT: List[str] = [
    "Bai",
    "Jes",
    "Asa",
    "Shr",
    "Bha",
    "Ash",
    "Kar",
    "Man",
    "Pou",
    "Mag",
    "Fal",
    "Cha",
]

# Day Names (0-indexed: Sunday=0, Saturday=6)
DAYS_NEPALI: List[str] = [
    "आइतबार",    # 0 - Sunday
    "सोमबार",    # 1 - Monday
    "मंगलबार",   # 2 - Tuesday
    "बुधबार",    # 3 - Wednesday
    "बिहिबार",   # 4 - Thursday
    "शुक्रबार",   # 5 - Friday
    "शनिबार",    # 6 - Saturday
]

DAYS_NEPALI_SHORT: List[str] = [
    "आइत",
    "सोम",
    "मंगल",
    "बुध",
    "बिहि",
    "शुक्र",
    "शनि",
]

DAYS_ENGLISH: List[str] = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]

DAYS_ENGLISH_SHORT: List[str] = [
    "Sun",
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
]

# Gregorian month names in Nepali
GREGORIAN_MONTHS_NEPALI: List[str] = [
    "जनवरी",
    "फेब्रुअरी",
    "मार्च",
    "अप्रिल",
    "मे",
    "जुन",
    "जुलाई",
    "अगस्ट",
    "सेप्टेम्बर",
    "अक्टोबर",
    "नोभेम्बर",
    "डिसेम्बर",
]

GREGORIAN_MONTHS_ENGLISH: List[str] = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

# Common Nepali time-related words
TIME_WORDS_NEPALI = {
    "today": "आज",
    "tomorrow": "भोलि",
    "yesterday": "हिजो",
    "week": "हप्ता",
    "month": "महिना",
    "year": "वर्ष",
    "day": "दिन",
    "hour": "घण्टा",
    "minute": "मिनेट",
    "second": "सेकेन्ड",
}

# Number words (for display/formatting)
NUMBER_WORDS_NEPALI = {
    0: "शुन्य",
    1: "एक",
    2: "दुई", 
    3: "तीन",
    4: "चार",
    5: "पाँच",
    6: "छ",
    7: "सात",
    8: "आठ",
    9: "नौ",
    10: "दश",
}


# Nepali Time Periods
TIME_PERIODS_NEPALI = {
    'morning': 'बिहान',      # 4:00 - 11:59
    'afternoon': 'दिउँसो',   # 12:00 - 15:59
    'evening': 'बेलुका',     # 16:00 - 19:59
    'night': 'राति',         # 20:00 - 3:59
}

