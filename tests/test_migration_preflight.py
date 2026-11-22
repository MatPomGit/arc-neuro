"""Regression tests for a read-only ARC Neuro migration inventory."""
import json
import sys
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
        self.assertEqual(report["record_count"], 69)
        self.assertEqual(report["record_kinds"], {"IDEA": 37, "MANUSCRIPT": 32})
        self.assertEqual(report["historical_record_count"], 63)
        self.assertEqual(report["historical_record_kinds"], {"IDEA": 31, "MANUSCRIPT": 32})
        self.assertEqual(report["later_record_ids"], sorted({
            "MSC-ZAH-P02", "MSC-ZAH-P03", "MSC-ZAH-P04",
            "MSC-ANX-P01", "MSC-FAT-P01", "MSC-INTERO-P01",
        }))
        self.assertEqual(sum(report["research_lines"].values()), 69)
        self.assertGreater(len(report["historical_stage_values"]), 5)

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
        catalog = json.loads((ROOT / "papers/catalog.json").read_text(encoding="utf-8"))
        historical = next(row for row in catalog["papers"] if row["id"] == "MSC-ADHD-P01")
        historical["id"] = "MSC-ADHD-P99"
        metadata = [
            json.loads((ROOT / "areas/index.json").read_text(encoding="utf-8")),
            json.loads((ROOT / "program.json").read_text(encoding="utf-8")),
            json.loads((ROOT / "portfolio/papers.json").read_text(encoding="utf-8")),
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
        self.assertEqual(
            set(report["later_record_ids"]) -
            {"MSC-ZAH-P02", "MSC-ZAH-P03", "MSC-ZAH-P04"},
            {"MSC-ANX-P01", "MSC-FAT-P01", "MSC-INTERO-P01"},
        )

    def test_duplicate_msc_fails(self):
        catalog = json.loads((ROOT / "papers/catalog.json").read_text(encoding="utf-8"))
        catalog["papers"][1]["id"] = catalog["papers"][0]["id"]
        other = [
            json.loads((ROOT / "areas/index.json").read_text(encoding="utf-8")),
            json.loads((ROOT / "program.json").read_text(encoding="utf-8")),
            json.loads((ROOT / "portfolio/papers.json").read_text(encoding="utf-8")),
        ]
        with patch("migration_preflight.json.loads", side_effect=[catalog, *other]):
            report = audit(ROOT)
        self.assertEqual(report["inventory_status"], "FAIL")
        self.assertTrue(any(s.startswith("duplicate_msc:") for s in report["findings"]))

    def test_symlinked_manuscript_is_rejected(self):
        original = Path.is_symlink
        def synthetic_symlink(path):
            return (path.as_posix().endswith(
                "papers/ndd/MSC-ADHD-P01/main.tex") or original(path))
        with patch.object(Path, "is_symlink", autospec=True,
                          side_effect=synthetic_symlink):
            report = audit(ROOT)
        self.assertEqual(report["inventory_status"], "FAIL")
        self.assertIn("symlink_tex:MSC-ADHD-P01", report["findings"])


if __name__ == "__main__":
    unittest.main()
