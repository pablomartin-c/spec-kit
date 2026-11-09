from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from expense_report.models import CategoryAggregate, ExpenseRow, ReportSummary

TOLERANCE = Decimal("0.01")


def _category_key(label: str) -> str:
    return label.strip().lower()


def summarize(rows: list[ExpenseRow]) -> ReportSummary:
    if not rows:
        raise ValueError("rows must not be empty")

    totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    display: dict[str, str] = {}
    grand = Decimal("0")
    largest = rows[0]

    for row in rows:
        key = _category_key(row.category)
        if key not in display:
            display[key] = row.category.strip()
        totals[key] += row.amount
        grand += row.amount
        if row.amount > largest.amount or (
            row.amount == largest.amount and row.source_row_number < largest.source_row_number
        ):
            largest = row

    by_category = [
        CategoryAggregate(key, display[key], totals[key])
        for key in sorted(display.keys(), key=lambda k: display[k].lower())
    ]

    # Verify internal consistency (SC-003)
    cat_sum = sum((c.total for c in by_category), start=Decimal("0"))
    if abs(cat_sum - grand) > TOLERANCE:
        raise ValueError("category totals do not match grand total")

    return ReportSummary(
        grand_total=grand,
        by_category=by_category,
        largest=largest,
        row_count=len(rows),
    )
