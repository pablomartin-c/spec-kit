---
description: "Task list for CSV Expense Mini-Report"
---

# Tasks: CSV Expense Mini-Report

**Input**: Design documents from `/specs/001-csv-expense-report/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli.md

**Tests**: Required (constitution Article III + spec success criteria).

**Organization**: By user story (P1 → P2 → P3), TDD within each phase.

## Format: `[ID] [P?] [Story] Description`

**Hecho cuando:** each task lists its verification command at the end of the description line (after `—`).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Python package skeleton and harness

- [x] T001 Create `pyproject.toml` with package `expense_report`, Python `>=3.12`, pytest dev dep, and console script `expense-report = expense_report.cli:main` — `uv sync` exits 0
- [x] T002 Create package dirs `src/expense_report/__init__.py` and empty module stubs per plan.md — `uv run python -c "import expense_report"` succeeds
- [x] T003 [P] Add root `.gitignore` entries for `.tmp/`, `__pycache__/`, `.venv/` (do not ignore `.specify/` or `specs/`) — file exists at repo root
- [x] T004 [P] Create `tests/conftest.py` with `FIXTURES` path helper pointing to `tests/fixtures/` — `uv run pytest --collect-only` exits 0

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared types, fixtures, and CSV reader contract used by all stories

**⚠️ CRITICAL**: No user story CLI work until reader + models tests pass

- [x] T005 [P] Add `tests/fixtures/valid_small.csv` (≥5 rows, 2+ categories) matching data-model header — file committed
- [x] T006 [P] Implement `ExpenseRow`, `ReportSummary`, `CategoryAggregate`, and exception types in `src/expense_report/models.py` per data-model.md — `uv run pytest tests/test_models.py` (after T007) passes
- [x] T007 [P] Write failing tests in `tests/test_models.py` for dataclass/errors — run before T006; **must FAIL** then pass after T006
- [x] T008 Write failing tests in `tests/test_reader.py` for happy parse of `valid_small.csv` (row count, decimal amounts, dates YYYY-MM-DD) — **must FAIL** before T009
- [x] T009 Implement `load_expenses(path)` in `src/expense_report/reader.py`: UTF-8 comma CSV, exact headers, amount `> 0`, non-empty category/description after strip, attach 1-based data row numbers — `uv run pytest tests/test_reader.py -k happy` passes

**Checkpoint**: `uv run pytest tests/test_models.py tests/test_reader.py` green (US1 not yet wired to CLI)

---

## Phase 3: User Story 1 — Generate expense summary (Priority: P1) 🎯 MVP

**Goal**: Read valid CSV → write report file with total, categories, largest expense (FR-001, FR-004, FR-006).

**Independent Test**: `uv run expense-report -i tests/fixtures/valid_small.csv -o .tmp/report.txt` exit 0; report contains required sections per `contracts/cli.md`.

### Tests for User Story 1

> Write FIRST; ensure RED before implementation.

- [x] T010 [P] [US1] Add failing tests in `tests/test_aggregate.py` for grand total, case-insensitive category grouping, largest expense tie-break (lowest row number) — **FAIL** before T011
- [x] T011 [P] [US1] Add failing golden test in `tests/test_report_writer.py` comparing output layout to snapshot for `valid_small.csv` — **FAIL** before T012
- [x] T012 [P] [US1] Add failing CLI test in `tests/test_cli.py`: success path creates output file with non-empty content — **FAIL** before T013–T015

### Implementation for User Story 1

- [x] T013 [US1] Implement `summarize(rows)` in `src/expense_report/aggregate.py` (0.01 tolerance for internal sums per SC-003) — `uv run pytest tests/test_aggregate.py` passes
- [x] T014 [US1] Implement `write_report(summary, path)` in `src/expense_report/report_writer.py` per `contracts/cli.md` — `uv run pytest tests/test_report_writer.py` passes
- [x] T015 [US1] Implement `main()` in `src/expense_report/cli.py` with `--input`/`--output` (call reader → aggregate → writer) — `uv run pytest tests/test_cli.py -k success` passes

**Checkpoint**: US1 complete — `uv run expense-report -i tests/fixtures/valid_small.csv -o .tmp/report.txt` + full `tests/test_cli.py` success tests green

---

## Phase 4: User Story 2 — File and row errors (Priority: P2)

**Goal**: Explicit failures; fail-fast row errors; no success report file on error (FR-005, FR-008).

**Independent Test**: missing input, header-only, bad row → non-zero exit, stderr mentions error, output path not created/overwritten on failure.

### Tests for User Story 2

- [x] T016 [P] [US2] Add `tests/fixtures/empty_data.csv` (header only) and `tests/fixtures/bad_amount_row3.csv` (invalid amount on row 3) — files committed
- [x] T017 [P] [US2] Failing tests in `tests/test_reader.py` for `EMPTY_DATA`, `ROW_INVALID` with row number in message — **FAIL** until T018
- [x] T018 [P] [US2] Failing CLI tests in `tests/test_cli.py`: missing file, empty data, bad row (assert exit code ≠ 0, no output file) — **FAIL** until T019–T020

### Implementation for User Story 2

- [x] T019 [US2] Extend `reader.py` with `INPUT_NOT_FOUND`, `HEADER_CONTRACT`, fail-fast `ROW_INVALID` (zero/negative amount, bad date, empty fields) — `uv run pytest tests/test_reader.py` passes
- [x] T020 [US2] Update `cli.py` to write report only after full successful parse+aggregate; errors to stderr + non-zero exit — `uv run pytest tests/test_cli.py` passes for US2 cases

**Checkpoint**: `uv run pytest` all green; US2 scenarios in quickstart.md runnable

---

## Phase 5: User Story 3 — Month filter (Priority: P3)

**Goal**: Optional `--month YYYY-MM` filters rows (FR-007).

**Independent Test**: `multi_month.csv` + `--month 2026-01` totals only January rows.

### Tests for User Story 3

- [x] T021 [P] [US3] Add `tests/fixtures/multi_month.csv` (rows in two months) — file committed
- [x] T022 [P] [US3] Failing tests in `tests/test_reader.py` or `tests/test_aggregate.py` for month filter and `NO_ROWS_IN_PERIOD` — **FAIL** until T023
- [x] T023 [P] [US3] Failing CLI test with `--month` flag — **FAIL** until T024

### Implementation for User Story 3

- [x] T024 [US3] Add optional month filter in reader/aggregate pipeline and `--month` on CLI per research.md R6 — `uv run pytest` passes including US3 CLI test

**Checkpoint**: quickstart P3 command succeeds

---

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T025 Update root `README.md` with install, test, and example `expense-report` command linking to `quickstart.md` — manual read confirms
- [x] T026 Run full quickstart.md validation checklist; record command outputs in task notes or PR — all steps match expected outcomes
- [x] T027 [P] Add `specs/001-csv-expense-report/checklists/implementation.md` coverage tick after implement (optional self-audit FR ↔ tests) — file exists

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 → Phase 2 → Phase 3 (MVP) → Phase 4 → Phase 5 → Phase 6
- Stop after Phase 3 to demo MVP (constitution simplicity)

### User Story Dependencies

- **US1**: after Phase 2 only
- **US2**: extends reader/CLI; tests assume US1 happy path still passes
- **US3**: extends reader/CLI; independent tests on `multi_month.csv`

### Parallel Opportunities

- T003, T004, T005, T006+T007 (tests first), T010–T012 (US1 tests), T016–T018 (US2 tests), T021–T023 (US3 tests)

---

## Coverage Matrix (Spec → Tasks → Verify)

| Spec | Task IDs | Verify command |
|------|----------|----------------|
| US1 / FR-001,004,006 | T010–T015 | `uv run expense-report -i tests/fixtures/valid_small.csv -o .tmp/report.txt` |
| US2 / FR-005,008 | T016–T020 | `uv run pytest tests/test_cli.py -k error` |
| US3 / FR-007 | T021–T024 | `uv run expense-report ... --month 2026-01` |
| FR-003 | T008–T009, T019 | `uv run pytest tests/test_reader.py` |
| SC-002 | T018–T020 | all US2 CLI tests exit ≠ 0 |
| SC-003 | T010, T013 | `uv run pytest tests/test_aggregate.py` |
| Constitution III | all `test_*` before impl | pytest red then green per phase |

---

## Implementation Strategy

### MVP First

1. Complete Phases 1–2
2. Complete Phase 3 (US1 only)
3. **STOP** — run quickstart happy path; optional commit
4. Continue US2 → US3 → Polish

### Suggested MVP scope

**Through T015** (User Story 1 only): 15 tasks after setup/foundation ≈ **T001–T015**.

---

## Notes

- One task group per agent turn during `/speckit-implement` (Project B rule)
- Do not commit credentials; fixtures use fictional data only
- Windows paths in examples use repo-relative `.tmp/` for outputs
