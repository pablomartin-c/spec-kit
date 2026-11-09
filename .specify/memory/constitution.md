# Spec Kit Practice Constitution

## Core Principles

### I. Spec-First
Durable truth lives in artifacts (`constitution`, `spec`, `plan`, `tasks`), not in chat history.
Code is a consequence of an accepted specification. If behavior must change, update the spec first,
then the plan/tasks, then the code.

### II. What/Why vs How
The specification describes **what** users can do and **why** it matters.
Technology choices, libraries, schemas, and folder layout belong only in the **plan**.
Mark unknowns with `[NEEDS CLARIFICATION]` instead of guessing.

### III. Test-First (NON-NEGOTIABLE)
No production behavior without a failing test first (red → green → refactor).
"Done" requires runnable evidence: the command that proves the acceptance criterion, plus its output.
Skipping TDD is out of scope for this practice project.

### IV. Evidence Over Opinion
Every acceptance criterion maps to a verification command.
Reviews and hand-offs prefer a verdict (criterion → command → result) over "looks fine".
Extra code without a contract is rejected or folded back into the spec before merge.

### V. Simplicity for Learning
Prefer the smallest stack that teaches the SDD loop.
No premature abstractions, no speculative features, no "just in case" modules.
One feature slice at a time; finish evidence before starting the next task.

## Security and Environment

- Never commit credentials, API keys, tokens, or secrets.
- Keep secrets in local env / secret store; document names only in README or plan.
- Prefer PowerShell scripts on Windows; call out steps that may need IT approval.

## Development Workflow

Artifact order for each feature:

`constitution` (once per project) → `spec` → `clarify` → `plan` → `tasks` → `analyze` → `implement`

- One artifact focus per turn; do not generate application code in the same turn as the first draft of a spec.
- Agent guidance for this repo lives in `AGENTS.md` and/or `.cursor/rules/*.mdc` when added.
- Spec Kit skills under `.cursor/skills/` are the preferred invocation path in Cursor.

## Governance

This constitution supersedes ad-hoc prompting when they conflict.
Amendments require an explicit edit to this file, a version bump, and a one-line rationale in the change.
All PRs must show: which principle(s) apply, and which command verified the change.

**Version**: 1.0.0 | **Ratified**: 2026-11-09 | **Last Amended**: 2026-11-09
