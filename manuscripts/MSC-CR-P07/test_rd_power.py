import unittest
from rd_power import scenario


class RDPowerTests(unittest.TestCase):
    def test_seed_and_accounting(self):
        args = (20, 8, .05, .5, .3, .75, .1, 10, 42)
        a = scenario(*args)
        self.assertEqual(a, scenario(*args))
        self.assertLessEqual(a["positive"], a["rejected"])
        self.assertLessEqual(a["rejected"], a["replicates"]-a["failed"])
        self.assertLessEqual(a["covered"], a["replicates"]-a["failed"])

    def test_null(self):
        a = scenario(20, 8, 0, .5, .3, .75, 0, 5, 42)
        self.assertAlmostEqual(a["beta"], 0)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            scenario(20, 8, 1, .5, .3, .75, 0, 5, 42)


if __name__ == "__main__":
    unittest.main()
