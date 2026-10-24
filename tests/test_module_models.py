import pytest
from expense_tracker.models import (
    validate_expense,
    Expense,
    Filters,
    add_expense,
    get_expense,
    update_expense,
    delete_expense,
    list_expenses,
)


@pytest.mark.models
@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.order(1)
class TestFunctionValidateExpense:
    """Unit tests for validate_expense function applying ECP and BVA."""

    def test_valid_expense_inputs(self):
        errors, amount = validate_expense("Coffee", "4.50", "Food", "2026-10-17")
        assert errors == {}
        assert amount == 4.50

    def test_empty_description_invalid(self):
        errors, _ = validate_expense("   ", "10.00", "Food", "2026-10-17")
        assert errors.get("description") == "Description is required."

    def test_description_min_valid_length(self):
        errors, _ = validate_expense("A", "10.00", "Other", "2026-10-17")
        assert "description" not in errors

    def test_description_max_valid_length(self):
        desc = "A" * 120
        errors, _ = validate_expense(desc, "10.00", "Other", "2026-10-17")
        assert "description" not in errors

    def test_description_exceeds_max_length(self):
        desc = "A" * 121
        errors, _ = validate_expense(desc, "10.00", "Other", "2026-10-17")
        assert errors.get("description") == "Keep it under 120 characters."

    def test_non_numeric_amount_invalid(self):
        errors, _ = validate_expense("Lunch", "twenty", "Food", "2026-10-17")
        assert errors.get("amount") == "Enter a valid amount."

    def test_negative_amount_invalid(self):
        errors, _ = validate_expense("Refund", "-15.00", "Bills", "2026-10-17")
        assert errors.get("amount") == "Amount must be greater than $0."

    def test_amount_zero_boundary(self):
        errors, _ = validate_expense("Item", "0.00", "Other", "2026-10-17")
        assert errors.get("amount") == "Amount must be greater than $0."

    def test_amount_minimum_positive_boundary(self):
        errors, amount = validate_expense("Item", "0.01", "Other", "2026-10-17")
        assert "amount" not in errors
        assert amount == 0.01

    def test_amount_max_allowed_boundary(self):
        errors, amount = validate_expense("Car", "1000000.00", "Transportation", "2026-10-17")
        assert "amount" not in errors
        assert amount == 1_000_000.00

    def test_amount_exceeds_max_boundary(self):
        errors, _ = validate_expense("House", "1000000.01", "Bills", "2026-10-17")
        assert errors.get("amount") == "That amount looks too large."

    def test_invalid_category(self):
        errors, _ = validate_expense("Movie", "15.00", "NonExistentCategory", "2026-10-17")
        assert errors.get("category") == "Choose a valid category."

    def test_invalid_date_format(self):
        errors, _ = validate_expense("Dinner", "25.00", "Food", "17/10/2026")
        assert errors.get("date") == "Enter a valid date."

    def test_empty_date(self):
        errors, _ = validate_expense("Dinner", "25.00", "Food", "")
        assert errors.get("date") == "Date is required."


@pytest.mark.models
@pytest.mark.regression
@pytest.mark.order(2)
class TestClassExpense:
    """Unit tests for Expense dataclass and Expense.from_row method."""

    def test_expense_direct_instantiation(self):
        e = Expense(1, "Groceries", 50.0, "Food", "2026-10-17", "2026-10-17T10:00:00")
        assert e.id == 1
        assert e.description == "Groceries"
        assert e.amount == 50.0

    def test_expense_from_row_mapping(self):
        mock_row = {
            "id": 10,
            "description": "Subway",
            "amount": 7.50,
            "category": "Food",
            "date": "2026-10-17",
            "created_at": "2026-10-17T11:00:00Z"
        }
        e = Expense.from_row(mock_row)
        assert e.id == 10
        assert e.description == "Subway"
        assert e.amount == 7.50
        assert e.category == "Food"

    def test_expense_equality(self):
        e1 = Expense(1, "Item", 10.0, "Other", "2026-10-17", "2026-10-17T10:00:00")
        e2 = Expense(1, "Item", 10.0, "Other", "2026-10-17", "2026-10-17T10:00:00")
        assert e1 == e2

    def test_expense_inequality(self):
        e1 = Expense(1, "Item", 10.0, "Other", "2026-10-17", "2026-10-17T10:00:00")
        e2 = Expense(2, "Item", 10.0, "Other", "2026-10-17", "2026-10-17T10:00:00")
        assert e1 != e2

    def test_filters_dataclass_defaults(self):
        f = Filters()
        assert f.search == ""
        assert f.category == "All"
        assert f.sort == "date-desc"


@pytest.mark.models
@pytest.mark.regression
@pytest.mark.order(3)
class TestFunctionsAddAndGetExpense:
    """Unit tests for add_expense and get_expense functions."""

    def test_add_expense_returns_valid_id(self, app):
        with app.app_context():
            new_id = add_expense("Test Lunch", 12.50, "Food", "2026-10-17")
            assert isinstance(new_id, int)
            assert new_id > 0

    def test_get_expense_retrieves_created_record(self, app):
        with app.app_context():
            new_id = add_expense("Metro Pass", 30.00, "Transportation", "2026-10-15")
            exp = get_expense(new_id)
            assert exp is not None
            assert exp.description == "Metro Pass"
            assert exp.amount == 30.00
            assert exp.category == "Transportation"
            assert exp.date == "2026-10-15"

    def test_get_expense_nonexistent_id_returns_none(self, app):
        with app.app_context():
            assert get_expense(999999) is None

    def test_add_expense_strips_description_whitespace(self, app):
        with app.app_context():
            new_id = add_expense("   Books   ", 45.00, "Shopping", "2026-10-16")
            exp = get_expense(new_id)
            assert exp.description == "Books"

    def test_add_multiple_expenses_unique_ids(self, app):
        with app.app_context():
            id1 = add_expense("Item 1", 10.0, "Other", "2026-10-17")
            id2 = add_expense("Item 2", 20.0, "Other", "2026-10-17")
            assert id2 > id1

    def test_add_expense_boundary_amount(self, app):
        with app.app_context():
            new_id = add_expense("Penny item", 0.01, "Other", "2026-10-17")
            exp = get_expense(new_id)
            assert exp.amount == 0.01


@pytest.mark.models
@pytest.mark.regression
@pytest.mark.order(4)
class TestFunctionUpdateExpense:
    """Unit tests for update_expense function."""

    def test_update_expense_description_and_amount(self, app):
        with app.app_context():
            new_id = add_expense("Old Name", 10.00, "Food", "2026-10-17")
            update_expense(new_id, "New Name", 25.00, "Food", "2026-10-17")
            exp = get_expense(new_id)
            assert exp.description == "New Name"
            assert exp.amount == 25.00

    def test_update_expense_category_change(self, app):
        with app.app_context():
            new_id = add_expense("Uber", 20.00, "Other", "2026-10-17")
            update_expense(new_id, "Uber", 20.00, "Transportation", "2026-10-17")
            exp = get_expense(new_id)
            assert exp.category == "Transportation"

    def test_update_expense_date_change(self, app):
        with app.app_context():
            new_id = add_expense("Dinner", 40.00, "Food", "2026-10-01")
            update_expense(new_id, "Dinner", 40.00, "Food", "2026-10-10")
            exp = get_expense(new_id)
            assert exp.date == "2026-10-10"

    def test_update_expense_whitespace_trimming(self, app):
        with app.app_context():
            new_id = add_expense("Coffee", 3.00, "Food", "2026-10-17")
            update_expense(new_id, "   Latte   ", 4.50, "Food", "2026-10-17")
            exp = get_expense(new_id)
            assert exp.description == "Latte"

    def test_update_nonexistent_id_no_error(self, app):
        with app.app_context():
            update_expense(88888, "Ghost", 10.0, "Other", "2026-10-17")
            assert get_expense(88888) is None


@pytest.mark.models
@pytest.mark.regression
@pytest.mark.order(5)
class TestFunctionDeleteExpense:
    """Unit tests for delete_expense function."""

    def test_delete_existing_expense(self, app):
        with app.app_context():
            new_id = add_expense("To Delete", 15.00, "Food", "2026-10-17")
            assert get_expense(new_id) is not None
            delete_expense(new_id)
            assert get_expense(new_id) is None

    def test_delete_nonexistent_expense(self, app):
        with app.app_context():
            delete_expense(777777)

    def test_delete_does_not_affect_other_expenses(self, app):
        with app.app_context():
            id1 = add_expense("Keep 1", 10.0, "Food", "2026-10-17")
            id2 = add_expense("Remove", 20.0, "Food", "2026-10-17")
            id3 = add_expense("Keep 2", 30.0, "Food", "2026-10-17")

            delete_expense(id2)
            assert get_expense(id1) is not None
            assert get_expense(id2) is None
            assert get_expense(id3) is not None

    def test_double_delete_same_id(self, app):
        with app.app_context():
            new_id = add_expense("Duplicate Delete", 5.0, "Other", "2026-10-17")
            delete_expense(new_id)
            delete_expense(new_id)
            assert get_expense(new_id) is None

    def test_delete_all_one_by_one(self, app):
        with app.app_context():
            id1 = add_expense("A", 1.0, "Other", "2026-10-17")
            id2 = add_expense("B", 2.0, "Other", "2026-10-17")
            delete_expense(id1)
            delete_expense(id2)
            assert len(list_expenses(Filters())) == 0
