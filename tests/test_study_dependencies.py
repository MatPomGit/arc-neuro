import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from import_study_dependencies import proposed_tools


class StudyDependencyTests(unittest.TestCase):
    def test_only_explicit_proposed_entries(self):
        text = """## Aplikacje
- **`app-test`** (`APP-01`): rola `PRIMARY`, decyzja `MVP`; status repozytorium `PLANNED_NOT_CREATED`.
## Biblioteki
- **`lib-test`**: status `SCAFFOLD_EXISTS`, proponowana zależność.
## Proweniencja
- **`lib-ignore`**: status `ACTIVE`.
"""
        rows = proposed_tools(text, "manuscripts/MSC-X-P01/study.md")
        self.assertEqual([r["ref"] for r in rows], ["app-test", "lib-test"])
        self.assertTrue(all(r["validation_status"] == "NOT_VERIFIED" for r in rows))
        self.assertIn("SCAFFOLD_EXISTS", rows[1]["notes"])
