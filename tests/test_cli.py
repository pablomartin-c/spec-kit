import subprocess
import sys
from pathlib import Path

import pytest

from expense_report.cli import main
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_cli_success(tmp_path: Path, capsys):
    out = tmp_path / "report.txt"
    main(["-i", str(FIXTURES / "valid_small.csv"), "-o", str(out)])
    assert out.is_file()
    assert out.read_text(encoding="utf-8").strip()


def test_cli_missing_input(tmp_path: Path):
    out = tmp_path / "report.txt"
    with pytest.raises(SystemExit) as exc:
        main(["-i", str(FIXTURES / "missing.csv"), "-o", str(out)])
    assert exc.value.code == 1
    assert not out.exists()


def test_cli_empty_data(tmp_path: Path):
    out = tmp_path / "report.txt"
    with pytest.raises(SystemExit) as exc:
        main(["-i", str(FIXTURES / "empty_data.csv"), "-o", str(out)])
    assert exc.value.code == 1
    assert not out.exists()


def test_cli_bad_row_no_output(tmp_path: Path):
    out = tmp_path / "report.txt"
    with pytest.raises(SystemExit) as exc:
        main(["-i", str(FIXTURES / "bad_amount_row3.csv"), "-o", str(out)])
    assert exc.value.code == 1
    assert not out.exists()


def test_cli_month_filter(tmp_path: Path):
    out = tmp_path / "jan.txt"
    main(
        [
            "-i",
            str(FIXTURES / "multi_month.csv"),
            "-o",
            str(out),
            "--month",
            "2026-01",
        ]
    )
    text = out.read_text(encoding="utf-8")
    assert "50.00" in text or "Grand Total: 50.00" in text


def test_entrypoint_installed():
    proc = subprocess.run(
        [sys.executable, "-m", "expense_report.cli", "--help"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
