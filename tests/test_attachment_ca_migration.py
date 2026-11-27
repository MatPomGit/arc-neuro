"""Run the migrated CA synthetic/validation regression suite without human data."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class AttachmentCAMigrationTests(unittest.TestCase):
    def test_synthetic_suite(self):
        result = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", str(ROOT / "manuscripts/MSC-ATTACH-P06/analysis"), "-p", "test_analysis.py", "-v"], cwd=ROOT, capture_output=True, text=True, timeout=90)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertRegex(result.stderr + result.stdout, r"Ran [1-9][0-9]* tests?")

if __name__ == "__main__":
    unittest.main()
