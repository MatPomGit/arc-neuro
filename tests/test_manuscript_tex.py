"""Weryfikacja 63 indywidualnych źródeł manuskryptów LaTeX."""
from pathlib import Path
import re
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
AREAS = {"ndd":16,"affect":4,"cognition":13,"social":22,"psychometrics":8}

class ManuscriptTexTests(unittest.TestCase):
    def test_complete_manuscript_sources(self):
        titles = set()
        catalog = json.loads((ROOT/"papers/catalog.json").read_text(encoding="utf-8"))
        by_id = {record["id"]: record for record in catalog["papers"]}
        total = 0
        for area, expected in AREAS.items():
            files = sorted((ROOT/"papers"/area).glob("MSC-*/main.tex"))
            self.assertEqual(len(files), expected, area)
            for path in files:
                with self.subTest(filename=str(path)):
                    self.assertFalse(path.is_symlink())
                    content = path.read_text(encoding="utf-8")
                    self.assertGreater(len(content), 2200)
                    self.assertIn("Pierwszorzędowy wskaźnik:", content)
                    self.assertIn("Zamrożenie estymandu", content)
                    self.assertIn("Szkic naukowy, wersja 0.1.1", content)
                    for keyword in ("\\documentclass", "\\begin{document}", "\\begin{abstract}",
                                    "\\section{Wprowadzenie}", "\\section{Materiał i metody}",
                                    "\\section{Wyniki}", "\\section{Dyskusja i ograniczenia}",
                                    "\\end{document}"):
                        self.assertIn(keyword, content)
                    matched = re.search(r"\\title\{([^{}]+)\}", content)
                    self.assertIsNotNone(matched)
                    self.assertIn(path.parent.name,by_id)
                    self.assertEqual(matched.group(1).replace("--","–"),by_id[path.parent.name]["title"])
                    self.assertNotIn(matched.group(1), titles)
                    titles.add(matched.group(1))
                    self.assertEqual(content.count(r"\begin{document}"), 1)
                    self.assertEqual(content.count(r"\end{document}"), 1)
                    self.assertNotIn("MatPomGit/", content)
                    total += 1
        self.assertEqual(total, 63)

if __name__ == "__main__":
    unittest.main()
