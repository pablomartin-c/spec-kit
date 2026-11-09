# Intent — CSV expense mini-report

## Problem

Someone needs a quick, repeatable summary from a fixed-format expenses CSV without opening a spreadsheet or writing ad-hoc formulas each time. Errors in the file (bad rows, empty files) must be visible, not silently ignored.

## Outcome

The user runs one command against a known CSV schema and gets a short, trustworthy expense report (totals and highlights) suitable for a sanity check before deeper analytics.

## Constraints

- Practice project for Spec-Driven Development; smallest scope that still teaches the full artifact loop.
- Broader domains (invoices, leads) are related ideas but not required for the first slice.
- No credentials or external services in v1.
