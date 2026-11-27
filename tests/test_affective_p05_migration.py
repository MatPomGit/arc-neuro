"""Migrated MSC-AFFECT-P05 is one real paper folder, with pinned provenance."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class AffectiveP05MigrationTest(unittest.TestCase):
    def test_one_article_folder_and_provenance(self):
        folder=ROOT/"manuscripts/MSC-AFFECT-P05"
        info=json.loads((folder/"migration.json").read_text(encoding="utf-8"))
        plan=(folder/"plan.md").read_text(encoding="utf-8")
        self.assertTrue((folder/"main.tex").is_file())
        self.assertEqual(info["target_path"],"manuscripts/MSC-AFFECT-P05/plan.md")
        self.assertEqual(info["local_license_path"],"manuscripts/MSC-AFFECT-P05/ORIGINAL_LICENSE")
        self.assertEqual(info["source_blob_sha"],"92791dd60a5c9d2f3e6f702a7bb54453668fc5b4")
        self.assertEqual(info["source_commit_sha"],"0ff5f1531f03270c4f9fdcc7f3af6d2e9aca85dd")
        self.assertEqual(info["status"],"PLANNED")
        self.assertEqual(info["migration_phase"],"copy_verified_integrated")
        self.assertEqual(info["source_license_spdx"],"Apache-2.0")
        self.assertIn("Apache License",(folder/"ORIGINAL_LICENSE").read_text(encoding="utf-8"))
        self.assertIn("Motion-Confound-Controlled Hand-Kinematic",plan)
        self.assertNotIn("../../docs/",plan)
        self.assertIn(info["source_commit_sha"],plan)
        self.assertIn("MSC-AFFECT-P05",(folder/"README.md").read_text(encoding="utf-8"))
    def test_no_duplicate_intake_and_complete_affect_area(self):
        self.assertFalse((ROOT/"research/affective/MSC-AFFECT-P05").exists())
        dirs=[p.name for p in (ROOT/"manuscripts").iterdir() if p.is_dir() and p.name == "MSC-AFFECT-P05"]
        self.assertEqual(set(dirs),{"MSC-AFFECT-P05","MSC-AR-P16","MSC-AR-P24","MSC-MGR-P01","MSC-INTERO-P01"})
        self.assertIn("MSC-AFFECT-P05",(ROOT/"manuscripts/affect/README.md").read_text(encoding="utf-8"))
if __name__=="__main__":
    unittest.main()
