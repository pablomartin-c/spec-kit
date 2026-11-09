# spec-kit

Personal workspace for practicing **Spec-Driven Development (SDD)**.

Active feature: **CSV expense mini-report** (`specs/001-csv-expense-report/`).

## What this repo is for

SDD keeps intent and evidence ahead of implementation. Spec Kit skills under `.cursor/skills/` drive constitution → spec → plan → tasks → implement.

## Status

| Area | Status |
| --- | --- |
| SDD artifacts | `specs/001-csv-expense-report/` (spec, plan, tasks) |
| Application | Python CLI `expense-report` |
| Tests | `uv run pytest` (19 tests) |

## Setup and verify

Requires [uv](https://github.com/astral-sh/uv) and Python 3.12+.

```powershell
cd spec-kit
uv sync
uv run pytest
```

Generate a report:

```powershell
New-Item -ItemType Directory -Force .tmp
uv run expense-report -i tests/fixtures/valid_small.csv -o .tmp/report.txt
Get-Content .tmp/report.txt
```

See [quickstart.md](specs/001-csv-expense-report/quickstart.md) for error paths and month filter.

## References

- [GitHub Spec Kit](https://github.com/github/spec-kit)
- Dominicode / CBRM: contract (`spec.md`) → lane (tests) → verdict (commands + output)
