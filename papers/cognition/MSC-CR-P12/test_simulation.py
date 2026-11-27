import unittest

import numpy as np

from simulation import sdt, simulate


class SignalDetectionTests(unittest.TestCase):
    def test_blanket_rejection_moves_criterion_not_sensitivity(self):
        d, c = sdt(np.array([[0, 0], [8, 8], [0, 8]]), 8)
        np.testing.assert_allclose(d[:2], [0, 0])
        self.assertGreater(c[0], 0)
        self.assertLess(c[1], 0)
        self.assertGreater(d[2], 0)
        self.assertTrue(np.isfinite(c).all())

    def test_seed_and_large_effect(self):
        def run(effect):
            return simulate(np.random.default_rng(58), 160, effect, 0.3, 0.15, reps=100)

        self.assertEqual(run(0.8), run(0.8))
        self.assertEqual(run(0.8)[3], 100)
        self.assertGreater(run(0.8)[0], run(0)[0] + 0.6)

    def test_primary_contrast_weights_only_far_domains(self):
        from analysis_model import primary_contrast

        expected = np.zeros((2, 3, 3))
        expected[1, 2, :] = [9, 0.2, 0.8]
        expected[1, 0, 1] = 0.1
        expected[0, 2, 2] = 0.3
        self.assertAlmostEqual(primary_contrast(expected), 0.3)

    def test_bank_keys_are_balanced_and_advice_is_paired(self):
        from collections import Counter
        from materials import bank

        entries = bank()
        self.assertEqual(len({row["id"] for row in entries}), 144)
        counts = Counter((row["domain"], row["form"], row["correct"]) for row in entries)
        self.assertTrue(all(6 <= count <= 10 for count in counts.values()))
        for row in entries:
            normalized = [advice.replace(answer, "OPCJA") for advice, answer in zip(row["advice"], row["answers"])]
            self.assertEqual(normalized[0], normalized[1])

    def test_appropriate_reliance_uses_disagreement(self):
        from metrics import behavior_metrics

        def trial(ai, initial, final, accepted):
            return dict(correct_option="A", ai_option=ai, initial=initial, final=final,
                        accepted=accepted, confidence=0.8)

        scores = behavior_metrics([trial("A", "B", "A", "1"), trial("A", "A", "A", "1"),
                                   trial("B", "A", "A", "0"), trial("B", "A", "B", "1")])
        self.assertEqual(scores["rair"], (1, 1))
        self.assertEqual(scores["rsr"], (0.5, 2))
        self.assertAlmostEqual(scores["brier"][0], 0.19)
