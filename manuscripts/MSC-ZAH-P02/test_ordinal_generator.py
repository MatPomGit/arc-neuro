import unittest
import numpy as np
from ordinal_simulation import generate

class GeneratorTests(unittest.TestCase):
    def test_design(self):
        y,x,groups,indices=generate(np.random.default_rng(42),32,24,"null")
        self.assertEqual(len(y),len(x))
        self.assertTrue(np.all((y>=0)&(y<=4)))
        self.assertEqual(np.linalg.matrix_rank(x),x.shape[1])
        self.assertEqual(len(indices),9)
        for ids in groups.values():
            self.assertEqual(len(ids),len(y))
            self.assertTrue(np.all(ids>=0))
    def test_reproducibility(self):
        a=generate(np.random.default_rng(42),32,24,"peak")
        b=generate(np.random.default_rng(42),32,24,"peak")
        np.testing.assert_array_equal(a[0],b[0])
        np.testing.assert_array_equal(a[1],b[1])

if __name__=="__main__":
    unittest.main()
