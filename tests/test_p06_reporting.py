"""Check aggregate reports and source labelling on synthetic data."""
import csv
import hashlib
import json
import importlib.util
import tempfile
import unittest
from unittest.mock import patch
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

    def test_failed_report_has_no_completion_marker(self):
        results={h:dict(hypothesis=h,unit="raw_score",estimate=.1,se=.05,
                        ci=[-.01,.21],p=.05,p_adjusted=.15,n_randomized=100,
                        n_used=98,reference="synthetic") for h in m.LABELS}
        def manifest_for(data):
            return dict(source="MAIN",dataset_sha256="a"*64,analysis_commit="b"*40,
                        protocol_version="draft-test",results_sha256=hashlib.sha256(
                        json.dumps(data,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest())
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)
            invalid={h:dict(v) for h,v in results.items()}
            del invalid["H1"]["estimate"]
            with self.assertRaises(KeyError):
                m.write_report(invalid,d,source="MAIN",provenance=manifest_for(invalid))
            self.assertFalse((out/"provenance.json").exists())
            self.assertFalse((out/"effects.csv").exists())
            m.write_report(results,d,source="MAIN",provenance=manifest_for(results))
            original=m.os.replace
            def fail_svg(src,dst):
                if Path(dst).name=="effects.svg":
                    raise OSError("injected failure")
                original(src,dst)
            with patch.object(m.os,"replace",side_effect=fail_svg):
                with self.assertRaises(OSError):
                    m.write_report(results,d,source="MAIN",provenance=manifest_for(results))
            self.assertFalse((out/"provenance.json").exists())


if __name__=="__main__":
    unittest.main()
