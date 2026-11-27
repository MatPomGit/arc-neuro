"""Regression contract for scientific ownership of all catalogued author drafts."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "manuscripts/catalog.json"
OWNER_FIELD = re.compile(
    r"(?im)^(?:\*\*Właściciel naukowy(?: i autor szkicu)?:\*\*|scientific_owner:)"
    r"[ \t]*(?P<value>[^\r\n]+)"
)
EXPECTED_NAME = re.compile(r"^Mateusz Pomianek(?=$|[ \t]*[.(])")


def owner_fields(readme):
    """Extract explicit scientific-owner fields, never author/canonical-repo fields."""
    return [match.group("value").strip() for match in OWNER_FIELD.finditer(readme)]


def inventory():
    records = json.loads(CATALOG.read_text(encoding="utf-8"))["papers"]
    if not isinstance(records, list) or not records:
        raise AssertionError("Missing or empty manuscript catalog")
    ids = [p["id"] for p in records]
    if len(ids) != len(set(ids)):
        raise AssertionError("Duplicate manuscript ids")
    findings = {}
    for p in records:
        path = ROOT / "manuscripts" / p["id"] / "README.md"
        if path.relative_to(ROOT).as_posix() != p["readme_path"]:
            raise AssertionError(f"Invalid README path in catalog: {p['id']}")
        if not path.is_file() or path.is_symlink():
            raise AssertionError(f"Missing or symlinked README: {p['id']}")
        findings[p["id"]] = owner_fields(path.read_text(encoding="utf-8"))
    return findings


class ScientificOwnerRegression(unittest.TestCase):
    def test_owner_declaration_parser(self):
        self.assertEqual(owner_fields("**Właściciel naukowy:** Mateusz Pomianek (`MatPomGit`)."),
                         ["Mateusz Pomianek (`MatPomGit`)."])
        self.assertEqual(owner_fields("scientific_owner: Mateusz Pomianek"), ["Mateusz Pomianek"])
        self.assertEqual(owner_fields("**Właściciel naukowy i autor szkicu:** Mateusz Pomianek"),
                         ["Mateusz Pomianek"])
        self.assertEqual(owner_fields("Autor: Mateusz Pomianek"), [])
        self.assertEqual(owner_fields("Praca pozostaje w kanonicznym repozytorium"), [])
        self.assertFalse(EXPECTED_NAME.match("Inna osoba"))

    def test_owner_metadata_examples_reject_wrong_people(self):
        self.assertFalse(EXPECTED_NAME.match("Inna osoba"))
        self.assertFalse(EXPECTED_NAME.match("Mateusz Pomianek-Kowalski"))

    def test_complete_catalog_inventory(self):
        """Every currently catalogued manuscript has one unambiguous owner."""
        found = inventory()
        self.assertTrue(found)
        for manuscript_id, fields in found.items():
            with self.subTest(manuscript_id=manuscript_id):
                self.assertEqual(len(fields), 1, "Expected exactly one scientific owner")
                self.assertRegex(fields[0], EXPECTED_NAME)

    def test_confirmed_owner_across_all_manuscripts(self):
        """Owner's explicit authorship confirmation applies to all catalogue IDs."""
        found = inventory()
        self.assertTrue(found)
        offenders = {paper_id: fields for paper_id, fields in found.items()
                     if len(fields) != 1 or not EXPECTED_NAME.match(fields[0])}
        self.assertFalse(offenders, f"OWNER_METADATA_MISSING_OR_INVALID: {offenders}")


if __name__ == "__main__":
    unittest.main()
