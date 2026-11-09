# Data Model: CSV Expense Mini-Report

## ExpenseRow

| Field | Type (logical) | Validation |
|-------|----------------|------------|
| `expense_date` | calendar date | `YYYY-MM-DD`, must be valid date |
| `amount` | money | Decimal > 0 |
| `category` | string | Non-empty after strip |
| `description` | string | Non-empty after strip |
| `source_row_number` | integer | 1-based index in CSV (for errors), not a CSV column |

## CategoryAggregate

| Field | Validation |
|-------|------------|
| `category_key` | Normalized key: `category.strip().lower()` for grouping |
| `display_label` | First-seen trimmed category text for report |
| `total` | Sum of `amount` for rows in scope |

## ReportSummary

| Field | Source |
|-------|--------|
| `grand_total` | Sum of all in-scope rows |
| `by_category` | List of `CategoryAggregate`, sorted by `display_label` |
| `largest` | `ExpenseRow` with max `amount` (tie-break: lowest `source_row_number`) |
| `row_count` | Count of in-scope rows |

## Error taxonomy (application)

| Code | When | User-visible |
|------|------|--------------|
| `INPUT_NOT_FOUND` | Input path missing/unreadable | stderr message |
| `EMPTY_DATA` | Headers only | stderr message |
| `HEADER_CONTRACT` | Missing/wrong column names | stderr message |
| `ROW_INVALID` | Row fails parse/validation | stderr + row number |
| `NO_ROWS_IN_PERIOD` | P3 filter matches nothing | stderr message |

## CSV file contract (physical)

Header row (exact names):

```text
expense_date,amount,category,description
```

Example data row:

```text
2026-01-15,42.50,Travel,Taxi airport
```

## State

Stateless CLI: each invocation reads CSV → produces report file or error. No persistence between runs.
