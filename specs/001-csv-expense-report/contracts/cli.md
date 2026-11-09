# CLI Contract: expense-report

## Command

```text
expense-report --input <path> --output <path> [--month YYYY-MM]
```

Short forms: `-i`, `-o`.

## Arguments

| Flag | Required | Description |
|------|----------|-------------|
| `--input` / `-i` | yes | Path to gastos CSV (UTF-8, comma, header) |
| `--output` / `-o` | yes | Path for text report file (created/overwritten on success only) |
| `--month` | no | Filter to calendar month `YYYY-MM` (P3) |

## Success

- Exit code: **0**
- Side effect: writes report file at `--output`
- stderr: empty or warnings only (none in v1)

## Failure

- Exit code: **non-zero**
- stderr: single-line or short multi-line human message identifying error kind; for `ROW_INVALID`, include **1-based data row number** (header = row 1, first data row = 2)
- **Must not** create or overwrite `--output` on failure

## Report file layout (success)

```text
Expense Report
==============
Grand Total: <amount with 2 decimals>

By Category
-----------
<category>: <total>
...

Largest Expense
---------------
Date: <expense_date>
Amount: <amount>
Category: <category>
Description: <description>
```

Currency symbol omitted (single implicit currency per file per spec).

## Mapping to functional requirements

| FR | Contract element |
|----|------------------|
| FR-001 | `--input`, `--output` |
| FR-003 | Header + row validation before write |
| FR-004 | Report sections |
| FR-005, FR-008 | Non-zero exit, no output file on error |
| FR-006 | Report file path |
| FR-007 | `--month` |
