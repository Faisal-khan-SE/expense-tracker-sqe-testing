"""Unit test suite for expense_tracker.formatting module.

This module validates currency, date, relative time, and local timestamp formatting
functions applying Equivalence Class Partitioning (ECP), Boundary Value Analysis (BVA),
exception testing, and pytest parameterization.

Traceability:
- Test IDs map directly to docs/test_design_notes.md (FMT-CUR-*, FMT-DAT-*, FMT-REL-*, FMT-LOC-*)
- Contributor: M-Ehtasham-SE (Lead QA / SQE Contributor)
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock
import pytest

from expense_tracker.formatting import (
    format_currency,
    format_date,
    format_relative,
    format_local,
)


@pytest.mark.formatting
@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.order(6)
class TestFormatCurrency:
    """Unit tests for format_currency function applying ECP and BVA.

    Target: format_currency(amount: float) -> str
    Techniques: ECP, BVA, Parameterization, Type Exceptions
    Test Count: 8 test methods (covering 12 representative input partitions)
    """

    @pytest.mark.parametrize(
        "amount,expected",
        [
            (12.50, "$12.50"),
            (45.0, "$45.00"),
            (-15.75, "$-15.75"),
            (-0.50, "$-0.50"),
        ],
    )
    def test_format_currency_standard_amounts(self, amount: float, expected: str):
        """ECP: Valid positive and negative float amounts formatted with two decimals."""
        assert format_currency(amount) == expected

    def test_format_currency_zero_boundary(self):
        """BVA: Exact zero boundary (FMT-CUR-02)."""
        assert format_currency(0.0) == "$0.00"
        assert format_currency(0) == "$0.00"

    def test_format_currency_minimum_positive_cent(self):
        """BVA: Minimum positive cent threshold (FMT-CUR-03)."""
        assert format_currency(0.01) == "$0.01"

    def test_format_currency_minimum_negative_cent(self):
        """BVA: Minimum negative cent threshold (FMT-CUR-04)."""
        assert format_currency(-0.01) == "$-0.01"

    @pytest.mark.parametrize(
        "amount,expected",
        [
            (999.99, "$999.99"),
            (1000.00, "$1,000.00"),
            (1000.01, "$1,000.01"),
            (999999.99, "$999,999.99"),
            (1000000.00, "$1,000,000.00"),
        ],
    )
    def test_format_currency_thousands_separator_boundaries(self, amount: float, expected: str):
        """BVA: Thousands separator comma grouping transitions (FMT-CUR-05, FMT-CUR-06, FMT-CUR-07)."""
        assert format_currency(amount) == expected

    @pytest.mark.parametrize(
        "amount,expected",
        [
            (4.556, "$4.56"),
            (4.554, "$4.55"),
            (10.999, "$11.00"),
        ],
    )
    def test_format_currency_float_rounding(self, amount: float, expected: str):
        """ECP: Floating-point precision rounding to nearest cent (FMT-CUR-08)."""
        assert format_currency(amount) == expected

    def test_format_currency_integer_input(self):
        """ECP: Integer values formatted as floats with two decimal places."""
        assert format_currency(100) == "$100.00"

    def test_format_currency_non_numeric_type_error(self):
        """Exception: Passing non-numeric types raises TypeError or ValueError."""
        with pytest.raises((TypeError, ValueError)):
            format_currency("not_a_number")  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            format_currency(None)  # type: ignore[arg-type]


@pytest.mark.formatting
@pytest.mark.regression
@pytest.mark.order(7)
class TestFormatDate:
    """Unit tests for format_date function applying ECP, BVA, and exceptions.

    Target: format_date(iso_date: str) -> str
    Techniques: ECP, BVA, Calendar Exceptions
    Test Count: 9 test methods (covering 14 representative input partitions)
    """

    @pytest.mark.parametrize(
        "iso_date,expected",
        [
            ("2026-06-15", "Jun 15, 2026"),
            ("2026-04-05", "Apr 5, 2026"),
            ("2026-11-20", "Nov 20, 2026"),
        ],
    )
    def test_format_date_valid_iso_dates(self, iso_date: str, expected: str):
        """ECP: Valid standard ISO dates formatted as 'Mon D, YYYY' (FMT-DAT-01, FMT-DAT-02)."""
        assert format_date(iso_date) == expected

    def test_format_date_year_start_boundary(self):
        """BVA: First day of the calendar year (FMT-DAT-03)."""
        assert format_date("2026-01-01") == "Jan 1, 2026"

    def test_format_date_year_end_boundary(self):
        """BVA: Last day of the calendar year (FMT-DAT-04)."""
        assert format_date("2026-12-31") == "Dec 31, 2026"

    def test_format_date_leap_year_february_29(self):
        """BVA: Leap year February 29 boundary (FMT-DAT-05)."""
        assert format_date("2024-02-29") == "Feb 29, 2024"

    def test_format_date_non_leap_year_february_29_raises_value_error(self):
        """BVA/Exception: Feb 29 on a non-leap year raises ValueError (FMT-DAT-06)."""
        with pytest.raises(ValueError):
            format_date("2026-02-29")

    @pytest.mark.parametrize(
        "invalid_iso",
        [
            "15/06/2026",
            "2026/06/15",
            "2026-10",
            "not-a-date",
            "",
        ],
    )
    def test_format_date_invalid_formats_raises_value_error(self, invalid_iso: str):
        """Invalid ECP: Malformed or non-ISO date strings raise ValueError (FMT-DAT-07)."""
        with pytest.raises(ValueError):
            format_date(invalid_iso)

    def test_format_date_invalid_calendar_month_raises_value_error(self):
        """Invalid ECP: Month out of 1..12 range raises ValueError (FMT-DAT-08)."""
        with pytest.raises(ValueError):
            format_date("2026-13-01")

    def test_format_date_invalid_day_of_month_raises_value_error(self):
        """Invalid ECP: Day exceeding month capacity raises ValueError."""
        with pytest.raises(ValueError):
            format_date("2026-04-31")

    def test_format_date_non_string_type_raises_type_error(self):
        """Exception: Passing None or non-string raises TypeError."""
        with pytest.raises(TypeError):
            format_date(None)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            format_date(20260615)  # type: ignore[arg-type]


@pytest.mark.formatting
@pytest.mark.regression
@pytest.mark.order(8)
class TestFormatRelative:
    """Unit tests for format_relative function applying threshold BVA and ECP.

    Target: format_relative(moment: datetime | None, now: datetime | None = None) -> str
    Techniques: ECP, Discrete Boundary Analysis, Future/Past Symmetry
    Test Count: 9 test methods (covering 16 representative input partitions)
    """

    @pytest.fixture
    def base_now(self) -> datetime:
        """Fixed deterministic reference moment in UTC."""
        return datetime(2026, 10, 23, 12, 0, 0, tzinfo=timezone.utc)

    def test_format_relative_none_returns_never(self):
        """ECP: None moment returns 'never' (FMT-REL-01)."""
        assert format_relative(None) == "never"

    @pytest.mark.parametrize(
        "seconds_delta,expected",
        [
            (0, "just now"),
            (10, "just now"),
            (44, "just now"),
            (-10, "in a moment"),
            (-44, "in a moment"),
        ],
    )
    def test_format_relative_immediate_boundaries(
        self, base_now: datetime, seconds_delta: int, expected: str
    ):
        """BVA: Immediate interval threshold (< 45s) past and future (FMT-REL-02, FMT-REL-03)."""
        moment = base_now - timedelta(seconds=seconds_delta)
        assert format_relative(moment, now=base_now) == expected

    def test_format_relative_minute_threshold_boundary(self, base_now: datetime):
        """BVA: Exact 45s threshold transition to '1 min ago' (FMT-REL-04)."""
        moment = base_now - timedelta(seconds=45)
        assert format_relative(moment, now=base_now) == "1 min ago"

    @pytest.mark.parametrize(
        "seconds_delta,expected",
        [
            (90, "2 min ago"),
            (300, "5 min ago"),
            (3540, "59 min ago"),
        ],
    )
    def test_format_relative_past_minutes(
        self, base_now: datetime, seconds_delta: int, expected: str
    ):
        """ECP: Past minute intervals below 3600 seconds (FMT-REL-05)."""
        moment = base_now - timedelta(seconds=seconds_delta)
        assert format_relative(moment, now=base_now) == expected

    @pytest.mark.parametrize(
        "seconds_delta,expected",
        [
            (-45, "in 1 min"),
            (-300, "in 5 min"),
            (-600, "in 10 min"),
        ],
    )
    def test_format_relative_future_minutes(
        self, base_now: datetime, seconds_delta: int, expected: str
    ):
        """ECP: Future minute intervals (FMT-REL-12)."""
        moment = base_now - timedelta(seconds=seconds_delta)
        assert format_relative(moment, now=base_now) == expected

    @pytest.mark.parametrize(
        "seconds_delta,expected",
        [
            (3600, "1 hr ago"),
            (7200, "2 hr ago"),
            (-7200, "in 2 hr"),
            (86399, "24 hr ago"),
        ],
    )
    def test_format_relative_hour_threshold_boundaries(
        self, base_now: datetime, seconds_delta: int, expected: str
    ):
        """BVA: Hourly interval boundaries and future hours (FMT-REL-06, FMT-REL-07)."""
        moment = base_now - timedelta(seconds=seconds_delta)
        assert format_relative(moment, now=base_now) == expected

    @pytest.mark.parametrize(
        "seconds_delta,expected",
        [
            (86400, "1 day ago"),
            (172800, "2 days ago"),
            (-86400, "in 1 day"),
            (-172800, "in 2 days"),
        ],
    )
    def test_format_relative_day_threshold_and_pluralization(
        self, base_now: datetime, seconds_delta: int, expected: str
    ):
        """BVA/ECP: Daily interval pluralization ('1 day' vs '2 days') (FMT-REL-08, FMT-REL-09)."""
        moment = base_now - timedelta(seconds=seconds_delta)
        assert format_relative(moment, now=base_now) == expected

    @pytest.mark.parametrize(
        "days_delta,is_relative",
        [
            (29, True),   # Within 30 days -> relative
            (31, False),  # 30+ days -> fallback to absolute date
        ],
    )
    def test_format_relative_thirty_day_cutoff_boundaries(
        self, base_now: datetime, days_delta: int, is_relative: bool
    ):
        """BVA: 30-day boundary cutoff transitioning to absolute date (FMT-REL-10, FMT-REL-11)."""
        moment = base_now - timedelta(days=days_delta)
        result = format_relative(moment, now=base_now)
        if is_relative:
            assert result == f"{days_delta} days ago"
        else:
            # Falls back to format_date(moment.astimezone().date().isoformat())
            expected_date = format_date(moment.astimezone().date().isoformat())
            assert result == expected_date

    def test_format_relative_default_now_parameter(self):
        """ECP: Omitting now parameter defaults to current UTC time."""
        recent_moment = datetime.now(timezone.utc) - timedelta(seconds=5)
        assert format_relative(recent_moment) == "just now"


@pytest.mark.formatting
@pytest.mark.regression
@pytest.mark.order(9)
class TestFormatLocal:
    """Unit tests for format_local function applying deterministic time mocking and ECP.

    Target: format_local(moment: datetime | None) -> str
    Techniques: ECP, Mocking Environmental Timezone, Clock Boundaries
    Test Count: 7 test methods (covering 8 representative scenarios)
    """

    def test_format_local_none_returns_empty_string(self):
        """ECP: None moment returns empty string (FMT-LOC-01)."""
        assert format_local(None) == ""

    def test_format_local_afternoon_strips_leading_zero(self):
        """ECP: Afternoon timestamp with hour formatted and leading zero stripped (FMT-LOC-02)."""
        mock_moment = MagicMock(spec=datetime)
        mock_local = MagicMock(spec=datetime)
        mock_local.date.return_value.isoformat.return_value = "2026-09-22"
        mock_local.strftime.return_value = "03:04 PM"
        mock_moment.astimezone.return_value = mock_local

        assert format_local(mock_moment) == "Sep 22, 2026, 3:04 PM"

    def test_format_local_morning_strips_leading_zero(self):
        """ECP: Morning timestamp with single digit hour (FMT-LOC-03)."""
        mock_moment = MagicMock(spec=datetime)
        mock_local = MagicMock(spec=datetime)
        mock_local.date.return_value.isoformat.return_value = "2026-09-22"
        mock_local.strftime.return_value = "09:15 AM"
        mock_moment.astimezone.return_value = mock_local

        assert format_local(mock_moment) == "Sep 22, 2026, 9:15 AM"

    def test_format_local_midnight_boundary(self):
        """BVA: Midnight hour (12:00 AM) boundary preservation (FMT-LOC-04)."""
        mock_moment = MagicMock(spec=datetime)
        mock_local = MagicMock(spec=datetime)
        mock_local.date.return_value.isoformat.return_value = "2026-01-01"
        mock_local.strftime.return_value = "12:00 AM"
        mock_moment.astimezone.return_value = mock_local

        assert format_local(mock_moment) == "Jan 1, 2026, 12:00 AM"

    def test_format_local_noon_boundary(self):
        """BVA: Noon hour (12:00 PM) boundary preservation (FMT-LOC-05)."""
        mock_moment = MagicMock(spec=datetime)
        mock_local = MagicMock(spec=datetime)
        mock_local.date.return_value.isoformat.return_value = "2026-07-04"
        mock_local.strftime.return_value = "12:00 PM"
        mock_moment.astimezone.return_value = mock_local

        assert format_local(mock_moment) == "Jul 4, 2026, 12:00 PM"

    def test_format_local_two_digit_hours(self):
        """ECP: Two-digit hours (10, 11, 12) correctly preserved without stripping."""
        mock_moment = MagicMock(spec=datetime)
        mock_local = MagicMock(spec=datetime)
        mock_local.date.return_value.isoformat.return_value = "2026-12-25"
        mock_local.strftime.return_value = "11:45 PM"
        mock_moment.astimezone.return_value = mock_local

        assert format_local(mock_moment) == "Dec 25, 2026, 11:45 PM"

    def test_format_local_with_real_timezone_aware_moment(self):
        """ECP: Real timezone-aware datetime integration produces valid format."""
        dt = datetime.now(timezone.utc)
        result = format_local(dt)
        assert isinstance(result, str)
        assert len(result) > 0
        assert ", " in result
        assert ("AM" in result) or ("PM" in result)
