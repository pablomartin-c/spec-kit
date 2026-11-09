from __future__ import annotations

from pathlib import Path

from expense_report.models import ReportSummary


def write_report(summary: ReportSummary, path: str | Path) -> None:
    out = Path(path)
    lines = [
        "Expense Report",
        "==============",
        f"Grand Total: {summary.grand_total:.2f}",
        "",
        "By Category",
        "-----------",
    ]
    for cat in summary.by_category:
        lines.append(f"{cat.display_label}: {cat.total:.2f}")
    lines.extend(
        [
            "",
            "Largest Expense",
            "---------------",
            f"Date: {summary.largest.expense_date.isoformat()}",
            f"Amount: {summary.largest.amount:.2f}",
            f"Category: {summary.largest.category}",
            f"Description: {summary.largest.description}",
            "",
        ]
    )
    out.write_text("\n".join(lines), encoding="utf-8")
