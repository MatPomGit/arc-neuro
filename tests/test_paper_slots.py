"""Testy struktury katalogów artykułów ARC Neuro."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
AREAS = {"ndd": 16, "affect": 4, "cognition": 13,
         "social": 22, "psychometrics": 8}

class PaperSlotStructureTests(unittest.TestCase):
    def test_slots(self):
        root = ROOT / "papers"
        self.assertTrue((root / "README.md").is_file())
        self.assertEqual({p.name for p in root.iterdir() if p.is_dir()}, set(AREAS))
        all_slots = []
        for area, expected in AREAS.items():
            folder = root / area
            self.assertTrue((folder / "README.md").is_file())
            slots = [p for p in folder.iterdir() if p.is_dir()]
            self.assertEqual(len(slots), expected, area)
            for p in slots:
                self.assertRegex(p.name, r"^slot-\d{3}$")
                self.assertEqual({x.name for x in p.iterdir()}, {"README.md"})
                all_slots.append(p.name)
        self.assertEqual(len(all_slots), 63)
        self.assertEqual(len(set(all_slots)), 63)

    def test_public_documents_do_not_expose_internal_mapping(self):
        # Public README may cite a separately approved proposal (e.g. P08).
        # Only neutral placeholder files are prohibited from naming MSC IDs.
        docs = [ROOT / "README.md", *(ROOT / "papers").rglob("README.md")]
        internal = re.compile(
            r"research[-_ ]autopilot|neuro_paper_slots|MatPomGit/devices",
            flags=re.IGNORECASE
        )
        msc_id = re.compile(r"MSC-[A-Z0-9]+-[PRS]\d+")
        for p in docs:
            with self.subTest(file=str(p)):
                self.assertFalse(p.is_symlink())
                text = p.read_text(encoding="utf-8")
                self.assertIsNone(internal.search(text))
                if p.is_relative_to(ROOT / "papers"):
                    self.assertIsNone(msc_id.search(text))

if __name__ == "__main__":
    unittest.main()
