import unittest
import numpy as np
from marginal_surface import marginal_surface, peak_contrasts

class SurfaceTests(unittest.TestCase):
    def test_symmetry(self):
        s=marginal_surface(np.zeros((4,4)),[-1.5,-.5,.5,1.5],1)
        np.testing.assert_allclose(s,3,atol=1e-7)
        np.testing.assert_allclose(peak_contrasts(s),0,atol=1e-7)
        s[1,1]=4
        self.assertTrue((peak_contrasts(s)[:4]>0).all())
    def test_monotonicity(self):
        self.assertTrue((marginal_surface(np.full((4,4),2),[-1.5,-.5,.5,1.5],0)>3).all())
    def test_invalid(self):
        with self.assertRaises(ValueError):
            marginal_surface(np.zeros((4,4)),[0,0,1,2],1)

if __name__=="__main__":
    unittest.main()
