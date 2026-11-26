"""Focused simulation tests, no large Monte Carlo sweep in CI."""
import unittest
import numpy as np
from choice_power import Scenario, generate, simulate, interval


class ChoicePowerTests(unittest.TestCase):
    def test_factorial_and_shared_subjects(self):
        n,data=generate(Scenario(recruited=40,attrition=0,trial_missing=0),np.random.default_rng(42))
        self.assertEqual(n,40)
        a,b=data["risk"],data["ambiguity"]
        self.assertEqual(len(a[0]),40*48)
        np.testing.assert_array_equal(a[2],b[2])
        np.testing.assert_array_equal(a[1]["gad5"],b[1]["gad5"])
        for _,x,_ in (a,b):
            self.assertEqual(len(x[["contrast","level"]].drop_duplicates()),12)

    def test_holm_and_failed_fit(self):
        def fake(y,x,groups,term):
            if x["level"].max()>1:
                return dict(gad_effect=dict(p=.03,estimate=-.15,ci95=[-.3,0]))
            raise ValueError("fixture failure")
        a=simulate(Scenario(recruited=40,beta_ambiguity=0,attrition=0),3,9,fitter=fake)
        self.assertEqual(a["tasks"]["risk"]["raw_reject"]["count"],3)
        self.assertEqual(a["tasks"]["risk"]["holm_reject"]["count"],0)
        self.assertEqual(a["tasks"]["ambiguity"]["failures"],{"fixture failure":3})
        self.assertEqual(a["tasks"]["ambiguity"]["unconditional_coverage"]["rate"],0)
        self.assertIsNone(a["tasks"]["ambiguity"]["coverage_given_fit"])
        self.assertEqual(a["fwer"]["count"],0)

    def test_null_and_directional_power(self):
        def fake(y,x,groups,term):
            return dict(gad_effect=dict(p=.001,estimate=.2,ci95=[.1,.3]))
        a=simulate(Scenario(recruited=40,beta_risk=0,beta_ambiguity=-.2),2,3,fitter=fake)
        self.assertEqual(a["fwer"]["rate"],1)
        self.assertEqual(a["tasks"]["ambiguity"]["holm_reject"]["rate"],1)
        self.assertEqual(a["all_directional_power"]["rate"],0)
        self.assertIsNone(a["tasks"]["risk"]["directional_power"])

    def test_wilson_and_validation(self):
        self.assertGreater(interval(0,100)["mc_ci95"][1],0)
        self.assertIsNone(interval(0,0))
        with self.assertRaises(ValueError):
            Scenario(rho=2).validate()
        with self.assertRaises(ValueError):
            simulate(Scenario(),0,1)

    def test_seed_reproducibility(self):
        s=Scenario(recruited=40)
        a=generate(s,np.random.default_rng(88))
        b=generate(s,np.random.default_rng(88))
        self.assertEqual(a[0],b[0])
        for t in a[1]:
            np.testing.assert_array_equal(a[1][t][0],b[1][t][0])
            self.assertTrue(a[1][t][1].equals(b[1][t][1]))


if __name__=="__main__":
    unittest.main()
