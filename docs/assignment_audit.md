# Assignment 3 Audit Report — Build Unit Test Automation Solution

| Field | Value |
|---|---|
| **Auditor** | Antigravity (AI senior test engineer) |
| **Initial audit** | 2026-10-23 (commit `c3581bd`, 148 tests) |
| **Last verified** | 2026-10-24 (commit `212c09a`, 254 tests) |
| **Branch** | `main` |
| **Python** | 3.14.7 |
| **pytest** | 8.4.1 · pytest-order 1.5.0 · pytest-xdist 3.8.0 |

---

## 1. Project Overview

**Name:** Expense Tracker (Python / Flask)
**Purpose:** A personal-finance web app — add, edit, delete, search, filter, and export expenses.
Built with Flask, Jinja2 templates, vanilla CSS/JS, and a local SQLite database (no ORM).

**Dependencies (runtime):** `Flask==3.1.2`, `segno==1.6.6`
**Dependencies (dev/test):** declared in `requirements-dev.txt` — `pytest==8.4.1`, `pytest-xdist>=3.8.0`, `pytest-order>=1.5.0`, `openpyxl>=3.1.5`
**Setup:** `pip install -r requirements-dev.txt` then `pytest -v`
**Run app:** `python app.py` → http://127.0.0.1:5000

---

## 2. Repository Files

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
| `test_module_models.py` | **35** | 5 ordered classes; `@pytest.mark.models`; ECP + BVA; `@pytest.mark.smoke` on class 1 |
| `test_formatting.py` | **63** | 4 ordered classes; `@pytest.mark.formatting`; 33 methods + parametrize |
| `test_stats.py` | **36** | 4 ordered classes; `@pytest.mark.stats`; 34 methods + parametrize |
| `test_data_driven.py` | **14** | CSV-driven; `@pytest.mark.data_driven`; schema validation + parametrize |
| `test_export_center.py` | 44 | Full Export Center: templates, job lifecycle, CSRF, sharing, schedules, retention |
| `test_exports.py` | 33 | Parametrised; covers options parsing, sanitize_filename, CSV/JSON/PDF, routes |
| `test_routes.py` | 8 | HTTP integration tests for CRUD routes |
| `test_csv_export.py` | 5 | Unit tests for `csv_export` and `csvutil` helpers |
| `test_validation.py` | 8 | Tests for `validate_expense` (partially duplicates `test_module_models.py`) |
| `conftest.py` | — | Shared `app` and `client` fixtures using temp SQLite DB |
| **TOTAL** | **254** | **254 passed, 0 failed, 0 skipped** |

### Configuration Files

| File | Content |
|---|---|
| `pytest.ini` | testpaths, naming conventions, 6 markers, `--strict-markers`, `-v`; parallel opt-in via comments |
| `requirements-dev.txt` | pytest, pytest-xdist, pytest-order, openpyxl |
| `requirements.txt` | Flask, segno (runtime only) |
| `README.md` | Setup, installation, all test commands, parallel execution, project structure |

### Documentation / Deliverables (`docs/`)

| File | Content |
|---|---|
| `test_design_notes.md` | ECP/BVA design spec — all 3 modules (98+ test cases designed) |
| `test_cases.xlsx` | 16 test cases with all required columns (ECP/BVA/data-driven) |
| `assignment_audit.md` | This file |
| `assignment_summary.md` | Concise summary with verified counts, commands, and checklist |

### External Test Data

| File | Content |
|---|---|
| `tests/data/test_cases.csv` | 10 rows driving `validate_expense` parametrized tests |

---

## 3. Test Execution Results

### Baseline (at initial audit — commit `c3581bd`)

**Command:** `pytest -v --tb=short`
**Result: 148 passed in 28.77s**

| Test file | Tests |
|---|---|
| `test_module_models.py` | 34 |
| `test_export_center.py` | 51 |
| `test_exports.py` | 25 |
| `test_routes.py` | 8 |
| `test_stats.py` | 7 |
| `test_csv_export.py` | 5 |
| `test_validation.py` | 8 |
| **TOTAL** | **148** |

### Current state (commit `212c09a` + config fixes)

**Sequential (default):**
```
pytest -v
============================ 254 passed in 11.18s =============================
```

**Parallel:**
```
pytest -n auto --dist=loadscope -v
created: 8/8 workers
============================ 254 passed in 10.76s =============================
```

**Group runs (all verified):**

| Command | Result |
|---|---|
| `pytest -v -m models` | 35 passed |
| `pytest -v -m formatting` | 63 passed |
| `pytest -v -m stats` | 36 passed |
| `pytest -v -m data_driven` | 14 passed |
| `pytest -v -m smoke` | 54 passed |
| `pytest -v -m regression` | 148 passed |

---

## 4. Requirement-by-Requirement Status

### Task 1 — Project Setup

| Requirement | Status | Evidence |
|---|---|---|
| Open-source Python application | **PASS** | Flask Expense Tracker in repo |
| Local development environment | **PASS** | `requirements.txt`, `requirements-dev.txt`, README setup steps |
| Setup demonstration video | **FAIL — manual** | No video file in repo. See `docs/assignment_summary.md` §6 for recording script. |

### Task 2 — Test Design and Automated Unit Tests

| Requirement | Status | Evidence |
|---|---|---|
| Three application modules selected | **PASS** | Module 1: `models.py`, Module 2: `formatting.py`, Module 3: `stats.py` |
| ECP, BVA, other techniques applied | **PASS** | All three modules use ECP + BVA. Design documented in `docs/test_design_notes.md` |
| Test design notes per module | **PASS** | `docs/test_design_notes.md` — 98+ designed cases, ECP/BVA tables, constraints |
| 5–10 unit tests per function | **PASS** | `validate_expense`: 14; `format_currency`: 8; `format_date`: 9; `format_relative`: 9; `format_local`: 7; `total_of`: 7; `expenses_in_month`: 9; `category_breakdown`: 9; `monthly_trend`: 9 |
| 5–10 unit tests per class | **PASS** | All classes meet ≥ 5 threshold |
| Module 2 tests | **PASS** | `tests/test_formatting.py` — 4 classes, 63 passing executions |
| Module 3 tests | **PASS** | `tests/test_stats.py` — 4 classes, 36 passing executions |

### Task 3 — CSV and Excel

| Requirement | Status | Evidence |
|---|---|---|
| Excel test-case sheet ≥ 4 test cases | **PASS** | `docs/test_cases.xlsx` — 16 documented rows, 11 columns |
| External CSV consumed by tests | **PASS** | `tests/data/test_cases.csv` (10 rows); `tests/test_data_driven.py` (14 passing tests) |

### Task 4 — Parallel Execution, Suites, Groups, Ordering

| Requirement | Status | Evidence |
|---|---|---|
| Configure parallel execution | **PASS** | `pytest-xdist` 3.8.0 installed; `pytest -n auto --dist=loadscope` → 254 passed (8 workers) |
| `-n auto` not baked in `addopts` | **PASS** | Sequential is default; parallel is opt-in. See `pytest.ini` comments explaining rationale. |
| Test suites / groups defined | **PASS** | 6 markers: `smoke`(54), `regression`(148), `models`(35), `formatting`(63), `stats`(36), `data_driven`(14) |
| Data-driven parameterization | **PASS** | `test_formatting.py` and `test_stats.py` use `@pytest.mark.parametrize`. CSV parametrize in `test_data_driven.py` |
| Execution ordering configured | **PASS** | `@pytest.mark.order(1–14)` on all assignment classes; verified sequential collection order |
| Ordering creates no hidden dependencies | **PASS** | Every test uses independent fixtures; all groups pass independently |

---

## 5. Defect Log

| ID | Severity | Status | Issue / Resolution |
|---|---|---|---|
| D1 | High | **RESOLVED** | `addopts` had `-n auto --dist=loadscope` baked in — prevented sequential mode and ordering. Fixed: removed from `addopts`; parallel is now opt-in. |
| D2 | High | **RESOLVED** | Markers `formatting`, `stats`, `data_driven` declared but unused. All six markers now actively applied. |
| D3 | High | **RESOLVED** | `test_stats.py` had 7 bare functions. Restructured into 4 classes (36 tests). |
| D4 | High | **RESOLVED** | No Excel workbook. Created `docs/test_cases.xlsx` (16 rows, 11 columns). |
| D5 | High | **RESOLVED** | No CSV test data. Created `tests/data/test_cases.csv` and `tests/test_data_driven.py`. |
| D6 | High | **OPEN** | No setup video recorded. Must be done manually. |
| D7 | High | **RESOLVED** | No Module 2 tests. Created `tests/test_formatting.py` (63 tests). |
| D8 | Medium | **RESOLVED** | `requirements.txt` contained test deps. Moved to `requirements-dev.txt` only. |
| D9 | Low | **RESOLVED** | `test_validation.py` partially duplicates models tests. Kept as-is (harmless). |

---

## 6. Test Isolation Assessment

| Concern | Assessment |
|---|---|
| SQLite concurrency | Each DB test uses `tempfile.mkstemp()` in `app` fixture — fresh file per test, deleted in teardown |
| Parallel worker isolation | `--dist=loadscope` keeps each class on one worker; no cross-worker DB sharing |
| CSV path | Resolved relative to `__file__` — works from any CWD |
| Shared state between pure-function tests | None — `formatting` and `stats` tests are pure; no fixtures |
| Hidden ordering dependency | None — each group verified independently |
| False positives | None detected — all assertions are specific expected values |

---

## 7. Commands for Manual Verification

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Full suite (sequential)
pytest -v

# Full suite (parallel)
pytest -n auto --dist=loadscope -v

# Individual groups
pytest -v -m models
pytest -v -m formatting
pytest -v -m stats
pytest -v -m data_driven
pytest -v -m smoke
pytest -v -m regression

# Individual test files
pytest -v tests/test_module_models.py
pytest -v tests/test_formatting.py
pytest -v tests/test_stats.py
pytest -v tests/test_data_driven.py

# Verify collection order (sequential, no xdist)
pytest --collect-only -q -m "models or formatting or stats or data_driven"

# Count per group
pytest --collect-only -q -m models       # 35
pytest --collect-only -q -m formatting   # 63
pytest --collect-only -q -m stats        # 36
pytest --collect-only -q -m data_driven  # 14
pytest --collect-only -q -m smoke        # 54
pytest --collect-only -q -m regression   # 148
pytest --collect-only -q                 # 254

# Run the app
python app.py  # open http://127.0.0.1:5000
```

---

## Appendix A — Git History

| SHA | Author | Message |
|---|---|---|
| `212c09a` | M-Ehtasham-SE | Task 4: enable parallel execution and complete marker coverage |
| `445a6b6` | M-Ehtasham-SE | Task 3: add docs/test_cases.xlsx with 16 documented test cases |
| `34becd9` | M-Ehtasham-SE | test: add CSV-driven parameterized cases |
| `6b186d4` | M-Ehtasham-SE | test: improve statistics module unit coverage |
| `a1429e6` | M-Ehtasham-SE | test: add formatting module unit coverage |
| `865ec10` | M-Ehtasham-SE | docs: complete ECP and BVA test design |
| `0d4c2f4` | M-Ehtasham-SE | docs: audit assignment requirements |
| `c3581bd` | Muhammad Faisal | Task 1 & 4 + Module 1: Setup testing environment and Model unit tests |

---

## Appendix B — Test Quality Assessment

| Aspect | Assessment |
|---|---|
| Assertions | Strong — specific expected values throughout; no `assert True` or empty bodies |
| Edge cases | Comprehensive in all three modules |
| Negative cases | Present for all validation paths |
| Test isolation | Excellent — fresh temp SQLite per test; no shared state |
| Mocking | Minimal and appropriate (`unittest.mock.MagicMock` for timezone in `format_local`) |
| Naming | Clear and descriptive throughout |
| Duplicate tests | `test_validation.py` partially duplicates models tests — not counted for coverage |
| False-positive risk | Low |
| Test discovery | All tests auto-discovered via `pytest.ini` naming conventions |
