"""Contracts for original LaTeX manuscripts and new prospective research plans."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
AREAS = {"ndd": 16, "affect": 5, "cognition": 15, "social": 25, "psychometrics": 8}
HISTORICAL_IDS = {
    line.strip() for line in
    (ROOT / "config/historical-manuscripts-63.txt").read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.startswith("#")
}
LEGACY_IDS = HISTORICAL_IDS | {"MSC-ZAH-P02", "MSC-ZAH-P03", "MSC-ZAH-P04"}
NEW_IDEAS = {"MSC-ANX-P01", "MSC-FAT-P01", "MSC-INTERO-P01"}


class ManuscriptTexTests(unittest.TestCase):
    def test_complete_manuscript_sources(self):
        titles = set()
        catalog = json.loads((ROOT / "papers/catalog.json").read_text(encoding="utf-8"))
        by_id = {record["id"]: record for record in catalog["papers"]}
        self.assertEqual(len(HISTORICAL_IDS), 63)
        self.assertEqual(set(by_id), LEGACY_IDS | NEW_IDEAS)
        total = 0
        for area, expected in AREAS.items():
            files = sorted((ROOT / "papers" / area).glob("MSC-*/main.tex"))
            self.assertEqual(len(files), expected, area)
            for path in files:
                with self.subTest(filename=str(path)):
                    self.assertFalse(path.is_symlink())
                    content = path.read_text(encoding="utf-8")
                    self.assertGreater(len(content), 2200)
                    for keyword in (r"\documentclass", r"\begin{document}",
                                    r"\begin{abstract}", r"\section{Wyniki}",
                                    r"\end{document}"):
                        self.assertIn(keyword, content)
                    matched = re.search(r"\\title\{([^{}]+)\}", content)
                    self.assertIsNotNone(matched)
                    ident = path.parent.name
                    self.assertIn(ident, by_id)
                    self.assertEqual(matched.group(1).replace("--", "–"), by_id[ident]["title"])
                    self.assertNotIn(matched.group(1), titles)
                    titles.add(matched.group(1))
                    self.assertEqual(content.count(r"\begin{document}"), 1)
                    self.assertEqual(content.count(r"\end{document}"), 1)
                    self.assertNotIn("MatPomGit/", content)
                    if ident in LEGACY_IDS:
                        for required in ("Pierwszorzędowy wskaźnik:",
                                         "Zamrożenie estymandu",
                                         r"\section{Wprowadzenie}",
                                         r"\section{Materiał i metody}",
                                         r"\section{Dyskusja i ograniczenia}"):
                            self.assertIn(required, content)
                        if ident == "MSC-CR-P06":
                            self.assertRegex(content, r"\\date\{Projekt badania, wersja 0\.[1-9]\d*\.\d+,")
                            self.assertEqual(by_id[ident]["stage"], "PROSPECTIVE")
                            self.assertIn("Nie rozpoczęto akwizycji danych", content)
                        else:
                            self.assertIn("Szkic naukowy, wersja 0.1.1", content)
                    else:
                        self.assertIn(ident, NEW_IDEAS)
                        self.assertEqual(by_id[ident]["record_kind"], "IDEA")
                        self.assertEqual(by_id[ident]["stage"], "IDEA_REVIEW")
                        self.assertIn(r"\textbf{Status:}", content)
                        self.assertIn("nie przeprowadzono badania", content)
                        self.assertIn(r"\section{Warunki przejścia do badania}", content)
                        self.assertGreaterEqual(len(re.findall(r"\\section\{", content)), 6)
                        self.assertRegex(content, r"(?i)etycz")
                        self.assertTrue(
                            r"\section{Plan analizy statystycznej}" in content or
                            r"\section{Główny estymand i modele statystyczne}" in content
                        )
                    total += 1
        self.assertEqual(total, 69)


if __name__ == "__main__":
    unittest.main()
