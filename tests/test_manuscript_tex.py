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
        catalog = json.loads((ROOT / "manuscripts/catalog.json").read_text(encoding="utf-8"))
        by_id = {record["id"]: record for record in catalog["papers"]}
        self.assertEqual(len(HISTORICAL_IDS), 63)
        self.assertEqual(set(by_id), LEGACY_IDS | NEW_IDEAS)
        total = 0
        for area, expected in AREAS.items():
            files = sorted((ROOT / "manuscripts" / ident / "main.tex" for ident, record in by_id.items() if record["area"] == area))
            self.assertEqual(len(files), expected, area)
            for path in files:
                with self.subTest(filename=str(path)):
                    self.assertFalse(path.is_symlink())
                    content = path.read_text(encoding="utf-8")
                    if path.parent.name in {"MSC-ADHD-P01", "MSC-ADHD-P02", "MSC-ADHD-P03", "MSC-ADHD-P05", "MSC-ADHD-R01", "MSC-ADHD-R02", "MSC-ADHD-S02"}:
                        ident = path.parent.name
                        self.assertIn(ident, by_id)
                        self.assertIn(r"\documentclass[man]{apa7}", content)
                        self.assertIn(r"\authorsnames{Mateusz Pomianek}", content)
                        self.assertIn(r"\addbibresource{references.bib}", content)
                        self.assertTrue((path.parent / "references.bib").is_file())
                        sections = re.findall(r"\\input\{(sections/[^}]+)\}", content)
                        self.assertGreaterEqual(len(sections), 6)
                        self.assertEqual(len(sections), len(set(sections)))
                        self.assertEqual(set(sections), {"sections/" + p.stem for p in (path.parent / "sections").glob("*.tex")})
                        expanded = content + "".join((path.parent / (s + ".tex")).read_text(encoding="utf-8") for s in sections)
                        self.assertGreater(len(expanded), 2200)
                        self.assertIn(r"\abstract{", expanded)
                        self.assertIn(r"\printbibliography", content)
                        self.assertEqual(content.count(r"\begin{document}"), 1)
                        self.assertEqual(content.count(r"\end{document}"), 1)
                        self.assertNotIn("MatPomGit/", content)
                        matched = re.search(r"\\title\{([^{}]+)\}", content)
                        self.assertIsNotNone(matched)
                        self.assertNotIn(matched.group(1), titles)
                        titles.add(matched.group(1))
                        total += 1
                        continue
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
                    if ident == "MSC-AAL-P02":
                        self.assertEqual(by_id[ident]["record_kind"], "IDEA")
                        self.assertEqual(by_id[ident]["stage"], "SOURCE_PLANNED_ARTICLE")
                        self.assertRegex(content, r"\\date\{Szkic naukowy, wersja 0\.\d+\.\d+\}")
                        for heading in ("Wprowadzenie", "Materiał i metody",
                                        "Plan analizy", "Dyskusja i ograniczenia"):
                            self.assertIn(r"\section{" + heading + "}", content)
                        endpoint = re.search(
                            r"\\subsection\{Pierwszorzędowy punkt końcowy i estymand\}"
                            r"\s*(.+?)(?=\\(?:sub)?section\{)",
                            content, re.DOTALL)
                        self.assertIsNotNone(endpoint)
                        self.assertGreater(len(endpoint.group(1).strip()), 200)
                        self.assertRegex(endpoint.group(1), r"(?i)estymand")
                        self.assertRegex(endpoint.group(1), r"(?i)nie zostały jeszcze zatwierdzone")
                        self.assertRegex(content, r"(?i)plan należy zamrozić przed dostępem do danych")
                        results = re.search(r"\\section\{Wyniki\}\s*(.+?)(?=\\section\{)",
                                            content, re.DOTALL)
                        self.assertIsNotNone(results)
                        self.assertIn(r"IDEA / SOURCE\_PLANNED\_ARTICLE", results.group(1))
                        self.assertIn("nie udokumentowano zebranych obserwacji", results.group(1))
                    elif ident in LEGACY_IDS:
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
                        elif ident == "MSC-CR-P07":
                            self.assertRegex(content, r"\\date\{Szkic naukowy, wersja 0\.[2-9]\d*\.\d+\}")
                            self.assertEqual(by_id[ident]["stage"], "PROSPECTIVE")
                            for required in ("marginalna różnica ryzyka", "efektami losowymi uczestnika i zadania",
                                             "H1 jest jedynym testem potwierdzającym",
                                             "akwizycja danych nie została rozpoczęta"):
                                self.assertIn(required, content)
                        elif ident == "MSC-DERA-P01":
                            self.assertEqual(by_id[ident]["stage"], "CANDIDATE_VALIDATION_DATA_REQUIRED")
                            self.assertRegex(content, r"\\date\{MSC-DERA-P01 \| Protokół prospektywny 1\.\d+\.\d+")
                            self.assertIn(r"\bibliography{references}", content)
                            self.assertIn("Nie przeprowadzono rekrutacji ani pomiarów", content)
                        elif ident == "MSC-CR-P12":
                            self.assertEqual(by_id[ident]["stage"], "IDEA_REVIEW")
                            self.assertRegex(content, r"\\date\{MSC-CR-P12 \| Protokół prospektywny 1\.\d+\.\d+")
                            self.assertIn(r"\bibliography{references}", content)
                            self.assertIn("Nie przeprowadzono rekrutacji ani pomiarów", content)
                        elif ident == "MSC-EEG-P01":
                            self.assertEqual(by_id[ident]["stage"], "PROPOSED")
                            self.assertIn("Manuskrypt metod 1.0.0", content)
                            self.assertIn(r"\bibliography{references}", content)
                        elif ident == "MSC-EEG-P02":
                            self.assertEqual(by_id[ident]["stage"], "PROPOSED")
                            self.assertIn("Protokół techniczny 1.0.0", content)
                            self.assertIn(r"\bibliography{references}", content)
                        elif ident == "MSC-EYE-P01":
                            self.assertEqual(by_id[ident]["stage"], "PLANNED")
                            self.assertIn("Protokół prospektywny 1.0.0", content)
                            self.assertIn(r"\bibliography{references}", content)
                        elif ident == "MSC-PAIN-P07":
                            self.assertEqual(by_id[ident]["stage"], "PROSPECTIVE")
                            self.assertRegex(content, r"\\date\{MSC-PAIN-P07 \\enspace PROSPECTIVE \\enspace wersja 1\.\d+\.\d+")
                            for required in (r"\subsection{Symulacja liczebności próby}",
                                             r"\input{power-summary.tex}",
                                             "Nie przeprowadzono rekrutacji ani pomiarów"):
                                self.assertIn(required, content)
                        elif ident in {"MSC-AAL-P08", "MSC-AAL-P06", "MSC-ADHD-P06", "MSC-ADHD-P07", "MSC-ADHD-P08", "MSC-ADHD-P10"}:
                            self.assertRegex(content, r"\\date\{Szkic naukowy, wersja 0\.\d+\.\d+\}")
                            self.assertIn("Nie", content)
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
