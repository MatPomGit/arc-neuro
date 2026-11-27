"""Synthetic simulation smoke tests and optional GLMM integration."""
import importlib.util
import random
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"manuscripts/MSC-CR-P06/materials"))
import sensitivity as s
import item_glmm as g
sys.path.pop(0)


class P06SensitivityTests(unittest.TestCase):
    def test_known_truth_and_mask(self):
        full,masked=s.generate(24,.08,.15,"MAR",7)
        self.assertEqual(len(full),48)
        self.assertEqual(full,s.generate(24,.08,.15,"MAR",7)[0])
        for a,b in zip(full,masked):
            self.assertTrue(0<=a["accuracy_T1"]<=1)
            self.assertEqual({k:v for k,v in a.items() if k!="accuracy_T1"},
                             {k:v for k,v in b.items() if k!="accuracy_T1"})
            self.assertIn(b["accuracy_T1"],(None,a["accuracy_T1"]))

    def test_session_missingness_and_common_data(self):
        full, masked=s.generate(24,.08,.30,"MAR",7,missing_scope="session")
        self.assertEqual(full,s.generate(24,.08,.30,"MCAR",7)[0])
        self.assertTrue(any(r["accuracy_T1"] is None for r in masked))
        for row in masked:
            self.assertEqual(row["accuracy_T1"] is None,row["brier_T1"] is None)
            self.assertEqual(row["accuracy_T1"] is None,row["justification_T1"] is None)
        out=s.simulate(n_per_arm=24,repetitions=2,m=2,iterations=1,seed=7,missing_scope="session")
        self.assertEqual(out["settings"]["missing_scope"],"session")
        self.assertIn("pmm_delta10_intervention",out["methods"])
        self.assertIn("pmm_delta10_control",out["methods"])

    def test_smoke(self):
        for mechanism in s.MECHANISMS:
            out=s.simulate(n_per_arm=24,repetitions=2,m=2,iterations=1,mechanism=mechanism,seed=13)
            self.assertEqual(out["truth_pp"],8)
            self.assertEqual(out["source"],"SYNTHETIC_MONTE_CARLO_ONLY")
            for fit in out["methods"].values():
                self.assertEqual(fit["successful"]+fit["failed"],2)
            self.assertEqual(out["methods"]["full"]["successful"],2)
            self.assertGreater(out["methods"]["pmm"]["successful"],0)

    def test_metrics(self):
        out=s.summarize([dict(estimate=7,ci=[5,9],p=.01),dict(estimate=9,ci=[8.5,10],p=.1)],8,3)
        self.assertEqual(out["bias"],0)
        self.assertEqual(out["rmse"],1)
        self.assertEqual(out["coverage"],.5)
        self.assertEqual(out["failed"],1)


class P06GLMMTests(unittest.TestCase):
    def fixture(self):
        participants,_=s.generate(24,.08,0,"MCAR",12)
        rng=random.Random(44)
        rows=[]
        for p in participants:
            for j in range(1,9):
                rows.append(dict(participant_id=p["participant_id"],item_id=p["sequence"][1]+f"{j:02d}",
                                 correct=int(rng.random()<(.25+.5*p["arm"]))))
        return participants,rows

    def test_prepare_and_reject(self):
        participants,rows=self.fixture()
        prep=g.prepare(participants,rows)
        self.assertEqual(prep["n_standardized"],48)
        self.assertEqual(len(prep["observations"]),384)
        with self.assertRaises(ValueError):
            g.prepare(participants,rows+[rows[0]])
        wrong=dict(rows[0],item_id="Z01")
        with self.assertRaises(ValueError):
            g.prepare(participants,[wrong]+rows[1:])

    @unittest.skipUnless(all(importlib.util.find_spec(x) for x in ("numpy","scipy","statsmodels")),
                         "Optional GLMM dependencies unavailable")
    def test_optional_fit(self):
        p,r=self.fixture()
        result=g.fit_glmm(p,r,draws=150,seed=44)
        self.assertEqual(result["n_observed_items"],384)
        self.assertGreater(result["estimate_pp"],0)
        self.assertLess(result["estimate_pp"],100)
        self.assertLess(result["credible_interval_95_pp"][0],result["credible_interval_95_pp"][1])


if __name__=="__main__":
    unittest.main()
