"""Check aggregate reports and source labelling on synthetic data."""
import csv
import hashlib
import json
import importlib.util
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

path=Path(__file__).resolve().parents[1]/"papers/cognition/MSC-CR-P06/materials/reporting.py"
spec=importlib.util.spec_from_file_location("p06_reporting",path)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class P06ReportingTests(unittest.TestCase):
    def test_aggregate_outputs(self):
        results={h:dict(hypothesis=h,unit="percentage_points" if h in ("H1","H2") else "raw_score",
                        estimate=.1,se=.05,ci=[-.01,.21],p=.05,p_adjusted=.15,n_randomized=100,n_used=98,
                        reference="synthetic") for h in m.LABELS}
        with tempfile.TemporaryDirectory() as d:
            m.write_report(results,d)
            with (Path(d)/"effects.csv").open(encoding="utf-8") as f:
                rows=list(csv.DictReader(f))
            self.assertEqual(len(rows),4)
            self.assertTrue(all(r["source"]=="SYNTHETIC" for r in rows))
            self.assertNotIn("participant_id",rows[0])
            svg=ET.parse(Path(d)/"effects.svg").getroot()
            self.assertEqual(svg.tag,"{http://www.w3.org/2000/svg}svg")
            self.assertIn("SYNTHETIC", "".join(svg.itertext()))
            with self.assertRaises(ValueError):
                m.write_report(results,d,source="UNKNOWN")
            with self.assertRaises(ValueError):
                m.write_report(results,d,source="MAIN")
            manifest=dict(source="MAIN",dataset_sha256="a"*64,analysis_commit="b"*40,protocol_version="draft-test",results_sha256="c"*64)
            with self.assertRaises(ValueError):
                m.write_report(results,d,source="MAIN",provenance=manifest)
            manifest["results_sha256"]=hashlib.sha256(json.dumps(results,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
            m.write_report(results,d,source="MAIN",provenance=manifest)
            self.assertEqual(json.loads((Path(d)/"provenance.json").read_text()),manifest)


if __name__=="__main__":
    unittest.main()
