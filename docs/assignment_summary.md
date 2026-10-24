# Assignment 3 Summary — Build Unit Test Automation Solution

| Field | Value |
|---|---|
| **Course** | Software Quality Engineering (SQE) |
| **Repository** | `M-Ehtasham-SE/expense-tracker-sqe-testing` |
| **Branch** | `main` |
| **Python** | 3.14.7 |
| **pytest** | 8.4.1 · pytest-order 1.5.0 · pytest-xdist 3.8.0 |
| **Total tests** | **254 passed, 0 failed, 0 skipped** |

---

## 1. Deliverables

| # | Deliverable | Path | Status |
|---|---|---|---|
| T1 | Project setup and environment | `README.md` Getting started section | DONE |
| T1 | Setup video | See Section 6 | MANUAL STEP REQUIRED |
| T2 | Module 1 models unit tests | `tests/test_module_models.py` | DONE 35 tests |
| T2 | Module 2 formatting unit tests | `tests/test_formatting.py` | DONE 63 tests |
| T2 | Module 3 stats unit tests | `tests/test_stats.py` | DONE 36 tests |
| T2 | Test design notes ECP/BVA | `docs/test_design_notes.md` | DONE |
| T3 | External CSV test data | `tests/data/test_cases.csv` | DONE 10 rows |
| T3 | CSV-driven automated tests | `tests/test_data_driven.py` | DONE 14 tests |
| T3 | Excel test-case workbook | `docs/test_cases.xlsx` | DONE 16 rows |
| T4 | Marker-based test suites | `pytest.ini` + markers | DONE 6 markers |
| T4 | Parallel execution | `pytest -n auto --dist=loadscope` | DONE verified |
| T4 | Execution ordering | `@pytest.mark.order(N)` | DONE verified |
| T4 | Parameterization | Multiple test files | DONE |

---

## 2. Test Count Matrix

### By marker group

| Marker | Group | Executions |
|---|---|---|
| `models` | Module 1 models.py | 35 |
| `formatting` | Module 2 formatting.py | 63 |
| `stats` | Module 3 stats.py | 36 |
| `data_driven` | Task 3 CSV-driven | 14 |
| `smoke` | Critical path subset | 54 |
| `regression` | All three modules + CSV | 113 |

### Module 1 classes (test_module_models.py — 35 tests total)

| Class | Order | Tests |
|---|---|---|
| TestFunctionValidateExpense | 1 | 14 |
| TestClassExpense | 2 | 5 |
| TestFunctionsAddAndGetExpense | 3 | 6 |
| TestFunctionUpdateExpense | 4 | 5 |
| TestFunctionDeleteExpense | 5 | 5 |

### Module 2 classes (test_formatting.py — 63 executions)

| Class | Order | Methods | Executions |
|---|---|---|---|
| TestFormatCurrency | 6 | 8 | 22 |
| TestFormatDate | 7 | 9 | 24 |
| TestFormatRelative | 8 | 9 | 14 |
| TestFormatLocal | 9 | 7 | 3 |

### Module 3 classes (test_stats.py — 36 executions)

| Class | Order | Methods | Executions |
|---|---|---|---|
| TestTotalOf | 10 | 7 | 9 |
| TestExpensesInMonth | 11 | 9 | 9 |
| TestCategoryBreakdown | 12 | 9 | 9 |
| TestMonthlyTrend | 13 | 9 | 9 |

---

## 3. Verified Commands and Results

### Full suite sequential (default)

```
pytest -v
============================ 254 passed in 11.18s =============================
```

### Parallel execution (Task 4)

```
pytest -n auto --dist=loadscope -v
created: 8/8 workers
============================ 254 passed in 10.76s =============================
```

NOTE: -n auto is NOT in addopts by design. Sequential is the default so that
pytest-order markers work deterministically. Parallel is explicit opt-in for speed.

### Group commands (all verified)

```
pytest -v -m models       # 35 passed
pytest -v -m formatting   # 63 passed
pytest -v -m stats        # 36 passed
pytest -v -m data_driven  # 14 passed
pytest -v -m smoke        # 54 passed
pytest -v -m regression   # 113 passed
```

### Single-file commands

```
pytest -v tests/test_module_models.py    # 35 passed
pytest -v tests/test_formatting.py       # 63 passed
pytest -v tests/test_stats.py            # 36 passed
pytest -v tests/test_data_driven.py      # 14 passed
```

---

## 4. Ordering Evidence

pytest-order @pytest.mark.order(N) is applied at class level.
Classes run in ascending order number in sequential mode.

Order 1  TestFunctionValidateExpense  test_module_models.py
Order 2  TestClassExpense             test_module_models.py
Order 3  TestFunctionsAddAndGetExpense test_module_models.py
Order 4  TestFunctionUpdateExpense    test_module_models.py
Order 5  TestFunctionDeleteExpense    test_module_models.py
Order 6  TestFormatCurrency           test_formatting.py
Order 7  TestFormatDate               test_formatting.py
Order 8  TestFormatRelative           test_formatting.py
Order 9  TestFormatLocal              test_formatting.py
Order 10 TestTotalOf                  test_stats.py
Order 11 TestExpensesInMonth          test_stats.py
Order 12 TestCategoryBreakdown        test_stats.py
Order 13 TestMonthlyTrend             test_stats.py
Order 14 TestDataDrivenExpenseValidation test_data_driven.py

IMPORTANT: Order marks are documentation and do NOT create hidden test dependencies.
Every test is independently runnable and uses its own fixtures.

---

## 5. Test Isolation and Parallel Safety

SQLite DB conflicts   : Each test gets a fresh temp file via tempfile.mkstemp()
                        in the app fixture (conftest.py). Deleted on teardown.
Parallel safety       : --dist=loadscope assigns each class to one worker.
CSV path resolution   : Path(__file__).parent / "data" / "test_cases.csv"
                        Relative to test file, not CWD.
Shared state          : None. Pure-function tests (formatting, stats) have no
                        shared state.
Ordering dependency   : None. Order is advisory only.

---

## 6. Setup Video — Manual Step Required

No video file is in the repository. Record this yourself and commit it.

Recording checklist:
  1. Open terminal in project root
  2. python --version
  3. py -m venv .venv
     .\.venv\Scripts\Activate.ps1
  4. pip install -r requirements.txt
  5. pip install -r requirements-dev.txt
  6. python app.py  (open http://127.0.0.1:5000, add one expense)
  7. pytest -v  (show 254 passed)
  8. pytest -v -m smoke  (show 54 passed)
  9. pytest -n auto --dist=loadscope -v  (show 254 passed, 8 workers)

Recommended file: docs/setup_demo.mp4
After recording:
  git add docs/setup_demo.mp4
  git commit -m "docs: add setup demo video"

---

## 7. Git History (Assignment Commits)

212c09a  Task 4: enable parallel execution and complete marker coverage
445a6b6  Task 3: add docs/test_cases.xlsx with 16 documented test cases
34becd9  test: add CSV-driven parameterized cases
6b186d4  test: improve statistics module unit coverage
a1429e6  test: add formatting module unit coverage
865ec10  docs: complete ECP and BVA test design
0d4c2f4  docs: audit assignment requirements
c3581bd  Task 1 & 4 + Module 1: Setup testing environment and Model unit tests

---

## 8. Unresolved Items

| Item | Action |
|---|---|
| Setup video | Record and commit docs/setup_demo.mp4 manually |
| test_validation.py | Partially duplicates TestFunctionValidateExpense; kept but not counted for coverage |
| Individual git contributions | Ensure each team member commits from their own account |
