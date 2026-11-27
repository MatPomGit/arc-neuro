"""Test limits without reducing scientific source material."""
from __future__ import annotations
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("arc_neuro_docs", ROOT / "scripts/validate_documentation.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validator)


class DocumentationPolicyTests(unittest.TestCase):
    def fixture(self, tmp: str) -> Path:
        dest = Path(tmp) / "xr"
        shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns(
            ".git", ".venv", "__pycache__", "build"))
        return dest

    def test_scaffold_budgets_pass(self):
        self.assertEqual([], validator.check_documentation(ROOT))

    def test_unicode_not_utf8_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp)
            p = root / "config/documentation-policy.json"
            data = json.loads(p.read_text())
            data["exact_limits"]["SUPPORT.md"] = 100
            p.write_text(json.dumps(data))
            (root / "SUPPORT.md").write_text("ą" * 100, encoding="utf-8")
            self.assertEqual([], validator.check_documentation(root))

    def test_overlong_architecture_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp)
            (root / "ARCHITECTURE.md").write_text("x" * 12001, encoding="utf-8")
            self.assertTrue(any("DOC LENGTH EXCEEDED: ARCHITECTURE.md" in e
                                for e in validator.check_documentation(root)))

    def test_adr_glob_limit_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp)
            (root / "docs/adr/0004-new.md").write_text("x" * 6501, encoding="utf-8")
            self.assertTrue(any("DOC LENGTH EXCEEDED: docs/adr/0004-new.md" in e
                                for e in validator.check_documentation(root)))

    def test_named_research_manuscripts_preserved(self):
        self.assertTrue((ROOT / "manuscripts/MSC-ADHD-P01/README.md").is_file())
        self.assertTrue((ROOT / "manuscripts/MSC-SAPIENS-P03/README.md").is_file())
        self.assertEqual([], validator.check_documentation(ROOT))

    def test_manuscripts_are_not_capped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp)
            (root / "manuscripts/P01").mkdir(parents=True)
            (root / "manuscripts/P01/manuscript.md").write_text(
                "hypothesis\n" * 12000, encoding="utf-8")
            self.assertEqual([], validator.check_documentation(root))

    def test_missing_required_governance_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp)
            (root / "GOVERNANCE.md").unlink()
            self.assertIn("DOC MISSING: GOVERNANCE.md",
                          validator.check_documentation(root))

    def test_boolean_version_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp)
            p = root / "config/documentation-policy.json"
            data = json.loads(p.read_text())
            data["schema_version"] = True
            p.write_text(json.dumps(data))
            self.assertIn("DOC POLICY: unsupported schema_version",
                          validator.check_documentation(root))

    def test_invalid_policy_path_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp)
            p = root / "config/documentation-policy.json"
            data = json.loads(p.read_text())
            data["exact_limits"]["../private.md"] = 1000
            p.write_text(json.dumps(data))
            self.assertIn("DOC POLICY: invalid limit or path ../private.md",
                          validator.check_documentation(root))

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp)
            outside = Path(tmp) / "private.md"
            outside.write_text("private")
            (root / "SUPPORT.md").unlink()
            (root / "SUPPORT.md").symlink_to(outside)
            self.assertIn("DOC SYMLINK: SUPPORT.md",
                          validator.check_documentation(root))

    def test_public_page_over_budget_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp)
            (root / "site/extra.md").write_text("x" * 6001, encoding="utf-8")
            self.assertTrue(any("DOC LENGTH EXCEEDED: site/extra.md" in e
                                for e in validator.check_documentation(root)))


    def test_contributing_not_required_or_present(self):
        self.assertFalse((ROOT / "CONTRIBUTING.md").exists())
        self.assertEqual([], validator.check_documentation(ROOT))

    def test_limit_on_named_manuscript_overview_is_finite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp)
            (root / "manuscripts/MSC-ADHD-P01/README.md").write_text(
                "x" * 10001, encoding="utf-8")
            self.assertTrue(any(
                "DOC LENGTH EXCEEDED: manuscripts/MSC-ADHD-P01/README.md" in error
                for error in validator.check_documentation(root)))

if __name__ == "__main__":
    unittest.main()
