"""Stage-05 evidence: audit all catalog README files without assigning authorship."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "papers/catalog.json"
# Confirmed by issue #27. Add identifiers only after an ownership determination.
CONFIRMED_OWNED = frozenset({"MSC-NDD-P01"})
OWNER_FIELD = re.compile(
    r"(?im)^(?:\*\*Właściciel naukowy(?: i autor szkicu)?:\*\*|scientific_owner:)"
    r"[ \t]*(?P<value>[^\r\n]+)"
)
EXPECTED_NAME = re.compile(r"^Mateusz Pomianek(?:\b|$)")


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
        path = ROOT / "papers" / p["area"] / p["id"] / "README.md"
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

    def test_complete_catalog_inventory(self):
        """Every indexed README is inspected, but unknown ownership is not invented."""
        found = inventory()
        self.assertTrue(CONFIRMED_OWNED.issubset(found), "Confirmed ID missing in catalog")
        for manuscript_id, fields in found.items():
            with self.subTest(manuscript_id=manuscript_id):
                self.assertLessEqual(len(fields), 1, "Ambiguous duplicate owner declarations")
                self.assertTrue(all(field.strip() for field in fields), "Empty owner declaration")

    def test_confirmed_owner_is_explicit_before_fix(self):
        """Intentional RED until the confirmed owner defect is repaired in a later stage."""
        found = inventory()
        offenders = {paper_id: found[paper_id] for paper_id in sorted(CONFIRMED_OWNED)
                     if len(found[paper_id]) != 1 or not EXPECTED_NAME.match(found[paper_id][0])}
        missing = sorted(paper_id for paper_id, fields in found.items() if not fields)
        self.assertFalse(offenders, f"OWNER_METADATA_MISSING_OR_INVALID: {offenders}; "
                          f"inventory_missing={len(missing)}/{len(found)}; missing_ids={missing}")


if __name__ == "__main__":
    unittest.main()
