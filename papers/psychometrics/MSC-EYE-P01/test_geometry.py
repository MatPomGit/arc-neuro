import unittest
from math import atan, degrees

from geometry import errors


class GeometryTests(unittest.TestCase):
    def test_center_and_off_axis(self):
        args = ((0.1, 0.1), (0, 0), 400)
        origin = errors((0, 0), (100, 0), *args)
        edge = errors((500, 0), (600, 0), *args)
        self.assertEqual(origin[0], edge[0])
        self.assertAlmostEqual(origin[1], degrees(atan(10 / 400)))
        self.assertAlmostEqual(edge[1], degrees(atan(60 / 400) - atan(50 / 400)))
        self.assertLess(edge[1], origin[1])
        self.assertEqual(errors((500, 0), (500, 0), *args), (0, 0))

    def test_invalid_geometry(self):
        for distance in (0, -1, float("nan")):
            with self.assertRaises(ValueError):
                errors((0, 0), (100, 0), (0.1, 0.1), (0, 0), distance)
