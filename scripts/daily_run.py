#!/usr/bin/env python3
"""
Daily Run Script
Runs tests, validates data, and prepares a git commit.

Usage:
    python scripts/daily_run.py
    # or
    make daily
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_command(cmd: str, description: str) -> bool:
    """Run a shell command and return True if successful."""
    print(f"\n{'='*50}")
    print(f"  {description}")
    print(f"{'='*50}")
    result = subprocess.run(cmd, shell=True, cwd=PROJECT_ROOT)
    success = result.returncode == 0
    status = "PASS" if success else "FAIL"
    print(f"  [{status}] {description}")
    return success


def main():
    print(f"\n🚀 Daily ML Run — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    results = {}

    # 1. Run pytest
    results["tests"] = run_command(
        "python -m pytest tests/ -v --tb=short",
        "Running pytest test suite",
    )

    # 2. Run linter
    results["lint"] = run_command(
        "python -m flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503",
        "Running flake8 linter",
    )

    # 3. Check CSV data files exist
    sample_dir = PROJECT_ROOT / "data" / "sample"
    csv_files = list(sample_dir.glob("*.csv"))
    results["data"] = len(csv_files) > 0
    print(f"\n  [{'PASS' if results['data'] else 'FAIL'}] Found {len(csv_files)} sample CSV file(s)")

    # 4. Summary
    print(f"\n{'='*60}")
    print("  DAILY RUN SUMMARY")
    print(f"{'='*60}")

    all_passed = True
    for check, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}")
        if not passed:
            all_passed = False

    if all_passed:
        print(f"\n  🎉 All checks passed!")

        # Git commit
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        run_command("git add -A", "Staging changes")
        run_command(
            f'git commit -m "daily: {timestamp} — all checks passed" || echo "Nothing to commit"',
            "Committing changes",
        )
        print("\n  Run 'git push' to push to GitHub.")
    else:
        print(f"\n  ⚠️  Some checks failed. Fix issues before committing.")
        sys.exit(1)


if __name__ == "__main__":
    main()
