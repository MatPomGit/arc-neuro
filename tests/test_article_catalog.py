"""Integralność publicznego katalogu prac badawczych."""
from pathlib import Path
import re
import unittest
ROOT = Path(__file__).resolve().parents[1]
AREAS = {"ndd":16, "affect":4, "cognition":13, "social":22, "psychometrics":8}
class ArticleCatalogTests(unittest.TestCase):
    def test_all_articles_have_unique_titles_and_descriptions(self):
        titles = set()
        for area, n in AREAS.items():
            page = (ROOT / "pages" / (area + ".md")).read_text(encoding="utf-8")
            names = re.findall(r"^### (.+)$", page, re.MULTILINE)
            self.assertEqual(len(names), n, area)
            for title in names:
                self.assertNotIn(title, titles)
                titles.add(title)
            chunks = re.split(r"^### .+$", page, flags=re.MULTILINE)[1:]
            self.assertTrue(all(len(x.strip()) >= 55 for x in chunks))
            self.assertNotRegex(page, r"MSC-[A-Z0-9]+-[PRS]\d+|slot-\d+")
        self.assertEqual(len(titles), 63)
    def test_index_links_to_every_area(self):
        page = (ROOT / "pages/articles.md").read_text(encoding="utf-8")
        self.assertIn("63", page)
        for area in AREAS:
            self.assertIn("](" + area + ".md)", page)
if __name__ == "__main__":
    unittest.main()
