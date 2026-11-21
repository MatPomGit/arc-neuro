"""Offline integrity checks for the AFF P05 plan handover, not scientific validation."""
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class AffectiveP05MigrationTest(unittest.TestCase):
    def test_pinned_source_and_plan(self):
        base=ROOT/"papers/affect/MSC-AFFECT-P05"
        metadata=json.loads((base/"migration.json").read_text(encoding="utf-8"))
        plan=(base/"plan.md").read_text(encoding="utf-8")
        self.assertEqual(metadata["source_blob_sha"],"92791dd60a5c9d2f3e6f702a7bb54453668fc5b4")
        self.assertEqual(metadata["source_commit_sha"],"0ff5f1531f03270c4f9fdcc7f3af6d2e9aca85dd")
        self.assertEqual(metadata["target_repository"],"MatPomGit/arc-neuro")
        self.assertEqual(metadata["status"],"PLANNED")
        self.assertIn("Motion-Confound-Controlled Hand-Kinematic",plan)
        self.assertNotIn("../../docs/",plan)
        self.assertIn(metadata["source_commit_sha"],plan)
        self.assertIn("MSC-AFFECT-P05",(base/"README.md").read_text(encoding="utf-8"))
    def test_programme_index_links(self):
        self.assertIn("(MSC-AFFECT-P05/plan.md)",(ROOT/"papers/affect/README.md").read_text(encoding="utf-8"))
        self.assertTrue((ROOT/"pages").exists())
if __name__=="__main__":
    unittest.main()
