"""Offline validation for AFFECT P05 intake outside public paper slots."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class AffectiveP05MigrationTest(unittest.TestCase):
    def test_research_intake_is_version_pinned(self):
        folder=ROOT/"research/affective/MSC-AFFECT-P05"
        info=json.loads((folder/"migration.json").read_text(encoding="utf-8"))
        plan=(folder/"plan.md").read_text(encoding="utf-8")
        self.assertEqual(info["source_blob_sha"],"92791dd60a5c9d2f3e6f702a7bb54453668fc5b4")
        self.assertEqual(info["source_commit_sha"],"0ff5f1531f03270c4f9fdcc7f3af6d2e9aca85dd")
        self.assertEqual(info["target_path"],"research/affective/MSC-AFFECT-P05/plan.md")
        self.assertEqual(info["status"],"PLANNED")
        self.assertIn("Motion-Confound-Controlled Hand-Kinematic",plan)
        self.assertNotIn("../../docs/",plan)
        self.assertIn(info["source_commit_sha"],plan)
        self.assertIn("MSC-AFFECT-P05",(folder/"README.md").read_text(encoding="utf-8"))
    def test_legacy_papers_are_not_changed(self):
        old=ROOT/"papers/affect"
        self.assertEqual(len([x for x in old.iterdir() if x.is_dir()]),4)
        self.assertNotIn("MSC-AFFECT-P05",(old/"README.md").read_text(encoding="utf-8"))
if __name__=="__main__":
    unittest.main()
