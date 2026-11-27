"""Regression tests for a read-only ARC Neuro migration inventory."""
from collections import Counter
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from migration_preflight import audit


class NeuroMigrationPreflightTests(unittest.TestCase):
    def test_inventory_pass_does_not_approve_v2_migration(self):
        report = audit(ROOT)
        self.assertEqual(report["inventory_status"], "PASS", report["findings"])
        self.assertEqual(report["migration_status"], "BLOCKED")
        self.assertFalse(report["migration_ready"])
        records = json.loads((ROOT / "manuscripts/catalog.json").read_text(encoding="utf-8"))["papers"]
        self.assertEqual(report["record_count"], len(records))
        self.assertEqual(report["record_kinds"], dict(Counter(p["record_kind"] for p in records)))
        self.assertEqual(report["historical_record_count"], 63)
        self.assertEqual(report["historical_record_kinds"], {"IDEA": 31, "MANUSCRIPT": 32})
        historical_ids = {line.strip() for line in (ROOT / "config/historical-manuscripts-63.txt").read_text(encoding="utf-8").splitlines()
                          if line.strip() and not line.lstrip().startswith("#")}
        self.assertEqual(report["later_record_ids"], sorted({p["id"] for p in records} - historical_ids))
        self.assertEqual(report["research_lines"], dict(Counter(p["area"] for p in records)))
        self.assertGreater(len(report["historical_stage_values"]), 5)

    def test_valid_catalog_growth_does_not_change_frozen_migration_evidence(self):
        records = json.loads((ROOT / "manuscripts/catalog.json").read_text(encoding="utf-8"))
        existing = {p["id"] for p in records["papers"]}
        index = 1
        while f"MSC-TEST-P{index:02d}" in existing:
            index += 1
        ident = f"MSC-TEST-P{index:02d}"
        before = audit(ROOT)
        records["papers"].append({
            "id": ident, "area": "affect", "record_kind": "IDEA",
            "stage": "IDEA_REVIEW", "title": "Synthetic inventory fixture",
            "manuscript_path": f"manuscripts/{ident}/main.tex",
            "readme_path": f"manuscripts/{ident}/README.md",
        })
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for relative in ("config/historical-manuscripts-63.txt",
                             "config/research-lines.json", "program.json"):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())
            (root / "manuscripts").mkdir()
            (root / "manuscripts/catalog.json").write_text(json.dumps(records), encoding="utf-8")
            for paper in records["papers"]:
                for key in ("manuscript_path", "readme_path"):
                    path = root / paper[key]
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.touch()
            after = audit(root)
            self.assertEqual(after["inventory_status"], "PASS", after["findings"])
            self.assertEqual(after["record_count"], before["record_count"] + 1)
            self.assertEqual(after["historical_record_count"], before["historical_record_count"])
            self.assertEqual(after["historical_record_kinds"], before["historical_record_kinds"])
            self.assertIn(ident, after["later_record_ids"])
            self.assertFalse(after["migration_ready"])
            (root / f"manuscripts/{ident}/main.tex").unlink()
            invalid = audit(root)
            self.assertEqual(invalid["inventory_status"], "FAIL")
            self.assertIn("missing_tex:" + ident, invalid["findings"])

    def test_frozen_historical_manifest_rejects_silent_replacement(self):
        original_read_bytes = Path.read_bytes

        def fake_read_bytes(path):
            content = original_read_bytes(path)
            if path.name == "historical-manuscripts-63.txt":
                return content.replace(b"MSC-AAL-P02", b"MSC-AAL-P99")
            return content

        with patch.object(Path, "read_bytes", autospec=True,
                          side_effect=fake_read_bytes):
            report = audit(ROOT)
        self.assertEqual(report["inventory_status"], "FAIL")
        self.assertIn("historical_63_snapshot_modified", report["findings"])
        self.assertIn("expected_63_historical_unique_msc", report["findings"])
        self.assertEqual(report["migration_status"], "BLOCKED")
        self.assertFalse(report["migration_ready"])

    def test_replacing_a_legacy_id_does_not_rewrite_historical_evidence(self):
        catalog = json.loads((ROOT / "manuscripts/catalog.json").read_text(encoding="utf-8"))
        historical = next(row for row in catalog["papers"] if row["id"] == "MSC-ADHD-P01")
        historical["id"] = "MSC-ADHD-P99"
        metadata = [
            json.loads((ROOT / "config/research-lines.json").read_text(encoding="utf-8")),
            json.loads((ROOT / "program.json").read_text(encoding="utf-8")),
            {"schema_version": 1, "papers": []},
        ]
        with patch("migration_preflight.json.loads", side_effect=[catalog, *metadata]):
            report = audit(ROOT)
        self.assertEqual(report["inventory_status"], "FAIL")
        self.assertIn("expected_63_historical_unique_msc", report["findings"])

    def test_three_later_ideas_are_excluded_from_migration_evidence(self):
        report = audit(ROOT)
        self.assertEqual(report["historical_record_count"], 63)
        self.assertEqual(report["migration_status"], "BLOCKED")
        self.assertFalse(report["migration_ready"])
        self.assertTrue({"MSC-ANX-P01", "MSC-FAT-P01", "MSC-INTERO-P01"} <= set(report["later_record_ids"]))

    def test_duplicate_msc_fails(self):
        catalog = json.loads((ROOT / "manuscripts/catalog.json").read_text(encoding="utf-8"))
        catalog["papers"][1]["id"] = catalog["papers"][0]["id"]
        other = [
            json.loads((ROOT / "config/research-lines.json").read_text(encoding="utf-8")),
            json.loads((ROOT / "program.json").read_text(encoding="utf-8")),
            {"schema_version": 1, "papers": []},
        ]
        with patch("migration_preflight.json.loads", side_effect=[catalog, *other]):
            report = audit(ROOT)
        self.assertEqual(report["inventory_status"], "FAIL")
        self.assertTrue(any(s.startswith("duplicate_msc:") for s in report["findings"]))

    def test_symlinked_manuscript_is_rejected(self):
        original = Path.is_symlink
        def synthetic_symlink(path):
            return (path.as_posix().endswith(
                "manuscripts/MSC-ADHD-P01/main.tex") or original(path))
        with patch.object(Path, "is_symlink", autospec=True,
                          side_effect=synthetic_symlink):
            report = audit(ROOT)
        self.assertEqual(report["inventory_status"], "FAIL")
        self.assertIn("symlink_tex:MSC-ADHD-P01", report["findings"])


if __name__ == "__main__":
    unittest.main()
