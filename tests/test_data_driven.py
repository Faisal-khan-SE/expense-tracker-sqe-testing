"""Data-driven test suite consuming external CSV test resources.

This module loads test cases from tests/data/test_cases.csv and uses pytest
parameterization to drive automated validation of expense_tracker.models.validate_expense.

Traceability:
- Task 3 deliverable: External CSV data source consumed by automated tests
- Marker: @pytest.mark.data_driven
- Contributor: M-Ehtasham-SE (Lead QA / SQE Contributor)
"""

import csv
from pathlib import Path
from typing import Any
import pytest

from expense_tracker.models import validate_expense

CSV_PATH = Path(__file__).parent / "data" / "test_cases.csv"

REQUIRED_HEADERS = {
    "test_id",
    "test_title",
    "description",
    "amount_raw",
    "category",
    "date_raw",
    "expected_valid",
}


def load_csv_test_cases(path: Path = CSV_PATH) -> list[dict[str, Any]]:
    """Loads and validates test cases from the specified CSV file.

    Resolves path relative to file structure, validates presence of required
    columns, and returns clean dictionary rows.
    """
    if not path.exists():
        raise FileNotFoundError(f"External CSV test data resource not found at: {path}")

    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not REQUIRED_HEADERS.issubset(set(reader.fieldnames)):
            missing = REQUIRED_HEADERS - set(reader.fieldnames or [])
            raise ValueError(f"CSV file is missing required headers: {missing}")

        for line_num, row in enumerate(reader, start=2):
            # Skip empty lines or pure whitespace rows
            if not any(v.strip() for v in row.values() if v):
                continue
            # Validate row integrity
            test_id = (row.get("test_id") or "").strip()
            if not test_id:
                raise ValueError(f"Malformed row at line {line_num}: missing test_id")
            records.append(row)

    if not records:
        raise ValueError(f"No test cases loaded from {path}")

    return records


# Pre-load records for pytest parameterization
CSV_RECORDS = load_csv_test_cases()


@pytest.mark.data_driven
@pytest.mark.regression
@pytest.mark.order(14)
class TestDataDrivenExpenseValidation:
    """Data-driven test suite executing cases loaded dynamically from external CSV."""

    def test_csv_resource_exists_and_meets_minimum_count(self):
        """Task 3 check: Verify external CSV exists, has valid headers, and >= 4 records."""
        assert CSV_PATH.exists(), f"CSV resource missing at {CSV_PATH}"
        records = load_csv_test_cases(CSV_PATH)
        assert len(records) >= 4, f"Assignment requires >= 4 test cases, found {len(records)}"

    def test_loader_validates_missing_file_raises_filenotfound(self, tmp_path: Path):
        """Verify loader raises FileNotFoundError when given non-existent file."""
        non_existent = tmp_path / "does_not_exist.csv"
        with pytest.raises(FileNotFoundError):
            load_csv_test_cases(non_existent)

    def test_loader_rejects_missing_required_headers(self, tmp_path: Path):
        """Verify loader raises ValueError when required headers are absent."""
        bad_csv = tmp_path / "bad_headers.csv"
        bad_csv.write_text("test_id,description\nTC-01,Test\n", encoding="utf-8")
        with pytest.raises(ValueError, match="missing required headers"):
            load_csv_test_cases(bad_csv)

    def test_loader_rejects_malformed_row_missing_test_id(self, tmp_path: Path):
        """Verify loader raises ValueError for malformed records without test_id."""
        malformed_csv = tmp_path / "malformed.csv"
        content = (
            "test_id,test_title,description,amount_raw,category,date_raw,expected_valid\n"
            ",Missing ID,Coffee,4.50,Food,2026-10-15,true\n"
        )
        malformed_csv.write_text(content, encoding="utf-8")
        with pytest.raises(ValueError, match="missing test_id"):
            load_csv_test_cases(malformed_csv)

    @pytest.mark.parametrize("row", CSV_RECORDS, ids=lambda r: f"{r['test_id']}: {r['test_title']}")
    def test_validate_expense_driven_by_csv(self, row: dict[str, Any]):
        """Parametrized test executing real application function driven by CSV dataset."""
        description = row["description"]
        amount_raw = row["amount_raw"]
        category = row["category"]
        date_raw = row["date_raw"]
        is_valid = row["expected_valid"].strip().lower() == "true"

        errors, parsed_amount = validate_expense(description, amount_raw, category, date_raw)

        if is_valid:
            assert errors == {}, f"Expected valid expense for {row['test_id']}, got errors: {errors}"
            expected_amt = float(row["expected_amount"])
            assert parsed_amount == expected_amt, (
                f"Parsed amount mismatch for {row['test_id']}: expected {expected_amt}, got {parsed_amount}"
            )
        else:
            expected_field = (row.get("expected_error_field") or "").strip()
            expected_msg = (row.get("expected_error_message") or "").strip()

            assert expected_field in errors, (
                f"Expected error field '{expected_field}' not in errors: {errors} for {row['test_id']}"
            )
            assert errors[expected_field] == expected_msg, (
                f"Error message mismatch for {row['test_id']}. Expected: '{expected_msg}', Got: '{errors[expected_field]}'"
            )
