"""Reliability contract and recovery tests on synthetic fixtures."""
import unittest
from collections import Counter
import numpy as np
from design import manifest
from reliability import (split_trials,half_cost,correlation,spearman_brown,
                         reliability,attenuation,paired_costs)
from synthetic import synthetic


class ReliabilityTests(unittest.TestCase):
    def test_exact_schedule_and_outcome_independence(self):
        rows=manifest(12)["switching"]
        halves=split_trials(rows,23)
        for half in halves:
            self.assertEqual(Counter(t["transition"] for t in half),{"switch":47,"repeat":47})
        keys=lambda h:{(t["block"],t["trial_index"]) for t in h}
        self.assertFalse(keys(halves[0])&keys(halves[1]))
        modified=[dict(t,rt_ms=1000,correct=False) for t in reversed(rows)]
        self.assertEqual([keys(h) for h in halves],[keys(h) for h in split_trials(modified,23)])

    def test_half_cost_known(self):
        rows=manifest(7)["switching"]
        half=split_trials(rows)[0]
        half=[dict(t,rt_ms=700 if t["transition"]=="switch" else 600,
                   correct=True,timeout=False,focus_lost=False,technical_error=False) for t in half]
        self.assertEqual(half_cost(half),100.)
        for t in half:
            if t["transition"]=="switch":
                t["timeout"]=True
        self.assertIsNone(half_cost(half))

    def test_sb_and_invalid(self):
        self.assertAlmostEqual(spearman_brown(.5),2/3)
        self.assertLess(spearman_brown(-.5),0)
        self.assertIsNone(spearman_brown(-1))
        self.assertIsNone(correlation(np.ones((5,2))))
        with self.assertRaises(ValueError):
            reliability(np.ones((5,2)))

    def test_recovery_and_bootstrap(self):
        rng=np.random.default_rng(42)
        latent=rng.normal(size=1000)
        a=np.c_[latent+rng.normal(size=1000),latent+rng.normal(size=1000)]
        result=reliability(a,200,9)
        self.assertAlmostEqual(result["spearman_brown"],2/3,delta=.08)
        self.assertEqual(result,reliability(a,200,9))
        self.assertEqual(result["valid_raw"],200)

    def test_attenuation_monotonic(self):
        a,b=(attenuation(.15,.85,r) for r in (.3,.9))
        self.assertLess(a["power"],b["power"])
        self.assertGreater(a["complete_n_80"],b["complete_n_80"])
        self.assertAlmostEqual(attenuation(.15,1,1)["observed_partial_r"],.15)
        with self.assertRaises(ValueError):
            attenuation(.15,.85,0)

    def test_provenance(self):
        a=list(synthetic(17,4))
        pairs,excluded=paired_costs(a)
        self.assertEqual(len(pairs)+sum(excluded.values()),4)
        with self.assertRaises(ValueError):
            paired_costs([dict(a[0],data_origin="observed")])
        with self.assertRaises(ValueError):
            paired_costs([a[0],a[0]])


if __name__=="__main__":
    unittest.main()
