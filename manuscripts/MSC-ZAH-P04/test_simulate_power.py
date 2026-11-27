import unittest
import numpy as np
from simulate_power import generate

class DesignTests(unittest.TestCase):
    def test_balance(self):
        y,x,g=generate(np.random.default_rng(42),12,8,2,.5)
        self.assertEqual(len(y),192)
        self.assertTrue(np.all((y>=0)&(y<=4)))
        self.assertEqual(np.linalg.matrix_rank(x),6)
        for clip in np.unique(g["clip"]):
            np.testing.assert_array_equal(np.unique(x[g["clip"]==clip,1],return_counts=True)[1],[4,4,4])
        self.assertEqual(len(set(zip(g["observer"],g["clip"]))),len(y))
    def test_seed(self):
        a=generate(np.random.default_rng(42),12,8,2,0)
        b=generate(np.random.default_rng(42),12,8,2,0)
        np.testing.assert_array_equal(a[0],b[0])
        np.testing.assert_array_equal(a[1],b[1])

if __name__=="__main__":
    unittest.main()
