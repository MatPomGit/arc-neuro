import unittest
from h1_power import Scenario,simulate
from choice_power import Scenario as ChoiceScenario,simulate as simulate_choice


class H1PowerTests(unittest.TestCase):
    def test_trial_pipeline_reproducibility(self):
        s=Scenario(recruited=64,attrition=0,beta_ms=10)
        a=simulate(s,2,123)
        self.assertEqual(a,simulate(s,2,123))
        self.assertEqual(a["fit"]["count"],2)
        self.assertGreater(a["mean_eligible_given_fit"],50)
        self.assertIsNotNone(a["nominal_coverage_given_fit"])

    def test_no_valid_trials_counted(self):
        a=simulate(Scenario(recruited=32,invalid_probability=.999),1,15)
        self.assertEqual(a["fit"]["count"],0)
        self.assertEqual(a["reject"]["denominator"],1)
        self.assertIsNone(a["nominal_coverage_given_fit"])

    def test_choice_actual_glmm_smoke(self):
        a=simulate_choice(ChoiceScenario(recruited=120,attrition=0,trial_missing=0,
                                         beta_risk=0,beta_ambiguity=-.2),1,123)
        self.assertEqual(a["repetitions"],1)
        for t in a["tasks"].values():
            self.assertEqual(t["fit"]["count"]+sum(t["failures"].values()),1)
        self.assertGreaterEqual(sum(t["fit"]["count"] for t in a["tasks"].values()),1)
        self.assertIsNotNone(a["fwer"])


if __name__=="__main__":
    unittest.main()
