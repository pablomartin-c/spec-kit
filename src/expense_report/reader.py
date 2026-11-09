from __future__ import annotations

import csv
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable

from expense_report.models import (
    REQUIRED_HEADERS,
    EmptyDataError,
    ExpenseRow,
    HeaderContractError,
    InputNotFoundError,
    NoRowsInPeriodError,
    RowInvalidError,
)


def _parse_month_filter(month: str | None) -> tuple[int, int] | None:
    if month is None:
        return None
    try:
        parsed = datetime.strptime(month.strip(), "%Y-%m")
    except ValueError as exc:
        raise RowInvalidError(f"Invalid --month format (expected YYYY-MM): {month}", 0) from exc
    return parsed.year, parsed.month


def _row_in_month(expense_date: date, year: int, month: int) -> bool:
    return expense_date.year == year and expense_date.month == month


def load_expenses(path: str | Path, *, month: str | None = None) -> list[ExpenseRow]:
    file_path = Path(path)
    if not file_path.is_file():
        raise InputNotFoundError(f"Cannot read input file: {file_path}")

    period = _parse_month_filter(month)
    rows: list[ExpenseRow] = []

    try:
        with file_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise HeaderContractError("Missing CSV header row")

            fieldnames = [name.strip() for name in reader.fieldnames]
            if list(fieldnames) != list(REQUIRED_HEADERS):
                raise HeaderContractError(
                    f"Invalid header; expected {','.join(REQUIRED_HEADERS)}"
                )

            for csv_row_index, raw in enumerate(reader, start=2):
                try:
                    date_text = (raw.get("expense_date") or "").strip()
                    amount_text = (raw.get("amount") or "").strip()
                    category = (raw.get("category") or "").strip()
                    description = (raw.get("description") or "").strip()

                    if not date_text or not amount_text or not category or not description:
                        raise ValueError("missing required field")

                    expense_date = date.fromisoformat(date_text)
                    amount = Decimal(amount_text)
                    if amount <= 0:
                        raise ValueError("amount must be greater than zero")

                    if period is not None:
                        y, m = period
                        if not _row_in_month(expense_date, y, m):
                            continue

                    rows.append(
                        ExpenseRow(
                            expense_date=expense_date,
                            amount=amount,
                            category=category,
                            description=description,
                            source_row_number=csv_row_index,
                        )
                    )
                except (ValueError, InvalidOperation) as exc:
                    detail = exc.args[0] if exc.args else str(exc)
                    raise RowInvalidError(
                        f"Invalid data at row {csv_row_index}: {detail}",
                        csv_row_index,
                    ) from exc

    except OSError as exc:
        raise InputNotFoundError(f"Cannot read input file: {file_path}") from exc

    if not rows:
        if period is not None:
            raise NoRowsInPeriodError("No rows matched the selected period")
        raise EmptyDataError("No data rows to summarize")

    return rows


def filter_rows_for_month(rows: Iterable[ExpenseRow], month: str) -> list[ExpenseRow]:
    """Convenience for tests; load_expenses already filters when month is passed."""
    period = _parse_month_filter(month)
    assert period is not None
    y, m = period
    filtered = [r for r in rows if _row_in_month(r.expense_date, y, m)]
    if not filtered:
        raise NoRowsInPeriodError("No rows matched the selected period")
    return filtered
