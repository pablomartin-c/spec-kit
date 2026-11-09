# Quickstart: CSV Expense Mini-Report

Prerequisites (after implementation phase):

- `uv` installed
- Repo root: `spec-kit`

## Setup

```powershell
cd C:\Users\pablo.martin_readygo\Desktop\SDD\spec-kit
uv sync
```

## Verify (tests)

```powershell
uv run pytest
```

**Expected**: all tests pass (0 failures).

## Happy path (P1)

```powershell
uv run expense-report -i tests/fixtures/valid_small.csv -o .tmp/report.txt
Get-Content .tmp/report.txt
```

**Expected**:

- Exit code `0`
- File `.tmp/report.txt` exists
- Contains `Grand Total`, `By Category`, `Largest Expense`

## Fail-fast invalid row (P2)

```powershell
uv run expense-report -i tests/fixtures/bad_amount_row3.csv -o .tmp/bad.txt
echo $LASTEXITCODE
Test-Path .tmp/bad.txt
```

**Expected**:

- Exit code non-zero
- stderr mentions row number
- `.tmp/bad.txt` should **not** exist (or not be updated — depends on pre-run state; prefer fresh path)

## Missing input (P2)

```powershell
uv run expense-report -i tests/fixtures/does_not_exist.csv -o .tmp/x.txt
```

**Expected**: non-zero exit, no report file.

## Month filter (P3, when implemented)

```powershell
uv run expense-report -i tests/fixtures/multi_month.csv -o .tmp/jan.txt --month 2026-01
```

**Expected**: totals reflect January rows only.

## Traceability smoke check

| Scenario | Spec |
|----------|------|
| Happy path | US1 |
| Missing / empty / bad row | US2 |
| Month filter | US3 |
