import unittest
from pathlib import Path

class PythonOnlyTests(unittest.TestCase):
    def test_no_r_sources(self):
        root=Path(__file__).resolve().parents[1]
        forbidden={".r",".rmd",".rproj",".rnw"}
        files=[str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and not any(part in {".git",".venv","venv","build","node_modules"} for part in p.relative_to(root).parts) and (p.suffix.lower() in forbidden or p.name.lower() in {"renv.lock",".rprofile",".renviron"})]
        self.assertEqual(files,[])
