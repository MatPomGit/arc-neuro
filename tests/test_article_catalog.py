"""Consistent named articles in curated Pages and the repository catalog."""
from pathlib import Path
import json
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]
CATALOG=json.loads((ROOT/"manuscripts/catalog.json").read_text(encoding="utf-8"))
AREAS={"ndd":16,"affect":4,"cognition":13,"social":22,"psychometrics":8}
HISTORICAL_IDS={line.strip() for line in (ROOT/"config/historical-manuscripts-63.txt").read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")}
NEW_IDEAS={"MSC-ANX-P01","MSC-FAT-P01","MSC-INTERO-P01"}
class ArticleCatalogTests(unittest.TestCase):
    def test_all_63_article_headings_match_canonical_catalog(self):
        self.assertEqual(len(HISTORICAL_IDS),63)
        self.assertTrue(HISTORICAL_IDS <= {p["id"] for p in CATALOG["papers"]})
        seen=set()
        for area,expected in AREAS.items():
            page=(ROOT/"site"/(area+".md")).read_text(encoding="utf-8")
            titles=re.findall(r"^### (MSC-[A-Z0-9]+-[PRS][0-9]+) — (.+)$",page,flags=re.MULTILINE)
            self.assertEqual(len(titles),expected,area)
            listed=[(p["id"],p["title"]) for p in CATALOG["papers"] if p["area"]==area and p["id"] in HISTORICAL_IDS]
            self.assertEqual(titles,listed)
            for ident,_ in titles:
                self.assertNotIn(ident,seen)
                seen.add(ident)
            chunks=re.split(r"^### .+$",page,flags=re.MULTILINE)[1:]
            self.assertTrue(all(len(x.strip())>=55 for x in chunks))
            self.assertNotRegex(page,r"slot-[0-9]+")
        self.assertEqual(seen,HISTORICAL_IDS)
        self.assertTrue(NEW_IDEAS <= {p["id"] for p in CATALOG["papers"]})
        for area in AREAS:
            page=(ROOT/"site"/(area+".md")).read_text(encoding="utf-8")
            self.assertTrue(all(f"### {ident} —" not in page for ident in NEW_IDEAS))
    def test_main_index_and_papers_index(self):
        page=(ROOT/"site/articles.md").read_text(encoding="utf-8")
        self.assertIn("63",page)
        for area in AREAS:
            self.assertIn("]("+area+".md)",page)
        idx=(ROOT/"manuscripts/README.md").read_text(encoding="utf-8")
        for p in CATALOG["papers"]:
            self.assertIn(f"({p['id']}/README.md)",idx)
if __name__=="__main__":
    unittest.main()
