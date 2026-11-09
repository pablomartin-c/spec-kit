from decimal import Decimal
from datetime import date

from expense_report.aggregate import summarize
from expense_report.models import ExpenseRow


def test_grand_total_and_categories():
    rows = [
        ExpenseRow(date(2026, 1, 1), Decimal("10"), "Food", "a", 2),
        ExpenseRow(date(2026, 1, 2), Decimal("20"), "food", "b", 3),
        ExpenseRow(date(2026, 1, 3), Decimal("5"), "Travel", "c", 4),
    ]
    summary = summarize(rows)
    assert summary.grand_total == Decimal("35")
    assert summary.row_count == 3
    food = next(c for c in summary.by_category if c.display_label.lower() == "food")
    assert food.total == Decimal("30")


def test_largest_tiebreak_lower_row_number():
    rows = [
        ExpenseRow(date(2026, 1, 1), Decimal("50"), "A", "first", 2),
        ExpenseRow(date(2026, 1, 2), Decimal("50"), "B", "second", 5),
    ]
    summary = summarize(rows)
    assert summary.largest.source_row_number == 2
