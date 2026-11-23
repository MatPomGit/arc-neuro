"""Regression for confirmed scientific ownership metadata, not authorship."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
OWNER_DECLARATION = re.compile(
    r"(?im)^(?:\*\*Właściciel naukowy(?: i autor szkicu)?:\**\*|scientific_owner:)\s*Mateusz Pomianek\b"
)


class ScientificOwnerRegression(unittest.TestCase):
    def test_owner_declaration_parser(self):
        self.assertRegex("**Właściciel naukowy:** Mateusz Pomianek", OWNER_DECLARATION)
        self.assertRegex("scientific_owner: Mateusz Pomianek", OWNER_DECLARATION)
        self.assertNotRegex("Autor: Mateusz Pomianek", OWNER_DECLARATION)
        self.assertNotRegex("Praca pozostaje w kanonicznym repozytorium", OWNER_DECLARATION)

    def test_confirmed_ndd_p01_owner_metadata(self):
        path = ROOT / "papers/ndd/MSC-NDD-P01/README.md"
        self.assertRegex(path.read_text(encoding="utf-8"), OWNER_DECLARATION)


if __name__ == "__main__":
    unittest.main()
