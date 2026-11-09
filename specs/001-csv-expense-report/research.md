# Research: CSV Expense Mini-Report

## R1 — Runtime and packaging

- **Decision**: Python 3.12, `pyproject.toml`, install with `uv sync`, console script `expense-report`.
- **Rationale**: Already on machine via `uv`; pytest ecosystem; fits constitution simplicity and Pablo's data background.
- **Alternatives considered**: Node (extra stack), pandas (heavy for v1), PowerShell-only (weaker TDD story for cross-training).

## R2 — CSV parsing rules

- **Decision**: UTF-8, comma delimiter, first row is header; required columns exactly `expense_date`, `amount`, `category`, `description` (case-sensitive header names).
- **Rationale**: Unambiguous contract tests; matches spec logical names.
- **Alternatives considered**: Auto-detect delimiter (out of scope); snake_case aliases (adds ambiguity).

## R3 — Date and amount validation

- **Decision**: `expense_date` must parse as `YYYY-MM-DD`. `amount` must parse as decimal, **strictly > 0** (reject zero and negative at first bad row).
- **Rationale**: Spec edge case demands visible rule; fail-fast aligned with Q1 A.
- **Alternatives considered**: Allow zero as valid (rejected — not "positive money value" in spec).

## R4 — Report file format

- **Decision**: Plain UTF-8 text with fixed sections: title, grand total (2 decimal places), category table (sorted by category name), largest expense block (date, amount, category, description).
- **Rationale**: Meets FR-006; easy snapshot testing (golden files).
- **Alternatives considered**: JSON report (not "human-readable mini informe" in assumptions); Markdown (optional later).

## R5 — CLI UX and failure signaling

- **Decision**: Required args: `--input` / `-i`, `--output` / `-o`. Exit code `0` on success; non-zero on any validation/read error; stderr carries error message including 1-based data row index on parse failure; **do not create/truncate output file on failure** (write only after successful aggregation).
- **Rationale**: Q2 B + Q1 A; avoids empty/misleading report files.
- **Alternatives considered**: Write errors to output file (rejected).

## R6 — P3 month filter

- **Decision**: Optional flag `--month YYYY-MM`; when present, include only rows whose `expense_date` falls in that calendar month; if none match, error with no report file.
- **Rationale**: Implements FR-007 without changing P1 contract.
- **Alternatives considered**: Separate subcommand (deferred for simplicity).
