import os
import unittest
import numpy as np
from ordinal_simulation import generate, fit

@unittest.skipUnless(os.environ.get("ARC_PYMC_SMOKE")=="1","Opt-in sampling smoke test")
class FitSmoke(unittest.TestCase):
    def test_real_sampling(self):
        y,x,groups,indices=generate(np.random.default_rng(42),16,16,"null")
        draws=fit(y,x,groups,42,draws=20,tune=30,chains=2,diagnostic=False)
        self.assertEqual(draws.shape,(40,x.shape[1]))
        self.assertTrue(np.isfinite(draws).all())

if __name__=="__main__":
    unittest.main()
