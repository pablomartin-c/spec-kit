from decimal import Decimal
from pathlib import Path

import pytest

from expense_report.models import (
    EmptyDataError,
    HeaderContractError,
    InputNotFoundError,
    NoRowsInPeriodError,
    RowInvalidError,
)
from expense_report.reader import load_expenses
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_happy_load_valid_small():
    rows = load_expenses(FIXTURES / "valid_small.csv")
    assert len(rows) == 20
    assert rows[0].expense_date.isoformat() == "2026-01-03"
    assert rows[0].amount == Decimal("12.50")
    assert all(r.amount > 0 for r in rows)


def test_missing_file():
    with pytest.raises(InputNotFoundError):
        load_expenses(FIXTURES / "does_not_exist.csv")


def test_empty_data(tmp_path: Path):
    path = tmp_path / "empty.csv"
    path.write_text("expense_date,amount,category,description\n", encoding="utf-8")
    with pytest.raises(EmptyDataError):
        load_expenses(path)


def test_bad_amount_row3(tmp_path: Path):
    src = (FIXTURES / "bad_amount_row3.csv").read_text(encoding="utf-8")
    path = tmp_path / "bad.csv"
    path.write_text(src, encoding="utf-8")
    with pytest.raises(RowInvalidError) as exc:
        load_expenses(path)
    assert exc.value.row_number == 3


def test_wrong_header(tmp_path: Path):
    path = tmp_path / "bad_header.csv"
    path.write_text("date,amount,cat,desc\n2026-01-01,1,a,b\n", encoding="utf-8")
    with pytest.raises(HeaderContractError):
        load_expenses(path)


def test_month_filter_january():
    rows = load_expenses(FIXTURES / "multi_month.csv", month="2026-01")
    assert len(rows) == 2
    assert all(r.expense_date.month == 1 for r in rows)


def test_month_filter_no_match():
    with pytest.raises(NoRowsInPeriodError):
        load_expenses(FIXTURES / "multi_month.csv", month="2026-03")
