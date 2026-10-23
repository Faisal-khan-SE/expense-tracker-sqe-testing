# Assignment 3 Audit Report — Build Unit Test Automation Solution

| Field | Value |
|---|---|
| **Auditor** | Antigravity (AI senior test engineer) |
| **Date** | 2026-10-23 |
| **Branch** | `main` |
| **Commit at audit** | `c3581bd` — Task 1 & 4 + Module 1 |
| **Python** | 3.14.7 |
| **Pytest** | 8.4.1 |

---

## 1. Project Overview

**Name:** Expense Tracker (Python / Flask)
**Purpose:** A personal-finance web app — add, edit, delete, search, filter, and export expenses.
Built with Flask, Jinja2 templates, vanilla CSS/JS, and a local SQLite database (no ORM).
Data export supports CSV, JSON, and PDF via a shared export engine, plus a full "Export Center"
with background jobs, sharing links, recurring schedules, and simulated cloud delivery.

**Dependencies (runtime):** `Flask==3.1.2`, `segno==1.6.6`
**Dependencies (dev/test):** `pytest==8.4.1`, `pytest-xdist>=3.8.0`, `pytest-order>=1.5.0`, `openpyxl>=3.1.5`
**Setup:** `pip install -r requirements-dev.txt` then `pytest -v`
**Run app:** `python app.py` → http://127.0.0.1:5000

---

## 2. Existing Files and Completed Work

### Source Modules (`expense_tracker/`)

| File | Purpose |
|---|---|
| `__init__.py` | App factory, Jinja filter registration, blueprint wiring |
| `models.py` | `Expense` dataclass, `Filters` dataclass, `validate_expense`, CRUD functions |
| `stats.py` | `total_of`, `expenses_in_month`, `category_breakdown`, `monthly_trend` |
| `formatting.py` | `format_currency`, `format_date`, `format_relative`, `format_local` |
| `csv_export.py` | `expenses_to_csv` — thin wrapper over the shared export engine |
| `categories.py` | `category_color` mapping, `CATEGORY_PRINT_RGB` |
| `db.py` | SQLite connection, schema management |
| `exports/` | Shared export engine: CSV/JSON/PDF formats, options parsing, report builder |
| `cloud/` | Export Center: job queue, templates, store, schedules, sharing, live sync |
| `routes/` | Flask blueprints: dashboard, expenses, export dialog, Export Center, share links |

### Test Files (`tests/`)

| File | Tests | Notes |
|---|---|---|
| `test_module_models.py` | 34 | **Newly added (c3581bd).** 5 ordered classes with `@pytest.mark.models` and `@pytest.mark.smoke` |
| `test_exports.py` | 25 | Parameterised; covers options parsing, sanitize_filename, CSV/JSON/PDF, routes |
| `test_export_center.py` | 51 | Full Export Center: templates, job lifecycle, CSRF, sharing, schedules, retention |
| `test_routes.py` | 8 | HTTP integration tests for CRUD routes |
| `test_stats.py` | 7 | Unit tests for stats module — **bare functions, no class/marker structure** |
| `test_csv_export.py` | 5 | Unit tests for `csv_export` and `csvutil` helpers |
| `test_validation.py` | 8 | Tests for `validate_expense` (partially duplicates `test_module_models.py`) |
| `conftest.py` | — | Shared `app` and `client` fixtures using temp SQLite DB |

### Configuration Files

| File | Content |
|---|---|
| `pytest.ini` | testpaths, naming conventions, 6 markers, `--strict-markers`, `-v` |
| `requirements-dev.txt` | pytest, pytest-xdist, pytest-order, openpyxl |
| `requirements.txt` | Flask, segno |
| `README.md` | Setup instructions, running tests, project structure |
| `code-analysis.md` | Detailed analysis of three export implementation versions |

---

## 3. Baseline Test Execution Results

**Command:**
```
pytest -v --tb=short
```

**Environment:** Python 3.14.7 · pytest 8.4.1 · pytest-order 1.5.0 · pytest-xdist 3.8.0 · Windows 11

**Result: 148 passed in 28.77s — 0 failures, 0 warnings, 0 skips**

| Test file | Collected | Passed | Failed |
|---|---|---|---|
| `test_module_models.py` | 34 | 34 | 0 |
| `test_export_center.py` | 51 | 51 | 0 |
| `test_exports.py` | 25 | 25 | 0 |
| `test_routes.py` | 8 | 8 | 0 |
| `test_stats.py` | 7 | 7 | 0 |
| `test_csv_export.py` | 5 | 5 | 0 |
| `test_validation.py` | 8 | 8 | 0 |
| **TOTAL** | **148** | **148** | **0** |

---

## 4. Requirement-by-Requirement Status Table

### Task 1 — Project Setup

| Requirement | Status | Evidence / Notes |
|---|---|---|
| Use an open-source Python application | **PASS** | Flask Expense Tracker; confirmed in repo |
| Set up local development environment | **PASS** | `requirements.txt` / `requirements-dev.txt` present; README has clear steps |
| Record a short setup demonstration video | **FAIL** | No video file found anywhere. No `.mp4/.mkv/.webm/.mov` exists. No link in README or docs. |

### Task 2 — Test Design and Automated Unit Tests

| Requirement | Status | Evidence / Notes |
|---|---|---|
| Select three different application modules | **PARTIAL** | Two modules formally covered (`models.py`, `formatting.py`). One remaining (`stats.py`). |
| Apply ECP, BVA, and other techniques | **PASS** (Modules 1 & 2) | `test_module_models.py` and `test_formatting.py` apply rigorous ECP, BVA, parameterization, and exception testing |
| Document test design notes per module | **PASS** | Complete specification created at [docs/test_design_notes.md](file:///d:/expense-tracker-sqe-testing/docs/test_design_notes.md) covering all 3 modules (98 test cases designed, ECP/BVA tables, constraints, ambiguity analysis, and contributor matrix) |
| 5–10 automated unit tests per function | **PASS** (Modules 1 & 2) | `validate_expense`: 14; `Expense`/`Filters`: 5; `add`/`get`: 6; `update`: 5; `delete`: 5; `format_currency`: 8 (16); `format_date`: 9 (14); `format_relative`: 9 (26); `format_local`: 7 |
| 5–10 automated unit tests per class/module | **PASS** (Modules 1 & 2) | Each class meets the ≥ 5 threshold (Module 1: 34 tests; Module 2: 33 methods, 63 test executions) |
| Module 2 tests | **PASS** | Implemented in `tests/test_formatting.py` with 4 classes, 33 methods, 63 passing tests |
| Module 3 tests | **FAIL** | No dedicated test class for Module 3 (recommended: `stats.py` restructure) |

### Task 3 — Excel Test-Case Sheet and CSV Data Source

| Requirement | Status | Evidence / Notes |
|---|---|---|
| Excel test-case sheet with ≥ 4 test cases | **FAIL** | No `.xlsx` or `.xls` file exists anywhere in the repository |
| Consume test data from an external CSV | **FAIL** | No CSV data file in `tests/`. `data_driven` marker declared in `pytest.ini` but **zero** tests use it |

### Task 4 — Parallel Execution, Suites, Groups, Ordering

| Requirement | Status | Evidence / Notes |
|---|---|---|
| Configure parallel execution | **PARTIAL** | `pytest-xdist` installed. `pytest.ini` `addopts` does **not** include `-n auto`. Not enabled by default. |
| Define different test suites / groups | **PARTIAL** | 6 markers declared. `models` and `smoke` actively used. `regression`, `formatting`, `stats`, `data_driven` are **all unused**. |
| Use data-driven parameterization | **PARTIAL** | `test_exports.py` and `test_export_center.py` use `@pytest.mark.parametrize` well. `test_module_models.py` uses **none**. |
| Configure execution order of test groups/cases | **PASS** | `test_module_models.py` uses `@pytest.mark.order(1)` through `order(5)`. `pytest-order` is installed and active. |

---

## 5. Three Recommended Modules and Their Testable Functions/Classes

### Module 1 — `expense_tracker/models.py` (DONE)

**Key targets:** `validate_expense`, `Expense`, `Filters`, `add_expense`, `get_expense`, `update_expense`, `delete_expense`
**Why:** Core business logic; pure validation is ideal for ECP/BVA; DB functions use isolated temp SQLite.
**Status:** 34 tests, all passing. Classes well-structured and ordered.

### Module 2 — `expense_tracker/formatting.py` (MISSING)

**Key targets and techniques:**
- `format_currency(amount)` — ECP: positive, zero, negative, large float; BVA: 0.00, 0.01, 999_999.99
- `format_date(iso_date)` — ECP: valid ISO date, wrong separator, invalid month; BVA: Jan 1 / Dec 31, leap day
- `format_relative(moment, now)` — ECP: None, past-seconds, past-minutes, past-hours, past-days, future; BVA: 44 s / 45 s boundary, 3599 s / 3600 s, 86399 s / 86400 s
- `format_local(moment)` — ECP: None, timezone-aware datetime, midnight edge

**Why:** Pure functions, no DB or Flask context required. Rich, precise BVA boundaries in `format_relative`.

### Module 3 — `expense_tracker/stats.py` (RESTRUCTURING REQUIRED)

**Key targets and techniques:**
- `total_of(expenses)` — ECP: empty list, single, multiple; BVA: 0 items, 1 item, floating-point precision
- `expenses_in_month(expenses, year, month)` — ECP: all match / none / partial; BVA: first and last day of month, December→January year rollover
- `category_breakdown(expenses)` — ECP: empty, single category, all 6 categories; verify percent, donut geometry, sort descending
- `monthly_trend(expenses, months_back, chart_height)` — ECP: no expenses, all in one month, spread; BVA: 1 vs 6 months_back, year-boundary rollover

**Why:** Pure computation, no DB/Flask needed. `test_stats.py` exists with 7 bare functions but needs class structure, markers, ordering, and expanded coverage.

---

## 6. Defects and Corrections Needed

| ID | Severity | Location | Issue |
|---|---|---|---|
| D1 | **High** | `pytest.ini` | `addopts` lacks `-n auto`. Parallel execution is installed but not activated. |
| D2 | **High** | `tests/` | Markers `regression`, `formatting`, `stats`, `data_driven` declared but **zero** tests use them. |
| D3 | **High** | `test_stats.py` | 7 bare functions — no class, no markers, no `@pytest.mark.order`. Must be restructured. |
| D4 | **High** | Repository | No Excel test-case sheet (`.xlsx`) exists anywhere. Task 3 entirely missing. |
| D5 | **High** | Repository | No external CSV data file. `data_driven` marker is orphaned. |
| D6 | **High** | Repository | No setup video recorded or linked. Task 1 video deliverable is missing. |
| D7 | **Resolved** | `tests/` | Resolved: Created `tests/test_formatting.py` with 4 classes, 33 methods, 63 passing tests. |
| D8 | **Medium** | `test_module_models.py` | No `@pytest.mark.parametrize` used — all boundary cases are separate methods. |
| D9 | **Resolved** | `docs/` | Resolved: Created comprehensive ECP/BVA design specification in `docs/test_design_notes.md`. |
| D10 | Low | `test_validation.py` | Largely duplicates `TestFunctionValidateExpense` coverage. Not broken but redundant. |
| D11 | Low | `pytest.ini` | No `-n` flag documented or enabled for parallel runs. |

---

## 7. Missing Deliverables Summary

| Deliverable | Status |
|---|---|
| `docs/assignment_audit.md` (this file) | Created now |
| Setup / demo video | **Completely missing** |
| Module 2 test file (`tests/test_formatting.py`) | **Created and verified** (63 passed) |
| Module 3 tests restructured (`tests/test_stats.py`) | Exists but inadequate |
| Test design notes (`docs/test_design_notes.md`) | **Created and verified** |
| Excel test-case sheet (`docs/test_cases.xlsx`) | **Completely missing** |
| External CSV data file (`tests/data/test_cases.csv`) | **Completely missing** |
| `@pytest.mark.parametrize` in Module 1 | Not present |
| Parallel execution configured in `pytest.ini` | Plugin present, not activated |
| `regression` / `stats` / `formatting` markers actively used | Declared but unused |

---

## 8. Ordered Implementation Plan (for subsequent prompts)

> Do not implement yet — awaiting review and approval.

**Priority 1 — Task 3 (Excel + CSV data-driven)**
1. Create `tests/data/test_cases.csv` (≥ 4 rows of `validate_expense` inputs).
2. Create `docs/test_cases.xlsx` via `openpyxl`, matching the CSV.
3. Add `@pytest.mark.data_driven` test class that reads CSV and parameterises calls.

**Priority 2 — Module 2 (formatting.py)**
4. Create `tests/test_formatting.py` with `TestFormatCurrency`, `TestFormatDate`, `TestFormatRelative`, `TestFormatLocal` classes.
5. Apply `@pytest.mark.formatting`, `@pytest.mark.order(N)`, `@pytest.mark.smoke` as appropriate.
6. ≥ 5 ECP+BVA test methods per class.

**Priority 3 — Module 3 (stats.py — restructure + expand)**
7. Rewrite `tests/test_stats.py` with `TestTotalOf`, `TestExpensesInMonth`, `TestCategoryBreakdown`, `TestMonthlyTrend`.
8. Apply `@pytest.mark.stats` and `@pytest.mark.order(N)` to each class.
9. Add missing edge cases and `@pytest.mark.parametrize` for boundary month inputs.

**Priority 4 — Parameterization in Module 1**
10. Add one `@pytest.mark.parametrize` test in `TestFunctionValidateExpense` for BVA amount boundaries.

**Priority 5 — Task 4 parallel + suite markers**
11. Add `-n auto` to `addopts` in `pytest.ini`.
12. Apply `@pytest.mark.regression` to comprehensive test classes.
13. Confirm `@pytest.mark.stats` and `@pytest.mark.formatting` are on all relevant classes.

**Priority 6 — Test design documentation**
14. Create `docs/test_design_notes.md` with ECP/BVA tables for all three modules.

**Priority 7 — Video (manual)**
15. Record a ~2–3 min screen capture: clone, venv, `pip install`, `pytest -v`, app in browser.
16. Commit the video file or hosted link to the repository.

---

## 9. Commands to Verify the Project Manually

```bash
# Install dependencies
pip install -r requirements-dev.txt

# Run full test suite
pytest -v

# Smoke tests only
pytest -v -m smoke

# Models tests only (ordered)
pytest -v -m models

# Parallel run (manual flag — NOT yet in addopts)
pytest -v -n auto

# Stats tests only
pytest -v -m stats

# Formatting tests only
pytest -v -m formatting

# Data-driven tests (currently 0 tests match)
pytest -v -m data_driven

# Run the app
python app.py

# Check individual Git contributions
git log --format="%an %ae %s" --no-merges

# Count tests by marker
pytest --collect-only -q -m models
pytest --collect-only -q -m stats
pytest --collect-only -q -m formatting
pytest --collect-only -q -m data_driven
pytest --collect-only -q -m regression
```

---

## Appendix A — Git History (at audit time)

| SHA | Author | Email | Message |
|---|---|---|---|
| `c3581bd` | Muhammad Faisal | muhammadfaisalsahb12@gmail.com | Task 1 & 4 + Module 1: Setup testing environment and Model unit tests |
| `be9b828` | kadenteh | kadenteh@icloud.com | Rebuild the Export Center on the shared engine and fix its defects |
| `2a6d815` | kadenteh | kadenteh@icloud.com | Make v2's engine the shared export core |
| `19ade1d` | kadenteh | kadenteh@icloud.com | Merge feature-data-export-v2 into the combined export branch |
| `5f6462b` | kadenteh | kadenteh@icloud.com | Add code analysis comparing the three data export implementations |
| `8b8290c` | kadenteh | kadenteh@icloud.com | Add cloud-style Export Center with sharing, schedules and live sync |
| `9f8eb92` | kadenteh | kadenteh@icloud.com | Add advanced export dialog with CSV, JSON, and PDF output |
| `8b9bdb3` | kadenteh | kadenteh@icloud.com | Initial commit: Flask expense tracker |

> **Concern:** Only `c3581bd` is attributed to Muhammad Faisal. All other commits are by `kadenteh`.
> Other team members have zero commits. The assignment requires **verifiable individual contributions** in Git history.

---

## Appendix B — Test Quality Assessment

| Aspect | Assessment |
|---|---|
| Assertions | Strong — specific expected values, not just existence checks |
| Edge cases | Good in `test_module_models.py` and `test_exports.py`; weaker in `test_stats.py` |
| Negative cases | Present for all validation paths in Module 1 |
| Test isolation | Excellent — every DB test uses fresh temp SQLite via `app` fixture |
| Mocking | Not needed — temp DB fixture fully isolates state |
| Naming | Clear and descriptive throughout; `test_stats.py` names adequate |
| Duplicate tests | `test_validation.py` largely duplicates `TestFunctionValidateExpense` |
| False-positive risk | Low — assertions are specific; no `assert True` or empty test bodies |
| Test discovery | All tests auto-discovered; naming conventions match `pytest.ini` |
