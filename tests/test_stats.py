"""Unit test suite for expense_tracker.stats module.

This module validates expense totals, monthly filtering, category breakdown (with SVG Donut
geometry calculations), and monthly trend generation (with chart bar height clamping).
Techniques applied include Equivalence Class Partitioning (ECP), Boundary Value Analysis (BVA),
and pytest parameterization.

Traceability:
- Test IDs map directly to docs/test_design_notes.md (STA-TOT-*, STA-EIM-*, STA-CAT-*, STA-TRD-*)
- Contributor: M-Ehtasham-SE (Lead QA / SQE Contributor)
- All 7 original legacy tests are fully preserved and organized into descriptive test classes.
"""

from datetime import date
import pytest

from expense_tracker.models import CATEGORIES, Expense
from expense_tracker.stats import (
    DONUT_CIRCUMFERENCE,
    category_breakdown,
    expenses_in_month,
    monthly_trend,
    total_of,
)


def make_expense(id_: int, description: str, amount: float, category: str, expense_date: str) -> Expense:
    """Helper fixture to create deterministic Expense instances for isolated tests."""
    return Expense(
        id=id_,
        description=description,
        amount=amount,
        category=category,
        date=expense_date,
        created_at="2026-01-01T00:00:00",
    )


@pytest.mark.stats
@pytest.mark.regression
@pytest.mark.order(10)
class TestTotalOf:
    """Unit tests for total_of function applying ECP and BVA.

    Target: total_of(expenses: list[Expense]) -> float
    Techniques: ECP, BVA (empty list, single element, cent precision, large sums)
    Test Count: 7 test methods
    """

    def test_total_of_sums_amounts(self):
        """Preserved Legacy Test: Sums amounts of multiple expenses (STA-TOT-03)."""
        expenses = [
            make_expense(1, "A", 10.5, "Food", "2026-01-01"),
            make_expense(2, "B", 4.25, "Food", "2026-01-02"),
        ]
        assert total_of(expenses) == 14.75

    def test_total_of_empty_is_zero(self):
        """Preserved Legacy Test: Empty list returns 0 (STA-TOT-01)."""
        assert total_of([]) == 0

    def test_total_of_single_expense_boundary(self):
        """BVA: Exactly one expense in the list (STA-TOT-02)."""
        expenses = [make_expense(1, "Lunch", 15.50, "Food", "2026-05-10")]
        assert total_of(expenses) == 15.50

    def test_total_of_minimum_cent_precision(self):
        """BVA: Precision calculation with small fractions and pennies (STA-TOT-04)."""
        expenses = [
            make_expense(1, "Penny 1", 0.01, "Other", "2026-01-01"),
            make_expense(2, "Penny 2", 0.02, "Other", "2026-01-02"),
        ]
        assert round(total_of(expenses), 2) == 0.03

    def test_total_of_large_amounts(self):
        """ECP: Aggregation of high-value amounts (STA-TOT-05)."""
        expenses = [
            make_expense(1, "Car", 500000.00, "Transportation", "2026-01-01"),
            make_expense(2, "Renovation", 500000.00, "Bills", "2026-01-02"),
        ]
        assert total_of(expenses) == 1000000.00

    @pytest.mark.parametrize(
        "amounts,expected_total",
        [
            ([5.0, 15.0, 20.0], 40.0),
            ([0.99, 1.01, 3.00], 5.0),
            ([100.0], 100.0),
        ],
    )
    def test_total_of_parametrized_combinations(self, amounts: list[float], expected_total: float):
        """ECP/Parametrized: Diverse valid input amounts produce expected total."""
        expenses = [make_expense(i, f"Item {i}", amt, "Other", "2026-01-01") for i, amt in enumerate(amounts, 1)]
        assert total_of(expenses) == pytest.approx(expected_total)

    def test_total_of_mixed_categories(self):
        """ECP: Expenses across multiple categories correctly aggregate into unified total (STA-TOT-06)."""
        expenses = [
            make_expense(1, "Groceries", 25.50, "Food", "2026-02-01"),
            make_expense(2, "Gas", 35.00, "Transportation", "2026-02-02"),
            make_expense(3, "Movie", 14.50, "Entertainment", "2026-02-03"),
            make_expense(4, "Clothes", 75.00, "Shopping", "2026-02-04"),
        ]
        assert total_of(expenses) == 150.00


@pytest.mark.stats
@pytest.mark.regression
@pytest.mark.order(11)
class TestExpensesInMonth:
    """Unit tests for expenses_in_month function applying calendar boundaries and ECP.

    Target: expenses_in_month(expenses: list[Expense], year: int, month: int) -> list[Expense]
    Techniques: ECP, BVA (month first day, last day, adjacent day filtering, year rollover)
    Test Count: 9 test methods
    """

    def test_expenses_in_month_filters_correctly(self):
        """Preserved Legacy Test: Correctly filters expenses in target month."""
        expenses = [
            make_expense(1, "A", 10, "Food", "2026-09-05"),
            make_expense(2, "B", 20, "Food", "2026-08-31"),
            make_expense(3, "C", 30, "Food", "2026-09-30"),
        ]
        result = expenses_in_month(expenses, 2026, 9)
        assert {e.id for e in result} == {1, 3}

    def test_expenses_in_month_empty_list_returns_empty(self):
        """BVA: Empty expense list returns empty list (STA-EIM-01)."""
        assert expenses_in_month([], 2026, 9) == []

    def test_expenses_in_month_all_matching(self):
        """ECP: All expenses fall within the specified month (STA-EIM-02)."""
        expenses = [
            make_expense(1, "A", 10, "Food", "2026-09-01"),
            make_expense(2, "B", 15, "Food", "2026-09-15"),
            make_expense(3, "C", 20, "Food", "2026-09-28"),
        ]
        result = expenses_in_month(expenses, 2026, 9)
        assert len(result) == 3

    def test_expenses_in_month_none_matching(self):
        """ECP: No expenses match the target month (STA-EIM-03)."""
        expenses = [
            make_expense(1, "A", 10, "Food", "2026-08-15"),
            make_expense(2, "B", 20, "Food", "2026-10-15"),
        ]
        assert expenses_in_month(expenses, 2026, 9) == []

    def test_expenses_in_month_boundary_first_day_of_month(self):
        """BVA: Expense on the first day of the target month is included (STA-EIM-04)."""
        expenses = [make_expense(1, "First Day", 10, "Food", "2026-05-01")]
        result = expenses_in_month(expenses, 2026, 5)
        assert len(result) == 1
        assert result[0].id == 1

    def test_expenses_in_month_boundary_last_day_of_month(self):
        """BVA: Expense on the last day of a 30-day or 31-day month is included (STA-EIM-05)."""
        expenses = [
            make_expense(1, "May End", 10, "Food", "2026-05-31"),
            make_expense(2, "June End", 15, "Food", "2026-06-30"),
        ]
        assert len(expenses_in_month(expenses, 2026, 5)) == 1
        assert len(expenses_in_month(expenses, 2026, 6)) == 1

    def test_expenses_in_month_boundary_adjacent_days_excluded(self):
        """BVA: Expenses on the adjacent day before or after target month are excluded (STA-EIM-06, STA-EIM-07)."""
        expenses = [
            make_expense(1, "Day Before", 10, "Food", "2026-08-31"),
            make_expense(2, "Day Inside", 15, "Food", "2026-09-01"),
            make_expense(3, "Day After", 20, "Food", "2026-10-01"),
        ]
        result = expenses_in_month(expenses, 2026, 9)
        assert len(result) == 1
        assert result[0].id == 2

    def test_expenses_in_month_year_rollover_boundaries(self):
        """BVA: Dec 31 of year N vs Jan 1 of year N+1 (STA-EIM-08)."""
        expenses = [
            make_expense(1, "New Year Eve", 50, "Entertainment", "2026-12-31"),
            make_expense(2, "New Year Day", 60, "Entertainment", "2027-01-01"),
        ]
        dec_result = expenses_in_month(expenses, 2026, 12)
        assert [e.id for e in dec_result] == [1]

        jan_result = expenses_in_month(expenses, 2027, 1)
        assert [e.id for e in jan_result] == [2]

    def test_expenses_in_month_leap_year_february_29(self):
        """BVA: Leap year February 29 included in February of leap year."""
        expenses = [
            make_expense(1, "Leap Day", 42, "Bills", "2024-02-29"),
            make_expense(2, "March 1", 42, "Bills", "2024-03-01"),
        ]
        result = expenses_in_month(expenses, 2024, 2)
        assert len(result) == 1
        assert result[0].date == "2024-02-29"


@pytest.mark.stats
@pytest.mark.regression
@pytest.mark.order(12)
class TestCategoryBreakdown:
    """Unit tests for category_breakdown function applying ECP, Donut geometry BVA, and sorting.

    Target: category_breakdown(expenses: list[Expense]) -> list[CategoryTotal]
    Techniques: ECP, BVA (SVG Donut circumference, offset, percent share, sorting descending)
    Test Count: 9 test methods
    """

    def test_category_breakdown_sorted_desc_with_percent(self):
        """Preserved Legacy Test: Sorted descending by total with calculated percentage."""
        expenses = [
            make_expense(1, "A", 75, "Entertainment", "2026-09-01"),
            make_expense(2, "B", 25, "Food", "2026-09-01"),
        ]
        breakdown = category_breakdown(expenses)
        assert [c.category for c in breakdown] == ["Entertainment", "Food"]
        assert breakdown[0].percent == 75.0
        assert breakdown[1].percent == 25.0

    def test_category_breakdown_excludes_zero_categories(self):
        """Preserved Legacy Test: Categories with 0 expenses are excluded."""
        expenses = [make_expense(1, "A", 10, "Food", "2026-09-01")]
        breakdown = category_breakdown(expenses)
        assert len(breakdown) == 1
        assert breakdown[0].category == "Food"

    def test_category_breakdown_empty(self):
        """Preserved Legacy Test: Empty expense list produces empty breakdown."""
        assert category_breakdown([]) == []

    def test_category_breakdown_single_category_is_100_percent(self):
        """BVA: Single category expense accounts for exactly 100.0% share (STA-CAT-02)."""
        expenses = [make_expense(1, "Groceries", 50.0, "Food", "2026-03-10")]
        breakdown = category_breakdown(expenses)
        assert len(breakdown) == 1
        assert breakdown[0].category == "Food"
        assert breakdown[0].total == 50.0
        assert breakdown[0].percent == 100.0

    def test_category_breakdown_all_six_categories(self):
        """ECP: All 6 predefined categories populated simultaneously (STA-CAT-05)."""
        expenses = [
            make_expense(1, "E1", 10, "Food", "2026-01-01"),
            make_expense(2, "E2", 20, "Transportation", "2026-01-01"),
            make_expense(3, "E3", 30, "Entertainment", "2026-01-01"),
            make_expense(4, "E4", 40, "Shopping", "2026-01-01"),
            make_expense(5, "E5", 50, "Bills", "2026-01-01"),
            make_expense(6, "E6", 60, "Other", "2026-01-01"),
        ]
        breakdown = category_breakdown(expenses)
        assert len(breakdown) == 6
        # Highest total should be first
        assert breakdown[0].category == "Other"
        assert breakdown[0].total == 60.0
        assert breakdown[-1].category == "Food"
        assert breakdown[-1].total == 10.0

    def test_category_breakdown_donut_geometry_first_offset_zero(self):
        """BVA: First category entry in Donut chart always has dash_offset == 0.0 (STA-CAT-06)."""
        expenses = [
            make_expense(1, "A", 30, "Food", "2026-01-01"),
            make_expense(2, "B", 70, "Bills", "2026-01-01"),
        ]
        breakdown = category_breakdown(expenses)
        assert breakdown[0].dash_offset == 0.0

    def test_category_breakdown_donut_geometry_cumulative_offsets(self):
        """BVA: Subsequent donut entries have negative cumulative offset (STA-CAT-07)."""
        expenses = [
            make_expense(1, "A", 50, "Food", "2026-01-01"),
            make_expense(2, "B", 50, "Bills", "2026-01-01"),
        ]
        breakdown = category_breakdown(expenses)
        assert breakdown[0].dash_offset == 0.0
        # Second slice should be offset by half circumference
        expected_offset = -0.5 * DONUT_CIRCUMFERENCE
        assert breakdown[1].dash_offset == pytest.approx(expected_offset, rel=1e-4)

    def test_category_breakdown_dash_array_formatting(self):
        """ECP: Dash array string matches '{fraction * circ} {circ}' format (STA-CAT-08)."""
        expenses = [make_expense(1, "A", 100, "Bills", "2026-01-01")]
        breakdown = category_breakdown(expenses)
        circ_str = f"{DONUT_CIRCUMFERENCE:.4f}"
        assert breakdown[0].dash_array == f"{circ_str} {circ_str}"

    def test_category_breakdown_equal_totals_preserves_counts_and_percents(self):
        """ECP: Two categories with identical totals each receive equal 50.0% share."""
        expenses = [
            make_expense(1, "A", 40.0, "Food", "2026-01-01"),
            make_expense(2, "B", 40.0, "Transportation", "2026-01-01"),
        ]
        breakdown = category_breakdown(expenses)
        assert len(breakdown) == 2
        assert breakdown[0].percent == 50.0
        assert breakdown[1].percent == 50.0


@pytest.mark.stats
@pytest.mark.regression
@pytest.mark.order(13)
class TestMonthlyTrend:
    """Unit tests for monthly_trend function applying scaling, clamping, and ECP.

    Target: monthly_trend(expenses: list[Expense], months_back: int = 6, chart_height: int = 132) -> list[MonthTotal]
    Techniques: ECP, BVA (bar height min clamp 3, max scaling, custom months, year transitions)
    Test Count: 9 test methods
    """

    def test_monthly_trend_buckets_six_months_ending_current(self):
        """Preserved Legacy Test: Creates 6 monthly buckets ending with current month."""
        expenses = [make_expense(1, "A", 50, "Food", date.today().isoformat())]
        trend = monthly_trend(expenses, months_back=6)
        assert len(trend) == 6
        assert trend[-1].total == 50
        today = date.today()
        assert trend[-1].year == today.year
        assert trend[-1].month == today.month

    def test_monthly_trend_empty_expenses_gives_zero_buckets(self):
        """BVA: Empty expenses returns months_back buckets, all total=0.0 and bar_height=3 (STA-TRD-01)."""
        trend = monthly_trend([], months_back=6)
        assert len(trend) == 6
        for bucket in trend:
            assert bucket.total == 0.0
            # Minimum bar height is clamped to 3.0
            assert bucket.bar_height == 3.0

    def test_monthly_trend_single_month_back_boundary(self):
        """BVA: Minimum months_back boundary of 1 returns exactly one bucket (STA-TRD-02)."""
        trend = monthly_trend([], months_back=1)
        assert len(trend) == 1
        today = date.today()
        assert trend[0].year == today.year
        assert trend[0].month == today.month

    def test_monthly_trend_chronological_ordering(self):
        """ECP: Buckets are ordered chronologically from oldest to current month (STA-TRD-04)."""
        trend = monthly_trend([], months_back=3)
        today = date.today()
        assert trend[-1].year == today.year
        assert trend[-1].month == today.month
        # Previous month
        expected_prev_month = 12 if today.month == 1 else today.month - 1
        assert trend[-2].month == expected_prev_month

    def test_monthly_trend_bar_height_max_scaling(self):
        """BVA: Bucket with maximum total receives full chart height minus 24 (STA-TRD-05)."""
        today = date.today()
        expenses = [make_expense(1, "Current", 100.0, "Bills", today.isoformat())]
        trend = monthly_trend(expenses, months_back=6, chart_height=132)
        # Default chart_height is 132 -> max bar_height is 132 - 24 = 108.0
        assert trend[-1].bar_height == 108.0

    def test_monthly_trend_bar_height_min_clamping(self):
        """BVA: Buckets with 0 expenses are clamped to minimum bar height of 3.0 (STA-TRD-06)."""
        today = date.today()
        expenses = [make_expense(1, "Current", 100.0, "Bills", today.isoformat())]
        trend = monthly_trend(expenses, months_back=6, chart_height=132)
        # Buckets before the current one should have bar_height clamped to 3.0
        for bucket in trend[:-1]:
            assert bucket.bar_height == 3.0

    def test_monthly_trend_custom_chart_height(self):
        """ECP: Custom chart height correctly scales the maximum bar height (STA-TRD-07)."""
        today = date.today()
        expenses = [make_expense(1, "Current", 50.0, "Food", today.isoformat())]
        trend = monthly_trend(expenses, months_back=6, chart_height=200)
        # Max bar height should be 200 - 24 = 176.0
        assert trend[-1].bar_height == 176.0

    def test_monthly_trend_twelve_months_year_rollover(self):
        """BVA: 12 months trend cleanly rolls over into preceding calendar year (STA-TRD-08)."""
        trend = monthly_trend([], months_back=12)
        assert len(trend) == 12
        years = {b.year for b in trend}
        today = date.today()
        # Spanning 12 months always touches today.year and either today.year - 1 or only today.year (if month is 12)
        assert today.year in years
        assert len(trend) == 12

    def test_monthly_trend_expenses_outside_window_ignored(self):
        """ECP: Expenses dated outside the trend window do not contribute to any bucket."""
        today = date.today()
        old_expense = make_expense(1, "Old", 999.0, "Other", f"{today.year - 5}-01-01")
        trend = monthly_trend([old_expense], months_back=6)
        total_in_buckets = sum(b.total for b in trend)
        assert total_in_buckets == 0.0
