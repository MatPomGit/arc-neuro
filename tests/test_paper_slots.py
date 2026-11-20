"""Strukturalna kontrola neutralnych katalogów artykułów ARC Neuro."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AREAS = {
    "ndd": 16,
    "affect": 4,
    "cognition": 13,
    "social": 22,
    "psychometrics": 8,
}

class PaperSlotStructureTests(unittest.TestCase):
    def test_slot_counts_and_unique_filenames(self):
        root = ROOT / "papers"
        self.assertTrue((root / "README.md").is_file())
        all_names = []
        for area, expected in AREAS.items():
            area_dir = root / area
            self.assertTrue((area_dir / "README.md").is_file())
            slots = sorted(p for p in area_dir.iterdir() if p.is_dir())
            self.assertEqual(len(slots), expected, area)
            for directory in slots:
                self.assertRegex(directory.name, r"^slot-[0-9]{3}$")
                self.assertTrue((directory / "README.md").is_file())
                all_names.append(directory.name)
        self.assertEqual(len(all_names), 63)
        self.assertEqual(len(set(all_names)), 63)

    def test_public_slots_contain_no_private_manuscript_ids(self):
        root = ROOT / "papers"
        for path in root.rglob("README.md"):
            if path.parent.name.startswith("slot-"):
                text = path.read_text(encoding="utf-8")
                self.assertNotRegex(text, r"MSC-[A-Z]+-[PRS][0-9]+")
                self.assertNotIn("MatPomGit/arc-", text)

if __name__ == "__main__":
    unittest.main()
