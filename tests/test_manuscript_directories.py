"""Contract for real manuscript directories and visible MSC titles."""
from pathlib import Path
import json
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]
AREAS={"ndd":16,"affect":5,"cognition":15,"social":25,"psychometrics":8}
NEW_IDEAS={"MSC-ANX-P01","MSC-FAT-P01","MSC-INTERO-P01"}
CATALOG=json.loads((ROOT/"papers/catalog.json").read_text(encoding="utf-8"))
class ManuscriptDirectoryTests(unittest.TestCase):
    def test_real_msc_paths_and_titles(self):
        records=CATALOG["papers"]
        self.assertEqual(len(records),69)
        self.assertEqual(len({p["id"] for p in records}),69)
        self.assertEqual({p["id"] for p in records if p["id"] in NEW_IDEAS and p["stage"]=="IDEA_REVIEW" and p["record_kind"]=="IDEA"},NEW_IDEAS)
        self.assertEqual(set(AREAS),{p["area"] for p in records})
        for area,expected in AREAS.items():
            root=ROOT/"papers"/area
            paths={p.name for p in root.iterdir() if p.is_dir()}
            mapped={p["id"] for p in records if p["area"]==area}
            self.assertEqual(len(paths),expected)
            self.assertEqual(paths,mapped)
        for p in records:
            with self.subTest(id=p["id"]):
                self.assertRegex(p["id"],r"^MSC-[A-Z0-9]+-[PRS][0-9]{2,}$")
                folder=ROOT/"papers"/p["area"]/p["id"]
                self.assertEqual(p["readme_path"],(folder/"README.md").relative_to(ROOT).as_posix())
                self.assertEqual(p["manuscript_path"],(folder/"main.tex").relative_to(ROOT).as_posix())
                self.assertTrue((folder/"main.tex").is_file())
                readme=(folder/"README.md").read_text(encoding="utf-8")
                self.assertIn(p["id"],readme)
                self.assertIn(p["title"],readme)
                self.assertIn(p["stage"],readme)
                self.assertFalse(folder.is_symlink())
                self.assertFalse((folder/"main.tex").is_symlink())
    def test_names_not_obscured_and_pages_separate(self):
        self.assertFalse(list((ROOT/"papers").glob("*/slot-*")))
        self.assertEqual(len(list((ROOT/"papers").glob("*/MSC-*/main.tex"))),69)
        self.assertTrue((ROOT/"pages/projects.md").exists())
    def test_no_private_sources_in_public_catalog(self):
        data=(ROOT/"papers/catalog.json").read_text(encoding="utf-8")
        self.assertNotIn("source_repo",data)
        self.assertNotIn("research-autopilot",data)
        self.assertNotIn("MatPomGit/devices",data)
if __name__=="__main__":
    unittest.main()
