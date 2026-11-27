import unittest
from itertools import combinations, product
import numpy as np
import randomization_power as rp

class RandomizationTests(unittest.TestCase):
    def test_exact_enumeration(self):
        person=np.repeat([0,1],4); tone=np.array([1,1,0,0,1,0,0,0]); y=np.array([1,1,0,0,1,0,1,0])
        scores=[sum(y[list(a)])+sum(y[list(b)]) for a,b in product(combinations(range(4),2), combinations(range(4,8),1))]
        expected=np.mean(scores); observed=np.dot(tone,y)
        self.assertAlmostEqual(rp.conditional_test(person,tone,y),np.mean(np.abs(scores-expected)>=abs(observed-expected)-1e-10))
    def test_boolean_score(self):
        p = [0,0,0,0]
        a = np.array([1,1,0,0])
        y = np.array([1,1,0,0])
        self.assertAlmostEqual(rp.conditional_test(p,a,y),rp.conditional_test(p,a.astype(bool),y.astype(bool)))
    def test_nuisance_scenario(self):
        out = rp.scenario(12,8,.2,3,42,1,.7,.55,.1)
        self.assertEqual(out["missing"], .1)
        self.assertLessEqual(out["rejects"]+out["failures"],3)
    def test_degenerate(self):
        self.assertIsNone(rp.conditional_test([0,0],[0,1],[1,1]))
    def test_bad_input(self):
        with self.assertRaises(ValueError): rp.conditional_test([0],[2],[1])
    def test_reproducibility(self):
        self.assertEqual(rp.scenario(8,8,0,3,42),rp.scenario(8,8,0,3,42))
    def test_label_symmetry(self):
        p,t,y=rp.simulate(np.random.default_rng(42),10,24,.3)
        self.assertAlmostEqual(rp.conditional_test(p,t,y),rp.conditional_test(p,1-t,y))
if __name__=='__main__': unittest.main()
