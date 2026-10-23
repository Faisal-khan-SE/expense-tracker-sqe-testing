# Test Design Specification: Equivalence Partitioning & Boundary Value Analysis

| Document Field | Value |
|---|---|
| **Project** | Flask Expense Tracker (`expense_tracker`) |
| **Document Purpose** | SQE Assignment 3 — Task 2 Test Design Specification |
| **Auditor / Author** | M-Ehtasham-SE (Lead QA / SQE Contributor) |
| **Audit Reference** | [assignment_audit.md](file:///d:/expense-tracker-sqe-testing/docs/assignment_audit.md) |
| **Target Modules** | Module 1: `expense_tracker.models`<br>Module 2: `expense_tracker.formatting`<br>Module 3: `expense_tracker.stats` |
| **Baseline Status** | 148 passing tests in baseline test suite (`pytest -v`) |

---

## 1. Executive Summary & Scope

This specification formalizes the black-box and white-box test design methodologies for the unit testing solution of the Flask Expense Tracker application. Test design systematically applies:
1. **Equivalence Class Partitioning (ECP)**: Splitting input domains into valid and invalid equivalence classes under the assumption that all inputs in a class produce equivalent behavior.
2. **Boundary Value Analysis (BVA)**: Probing extrema, transitions, and values immediately above and below boundaries where defects cluster.
3. **Error Guessing & Exception Cases**: Verifying defensive programming constructs (type errors, missing keys, boundary clampings, timezone handling).

All constraints documented herein are derived strictly from the actual application source code:
- `expense_tracker/models.py`
- `expense_tracker/formatting.py`
- `expense_tracker/stats.py`

No artificial business rules or imaginary external constraints have been introduced.

---

## 2. Clarification of Assignment Test-Count Ambiguities

The assignment specification presents two distinct test-count statements:
1. *"Create 5–10 automated unit test cases per person for each function of a class."*
2. *"Create 5–10 automated unit test cases per person for each selected class/module."*

### Analysis of Ambiguity
- **Ambiguity**: If treated as identical counts, either function-level testing is under-specified or module-level testing is vastly overstated. For example, a module containing 4 functions evaluated under Statement 1 requires `4 × (5 to 10) = 20 to 40` test cases per contributor. Statement 2, if read in isolation, might imply only 5 to 10 tests across the whole module.
- **Strict Compliance Resolution**:
  - We reconcile this by enforcing a **hierarchical testing floor**:
    1. **Function-Level Floor**: Every targeted function or method under test MUST have at least **5 distinct test cases** covering valid ECP, invalid ECP, and BVA edge cases.
    2. **Class/Module-Level Aggregation**: Each test class grouping related functions or an individual component class must contain **5 to 14 test cases**, and every selected module must achieve an aggregate count of **20 to 35 test cases**.
  - This ensures that neither requirement is compromised and guarantees thorough, professional branch and boundary coverage.

---

## 3. Module 1: `expense_tracker.models`

### 3.1 Component Architecture & Source Constraints
Source file: `expense_tracker/models.py`
Primary test targets:
- Function: `validate_expense(description, amount_raw, category, date_raw)`
- Dataclass: `Expense`, method `from_row(cls, row)`, and `Filters`
- DB CRUD functions: `add_expense`, `get_expense`, `update_expense`, `delete_expense`, `list_expenses`

#### Actual Constraints in Code:
1. `description`: Stripped of leading/trailing whitespace.
   - Required: `len(description.strip()) > 0` (otherwise `"Description is required."`)
   - Max length: `len(description.strip()) <= 120` (otherwise `"Keep it under 120 characters."`)
2. `amount_raw`: Parsed to `float`.
   - Must be float-convertible (otherwise `"Enter a valid amount."`)
   - Must be strictly positive: `parsed_amount > 0` (otherwise `"Amount must be greater than $0."`)
   - Maximum allowed upper limit: `parsed_amount <= 1_000_000` (otherwise `"That amount looks too large."`)
3. `category`: Must exist within constant `CATEGORIES`:
   - `CATEGORIES = ["Food", "Transportation", "Entertainment", "Shopping", "Bills", "Other"]`
   - Any other value produces `"Choose a valid category."`
4. `date_raw`: Stripped of whitespace.
   - Required: non-empty (otherwise `"Date is required."`)
   - Must match strict ISO format: `datetime.strptime(date_raw, "%Y-%m-%d")` (otherwise `"Enter a valid date."`)
5. `add_expense` / `update_expense`:
   - `description.strip()` is stored to SQLite.
   - `created_at` timestamp is generated as `datetime.now(timezone.utc).isoformat()`.

---

### 3.2 `validate_expense` — ECP & BVA Matrix

| Parameter | Partition Type | Partition Description | Representative Test Input | Expected Output / Error | Test ID |
|---|---|---|---|---|---|
| `description` | Valid ECP | Non-empty string within 1..120 chars | `"Coffee"` | Valid, no error | `MOD-VAL-01` |
| `description` | Invalid ECP | Whitespace only / empty string | `"   "` or `""` | `errors["description"] == "Description is required."` | `MOD-VAL-02` |
| `description` | BVA (Min) | Exactly 1 character (min valid length) | `"A"` | Valid, no error | `MOD-VAL-03` |
| `description` | BVA (Max) | Exactly 120 characters (max valid length) | `"A" * 120` | Valid, no error | `MOD-VAL-04` |
| `description` | BVA (Max+1)| Exactly 121 characters (exceeds max) | `"A" * 121` | `errors["description"] == "Keep it under 120 characters."` | `MOD-VAL-05` |
| `amount_raw` | Invalid ECP | Non-numeric string | `"twenty"` | `errors["amount"] == "Enter a valid amount."` | `MOD-VAL-06` |
| `amount_raw` | Invalid ECP | Negative value | `"-15.00"` | `errors["amount"] == "Amount must be greater than $0."` | `MOD-VAL-07` |
| `amount_raw` | BVA (Zero) | Exact zero boundary | `"0.00"` | `errors["amount"] == "Amount must be greater than $0."` | `MOD-VAL-08` |
| `amount_raw` | BVA (Min+) | Smallest positive cent | `"0.01"` | Valid, `parsed_amount == 0.01` | `MOD-VAL-09` |
| `amount_raw` | BVA (Max) | Upper limit threshold | `"1000000.00"` | Valid, `parsed_amount == 1000000.00` | `MOD-VAL-10` |
| `amount_raw` | BVA (Max+) | Upper limit threshold + 1 cent | `"1000000.01"` | `errors["amount"] == "That amount looks too large."` | `MOD-VAL-11` |
| `category` | Valid ECP | One of 6 permitted categories | `"Food"`, `"Transportation"` | Valid, no error | `MOD-VAL-01` |
| `category` | Invalid ECP | Unregistered category string | `"NonExistentCategory"` | `errors["category"] == "Choose a valid category."` | `MOD-VAL-12` |
| `date_raw` | Invalid ECP | Non-ISO date format (DD/MM/YYYY) | `"17/10/2026"` | `errors["date"] == "Enter a valid date."` | `MOD-VAL-13` |
| `date_raw` | Invalid ECP | Empty date string | `""` | `errors["date"] == "Date is required."` | `MOD-VAL-14` |

---

### 3.3 `Expense`, `Filters`, and CRUD Operations — Test Design

| Target Class / Function | Partition / Scenario | Test Input / Precondition | Expected Outcome | Test ID |
|---|---|---|---|---|
| `Expense` dataclass | Direct construction | `Expense(1, "Groceries", 50.0, "Food", "2026-10-17", "...")` | Fields populated properly | `MOD-EXP-01` |
| `Expense.from_row` | Mapping from SQLite `Row` or dict | Row mapping with `id`, `description`, `amount`, `category`, `date`, `created_at` | Instance populated identical to row keys | `MOD-EXP-02` |
| `Expense` equality | Dataclass equality (`__eq__`) | Two instances with matching field values | `e1 == e2` evaluates `True` | `MOD-EXP-03` |
| `Expense` inequality | Dataclass inequality (`__ne__`) | Instances with differing `id` | `e1 != e2` evaluates `True` | `MOD-EXP-04` |
| `Filters` dataclass | Default construction | `Filters()` | `search=""`, `category="All"`, `sort="date-desc"` | `MOD-EXP-05` |
| `add_expense` | Insertion of valid record | DB initialized; insert valid expense record | Returns positive integer `lastrowid` > 0 | `MOD-AG-01` |
| `get_expense` | Retrieval of existing record | Insert record with known ID; retrieve | Returns `Expense` instance matching inserted fields | `MOD-AG-02` |
| `get_expense` | Retrieval of nonexistent ID | Query ID `999999` in empty/test DB | Returns `None` | `MOD-AG-03` |
| `add_expense` | Description whitespace stripping | Insert with description `"   Books   "` | Stored description is `"Books"` | `MOD-AG-04` |
| `add_expense` | Successive insertions (monotonic IDs) | Insert record A then record B | `id2 > id1` | `MOD-AG-05` |
| `add_expense` | BVA minimum amount storage | Insert with `amount=0.01` | Retrieved record has `amount == 0.01` | `MOD-AG-06` |
| `update_expense` | Update description & amount | Existing record ID; new description & amount | Record updated in SQLite database | `MOD-UPD-01` |
| `update_expense` | Update category change | Existing record ID; change `"Other"` to `"Transportation"` | Retrieved record has updated category | `MOD-UPD-02` |
| `update_expense` | Update date change | Existing record ID; change `"2026-10-01"` to `"2026-10-10"` | Retrieved record has updated date | `MOD-UPD-03` |
| `update_expense` | Update description whitespace strip | Update with `"   Latte   "` | Retrieved description is `"Latte"` | `MOD-UPD-04` |
| `update_expense` | Nonexistent record update | Update ID `88888` | Silent no-op, returns None without crashing | `MOD-UPD-05` |
| `delete_expense` | Delete existing record | Existing record ID; delete | Record subsequently returns `None` on `get_expense` | `MOD-DEL-01` |
| `delete_expense` | Delete nonexistent ID | Delete ID `777777` | Silent no-op without exception | `MOD-DEL-02` |
| `delete_expense` | Isolation of deletion | Records A, B, C; delete B | A and C remain intact in DB | `MOD-DEL-03` |
| `delete_expense` | Double deletion idempotent | Delete same record ID twice | No error; record remains deleted | `MOD-DEL-04` |
| `delete_expense` | Complete cleanup | Delete all records one by one | `list_expenses(Filters())` returns empty list | `MOD-DEL-05` |

---

## 4. Module 2: `expense_tracker.formatting`

### 4.1 Component Architecture & Source Constraints
Source file: `expense_tracker/formatting.py`
Primary test targets:
1. `format_currency(amount: float) -> str`
   - Implementation: `f"${amount:,.2f}"`
   - Comma grouping for thousands, standard two-decimal float formatting.
2. `format_date(iso_date: str) -> str`
   - Implementation: `dt = datetime.strptime(iso_date, "%Y-%m-%d"); return f"{dt.strftime('%b')} {dt.day}, {dt.year}"`
   - Windows-safe portable date formatting without `%d` leading zeros (e.g. `"Sep 22, 2026"`).
3. `format_relative(moment: datetime | None, now: datetime | None = None) -> str`
   - If `moment is None`: returns `"never"`.
   - `seconds = (now - moment).total_seconds()`, `future = seconds < 0`, `seconds = abs(seconds)`.
   - Discrete threshold rules:
     - `seconds < 45`: `"in a moment"` (future) / `"just now"` (past).
     - `seconds < 3600`: `round(seconds / 60)` -> `"in {n} min"` / `"{n} min ago"`.
     - `seconds < 86400`: `round(seconds / 3600)` -> `"in {n} hr"` / `"{n} hr ago"`.
     - `seconds < 2,592,000` (30 days): `round(seconds / 86400)` -> `"in {n} day(s)"` / `"{n} day(s) ago"`.
     - `seconds >= 2,592,000`: delegates to `format_date(moment.astimezone().date().isoformat())`.
4. `format_local(moment: datetime | None) -> str`
   - If `moment is None`: returns `""`.
   - Formats to local timezone with stripped leading zero on hour: `f"{format_date(...)}, {local.strftime('%I:%M %p').lstrip('0')}"`.

---

### 4.2 `formatting.py` — ECP & BVA Matrix

| Target Function | Partition / Boundary Type | Scenario Description | Test Input | Expected Output | Test ID |
|---|---|---|---|---|---|
| `format_currency` | Valid ECP | Standard positive float | `12.50` | `"$12.50"` | `FMT-CUR-01` |
| `format_currency` | BVA (Zero) | Exact zero | `0.00` | `"$0.00"` | `FMT-CUR-02` |
| `format_currency` | BVA (Min+) | Smallest positive cent | `0.01` | `"$0.01"` | `FMT-CUR-03` |
| `format_currency` | Valid ECP | Negative currency | `-15.75` | `"$-15.75"` | `FMT-CUR-04` |
| `format_currency` | BVA (Thousands -) | Just below comma separator | `999.99` | `"$999.99"` | `FMT-CUR-05` |
| `format_currency` | BVA (Thousands +) | At comma separator threshold | `1000.00` | `"$1,000.00"` | `FMT-CUR-06` |
| `format_currency` | Valid ECP | Large million currency | `1000000.00` | `"$1,000,000.00"` | `FMT-CUR-07` |
| `format_currency` | BVA (Float round)| Floating point rounding | `4.556` | `"$4.56"` | `FMT-CUR-08` |
| `format_date` | Valid ECP | Standard mid-month ISO date | `"2026-06-15"` | `"Jun 15, 2026"` | `FMT-DAT-01` |
| `format_date` | ECP (Single digit)| Single digit day (no zero pad) | `"2026-04-05"` | `"Apr 5, 2026"` | `FMT-DAT-02` |
| `format_date` | BVA (Year start) | First day of year | `"2026-01-01"` | `"Jan 1, 2026"` | `FMT-DAT-03` |
| `format_date` | BVA (Year end) | Last day of year | `"2026-12-31"` | `"Dec 31, 2026"` | `FMT-DAT-04` |
| `format_date` | BVA (Leap day) | Valid leap year day | `"2024-02-29"` | `"Feb 29, 2024"` | `FMT-DAT-05` |
| `format_date` | Invalid ECP (Non-leap)| Feb 29 on non-leap year | `"2026-02-29"` | Raises `ValueError` | `FMT-DAT-06` |
| `format_date` | Invalid ECP (Slash)| Slashes instead of dashes | `"15/06/2026"` | Raises `ValueError` | `FMT-DAT-07` |
| `format_date` | Invalid ECP (Month)| Invalid month number (13) | `"2026-13-01"` | Raises `ValueError` | `FMT-DAT-08` |
| `format_relative`| Valid ECP (None) | None datetime | `moment=None` | `"never"` | `FMT-REL-01` |
| `format_relative`| BVA (Past immediate)| 44 seconds in past | `now - 44s` | `"just now"` | `FMT-REL-02` |
| `format_relative`| BVA (Future immediate)| 44 seconds in future | `now + 44s` | `"in a moment"` | `FMT-REL-03` |
| `format_relative`| BVA (Minute threshold)| 45 seconds in past | `now - 45s` | `"1 min ago"` | `FMT-REL-04` |
| `format_relative`| Valid ECP (Minutes)| Multiple minutes in past | `now - 300s` (5 min) | `"5 min ago"` | `FMT-REL-05` |
| `format_relative`| BVA (Hour threshold)| 3600 seconds in past | `now - 3600s` (1 hr) | `"1 hr ago"` | `FMT-REL-06` |
| `format_relative`| Valid ECP (Hours) | Multiple hours in future | `now + 7200s` (2 hr) | `"in 2 hr"` | `FMT-REL-07` |
| `format_relative`| BVA (Single day) | Exactly 1 day (singular) | `now - 86400s` (1 day)| `"1 day ago"` | `FMT-REL-08` |
| `format_relative`| Valid ECP (Days plural)| Multiple days (plural) | `now - 172800s` (2 days)| `"2 days ago"` | `FMT-REL-09` |
| `format_relative`| BVA (30-day cutoff)| 29 days in past (< limit) | `now - (86400 * 29)s` | `"29 days ago"` | `FMT-REL-10` |
| `format_relative`| BVA (Over 30 days) | 31 days in past (>= limit) | `now - (86400 * 31)s` | Formatted date via `format_date` | `FMT-REL-11` |
| `format_relative`| Valid ECP (Future min)| Future minutes | `now + 600s` (10 min) | `"in 10 min"` | `FMT-REL-12` |
| `format_local` | Valid ECP (None) | None moment | `moment=None` | `""` | `FMT-LOC-01` |
| `format_local` | Valid ECP (PM) | Afternoon datetime | `15:04 UTC` | Date string + `", 3:04 PM"` | `FMT-LOC-02` |
| `format_local` | Valid ECP (AM) | Morning datetime | `09:15 UTC` | Date string + `", 9:15 AM"` | `FMT-LOC-03` |
| `format_local` | BVA (Midnight) | Midnight boundary | `00:00 UTC` | Date string + `", 12:00 AM"` | `FMT-LOC-04` |
| `format_local` | BVA (Noon) | Noon boundary | `12:00 UTC` | Date string + `", 12:00 PM"` | `FMT-LOC-05` |

---

## 5. Module 3: `expense_tracker.stats`

### 5.1 Component Architecture & Source Constraints
Source file: `expense_tracker/stats.py`
Primary test targets:
1. `total_of(expenses: list[Expense]) -> float`
   - Implementation: `sum(e.amount for e in expenses)`
   - Pure function computing sum; returns `0` on empty list.
2. `expenses_in_month(expenses: list[Expense], year: int, month: int) -> list[Expense]`
   - Implementation: Parses `e.date.split("-")`, filters `int(y) == year and int(m) == month`.
3. `category_breakdown(expenses: list[Expense]) -> list[CategoryTotal]`
   - Computes category sums and counts for all `c in CATEGORIES`.
   - Excludes categories where `count == 0`.
   - Sorts descending by `total`.
   - Computes SVG Donut geometry:
     - `DONUT_SIZE = 200`, `DONUT_STROKE = 28`, `DONUT_RADIUS = 86`
     - `DONUT_CIRCUMFERENCE = 2 * pi * 86 = 540.3539...`
     - `dash_array = f"{fraction * DONUT_CIRCUMFERENCE:.4f} {DONUT_CIRCUMFERENCE:.4f}"`
     - `dash_offset = -cumulative * DONUT_CIRCUMFERENCE`
4. `monthly_trend(expenses: list[Expense], months_back: int = 6, chart_height: int = 132) -> list[MonthTotal]`
   - Generates `months_back` monthly buckets ending at `date.today()`, ordered chronologically.
   - Computes `max_total = max((b.total for b in buckets), default=0) or 1`.
   - Computes bar height: `max(3, (bucket.total / max_total) * (chart_height - 24))`.
     - Minimum clamp is `3.0`.
     - Maximum height is `chart_height - 24` (default: `108.0`).

---

### 5.2 `stats.py` — ECP & BVA Matrix

| Target Function | Partition / Boundary Type | Scenario Description | Test Input | Expected Output | Test ID |
|---|---|---|---|---|---|
| `total_of` | BVA (Empty) | Empty expense list | `[]` | `0` (or `0.0`) | `STA-TOT-01` |
| `total_of` | BVA (Single) | Exactly 1 expense | `[Expense(amount=15.50)]` | `15.50` | `STA-TOT-02` |
| `total_of` | Valid ECP (Multi) | Multiple expenses | `[10.50, 4.25, 20.25]` | `35.00` | `STA-TOT-03` |
| `total_of` | BVA (Penny amount) | Smallest cent boundary | `[Expense(amount=0.01)]` | `0.01` | `STA-TOT-04` |
| `total_of` | Valid ECP (Large) | Large expense aggregation | `[500000.00, 500000.00]` | `1000000.00` | `STA-TOT-05` |
| `total_of` | Valid ECP (Mixed) | Expenses across different categories | Food (12.0) + Bills (88.0) | `100.00` | `STA-TOT-06` |
| `expenses_in_month`| BVA (Empty) | Empty expense list | `expenses=[]`, 2026, 9 | `[]` | `STA-EIM-01` |
| `expenses_in_month`| Valid ECP (All match)| All expenses in month | 3 expenses in 2026-09 | List of 3 expenses | `STA-EIM-02` |
| `expenses_in_month`| Valid ECP (No match) | Zero expenses match month | All in 2026-08; query 2026-09 | `[]` | `STA-EIM-03` |
| `expenses_in_month`| BVA (Month start) | First day of month | Date `"2026-09-01"` | Included in result | `STA-EIM-04` |
| `expenses_in_month`| BVA (Month end) | Last day of month | Date `"2026-09-30"` | Included in result | `STA-EIM-05` |
| `expenses_in_month`| BVA (Day before) | Last day of previous month | Date `"2026-08-31"`; query 2026-09 | Excluded from result | `STA-EIM-06` |
| `expenses_in_month`| BVA (Day after) | First day of next month | Date `"2026-10-01"`; query 2026-09 | Excluded from result | `STA-EIM-07` |
| `expenses_in_month`| BVA (Year boundary)| Dec 31 vs Jan 1 rollover | 2026-12-31 vs 2027-01-01; query 2026-12 | Only Dec 31 included | `STA-EIM-08` |
| `category_breakdown`| BVA (Empty) | Empty expenses | `[]` | `[]` | `STA-CAT-01` |
| `category_breakdown`| BVA (Single cat) | Single category (100% share) | `[Expense(cat="Food", amt=50)]` | 1 entry, `percent == 100.0` | `STA-CAT-02` |
| `category_breakdown`| Valid ECP (Multi) | Multiple categories | Food (25), Entertainment (75) | Sorted desc: Entertainment (75%), Food (25%) | `STA-CAT-03` |
| `category_breakdown`| Valid ECP (Exclude)| Unused categories excluded | Only Food present | Exactly 1 entry; 0-count categories omitted | `STA-CAT-04` |
| `category_breakdown`| Valid ECP (All 6) | All 6 categories populated | 1 expense in each of the 6 categories | 6 entries returned in descending order | `STA-CAT-05` |
| `category_breakdown`| BVA (Donut 1st) | First entry donut offset | Any multi-category list | `breakdown[0].dash_offset == 0.0` | `STA-CAT-06` |
| `category_breakdown`| BVA (Donut cum) | Subsequent entry offset | Multi-category list | `breakdown[1].dash_offset < 0` (negative cumulative) | `STA-CAT-07` |
| `category_breakdown`| Valid ECP (Donut circ)| Dash array format | Any entry | Contains `f"{DONUT_CIRCUMFERENCE:.4f}"` | `STA-CAT-08` |
| `monthly_trend` | BVA (Empty) | Empty expenses | `[]`, `months_back=6` | 6 buckets, all `total=0.0`, all `bar_height=3.0` | `STA-TRD-01` |
| `monthly_trend` | BVA (Single month)| `months_back=1` boundary | 1 expense in current month | Exactly 1 bucket returned | `STA-TRD-02` |
| `monthly_trend` | Valid ECP (Current) | Expense in current month | Expense dated today | Last bucket matches amount, earlier buckets 0 | `STA-TRD-03` |
| `monthly_trend` | Valid ECP (Chronology)| Bucket chronology check | Default 6 months | `months[-1]` is current month; months are sequential | `STA-TRD-04` |
| `monthly_trend` | BVA (Max bar height)| Non-zero max bucket | Expense 100.0 in current month | `bucket.bar_height == (132 - 24) == 108.0` | `STA-TRD-05` |
| `monthly_trend` | BVA (Min bar clamp)| Zero amount bucket | Buckets with total == 0 | `bucket.bar_height == 3.0` | `STA-TRD-06` |
| `monthly_trend` | Valid ECP (Custom h)| Custom chart height | `chart_height=200` | Max bar height scales to `200 - 24 == 176.0` | `STA-TRD-07` |
| `monthly_trend` | Valid ECP (Year rollover)| Past 12 months trend | `months_back=12` | Month roll-under correctly decrements year | `STA-TRD-08` |

---

## 6. Comprehensive Traceability and Coverage Matrix

This matrix maps every class and function across the three targeted modules to its testing technique, test count, test IDs, implementation file, and verified Git contributor.

> **Contributor Verification Rule**: Contributors are strictly verified from the repository's Git commit history:
> - **Muhammad Faisal (`muhammadfaisalsahb12@gmail.com`)**: Authored commit `c3581bd` establishing the test architecture and Module 1 (`tests/test_module_models.py`).
> - **M-Ehtasham-SE (`ehtashamsd@gmail.com`)**: Authored commit `0d4c2f4` (Audit Report), authoring `docs/test_design_notes.md`, and assigned for Module 2 and Module 3 test suites.
> - **kadenteh (`kadenteh@icloud.com`)**: Authored initial application and legacy base tests (`test_exports.py`, `test_export_center.py`, `test_routes.py`, `test_stats.py` bare functions).

| Module | Class / Component | Function / Target | Technique Applied | Test Count | Test ID Range | Implementation File | Verified Contributor | Status |
|---|---|---|---|:---:|---|---|---|:---:|
| `models` | `TestFunctionValidateExpense` | `validate_expense` | ECP, BVA | 14 | `MOD-VAL-01` .. `14` | `tests/test_module_models.py` | Muhammad Faisal | **PASSED** (Baseline) |
| `models` | `TestClassExpense` | `Expense`, `Filters` | ECP, State Mapping | 5 | `MOD-EXP-01` .. `05` | `tests/test_module_models.py` | Muhammad Faisal | **PASSED** (Baseline) |
| `models` | `TestFunctionsAddAndGetExpense`| `add_expense`, `get_expense` | ECP, DB Isolation | 6 | `MOD-AG-01` .. `06` | `tests/test_module_models.py` | Muhammad Faisal | **PASSED** (Baseline) |
| `models` | `TestFunctionUpdateExpense` | `update_expense` | ECP, State Mutation | 5 | `MOD-UPD-01` .. `05` | `tests/test_module_models.py` | Muhammad Faisal | **PASSED** (Baseline) |
| `models` | `TestFunctionDeleteExpense` | `delete_expense` | ECP, Idempotency | 5 | `MOD-DEL-01` .. `05` | `tests/test_module_models.py` | Muhammad Faisal | **PASSED** (Baseline) |
| **Module 1 Subtotal** | **5 Test Classes** | **7 Functions/Classes** | **ECP, BVA** | **35** | | | **Muhammad Faisal** | **Verified** |
| `formatting` | `TestFormatCurrency` | `format_currency` | ECP, BVA | 8 | `FMT-CUR-01` .. `08` | `tests/test_formatting.py` | M-Ehtasham-SE | **PASSED** (16 parameterized) |
| `formatting` | `TestFormatDate` | `format_date` | ECP, BVA, Exception | 9 | `FMT-DAT-01` .. `08` | `tests/test_formatting.py` | M-Ehtasham-SE | **PASSED** (14 parameterized) |
| `formatting` | `TestFormatRelative` | `format_relative` | ECP, BVA Thresholds | 9 | `FMT-REL-01` .. `12` | `tests/test_formatting.py` | M-Ehtasham-SE | **PASSED** (26 parameterized) |
| `formatting` | `TestFormatLocal` | `format_local` | ECP, BVA (Time boundaries)| 7 | `FMT-LOC-01` .. `05` | `tests/test_formatting.py` | M-Ehtasham-SE | **PASSED** (7 tests) |
| **Module 2 Subtotal** | **4 Test Classes** | **4 Functions** | **ECP, BVA** | **33 (63 run)**| | | **M-Ehtasham-SE** | **PASSED** |
| `stats` | `TestTotalOf` | `total_of` | ECP, BVA | 6 | `STA-TOT-01` .. `06` | `tests/test_stats.py` (Restructure) | M-Ehtasham-SE | Planned |
| `stats` | `TestExpensesInMonth` | `expenses_in_month` | ECP, BVA (Month edges)| 8 | `STA-EIM-01` .. `08` | `tests/test_stats.py` (Restructure) | M-Ehtasham-SE | Planned |
| `stats` | `TestCategoryBreakdown` | `category_breakdown` | ECP, Geometry BVA | 8 | `STA-CAT-01` .. `08` | `tests/test_stats.py` (Restructure) | M-Ehtasham-SE | Planned |
| `stats` | `TestMonthlyTrend` | `monthly_trend` | ECP, Scaling BVA | 8 | `STA-TRD-01` .. `08` | `tests/test_stats.py` (Restructure) | M-Ehtasham-SE | Planned |
| **Module 3 Subtotal** | **4 Test Classes** | **4 Functions** | **ECP, BVA** | **30** | | | **M-Ehtasham-SE** | **Planned** |
| **GRAND TOTAL** | **13 Test Classes** | **15 Functions/Classes** | | **98 (128 run)**| | | **2 Verified Team Members**| |

---

## 7. Cross-Check Against Codebase and Pre-Existing Tests

1. **Module 1 (`models.py`)**:
   - `TestFunctionValidateExpense`: Exactly matches lines 50–85 of `expense_tracker/models.py`.
   - All 35 tests in `tests/test_module_models.py` pass cleanly in the baseline execution.
2. **Module 2 (`formatting.py`)**:
   - Every partition directly corresponds to branches in lines 6–40 of `expense_tracker/formatting.py`.
   - Thresholds at 45s, 3600s, 86400s, and 2,592,000s directly mirror the loop in `format_relative`.
3. **Module 3 (`stats.py`)**:
   - `total_of`, `expenses_in_month`, `category_breakdown`, and `monthly_trend` match lines 15–111 of `expense_tracker/stats.py`.
   - The donut circumference formula and bar height min clamp (`max(3, ...)`) directly map to lines 9–12 and 109 of `stats.py`.
   - The pre-existing 7 bare test functions in `tests/test_stats.py` currently pass, but this design formalizes their evolution into a 30-test suite across 4 structured, ordered classes.
