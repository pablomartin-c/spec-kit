from __future__ import annotations

import argparse
import sys
from pathlib import Path

from expense_report.aggregate import summarize
from expense_report.models import ExpenseReportError
from expense_report.reader import load_expenses
from expense_report.report_writer import write_report


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate expense report from a gastos CSV.")
    parser.add_argument("-i", "--input", required=True, help="Input CSV path")
    parser.add_argument("-o", "--output", required=True, help="Output report file path")
    parser.add_argument("--month", help="Filter rows to YYYY-MM")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)
    output_path = Path(args.output)

    try:
        rows = load_expenses(args.input, month=args.month)
        summary = summarize(rows)
        write_report(summary, output_path)
    except ExpenseReportError as exc:
        if exc.code == "ROW_INVALID" and isinstance(exc, ExpenseReportError):
            msg = getattr(exc, "message", str(exc))
            if hasattr(exc, "row_number"):
                print(f"{msg}", file=sys.stderr)
            else:
                print(msg, file=sys.stderr)
        else:
            print(getattr(exc, "message", str(exc)), file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # pragma: no cover
        print(str(exc), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
