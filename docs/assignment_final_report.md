# Assignment 3 Final Acceptance Audit Report — Build Unit Test Automation Solution

**Course:** Software Quality Engineering (SQE)  
**Evaluator:** University SQE Senior Auditor (Strict Acceptance Mode)  
**Repository:** `M-Ehtasham-SE/expense-tracker-sqe-testing`  
**Branch:** `main`  
**Audit Timestamp:** 2026-10-24 12:15:00 UTC+5  
**Final Readiness Verdict:** **NOT READY (Blocked on Manual Deliverable)**

---

## Executive Summary & Final Readiness Verdict

| Verdict Dimension | Status | Notes |
|---|:---:|---|
| **Automated Test Automation (Code)** | **100% PASS** | 254/254 tests passing (148 regression, 54 smoke, 35 models, 63 formatting, 36 stats, 14 data-driven). |
| **Test Design Specification** | **PASS** | `docs/test_design_notes.md` fully documents ECP and BVA for all three modules. |
| **Excel Workbook & CSV Resource** | **PASS** | `docs/test_cases.xlsx` (16 test cases, 11 columns, ECP/BVA documented); `tests/data/test_cases.csv` (10 records, consumed via pytest). |
| **Suites, Groups, Parallel & Ordering** | **PASS** | 6 active markers; sequential default preserves `pytest-order(1..14)`; parallel verified via `pytest-xdist`. |
| **Setup Demonstration Video** | **FAIL / BLOCKED** | **No video file found in the repository.** Manual recording by student is required. |
| **Overall Submission Verdict** | **NOT READY** | Technical code & docs are complete; final submission cannot be claimed 100% ready until setup video is recorded and attached. |

---

## 1. Requirement-by-Requirement Evaluation

### TASK 1: Project Setup & Environment

#### 1.1 Open-Source Python Project
- **Requirement:** Select and evaluate a real open-source Python application.
- **Status:** **PASS**
- **Evidence Path:** [app.py](file:///d:/expense-tracker-sqe-testing/app.py), [expense_tracker/](file:///d:/expense-tracker-sqe-testing/expense_tracker/)
- **Verification Inspection:** Python Flask web application (`expense-tracker`) with SQLite database, models, formatting, statistics, export engine, and cloud sync.
- **Actual Result:** Genuine Python Flask application with modular architecture.
- **Remaining Action:** None.

#### 1.2 Local Development Environment and Reproducible Setup
- **Requirement:** Provide clear, reproducible instructions and explicit dependency specifications for clean installation.
- **Status:** **PASS**
- **Evidence Path:** [requirements.txt](file:///d:/expense-tracker-sqe-testing/requirements.txt), [requirements-dev.txt](file:///d:/expense-tracker-sqe-testing/requirements-dev.txt), [README.md](file:///d:/expense-tracker-sqe-testing/README.md)
- **Verification Command:**
  ```bash
  pip install -r requirements.txt
  pip install -r requirements-dev.txt
  ```
- **Actual Result:** Clean dependency separation. Runtime dependencies (`Flask==3.1.2`, `segno==1.6.6`) in `requirements.txt`; development/test dependencies (`pytest>=8.0`, `pytest-xdist>=3.0`, `pytest-order>=1.0`, `openpyxl>=3.1`) in `requirements-dev.txt`.
- **Remaining Action:** None.

#### 1.3 Genuine Setup Demonstration Video
- **Requirement:** Record a short demonstration video walking through repository setup, environment activation, test execution, and application launch.
- **Status:** **FAIL / BLOCKED (Manual Action Required)**
- **Evidence Path:** Missing from repository (searched `.mp4`, `.mkv`, `.webm`, `.mov`, `.avi`).
- **Verification Command:**
  ```powershell
  Get-ChildItem -Path . -Recurse -Include *.mp4,*.mkv,*.webm,*.mov,*.avi -File
  ```
- **Actual Result:** 0 files returned. No video committed or hosted link provided.
- **Remaining Action:** Student must record a ~2–3 minute video demonstrating:
  1. `git clone` & environment setup
  2. `pip install -r requirements-dev.txt`
  3. `pytest -v` (showing 254 passed)
  4. Running the app with `python app.py` and accessing in browser
  Commit to `docs/setup_demo.mp4` or include a persistent URL in `README.md`.

---

### TASK 2: Test Design and Automated Unit Tests

#### 2.1 Three Actual Application Modules
- **Requirement:** Select three distinct modules within the application.
- **Status:** **PASS**
- **Evidence Path:**
  - Module 1: [expense_tracker/models.py](file:///d:/expense-tracker-sqe-testing/expense_tracker/models.py)
  - Module 2: [expense_tracker/formatting.py](file:///d:/expense-tracker-sqe-testing/expense_tracker/formatting.py)
  - Module 3: [expense_tracker/stats.py](file:///d:/expense-tracker-sqe-testing/expense_tracker/stats.py)
- **Verification Inspection:** Modules represent three completely distinct responsibilities: database CRUD & validation, text & datetime presentation formatting, and financial statistical computations / SVG donut chart geometry.
- **Actual Result:** 3 distinct core application modules targeted.
- **Remaining Action:** None.

#### 2.2 ECP/BVA and Other Appropriate Techniques
- **Requirement:** Systematically apply Equivalence Class Partitioning (ECP) and Boundary Value Analysis (BVA).
- **Status:** **PASS**
- **Evidence Path:** [docs/test_design_notes.md](file:///d:/expense-tracker-sqe-testing/docs/test_design_notes.md), [tests/test_module_models.py](file:///d:/expense-tracker-sqe-testing/tests/test_module_models.py), [tests/test_formatting.py](file:///d:/expense-tracker-sqe-testing/tests/test_formatting.py), [tests/test_stats.py](file:///d:/expense-tracker-sqe-testing/tests/test_stats.py)
- **Verification Inspection:**
  - `models.py`: ECP for description/category/date; BVA on amount at `$0.00`, `$0.01`, `$1,000,000.00`, `$1,000,000.01`; description boundary at 1, 120, 121 chars.
  - `formatting.py`: BVA on currency thousands commas, float rounding; relative time thresholds at 44s/45s, 3599s/3600s, 86399s/86400s; calendar leap year Feb 29; midnight/noon edge cases.
  - `stats.py`: ECP for empty vs populated lists; single-category 100% partition; BVA on month boundaries (1st day, last day, adjacent days); year rollover; SVG donut stroke-dasharray offset geometry; bar height clamping (`max(3.0, ...)`).
- **Actual Result:** Exhaustive ECP/BVA partition coverage.
- **Remaining Action:** None.

#### 2.3 Test-Design Notes Committed to Git
- **Requirement:** Formal test design documentation committed to the repository.
- **Status:** **PASS**
- **Evidence Path:** [docs/test_design_notes.md](file:///d:/expense-tracker-sqe-testing/docs/test_design_notes.md) (commit `865ec10`)
- **Verification Inspection:** 301-line document detailing executive summary, ambiguity analysis, source code constraints, ECP/BVA tables for all 3 modules, and complete traceability matrix.
- **Actual Result:** Fully documented and version-controlled.
- **Remaining Action:** None.

#### 2.4 Test-Count Thresholds (5–10 per Function, 5–10 per Class/Module)
- **Requirement:** Fulfill the 5–10 automated test cases per relevant function and per class/module floor.
- **Status:** **PASS**
- **Evidence Path:**
  - Module 1 ([tests/test_module_models.py](file:///d:/expense-tracker-sqe-testing/tests/test_module_models.py)):
    - `validate_expense`: 14 methods + 1 parameterized = 15 tests (≥ 5 threshold met)
    - `Expense` / `Filters`: 5 tests (≥ 5 threshold met)
    - `add_expense` / `get_expense`: 6 tests (≥ 5 threshold met)
    - `update_expense`: 5 tests (≥ 5 threshold met)
    - `delete_expense`: 5 tests (≥ 5 threshold met)
    - **Module 1 Subtotal:** 35 passing tests across 5 classes.
  - Module 2 ([tests/test_formatting.py](file:///d:/expense-tracker-sqe-testing/tests/test_formatting.py)):
    - `format_currency`: 8 methods (18 parameterized executions) (≥ 5 threshold met)
    - `format_date`: 9 methods (11 parameterized executions) (≥ 5 threshold met)
    - `format_relative`: 9 methods (26 parameterized executions) (≥ 5 threshold met)
    - `format_local`: 7 methods (8 parameterized executions) (≥ 5 threshold met)
    - **Module 2 Subtotal:** 33 methods, 63 passing test executions across 4 classes.
  - Module 3 ([tests/test_stats.py](file:///d:/expense-tracker-sqe-testing/tests/test_stats.py)):
    - `total_of`: 7 methods (9 parameterized executions) (≥ 5 threshold met)
    - `expenses_in_month`: 9 methods (9 executions) (≥ 5 threshold met)
    - `category_breakdown`: 9 methods (9 executions) (≥ 5 threshold met)
    - `monthly_trend`: 9 methods (9 executions) (≥ 5 threshold met)
    - **Module 3 Subtotal:** 34 methods, 36 passing test executions across 4 classes.
- **Verification Command:**
  ```bash
  pytest -v tests/test_module_models.py
  pytest -v tests/test_formatting.py
  pytest -v tests/test_stats.py
  ```
- **Actual Result:** All targeted functions contain between 5 and 14 test methods. All classes contain ≥ 5 tests.
- **Remaining Action:** None.

#### 2.5 Individual Contributions Supported by Genuine Git History
- **Requirement:** Individual team members must have identifiable, genuine Git commits.
- **Status:** **PASS**
- **Evidence Path:** Git commit log (`git log --format="%h | %an <%ae> | %s"`)
- **Verification Inspection:**
  - `c3581bd` | **Muhammad Faisal** (`muhammadfaisalsahb12@gmail.com`) | `Task 1 & 4 + Module 1: Setup testing environment and Model unit tests`
  - `865ec10` | **M-Ehtasham-SE** (`ehtashamsd@gmail.com`) | `docs: complete ECP and BVA test design`
  - `a1429e6` | **M-Ehtasham-SE** (`ehtashamsd@gmail.com`) | `test: add formatting module unit coverage`
  - `6b186d4` | **M-Ehtasham-SE** (`ehtashamsd@gmail.com`) | `test: improve statistics module unit coverage`
  - `34becd9` | **M-Ehtasham-SE** (`ehtashamsd@gmail.com`) | `test: add CSV-driven parameterized cases`
  - `445a6b6` | **M-Ehtasham-SE** (`ehtashamsd@gmail.com`) | `Task 3: add docs/test_cases.xlsx with 16 documented test cases`
  - `212c09a` | **M-Ehtasham-SE** (`ehtashamsd@gmail.com`) | `Task 4: enable parallel execution and complete marker coverage`
  - `4dd6ae8` | **M-Ehtasham-SE** (`ehtashamsd@gmail.com`) | `docs & config: finalize Assignment 3 documentation, audit, and execution configuration`
- **Actual Result:** 2 distinct, verifiable student contributors with genuine commits and clear attribution across all tasks.
- **Remaining Action:** None.

---

### TASK 3: Excel Test-Case Sheet and CSV Data Source

#### 3.1 Excel Workbook with ≥ 4 Documented Test Cases
- **Requirement:** Provide an Excel workbook (`.xlsx`) containing at least 4 test cases with standard testing columns and ECP/BVA techniques documented.
- **Status:** **PASS**
- **Evidence Path:** [docs/test_cases.xlsx](file:///d:/expense-tracker-sqe-testing/docs/test_cases.xlsx)
- **Verification Inspection:**
  - Sheet title: `Test Cases`
  - Rows: 1 header row + 16 data rows (16 test cases, exceeding the ≥ 4 requirement)
  - Columns (11): `Test Case ID`, `Module`, `Function`, `Objective`, `Preconditions`, `Input Data`, `Steps`, `Expected Result`, `Actual Result`, `Status`, `Technique`
  - Techniques documented: `ECP — Valid partition`, `ECP — Invalid partition`, `BVA — Below lower boundary`, `BVA — Above upper boundary`, `BVA — Exact lower boundary`, `Data-Driven — CSV row`
  - Integrity: `Actual Result` is set to `Not Executed` for manual execution status (no invented manual results). `Status` is marked `Pass` corresponding to automated test execution.
- **Verification Script:**
  ```python
  import openpyxl
  wb = openpyxl.load_workbook('docs/test_cases.xlsx')
  ws = wb.active
  assert ws.max_row == 17  # 1 header + 16 test cases
  assert ws.max_column == 11
  ```
- **Actual Result:** Perfectly formed, styled `.xlsx` workbook.
- **Remaining Action:** None.

#### 3.2 External CSV Data Source Consumed by Automated Tests
- **Requirement:** Store test data in an external CSV file, resolve path relative to repository, validate headers, and consume via parameterized automated tests.
- **Status:** **PASS**
- **Evidence Path:** [tests/data/test_cases.csv](file:///d:/expense-tracker-sqe-testing/tests/data/test_cases.csv), [tests/test_data_driven.py](file:///d:/expense-tracker-sqe-testing/tests/test_data_driven.py)
- **Verification Inspection:**
  - CSV contains 10 records with columns: `test_id,test_title,description,amount_raw,category,date_raw,expected_valid,expected_error_field,expected_error_message,expected_amount`.
  - [tests/test_data_driven.py](file:///d:/expense-tracker-sqe-testing/tests/test_data_driven.py) resolves path relative to `Path(__file__).parent / "data" / "test_cases.csv"`.
  - Includes defensive checks: verifies required headers, skips empty rows, validates non-empty `test_id`, raises `FileNotFoundError` and `ValueError`.
  - Dynamically drives `test_validate_expense_driven_by_csv` across all 10 rows.
  - Marked with `@pytest.mark.data_driven`.
- **Verification Command:**
  ```bash
  pytest -v -m data_driven
  ```
- **Actual Result:** 14 passed in 0.09s (4 schema/loader integrity tests + 10 CSV-driven parameterized tests).
- **Remaining Action:** None.

---

### TASK 4: Test Suites, Parallel Execution, Parameterization, and Ordering

#### 4.1 Test Suites / Marker Groups
- **Requirement:** Define and register markers to enable running distinct test suites independently.
- **Status:** **PASS**
- **Evidence Path:** [pytest.ini](file:///d:/expense-tracker-sqe-testing/pytest.ini)
- **Verification Command & Exact Counts:**
  ```bash
  pytest --collect-only -q -m models       # 35 collected
  pytest --collect-only -q -m formatting   # 63 collected
  pytest --collect-only -q -m stats        # 36 collected
  pytest --collect-only -q -m data_driven  # 14 collected
  pytest --collect-only -q -m smoke        # 54 collected
  pytest --collect-only -q -m regression   # 148 collected
  ```
- **Actual Result:** All 6 markers registered under `--strict-markers` and actively populated. Every group can run completely independently with zero cross-suite failures.
- **Remaining Action:** None.

#### 4.2 Parallel Execution Configuration
- **Requirement:** Configure and demonstrate parallel execution using `pytest-xdist`.
- **Status:** **PASS**
- **Evidence Path:** [pytest.ini](file:///d:/expense-tracker-sqe-testing/pytest.ini), [README.md](file:///d:/expense-tracker-sqe-testing/README.md)
- **Verification Command:**
  ```bash
  pytest -n auto --dist=loadscope -q
  ```
- **Actual Result:** `254 passed in 11.11s` with 8 parallel worker processes.
- **Design Rationale:** `-n auto` is deliberately opt-in rather than baked into `addopts` to prevent worker-spinup overhead on smaller runs and to preserve strict sequential execution ordering by default.
- **Remaining Action:** None.

#### 4.3 Data-Driven Parameterization
- **Requirement:** Apply `@pytest.mark.parametrize` appropriately for boundary testing and data tables.
- **Status:** **PASS**
- **Evidence Path:**
  - `tests/test_formatting.py`: `test_format_currency_standard_amounts`, `test_format_currency_thousands_separator_boundaries`, `test_format_currency_float_rounding`, `test_format_date_valid_iso_dates`, `test_format_relative_immediate_boundaries`, `test_format_relative_past_minutes`, etc.
  - `tests/test_stats.py`: `test_total_of_parametrized_combinations`
  - `tests/test_data_driven.py`: `test_validate_expense_driven_by_csv[row]`
- **Actual Result:** Over 40 distinct parameterized test instances dynamically generated.
- **Remaining Action:** None.

#### 4.4 Test Execution Ordering
- **Requirement:** Configure execution ordering using `pytest-order` and provide evidence.
- **Status:** **PASS**
- **Evidence Path:** All 14 assignment test classes decorated with `@pytest.mark.order(1)` through `@pytest.mark.order(14)`.
- **Verification Command:**
  ```bash
  pytest --collect-only -q -m "models or formatting or stats or data_driven"
  ```
- **Actual Result (Sequential Collection Order):**
  1. `TestFunctionValidateExpense` (`order(1)`)
  2. `TestClassExpense` (`order(2)`)
  3. `TestFunctionsAddAndGetExpense` (`order(3)`)
  4. `TestFunctionUpdateExpense` (`order(4)`)
  5. `TestFunctionDeleteExpense` (`order(5)`)
  6. `TestFormatCurrency` (`order(6)`)
  7. `TestFormatDate` (`order(7)`)
  8. `TestFormatRelative` (`order(8)`)
  9. `TestFormatLocal` (`order(9)`)
  10. `TestTotalOf` (`order(10)`)
  11. `TestExpensesInMonth` (`order(11)`)
  12. `TestCategoryBreakdown` (`order(12)`)
  13. `TestMonthlyTrend` (`order(13)`)
  14. `TestDataDrivenExpenseValidation` (`order(14)`)
- **Ordering Independence:** Tests are completely isolated; ordering is advisory and creates no state dependencies.
- **Remaining Action:** None.

---

### SUBMISSION & REPOSITORY HYGIENE

#### 5.1 Tracked Files & Repository Hygiene
- **Requirement:** Clean repository without committed caches, `.pyc`, `.venv`, secrets, or stray binaries.
- **Status:** **PASS**
- **Evidence Path:** [.gitignore](file:///d:/expense-tracker-sqe-testing/.gitignore), `git status --ignored`
- **Verification Command:**
  ```bash
  git status --ignored
  ```
- **Actual Result:** Only expected build caches (`.pytest_cache`, `__pycache__`) in `.gitignore`. Zero secrets, zero virtual environments committed.
- **Remaining Action:** None.

#### 5.2 README Accuracy
- **Requirement:** All commands documented in `README.md` must accurately reflect actual behavior and counts.
- **Status:** **PASS**
- **Evidence Path:** [README.md](file:///d:/expense-tracker-sqe-testing/README.md)
- **Verification Command:** All 10 command variations in README executed and verified against actual pytest output.
- **Actual Result:** 100% agreement between documented counts and actual execution output.
- **Remaining Action:** None.

#### 5.3 Public Repository & Remote Push Status
- **Requirement:** Ensure commits are pushed to the remote repository.
- **Status:** **PASS (Current commits up to date on remotes)**
- **Evidence Path:** `git remote -v`, `git log origin/main..main`
- **Verification Command:**
  ```bash
  git remote -v
  git status
  ```
- **Actual Result:**
  - `origin`: `https://github.com/M-Ehtasham-SE/expense-tracker-sqe-testing.git` (Up to date at `4dd6ae8`)
  - `upstream`: `https://github.com/Faisal-khan-SE/expense-tracker-sqe-testing.git` (Up to date at `4dd6ae8`)
- **Submission Note:** As instructed, no post-deadline pushes have been executed without explicit confirmation.
- **Remaining Action:** None.

---

## 2. Final Automated Test Execution Summary Table

| Test Scope / Command | Total Collected | Passed | Failed | Skipped | Execution Time |
|---|:---:|:---:|:---:|:---:|:---:|
| **Full Sequential Suite** (`pytest -v`) | **254** | **254** | **0** | **0** | **11.29s** |
| **Full Parallel Suite** (`pytest -n auto -q`) | **254** | **254** | **0** | **0** | **11.11s** |
| **Module 1** (`pytest -v tests/test_module_models.py`) | **35** | **35** | **0** | **0** | **1.54s** |
| **Module 2** (`pytest -v tests/test_formatting.py`) | **63** | **63** | **0** | **0** | **0.20s** |
| **Module 3** (`pytest -v tests/test_stats.py`) | **36** | **36** | **0** | **0** | **0.11s** |
| **CSV Data-Driven** (`pytest -v tests/test_data_driven.py`) | **14** | **14** | **0** | **0** | **0.09s** |
| **Smoke Suite** (`pytest -q -m smoke`) | **54** | **54** | **0** | **0** | **0.25s** |
| **Regression Suite** (`pytest -q -m regression`) | **148** | **148** | **0** | **0** | **1.60s** |
| **Legacy Export Suite** (`test_exports.py` + `test_export_center.py`) | **85** | **85** | **0** | **0** | **~8s** |
| **Routes & Validation** (`test_routes.py` + `test_validation.py`) | **16** | **16** | **0** | **0** | **~0.3s** |

---

## 3. Outstanding Actions Required Before Final Student Submission

1. **Setup Demonstration Video (MANDATORY)**:
   - Record a 2–3 minute video screen recording following the script in [docs/assignment_summary.md](file:///d:/expense-tracker-sqe-testing/docs/assignment_summary.md) Section 6.
   - Commit the video file to `docs/setup_demo.mp4` or paste a Google Drive / YouTube link into [README.md](file:///d:/expense-tracker-sqe-testing/README.md).
2. **Confirm Submission on Google Classroom (GCR)**:
   - Submit the repository link: `https://github.com/M-Ehtasham-SE/expense-tracker-sqe-testing`
   - Attach or link `docs/test_cases.xlsx` and the video file if GCR requires direct attachments.
3. **Post-Deadline Push Authorization**:
   - Only push if authorized by your university instructor.
