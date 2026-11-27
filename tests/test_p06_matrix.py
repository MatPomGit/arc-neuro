"""Matrix execution and reporting smoke test; not a power study."""
import csv
import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"manuscripts/MSC-CR-P06/materials"))
import simulation_matrix as m
sys.path.pop(0)


class P06MatrixTests(unittest.TestCase):
    def test_profiles(self):
        self.assertEqual(len(m.scenarios("full")),24)
        self.assertEqual(len(m.scenarios("screen")),12)
        self.assertEqual(len(m.scenarios("smoke")),6)
        self.assertEqual(len({sid for sid,_ in m.scenarios("full")}),24)
        with self.assertRaises(ValueError):
            m.run_matrix("smoke",selected="INVALID")
        with self.assertRaises(ValueError):
            m.run_matrix("full")

    def test_matched_seeds(self):
        groups={}
        for sid, settings in m.scenarios("full"):
            key=sid.split("-",1)[1]
            self.assertEqual(settings["seed"],groups.setdefault(key,settings["seed"]))
        self.assertEqual(len(set(groups.values())),len(groups))

    def test_smoke_matrix_and_reports(self):
        result=m.run_matrix("smoke")
        self.assertEqual(len(result["scenarios"]),6)
        self.assertEqual(result["interpretation"],"TECHNICAL_SMOKE_ONLY")
        oracle={}
        for s in result["scenarios"]:
            key=s["scenario"].split("-",1)[1]
            self.assertEqual(s["methods"]["full"],oracle.setdefault(key,s["methods"]["full"]))
            for fit in s["methods"].values():
                self.assertEqual(fit["successful"]+fit["failed"],4)
            self.assertEqual(s["methods"]["full"]["successful"],4)
            self.assertGreater(s["methods"]["pmm"]["successful"],0)
        with tempfile.TemporaryDirectory() as d:
            m.write_results(result,d)
            self.assertEqual(json.loads((Path(d)/"matrix.json").read_text()),result)
            with (Path(d)/"matrix.csv").open(newline="",encoding="utf-8") as f:
                rows=list(csv.DictReader(f))
            self.assertEqual(len(rows),42)
            ET.parse(Path(d)/"matrix.svg")
        # Compact actual-run evidence in CI logs, not empirical results.
        print("P06_MATRIX_SMOKE_JSON="+json.dumps([
            {"scenario":s["scenario"],"missing_fraction":s["realized_missing_fraction"],
             "methods":{k:{v:r[v] for v in ("successful","failed","bias","rmse","coverage","rejection_rate")}
                        for k,r in s["methods"].items()}}
            for s in result["scenarios"]],separators=(",",":"),allow_nan=False),flush=True)


if __name__=="__main__":
    unittest.main()
