import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from environment import collect


class EnvironmentTests(unittest.TestCase):
    def test_report_and_source_hashes(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"report.json"
            p.write_bytes(b'{"synthetic":true}')
            a=collect(p)
            self.assertEqual(a["report_sha256"],hashlib.sha256(p.read_bytes()).hexdigest())
            self.assertEqual(a["source_sha256"],collect(p)["source_sha256"])
            self.assertIn("environment.py",a["source_sha256"])
            self.assertIn("requirements-ci.txt",a["source_sha256"])
            p.write_bytes(b'{"synthetic":false}')
            self.assertNotEqual(a["report_sha256"],collect(p)["report_sha256"])

    def test_unknown_git_status_not_clean(self):
        with patch("environment.cmd",return_value=None):
            a=collect()
        self.assertIsNone(a["git_sha"])
        self.assertIsNone(a["git_tracked_dirty"])


if __name__=="__main__":
    unittest.main()
