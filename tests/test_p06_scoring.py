"""Synthetic regression tests, not empirical validation."""
import importlib.util
from pathlib import Path
import unittest

MATERIALS = Path(__file__).resolve().parents[1] / "papers/cognition/MSC-CR-P06/materials"
spec = importlib.util.spec_from_file_location("p06_scoring", MATERIALS / "scoring.py")
scoring = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scoring)


class P06ScoringTests(unittest.TestCase):
    def setUp(self):
        self.forms = scoring.load_bank()
        self.items = self.forms["A"]
        self.rows = [{"item_id": i, "response": x["key"], "confidence": 100,
                      "justification_score": 2 if x["justify"] else None}
                     for i, x in self.items.items()]

    def test_perfect(self):
        s = scoring.score_form(self.items, self.rows)
        self.assertEqual((s["accuracy"], s["brier"], s["confidence_bias"], s["justification_mean"]), (1, 0, 0, 2))
        self.assertEqual(s["n_answered"], 24)
        self.assertEqual(sum(s["confusion"][k][k] for k in scoring.CATEGORIES), 24)

    def test_confidently_wrong(self):
        for row in self.rows:
            row["response"] = {"U":"S","S":"N","N":"U"}[row["response"]]
        s = scoring.score_form(self.items, self.rows)
        self.assertEqual((s["accuracy"], s["brier"], s["confidence_bias"]), (0, 1, 1))

    def test_missing_boundaries(self):
        s = scoring.score_form(self.items, self.rows[:20])
        self.assertEqual(s["accuracy"], 1)
        self.assertEqual(s["brier"], 0)
        self.assertEqual(sum(s["missing_by_key"].values()), 4)
        s = scoring.score_form(self.items, self.rows[:19])
        self.assertIsNone(s["accuracy"])
        self.assertIsNone(s["brier"])
        self.assertEqual(sum(s["missing_by_key"].values()), 5)

    def test_confidence_separate_denominator(self):
        for row in self.rows[:5]:
            row["confidence"] = None
        s = scoring.score_form(self.items, self.rows)
        self.assertEqual(s["accuracy"], 1)
        self.assertEqual(s["n_confidence_pairs"], 19)
        self.assertIsNone(s["brier"])

    def test_human_rating_zero_not_missing(self):
        selected = [r for r in self.rows if r["justification_score"] is not None]
        selected[0]["justification_score"] = 0
        selected[1]["justification_score"] = None
        self.assertEqual(scoring.score_form(self.items, self.rows)["justification_mean"], 1.6)
        selected[2]["justification_score"] = None
        self.assertIsNone(scoring.score_form(self.items, self.rows)["justification_mean"])

    def test_all_missing(self):
        s = scoring.score_form(self.items, [])
        self.assertEqual(s["missing_by_key"], {"U":8,"S":8,"N":8})
        self.assertIsNone(s["accuracy"])
        self.assertIsNone(s["justification_mean"])

    def test_reject_invalid(self):
        for row in [{"item_id":"B01"}, {"item_id":"A01","response":"X"},
                    {"item_id":"A01","response":"U","confidence":float("nan")},
                    {"item_id":"A01","response":"U","confidence":101},
                    {"item_id":"A01","confidence":80},
                    {"item_id":"A03","justification_score":2},
                    {"item_id":"A01","justification_score":True}]:
            with self.subTest(row=row), self.assertRaises(ValueError):
                scoring.score_form(self.items,[row])
        with self.assertRaises(ValueError):
            scoring.score_form(self.items,[self.rows[0],self.rows[0]])

    def test_kappa(self):
        self.assertAlmostEqual(scoring.quadratic_kappa([(0,0),(1,1),(2,2)]),1)
        self.assertAlmostEqual(scoring.quadratic_kappa([(0,2),(2,0)]),-1)
        self.assertIsNone(scoring.quadratic_kappa([(1,1)]))
        self.assertIsNone(scoring.quadratic_kappa([(None,2)]))
        with self.assertRaises(ValueError):
            scoring.quadratic_kappa([(3,0)])


if __name__ == "__main__":
    unittest.main()
