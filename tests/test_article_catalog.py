"""Consistent named articles in curated Pages and the repository catalog."""
from pathlib import Path
import json
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]
CATALOG=json.loads((ROOT/"papers/catalog.json").read_text(encoding="utf-8"))
AREAS={"ndd":16,"affect":4,"cognition":13,"social":22,"psychometrics":8}
class ArticleCatalogTests(unittest.TestCase):
    def test_all_63_article_headings_match_canonical_catalog(self):
        seen=set()
        for area,expected in AREAS.items():
            page=(ROOT/"pages"/(area+".md")).read_text(encoding="utf-8")
            titles=re.findall(r"^### (MSC-[A-Z0-9]+-[PRS][0-9]+) — (.+)$",page,flags=re.MULTILINE)
            self.assertEqual(len(titles),expected,area)
            listed=[(p["id"],p["title"]) for p in CATALOG["papers"] if p["area"]==area and not p["id"].startswith("MSC-SUV-")]
            self.assertEqual(titles,listed)
            for ident,_ in titles:
                self.assertNotIn(ident,seen)
                seen.add(ident)
            chunks=re.split(r"^### .+$",page,flags=re.MULTILINE)[1:]
            self.assertTrue(all(len(x.strip())>=55 for x in chunks))
            self.assertNotRegex(page,r"slot-[0-9]+")
        self.assertEqual(len(seen),63)
    def test_main_index_and_papers_index(self):
        page=(ROOT/"pages/articles.md").read_text(encoding="utf-8")
        self.assertIn("63",page)
        for area in AREAS:
            self.assertIn("]("+area+".md)",page)
        idx=(ROOT/"papers/README.md").read_text(encoding="utf-8")
        for p in CATALOG["papers"]:
            self.assertIn(f"({p['area']}/{p['id']}/README.md)",idx)
if __name__=="__main__":
    unittest.main()
