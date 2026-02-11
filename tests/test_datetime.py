"""Tests for BSDateTime class and timezone support."""

import pytest
from datetime import datetime, date, time, timedelta, timezone as py_timezone
from nepalify.dates import BSDateTime, BSDate, NepaliTimeZone, NPT
from nepalify.dates import nepali_now, to_nepali_timezone, to_utc_timezone


class TestBSDateTime:
    """Tests for BSDateTime class."""
    
    def test_create_datetime(self):
        """Test creating a BSDateTime instance."""
        dt = BSDateTime(2080, 10, 24, 14, 30, 0)
        assert dt.year == 2080
        assert dt.month == 10
        assert dt.day == 24
        assert dt.hour == 14
        assert dt.minute == 30
        assert dt.second == 0
        assert dt.microsecond == 0
    
    def test_create_with_microsecond(self):
        """Test creating BSDateTime with microseconds."""
        dt = BSDateTime(2080, 10, 24, 14, 30, 0, 123456)
        assert dt.microsecond == 123456
    
    def test_create_with_timezone(self):
        """Test creating BSDateTime with timezone."""
        dt = BSDateTime(2080, 10, 24, 14, 30, 0, tzinfo=NepaliTimeZone())
        assert dt.tzinfo is not None
        assert str(dt.tzinfo) == "NPT" or "Asia/Kathmandu" in str(dt.tzinfo)
    
    def test_invalid_datetime_raises(self):
        """Test that invalid datetime raises ValueError."""
        with pytest.raises(ValueError):
            BSDateTime(2080, 13, 1, 0, 0, 0)  # Invalid month
        
        with pytest.raises(ValueError):
            BSDateTime(2080, 1, 35, 0, 0, 0)  # Invalid day
    
    def test_now(self):
        """Test BSDateTime.now() returns current datetime."""
        now = BSDateTime.now()
        assert isinstance(now, BSDateTime)
        assert 1901 <= now.year <= 2199
    
    def test_now_with_timezone(self):
        """Test BSDateTime.now() with timezone."""
        now = BSDateTime.now(NepaliTimeZone())
        assert now.tzinfo is not None
    
    def test_today(self):
        """Test BSDateTime.today() returns midnight."""
        today = BSDateTime.today()
        assert today.hour == 0
        assert today.minute == 0
        assert today.second == 0
    
    def test_from_ad(self):
        """Test converting from AD datetime."""
        ad_dt = datetime(2024, 2, 6, 14, 30, 0)
        bs_dt = BSDateTime.from_ad(ad_dt)
        assert bs_dt.year == 2080
        assert bs_dt.month == 10
        assert bs_dt.hour == 14
        assert bs_dt.minute == 30
    
    def test_from_ad_date_only(self):
        """Test converting from AD date (no time)."""
        ad_date = date(2024, 2, 6)
        bs_dt = BSDateTime.from_ad(ad_date)
        assert bs_dt.year == 2080
        assert bs_dt.hour == 0  # Midnight
    
    def test_to_ad(self):
        """Test converting to AD datetime."""
        bs_dt = BSDateTime(2080, 10, 24, 14, 30, 0)
        ad_dt = bs_dt.to_ad()
        assert isinstance(ad_dt, datetime)
        assert ad_dt.hour == 14
        assert ad_dt.minute == 30
    
    def test_to_date(self):
        """Test converting to BSDate."""
        bs_dt = BSDateTime(2080, 10, 24, 14, 30, 0)
        bs_date = bs_dt.to_date()
        assert isinstance(bs_date, BSDate)
        assert bs_date.year == 2080
        assert bs_date.month == 10
        assert bs_date.day == 24
    
    def test_combine(self):
        """Test combining BSDate and time."""
        bs_date = BSDate(2080, 10, 24)
        t = time(14, 30, 0)
        bs_dt = BSDateTime.combine(bs_date, t)
        assert bs_dt.year == 2080
        assert bs_dt.hour == 14
        assert bs_dt.minute == 30
    
    def test_add_timedelta(self):
        """Test adding timedelta to BSDateTime."""
        dt = BSDateTime(2080, 10, 24, 10, 0, 0)
        new_dt = dt + timedelta(hours=5)
        assert new_dt.hour == 15
    
    def test_add_timedelta_day_rollover(self):
        """Test adding timedelta that rolls over to next day."""
        dt = BSDateTime(2080, 10, 24, 22, 0, 0)
        new_dt = dt + timedelta(hours=5)
        assert new_dt.day == 25
        assert new_dt.hour == 3
    
    def test_subtract_timedelta(self):
        """Test subtracting timedelta from BSDateTime."""
        dt = BSDateTime(2080, 10, 24, 10, 0, 0)
        new_dt = dt - timedelta(hours=5)
        assert new_dt.hour == 5
    
    def test_subtract_datetimes(self):
        """Test subtracting two BSDateTimes returns timedelta."""
        dt1 = BSDateTime(2080, 10, 24, 14, 30, 0)
        dt2 = BSDateTime(2080, 10, 24, 10, 30, 0)
        diff = dt1 - dt2
        assert isinstance(diff, timedelta)
        assert diff.seconds == 4 * 3600  # 4 hours
    
    def test_equality(self):
        """Test BSDateTime equality."""
        dt1 = BSDateTime(2080, 10, 24, 14, 30, 0)
        dt2 = BSDateTime(2080, 10, 24, 14, 30, 0)
        assert dt1 == dt2
    
    def test_inequality(self):
        """Test BSDateTime inequality."""
        dt1 = BSDateTime(2080, 10, 24, 14, 30, 0)
        dt2 = BSDateTime(2080, 10, 24, 14, 30, 1)
        assert dt1 != dt2
    
    def test_less_than(self):
        """Test BSDateTime comparison."""
        dt1 = BSDateTime(2080, 10, 24, 10, 0, 0)
        dt2 = BSDateTime(2080, 10, 24, 14, 0, 0)
        assert dt1 < dt2
    
    def test_greater_than(self):
        """Test BSDateTime comparison."""
        dt1 = BSDateTime(2080, 10, 24, 14, 0, 0)
        dt2 = BSDateTime(2080, 10, 24, 10, 0, 0)
        assert dt1 > dt2
    
    def test_str(self):
        """Test string representation."""
        dt = BSDateTime(2080, 10, 24, 14, 30, 0)
        assert "2080-10-24" in str(dt)
        assert "14:30" in str(dt)
    
    def test_repr(self):
        """Test repr representation."""
        dt = BSDateTime(2080, 10, 24, 14, 30, 0)
        assert "BSDateTime" in repr(dt)
    
    def test_isoformat(self):
        """Test ISO format output."""
        dt = BSDateTime(2080, 10, 24, 14, 30, 0)
        iso = dt.isoformat()
        assert "2080-10-24" in iso
        assert "14:30:00" in iso


    def test_timestamp(self):
        """Test timestamp() returns float seconds."""
        dt = BSDateTime(2080, 10, 24, 14, 30, 0)
        ts = dt.timestamp()
        assert isinstance(ts, float)
        assert ts > 0
        
        # Validation with standard datetime
        ad_dt = dt.to_ad()
        assert ts == ad_dt.timestamp()

    def test_fromtimestamp(self):
        """Test fromtimestamp() creates correct BSDateTime."""
        # Use current time to avoid timezone issues with hardcoded timestamps
        now_ad = datetime.now()
        ts = now_ad.timestamp()
        
        bs_dt = BSDateTime.fromtimestamp(ts)
        assert isinstance(bs_dt, BSDateTime)
        # Should be very close (within 1 second)
        assert abs(bs_dt.timestamp() - ts) < 1.0

    def test_timetuple(self):
        """Test timetuple() returns valid struct_time."""
        dt = BSDateTime(2080, 10, 24, 14, 30, 0)
        tt = dt.timetuple()
        
        import time as _time
        assert isinstance(tt, _time.struct_time)
        assert tt.tm_year == 2080
        assert tt.tm_mon == 10
        assert tt.tm_mday == 24
        assert tt.tm_hour == 14
        assert tt.tm_min == 30
        assert tt.tm_sec == 0


class TestBSDateTimeStrftime:

    """Tests for BSDateTime strftime formatting."""
    
    def test_time_format_24h(self):
        """Test 24-hour time format."""
        dt = BSDateTime(2080, 10, 24, 14, 30, 0)
        result = dt.strftime("%H:%M:%S")
        assert result == "14:30:00"
    
    def test_time_format_12h(self):
        """Test 12-hour time format."""
        dt = BSDateTime(2080, 10, 24, 14, 30, 0)
        result = dt.strftime("%I:%M %p")
        assert "02:30" in result
        assert "PM" in result
    
    def test_time_format_nepali_period(self):
        """Test Nepali time period (AM/PM alternative)."""
        # Morning
        dt_morning = BSDateTime(2080, 10, 24, 9, 0, 0)
        # Old: dt.strftime("%I:%M %p", nepali=True)
        # New: Use %P for Nepali period
        result = dt_morning.strftime("%P")
        assert "बिहान" in result
        
        # Afternoon
        dt_afternoon = BSDateTime(2080, 10, 24, 14, 0, 0)
        result = dt_afternoon.strftime("%P")
        assert "दिउँसो" in result
    
    def test_date_and_time_format(self):
        """Test combined date and time format."""
        dt = BSDateTime(2080, 10, 24, 14, 30, 0)
        result = dt.strftime("%Y-%m-%d %H:%M:%S")
        assert result == "2080-10-24 14:30:00"
    
    def test_nepali_format(self):
        """Test Nepali digits in time."""
        dt = BSDateTime(2080, 10, 24, 14, 30, 0)
        # Old: dt.strftime("%H:%M", nepali=True)
        # New: Use %h:%i
        result = dt.strftime("%h:%i")
        assert "१४" in result
        assert "३०" in result


class TestNepaliTimeZone:
    """Tests for Nepal Timezone (UTC+05:45)."""
    
    def test_timezone_offset(self):
        """Test NPT offset is +05:45."""
        npt = NepaliTimeZone()
        offset = npt.utcoffset(None)
        assert offset == timedelta(hours=5, minutes=45)
    
    def test_timezone_name(self):
        """Test timezone name."""
        npt = NepaliTimeZone()
        name = npt.tzname(None)
        assert "NPT" in name or "Asia/Kathmandu" in str(npt)
    
    def test_npt_singleton(self):
        """Test NPT is a valid timezone instance."""
        assert NPT is not None
        offset = NPT.utcoffset(None)
        assert offset == timedelta(hours=5, minutes=45)
    
    def test_nepali_now(self):
        """Test nepali_now() returns current NPT time."""
        now = nepali_now()
        assert isinstance(now, datetime)
        assert now.tzinfo is not None
    
    def test_to_nepali_timezone(self):
        """Test converting UTC to NPT."""
        utc_dt = datetime(2024, 2, 7, 5, 15, 0, tzinfo=py_timezone.utc)
        npt_dt = to_nepali_timezone(utc_dt)
        # 5:15 UTC + 5:45 = 11:00 NPT
        assert npt_dt.hour == 11
        assert npt_dt.minute == 0
    
    def test_to_utc_timezone(self):
        """Test converting NPT to UTC."""
        npt_dt = datetime(2024, 2, 7, 11, 0, 0, tzinfo=NepaliTimeZone())
        utc_dt = to_utc_timezone(npt_dt)
        # 11:00 NPT - 5:45 = 5:15 UTC
        assert utc_dt.hour == 5
        assert utc_dt.minute == 15


class TestTimePeriods:
    """Tests for Nepali time periods (morning, afternoon, evening, night)."""
    
    def test_morning_period(self):
        """Test morning (बिहान) period: 4:00-11:59."""
        dt = BSDateTime(2080, 10, 24, 8, 0, 0)
        result = dt.strftime("%P")
        assert "बिहान" in result
    
    def test_afternoon_period(self):
        """Test afternoon (दिउँसो) period: 12:00-15:59."""
        dt = BSDateTime(2080, 10, 24, 14, 0, 0)
        result = dt.strftime("%P")
        assert "दिउँसो" in result
    
    def test_evening_period(self):
        """Test evening (बेलुका) period: 16:00-19:59."""
        dt = BSDateTime(2080, 10, 24, 18, 0, 0)
        result = dt.strftime("%P")
        assert "बेलुका" in result
    
    def test_night_period(self):
        """Test night (राति) period: 20:00-3:59."""
        dt = BSDateTime(2080, 10, 24, 22, 0, 0)
        result = dt.strftime("%P")
        assert "राति" in result
