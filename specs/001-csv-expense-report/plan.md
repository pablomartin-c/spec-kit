# Implementation Plan: CSV Expense Mini-Report

**Branch**: `001-csv-expense-report` | **Date**: 2026-11-09 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-csv-expense-report/spec.md`

## Summary

Build a small **Python CLI** that reads a fixed-schema **gastos** CSV, validates fail-fast, computes totals and highlights, and writes a **text report file** to a user-chosen path. **pytest** proves each requirement; P3 month filter is a follow-on slice after P1/P2.

## Technical Context

**Language/Version**: Python 3.12 (managed via `uv`; aligns with existing `specify` toolchain on this machine)

**Primary Dependencies**: Standard library only for runtime (`csv`, `argparse`, `datetime`, `pathlib`). Dev: `pytest` (via `pyproject.toml` / `uv`).

**Storage**: Local files only (input CSV, output report text file, test fixtures).

**Testing**: `pytest` — unit tests for parsing/aggregation; CLI/integration tests for exit codes and output files.

**Target Platform**: Windows 10+ (PowerShell); portable to other OS with same Python version.

**Project Type**: CLI tool + importable library modules (constitution: testable slices).

**Performance Goals**: Handle practice fixtures up to ~10k rows in under 2s on a laptop (no optimization work in v1).

**Constraints**: No network, no secrets, UTF-8 CSV, comma delimiter, header row required. Fail-fast on first bad data row; no partial report on error.

**Scale/Scope**: One feature directory; P1+P2 MVP first; P3 month filter second increment.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Plan compliance |
|-----------|-----------------|
| I. Spec-First | Plan traces every module to FR/US in spec; P3 deferred explicitly |
| II. What/Why vs How | Stack chosen here only; spec unchanged |
| III. Test-First | Tasks order: failing tests per slice before implementation |
| IV. Evidence | quickstart.md lists commands + expected exit/report outcomes |
| V. Simplicity | Single package, no database, no web layer |

**Post-design re-check**: PASS — no unjustified complexity.

## Project Structure

### Documentation (this feature)

```text
specs/001-csv-expense-report/
├── plan.md              # This file
├── research.md          # Phase 0
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1
├── contracts/           # Phase 1
│   └── cli.md
├── spec.md
├── intent.md
└── tasks.md             # Created by /speckit-tasks (next)
```

### Source Code (repository root)

```text
pyproject.toml
src/expense_report/
├── __init__.py
├── models.py            # ExpenseRow, ReportSummary, errors
├── reader.py            # CSV contract validation + parse
├── aggregate.py         # totals, by-category, largest
├── report_writer.py     # text report layout
└── cli.py                 # argparse entrypoint

tests/
├── conftest.py
├── fixtures/
│   ├── valid_small.csv
│   ├── empty_data.csv
│   ├── bad_amount_row3.csv
│   └── multi_month.csv    # for P3 when implemented
├── test_reader.py
├── test_aggregate.py
└── test_cli.py
```

**Structure Decision**: Single Python package under `src/` (stdlib-first) with thin CLI. Matches Hello SDD habits pattern and keeps verification commands one-liners (`uv run pytest`, `uv run expense-report`).

## Spec Traceability

| Spec ref | Design surface |
|----------|----------------|
| US1, FR-001,4,6 | `cli.py`, `aggregate.py`, `report_writer.py` |
| US2, FR-003,5,8 | `reader.py`, error types in `models.py` |
| US3, FR-007 | `reader.py` filter + `aggregate.py` (P3 phase) |
| SC-003 | `aggregate.py` + tests with 0.01 tolerance |
| Edge: negative/zero amount | `reader.py` reject row (fail-fast) |
| Edge: category case | normalize in `aggregate.py` (spec assumption) |

## Build Order

1. **Foundation**: `pyproject.toml`, package skeleton, fixtures.
2. **P1**: reader → aggregate → report writer → CLI happy path + tests.
3. **P2**: missing file, header-only, invalid row fail-fast + CLI exit code ≠ 0, no output file on error.
4. **P3** (optional slice): `--month YYYY-MM` on CLI; tests on `multi_month.csv`.

## Complexity Tracking

> No constitution violations requiring justification.

## Phase Outputs

| Artifact | Path |
|----------|------|
| Research | [research.md](./research.md) |
| Data model | [data-model.md](./data-model.md) |
| CLI contract | [contracts/cli.md](./contracts/cli.md) |
| Validation guide | [quickstart.md](./quickstart.md) |
