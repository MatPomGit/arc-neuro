"""Validate provisional v3 records against the historical catalogue, offline."""
import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/paper.v3.schema.json").read_text(encoding="utf-8"))
CATALOG = json.loads((ROOT / "manuscripts/catalog.json").read_text(encoding="utf-8"))["papers"]


class V3MetadataTests(unittest.TestCase):
    def test_exact_record_coverage(self):
        expected = {p["id"] for p in CATALOG}
        self.assertEqual(len(expected), len(CATALOG))
        actual = {p.parent.name for p in (ROOT / "manuscripts").glob("MSC-*/paper.json")}
        self.assertEqual(actual, expected)

    def test_metadata_preserves_identity_and_source(self):
        for old in CATALOG:
            ident = old["id"]
            with self.subTest(id=ident):
                folder = ROOT / "manuscripts" / ident
                path = folder / "paper.json"
                self.assertFalse(path.is_symlink())
                record = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(set(SCHEMA["required"]) - set(record), set())
                self.assertEqual(set(record) - set(SCHEMA["properties"]), set())
                for key in ("id", "title", "area"):
                    self.assertEqual(record[key], old[key])
                self.assertEqual(record["schema_version"], 3)
                for key in ("research_state", "publication_stage", "relation"):
                    self.assertIn(record[key], SCHEMA["properties"][key]["enum"])
                self.assertEqual(record["manuscript"]["path"], old["manuscript_path"])
                self.assertEqual(old["manuscript_path"], f"manuscripts/{ident}/main.tex")
                self.assertTrue((ROOT / old["manuscript_path"]).is_file())
                self.assertFalse(record["public_listing"])
                self.assertIsNone(record["stage_evidence"])
                self.assertNotIn(record["publication_stage"], {"submitted", "accepted", "published"})
                if old["record_kind"] == "IDEA":
                    self.assertEqual(record["publication_stage"], "concept")
                self.assertEqual(set(record["dependencies"]), {"tools", "equipment", "datasets"})
                for group in record["dependencies"].values():
                    self.assertIsInstance(group, list)


if __name__ == "__main__":
    unittest.main()
