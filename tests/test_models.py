from decimal import Decimal
from datetime import date

import pytest

from expense_report.models import (
    CategoryAggregate,
    ExpenseRow,
    ReportSummary,
    RowInvalidError,
    InputNotFoundError,
)


def test_expense_row_fields():
    row = ExpenseRow(
        expense_date=date(2026, 1, 15),
        amount=Decimal("10.00"),
        category="Food",
        description="Lunch",
        source_row_number=2,
    )
    assert row.category == "Food"
    assert row.source_row_number == 2


def test_error_codes():
    assert InputNotFoundError("x").code == "INPUT_NOT_FOUND"
    err = RowInvalidError("bad", 3)
    assert err.code == "ROW_INVALID"
    assert err.row_number == 3


def test_report_summary_structure():
    row = ExpenseRow(
        expense_date=date(2026, 1, 1),
        amount=Decimal("5"),
        category="A",
        description="d",
        source_row_number=2,
    )
    summary = ReportSummary(
        grand_total=Decimal("5"),
        by_category=[
            CategoryAggregate("a", "A", Decimal("5")),
        ],
        largest=row,
        row_count=1,
    )
    assert summary.row_count == 1
