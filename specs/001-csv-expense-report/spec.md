# Feature Specification: CSV Expense Mini-Report

**Feature Branch**: `001-csv-expense-report`

**Created**: 2026-11-09

**Status**: Implemented (verified 2026-11-09)

**Input**: User description: "Mini informe sobre CSV fijo (facturas, gastos, leads) — practice capstone; first slice on fixed-schema **gastos** (expenses) CSV."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate expense summary from a valid CSV (Priority: P1)

An analyst has a monthly expenses export with a fixed column layout. They want a one-shot summary: how much was spent in total, how spending splits across categories, and which single expense was largest.

**Why this priority**: Delivers the core value of the capstone (CSV → mini informe) with no extra features.

**Independent Test**: Provide a small valid sample CSV and verify the report shows total, per-category totals, and the largest expense line.

**Acceptance Scenarios**:

1. **Given** a readable CSV that matches the agreed column contract and contains at least one data row, **When** the user requests a report specifying the input CSV and a destination path for the report file, **Then** a report file is written at that destination and includes grand total spend, spend grouped by category (each category once), and the largest expense (amount plus identifying fields from the row).
2. **Given** a valid CSV with multiple categories, **When** the user requests a report, **Then** category breakdown sums equal the grand total within a defined rounding tolerance.

---

### User Story 2 - Understand file and row problems (Priority: P2)

The user sometimes receives broken or empty files. They need clear failure messages instead of partial or misleading numbers.

**Why this priority**: Trust in the informe depends on explicit errors; silent skips corrupt decisions.

**Independent Test**: Run against missing path, empty file, and a file with invalid rows; each case yields a distinct, actionable error without a success-style summary.

**Acceptance Scenarios**:

1. **Given** a path that does not exist or is not readable, **When** the user requests a report, **Then** the system reports that the file cannot be read and does not print numeric totals.
2. **Given** a file with only headers and no data rows, **When** the user requests a report, **Then** the system reports that there is no data to summarize.
3. **Given** a row that violates the column contract (e.g. non-numeric amount, missing required field), **When** the user requests a report, **Then** the system stops at the first invalid row, reports which row failed, exits without writing a success-style report file, and does not emit partial totals.

---

### User Story 3 - Optional period filter (Priority: P3)

The user may want the same file summarized only for a calendar month (e.g. last closed month).

**Why this priority**: Common real-world ask; can be deferred after P1/P2.

**Independent Test**: Same CSV with rows in two months; filter by month returns totals only for that month.

**Acceptance Scenarios**:

1. **Given** a valid multi-month CSV, **When** the user requests a report for a specific year-month, **Then** totals and category breakdown include only rows in that month.
2. **Given** a month filter with no matching rows, **When** the user requests a report, **Then** the system reports that no rows matched the period.

---

### Edge Cases

- CSV with duplicate category names (same label, different casing): group categories case-insensitively after trimming surrounding whitespace.
- Zero or negative amounts: behavior must be defined and visible in the report or rejected with a clear rule.
- Very large files: v1 may assume modest row counts suitable for local practice data; document limit in assumptions.
- Wrong delimiter or missing header: treat as contract violation, not as empty categories.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The user MUST be able to request an expense report by supplying the location of a single input CSV file and a destination path where the report will be written.
- **FR-002**: The system MUST support only the **gastos** fixed schema in v1 (see Key Entities); invoice and lead schemas are out of scope until a later feature.
- **FR-003**: The system MUST validate that required columns are present before computing aggregates.
- **FR-004**: The system MUST compute and present grand total spend, spend per category, and the single largest expense row.
- **FR-005**: The system MUST reject or clearly flag unreadable inputs (missing file, empty data, contract violations) without writing a misleading report file at the destination path.
- **FR-006**: The system MUST write the human-readable report to the user-chosen output file path on success; the user MUST be able to read the summary without opening the source CSV.
- **FR-008**: On row-level contract violations, the system MUST fail fast on the first invalid data row (no skip-and-continue, no partial report file).
- **FR-007**: When a period filter is used (P3), the system MUST include only rows whose expense date falls in the selected calendar month.

### Key Entities *(include if feature involves data)*

- **Expense row**: One spend line; attributes: **expense date**, **amount** (positive money value), **category** (label), **description** (short text). Vendor is out of scope for v1.
- **Category aggregate**: Category label plus sum of amounts for that category in the selected scope (whole file or filtered month).
- **Report**: Human-readable summary containing totals, category table, and largest expense highlight.

**Fixed CSV column contract (logical names, v1)**:

| Column      | Required | Meaning                          |
|-------------|----------|----------------------------------|
| expense_date | yes     | Calendar date of the spend       |
| amount      | yes      | Numeric spend amount             |
| category    | yes      | Grouping label                   |
| description | yes      | Line detail                      |

### Out of Scope (v1)

- Ingesting **facturas** or **leads** files (separate schemas/features later).
- Editing, appending, or correcting CSV contents.
- Dashboards, charts, or scheduled jobs.
- Cloud warehouses, dbt, or database persistence.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: From a 20-row sample CSV, a reviewer can obtain a report file with total, category breakdown, and largest expense in one user action without manual spreadsheet formulas.
- **SC-002**: For each documented failure scenario in User Story 2, 100% of test cases produce an explicit error outcome (no numeric success summary).
- **SC-003**: Category breakdown sums match grand total on all acceptance fixtures within **0.01** currency units tolerance.
- **SC-004**: A new teammate can predict required CSV columns from the spec alone without reading source code.

## Assumptions

- Single currency per file; no FX conversion in v1.
- UTF-8 encoding and comma-separated values with a header row (exact parsing rules belong in the plan, not here).
- Practice datasets are local files committed or bundled as fixtures; no PII beyond fictional names.
- "Mini informe" means a concise text summary, not a paginated PDF.
- Category labels are compared case-insensitively after trim.
