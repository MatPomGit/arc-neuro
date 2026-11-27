"""Run each ARC H1 unittest in a fresh Python process.

This avoids process-lifetime contamination from native numerical libraries
while preserving the same unittest assertions and exit semantics.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
PATTERN = "test_h1*.py"


def flatten(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def main() -> None:
    loader = unittest.TestLoader()
    suite = loader.discover(str(TEST_DIR), pattern=PATTERN)
    tests = sorted(test.id() for test in flatten(suite))
    if not tests:
        raise RuntimeError("No H1 tests discovered.")

    failures: list[str] = []
    for index, test_id in enumerate(tests, start=1):
        print(f"[H1-TEST {index}/{len(tests)}] {test_id}", flush=True)
        completed = subprocess.run(
            [sys.executable, "-m", "unittest", test_id],
            cwd=TEST_DIR,
            check=False,
        )
        if completed.returncode != 0:
            failures.append(test_id)

    if failures:
        print("FAILED isolated H1 tests:", file=sys.stderr)
        for test_id in failures:
            print(f"  {test_id}", file=sys.stderr)
        raise SystemExit(1)

    print(f"H1 ISOLATED TESTS PASSED: {len(tests)}/{len(tests)}")


if __name__ == "__main__":
    main()
