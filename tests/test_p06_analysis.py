"""Synthetic ANCOVA and multiple-imputation pooling tests."""
import importlib.util
import random
import unittest
from pathlib import Path

path=Path(__file__).resolve().parents[1]/"papers/cognition/MSC-CR-P06/materials/analysis.py"
spec=importlib.util.spec_from_file_location("p06_analysis",path)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def fixture():
    rng=random.Random(173)
    rows=[]
    # Orthogonal balanced design, deterministic synthetic residual variation.
    for arm in (0,1):
        for stratum in (0,1):
            for seq in m.SEQUENCES:
                for k in range(6):
                    x=.25+.08*k
                    e=rng.uniform(-.05,.05)
                    rows.append(dict(participant_id=f"synthetic-{len(rows)}",arm=arm,stratum=stratum,sequence=seq,
                        accuracy_T0=x,accuracy_T1=.2+.55*x+.08*arm+e,
                        accuracy_T2=.25+.45*x+.04*arm+e,
                        brier_T0=.4-.3*x,brier_T1=.25-.2*x-.04*arm+e,
                        justification_T0=2*x,justification_T1=.4+1.1*x+.2*arm+e))
    return rows


class P06AnalysisTests(unittest.TestCase):
    def test_holm(self):
        self.assertEqual(m.holm({"a":.01,"b":.04,"c":.03}),{"a":.03,"c":.06,"b":.06})
        self.assertEqual(m.holm({"a":.9,"b":.8}),{"b":1.,"a":1.})

    def test_rubin(self):
        r=m.rubin([{"estimate":1.,"variance":.25},{"estimate":3.,"variance":.25}])
        self.assertEqual(r["estimate"],2.)
        self.assertEqual(r["within_variance"],.25)
        self.assertEqual(r["between_variance"],2.)
        self.assertEqual(r["variance"],3.25)

    def test_effects_and_units(self):
        rows=fixture()
        r=m.analyze_complete_cases(rows)
        self.assertAlmostEqual(r["H1"]["estimate"],8,delta=1.5)
        self.assertLess(r["H3"]["estimate"],0)
        self.assertGreater(r["H4"]["estimate"],0)
        self.assertEqual(r["H1"]["unit"],"percentage_points")
        self.assertEqual(r["H1"]["n_used"],144)
        self.assertGreaterEqual(r["H3"]["p_adjusted"],r["H3"]["p"])

    def test_independent_statsmodels_reference(self):
        # statsmodels 0.14.6, numpy 2.3.5, OLS.fit(cov_type="HC3",use_t=False)
        # Independent calculation on fixture(), uncentered baseline.
        expected={
            "H1":(8.056666308164788,.47562979352200596),
            "H2":(4.05666630816479,.4756297935220059),
            "H3":(-.03943333691835202,.004756297935220063),
            "H4":(.2005666630816481,.004756297935220058),
        }
        for h,(estimate,se) in expected.items():
            r=m.fit_endpoint(fixture(),h)
            self.assertAlmostEqual(r["estimate"],estimate,places=9)
            self.assertAlmostEqual(r["se"],se,places=9)

    def test_adjustment_invariance(self):
        rows=fixture()
        a=m.fit_endpoint(rows,"H1")
        for r in rows:
            r["accuracy_T1"]+=.02*r["arm"]+.05*r["stratum"]
        b=m.fit_endpoint(rows,"H1")
        self.assertAlmostEqual(b["estimate"]-a["estimate"],2,places=8)
        self.assertAlmostEqual(a["variance"],b["variance"],places=8)

    def test_missing_and_pool(self):
        original=fixture()
        completed=[dict(r) for r in original]
        original[-1]["accuracy_T1"]=None
        self.assertEqual(m.missingness(original)["1"]["missing"]["accuracy_T1"],1)
        self.assertEqual(m.fit_endpoint(original,"H1")["n_used"],143)
        second=[dict(r) for r in completed]
        second[-1]["accuracy_T1"]-=.04
        pooled=m.analyze_imputations(original,[completed,second],expected_m=2)
        shifted=m.analyze_imputations(original,[completed,second],expected_m=2,delta=-.05,shifted_arm=1)
        self.assertEqual(pooled["H1"]["n_used"],144)
        self.assertLess(shifted["H1"]["estimate"],pooled["H1"]["estimate"])
        self.assertEqual(shifted["H2"]["estimate"],pooled["H2"]["estimate"])
        self.assertEqual(original[-1]["accuracy_T1"],None)

    def test_reject_corrupt_imputations(self):
        rows=fixture()
        bad=[dict(r) for r in rows]
        bad[0]["accuracy_T1"]+=.01
        with self.assertRaises(ValueError):
            m.analyze_imputations(rows,[rows,bad],expected_m=2)
        with self.assertRaises(ValueError):
            m.analyze_imputations(rows,[rows,rows[:-1]],expected_m=2)
        with self.assertRaises(ValueError):
            m.analyze_imputations(rows,[rows,rows])

    def test_reject_bad_data(self):
        rows=fixture()
        with self.assertRaises(ValueError):
            m.validate(rows+rows[:1])
        for key,val in (("arm",True),("accuracy_T1",1.1),("brier_T0",float("nan")),("sequence","AAC"),("email","test")):
            bad=[dict(r) for r in rows]
            bad[0][key]=val
            with self.subTest(key=key),self.assertRaises(ValueError):
                m.validate(bad)

    def test_rank_deficient(self):
        rows=fixture()
        for r in rows:
            r["sequence"]="ABC"
        with self.assertRaises(ValueError):
            m.fit_endpoint(rows,"H1")


if __name__=="__main__":
    unittest.main()
