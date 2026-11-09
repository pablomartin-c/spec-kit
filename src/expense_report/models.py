from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


REQUIRED_HEADERS = ("expense_date", "amount", "category", "description")


class ExpenseReportError(Exception):
    """Base error with a stable code for CLI messaging."""

    code: str = "UNKNOWN"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class InputNotFoundError(ExpenseReportError):
    code = "INPUT_NOT_FOUND"


class EmptyDataError(ExpenseReportError):
    code = "EMPTY_DATA"


class HeaderContractError(ExpenseReportError):
    code = "HEADER_CONTRACT"


class RowInvalidError(ExpenseReportError):
    code = "ROW_INVALID"

    def __init__(self, message: str, row_number: int) -> None:
        super().__init__(message)
        self.row_number = row_number


class NoRowsInPeriodError(ExpenseReportError):
    code = "NO_ROWS_IN_PERIOD"


@dataclass(frozen=True)
class ExpenseRow:
    expense_date: date
    amount: Decimal
    category: str
    description: str
    source_row_number: int


@dataclass(frozen=True)
class CategoryAggregate:
    category_key: str
    display_label: str
    total: Decimal


@dataclass(frozen=True)
class ReportSummary:
    grand_total: Decimal
    by_category: list[CategoryAggregate]
    largest: ExpenseRow
    row_count: int
