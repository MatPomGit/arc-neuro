"""Deterministic synthetic checks of classical test theory and power planning."""
import importlib.util
from pathlib import Path
import unittest

path=Path(__file__).resolve().parents[1]/"manuscripts/MSC-CR-P06/materials/psychometrics.py"
spec=importlib.util.spec_from_file_location("p06_psychometrics",path)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class P06PsychometricsTests(unittest.TestCase):
    def test_identical_items(self):
        rows=[dict(a=v,b=v,c=v) for v in (0,0,1,1)]
        s=m.analyze_form("abc",rows,bootstrap=0)
        self.assertEqual(s["kr20"],1)
        self.assertAlmostEqual(s["items"]["a"]["corrected_item_total"],1)
        self.assertEqual(s["items"]["a"]["p_correct"],.5)
        self.assertEqual(s["floor_complete"],.5)
        self.assertEqual(s["ceiling_complete"],.5)

    def test_negative_discrimination(self):
        s=m.analyze_form("abc",[dict(a=v,b=1-v,c=1-v) for v in (0,0,1,1)],bootstrap=0)
        self.assertAlmostEqual(s["items"]["a"]["corrected_item_total"],-1)
        self.assertIn("review_discrimination",s["items"]["a"]["flags"])
        self.assertLess(s["kr20"],0)

    def test_missing_and_constant(self):
        s=m.analyze_form("ab",[{"a":1,"b":1},{"a":1},{"a":1,"b":1}],bootstrap=0)
        self.assertEqual(s["n_complete"],2)
        self.assertEqual(s["items"]["a"]["n"],3)
        self.assertEqual(s["items"]["b"]["missing"],1)
        self.assertIsNone(s["kr20"])
        self.assertIsNone(s["items"]["a"]["corrected_item_total"])
        self.assertIsNone(m.analyze_form("ab",[],bootstrap=0)["items"]["a"]["wilson_95"])

    def test_wilson(self):
        lo,hi=m.wilson(5,10)
        self.assertAlmostEqual(lo,0.236593,places=5)
        self.assertAlmostEqual(hi,0.763407,places=5)
        self.assertIsNone(m.wilson(0,0))
        with self.assertRaises(ValueError):
            m.wilson(11,10)

    def test_bootstrap_reproducible(self):
        rows=[dict(a=v,b=v,c=v) for v in [0,1]*10]
        a=m.analyze_form("abc",rows,bootstrap=200,seed=17)
        b=m.analyze_form("abc",rows,bootstrap=200,seed=17)
        self.assertEqual(a,b)
        self.assertEqual(a["kr20_bootstrap_95"],[1,1])

    def test_form_matching(self):
        rows=[dict(participant_id="p1",sequence="ABC",A=.5,B=.75,C=1),
              dict(participant_id="p2",sequence="CBA",A=.75,B=.5,C=None)]
        s=m.compare_forms(rows)
        self.assertEqual(s["pairs"]["AB"]["overall"]["mean_difference"],0)
        self.assertEqual(s["pairs"]["AC"]["overall"]["n"],1)
        self.assertEqual(s["sequence_counts"]["ABC"],1)
        self.assertEqual(s["status"],"DESCRIPTIVE_NOT_EQUIVALENCE_TEST")
        with self.assertRaises(ValueError):
            m.compare_forms(rows+rows)

    def test_size_sensitivity(self):
        self.assertEqual(m.sample_size(.35,0)["recruit_total"],304)
        self.assertEqual(m.sample_size(.35,.5)["recruit_total"],230)
        self.assertLess(m.sample_size(.35,.7)["recruit_total"],230)
        with self.assertRaises(ValueError):
            m.sample_size(.35,1)

    def test_simulation_reproducibility(self):
        a=m.simulate_ancova(40,.5,.5,repetitions=80,seed=4)
        b=m.simulate_ancova(40,.5,.5,repetitions=80,seed=4)
        self.assertEqual(a,b)
        self.assertTrue(0<=a["rejection_rate"]<=1)
        self.assertEqual(a["status"],"SYNTHETIC_PLANNING_ONLY")

    def test_invalid_scores(self):
        for row in ({"a":True},{"a":2},{"z":0}):
            with self.subTest(row=row),self.assertRaises(ValueError):
                m.analyze_form("ab",[row],bootstrap=0)

if __name__=="__main__":
    unittest.main()
