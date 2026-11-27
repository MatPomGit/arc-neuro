"""Contract for real manuscript directories and visible MSC titles."""
from pathlib import Path
import json
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]
AREAS={line["id"] for line in json.loads((ROOT/"config/research-lines.json").read_text(encoding="utf-8"))["lines"]}
NEW_IDEAS={"MSC-ANX-P01","MSC-FAT-P01","MSC-INTERO-P01"}
CATALOG=json.loads((ROOT/"manuscripts/catalog.json").read_text(encoding="utf-8"))
class ManuscriptDirectoryTests(unittest.TestCase):
    def test_real_msc_paths_and_titles(self):
        records=CATALOG["papers"]
        self.assertTrue(records)
        self.assertEqual({p.name for p in (ROOT/"manuscripts").glob("MSC-*") if p.is_dir()}, {p["id"] for p in records})
        self.assertEqual(len({p["id"] for p in records}),len(records))
        self.assertEqual({p["id"] for p in records if p["id"] in NEW_IDEAS and p["stage"]=="IDEA_REVIEW" and p["record_kind"]=="IDEA"},NEW_IDEAS)
        self.assertTrue({p["area"] for p in records} <= AREAS)
        for area in AREAS:
            root=ROOT/"manuscripts"
            paths={p.name for p in root.glob("MSC-*") if p.is_dir() and p.name in {r["id"] for r in records if r["area"]==area}}
            mapped={p["id"] for p in records if p["area"]==area}
            self.assertEqual(paths,mapped)
        for p in records:
            with self.subTest(id=p["id"]):
                self.assertRegex(p["id"],r"^MSC-[A-Z0-9]+-[PRS][0-9]{2,}$")
                folder=ROOT/"manuscripts"/p["id"]
                self.assertEqual(p["readme_path"],(folder/"README.md").relative_to(ROOT).as_posix())
                self.assertEqual(p["manuscript_path"],(folder/"main.tex").relative_to(ROOT).as_posix())
                self.assertTrue((folder/"main.tex").is_file())
                readme=(folder/"README.md").read_text(encoding="utf-8")
                self.assertIn(p["id"],readme)
                self.assertIn(p["title"],readme)
                self.assertIn(p["stage"],readme)
                self.assertFalse(folder.is_symlink())
                self.assertFalse((folder/"main.tex").is_symlink())
    def test_confirmed_authorship_in_every_catalog_manuscript(self):
        """All catalogue drafts: README metadata and LaTeX authorship agree."""
        records = CATALOG["papers"]
        self.assertTrue(records)
        for paper in records:
            with self.subTest(manuscript_id=paper["id"]):
                readme = (ROOT / paper["readme_path"]).read_text(encoding="utf-8")
                tex = (ROOT / paper["manuscript_path"]).read_text(encoding="utf-8")
                self.assertRegex(
                    readme,
                    r"(?m)^\*\*Właściciel naukowy i autor szkicu:\*\* Mateusz Pomianek\b",
                )
                author_fields = re.findall(r"\\(?:author|authorsnames)(?:\[[^\]]*\])?\{([^}]*)\}", tex)
                self.assertEqual(len(author_fields), 1, "Expected one LaTeX author declaration")
                self.assertIn("Mateusz Pomianek", author_fields[0])

    def test_names_not_obscured_and_pages_separate(self):
        self.assertFalse(list((ROOT/"manuscripts").glob("slot-*")))
        self.assertEqual({p.parent.name for p in (ROOT/"manuscripts").glob("MSC-*/main.tex")},
                         {p["id"] for p in CATALOG["papers"]})
        self.assertTrue((ROOT/"site/projects.md").exists())
    def test_no_private_sources_in_public_catalog(self):
        data=(ROOT/"manuscripts/catalog.json").read_text(encoding="utf-8")
        self.assertNotIn("source_repo",data)
        self.assertNotIn("research-autopilot",data)
        self.assertNotIn("MatPomGit/devices",data)
if __name__=="__main__":
    unittest.main()
