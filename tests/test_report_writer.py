from decimal import Decimal
from datetime import date
from pathlib import Path

from expense_report.aggregate import summarize
from expense_report.models import ExpenseRow
from expense_report.reader import load_expenses
from expense_report.report_writer import write_report
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_report_layout_matches_contract(tmp_path: Path):
    rows = load_expenses(FIXTURES / "valid_small.csv")
    summary = summarize(rows)
    out = tmp_path / "report.txt"
    write_report(summary, out)
    text = out.read_text(encoding="utf-8")
    assert "Expense Report" in text
    assert "Grand Total:" in text
    assert "By Category" in text
    assert "Largest Expense" in text
    assert "Date:" in text
    assert f"{summary.grand_total:.2f}" in text
