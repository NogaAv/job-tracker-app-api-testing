#!/usr/bin/env python3
"""Convenience runner for project pytest workflows.

Examples:
  python run_tests.py --help
  python run_tests.py --tcid TC-001
  python run_tests.py -k login
  python run_tests.py tests/public/test_verify_public_status_endpoint.py
  python run_tests.py --tcid TC-005 --tcid TC-006 -q
  python run_tests.py tests/auth/test_verify_login.py -k "login and valid"
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "reports"


def make_report_dir(custom_dir: str | None = None) -> Path:
    """Create a timestamped reports folder for this run."""
    if custom_dir:
        custom_path = Path(custom_dir)
        if not custom_path.is_absolute():
            custom_path = ROOT / custom_path
        report_dir = custom_path.resolve()
        report_dir.mkdir(parents=True, exist_ok=True)
        return report_dir

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    report_dir = REPORTS_DIR / stamp
    report_dir.mkdir(parents=True, exist_ok=True)
    return report_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run pytest the easy way for this API test project. "
            "Choose a tcid marker, use pytest -k filtering, or pass a file path."
        ),
        epilog=(
            "Examples:\n"
            "  python run_tests.py --help\n"
            "  python run_tests.py --tcid TC-001\n"
            "  python run_tests.py -k login\n"
            "  python run_tests.py tests/public/test_verify_public_status_endpoint.py\n"
            "  python run_tests.py --tcid TC-005 --tcid TC-006\n"
            "  python run_tests.py tests/auth/test_verify_login.py -q\n"
            "\n"
            "Notes:\n"
            "  - --tcid works with the project custom marker registered in pytest.ini\n"
            "  - -k behaves like pytest -k and filters by test name/expression\n"
            "  - passing a file path behaves like pytest <file>\n"
            "  - each run creates a timestamped report folder under reports/"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--tcid",
        action="append",
        default=[],
        help="Run tests linked to this tcid marker. Can be used multiple times, e.g. --tcid TC-001.",
    )
    parser.add_argument(
        "-k",
        dest="keyword",
        help="Keyword expression to match tests, same as pytest -k.",
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Optional pytest target(s): file path, directory, or node ID. Example: tests/auth/test_verify_login.py",
    )
    parser.add_argument(
        "--report-dir",
        help="Optional custom report path. Defaults to reports/<timestamp>.",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip creating a timestamped report directory and junit xml output.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args, extra_pytest_args = parser.parse_known_args()

    pytest_cmd = [sys.executable, "-m", "pytest"]

    if args.tcid:
        for tcid in args.tcid:
            pytest_cmd.extend(["--tcid", tcid])

    if args.keyword:
        pytest_cmd.extend(["-k", args.keyword])

    if args.targets:
        pytest_cmd.extend(args.targets)

    report_dir = None
    if not args.no_report:
        report_dir = make_report_dir(args.report_dir)
        pytest_cmd.extend(["--junitxml", str(report_dir / "junit.xml")])

    pytest_cmd.extend(extra_pytest_args)

    print("Running command:")
    print("  " + " ".join(pytest_cmd))
    if report_dir:
        print(f"Report folder: {report_dir}")
    print()

    completed = subprocess.run(pytest_cmd, cwd=ROOT, capture_output=True, text=True)

    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)

    if report_dir:
        output_path = report_dir / "pytest-output.txt"
        full_output = (
            "Command run:\n" + " ".join(pytest_cmd) + "\n\n" + completed.stdout + completed.stderr
        )
        output_path.write_text(full_output, encoding="utf-8")

    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
