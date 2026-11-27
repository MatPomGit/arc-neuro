# SPDX-License-Identifier: Apache-2.0
# Modified in ARC Neuro: resolve the migrated protocol configuration locally.
"""Test CA selection and data-integrity failure modes on synthetic exports."""

import json
from pathlib import Path
import tempfile
import unittest

from analysis import read_tables, select_attempts, summarize, validate
from synthetic import add_attempt, fixture, write_export

CONFIG = Path(__file__).resolve().parents[1] / "protocol/design_config.json"


class ExportTests(unittest.TestCase):
    """Assert expected scientific denominators and selection boundaries."""

    def setUp(self):
        """Load the real study configuration with synthetic observations."""
        self.config = json.loads(CONFIG.read_text())
        self.tables = fixture(self.config)

    def report(self):
        """Validate before producing any descriptive results."""
        return summarize(validate(self.tables, self.config), self.config)

    def attempt(self, sid="s1", **kwargs):
        """Add one independent synthetic test attempt."""
        add_attempt(self.tables, self.config, sid, **kwargs)

    def test_no_responses(self):
        """Retain a zero-responder in all scheduled denominators."""
        rates = self.report()["CA-F1"]["SYNTHETIC_001"]
        self.assertEqual(rates["full_plan"]["denominator"], 42)
        self.assertEqual(rates["full_plan"]["proportion"], 0)
        self.assertIsNone(rates["confirmed_delivery"]["proportion"])

    def test_no_enrolled_people(self):
        """Do not manufacture rates for an empty study export."""
        self.tables = {name: [] for name in self.tables}
        self.assertEqual(self.report()["CA-F1"], {})

    def test_first_timely_submission_only(self):
        """Ignore CSV ordering and count one completion per prompt."""
        self.attempt("later", delay=120)
        self.attempt("first", delay=60)
        self.assertEqual(self.report()["selection_audit_private"],
                         {"first": "selected", "later": "duplicate"})

    def test_window_boundary(self):
        """Include exactly 20 minutes, exclude one second later."""
        self.attempt("boundary", delay=1200)
        self.attempt("late", prompt=3, delay=1201)
        self.assertEqual(self.report()["attempt_counts"],
                         {"late": 1, "selected": 1})

    def test_withdrawal(self):
        """Preserve the full schedule and reject responses after withdrawal."""
        self.tables["participants"][0].update(
            withdrawal_offset="7230", completion_status="withdrawn"
        )
        for row in self.tables["prompts"]:
            row["enabled_before_withdrawal"] = (
                "true" if int(row["planned_offset_s"]) <= 7230 else "false"
            )
        self.attempt(delay=60)
        report = self.report()
        self.assertEqual(report["attempt_counts"], {"after_withdrawal": 1})
        self.assertEqual(report["CA-F1"]["SYNTHETIC_001"][
            "until_withdrawal"]["denominator"], 2)

    def test_structural_missingness(self):
        """Exclude first-prompt interval items from displayed denominators."""
        self.attempt(prompt=1)
        self.assertEqual(self.report()["CA-M1_M2"]["X_distance"][
            "missing"]["selected"]["denominator"], 0)

    def test_zero_is_valid(self):
        """Keep a valid zero instead of coercing it to missing."""
        self.attempt(value=0)
        m = self.report()["CA-M1_M2"]["A_state"]
        self.assertEqual(m["missing"]["selected"]["numerator"], 0)
        self.assertEqual(m["by_person"]["SYNTHETIC_001"]["median"], 0)

    def test_constant_ceiling_and_zero_variance(self):
        """Report a constant maximum without discarding participants."""
        for day in (1, 2):
            for prompt in range(1, 7):
                self.attempt(f"s{day}_{prompt}", day=day, prompt=prompt,
                             value=100)
        m = self.report()["CA-M1_M2"]["A_target"]["by_person"][
            "SYNTHETIC_001"]
        self.assertEqual(m["sd"], 0)
        self.assertEqual(m["ceiling"]["proportion"], 1)

    def test_item_dwell_time_reported(self):
        """Report display-to-answer dwell without inferring active attention."""
        self.attempt()
        dwell = self.report()["CA-F2_item_dwell"]["C_state"]["selected"]
        self.assertEqual(dwell["n"], 1)
        self.assertEqual(dwell["median"], 10)

    def test_bootstrap_suppressed_below_minimum_people(self):
        """Do not emit a percentile interval below the frozen people gate."""
        result = self.report()["person_bootstrap"]["CA-F1:until_withdrawal"]
        self.assertEqual(result["n_people"], 1)
        self.assertIsNone(result["interval"])

    def test_ca_d1_centered_correlation(self):
        """Compute the prespecified within-person descriptive relation."""
        counter = 0
        for day in (1, 2):
            for prompt in range(1, 7):
                counter += 1
                self.attempt(
                    f"pair_{day}_{prompt}",
                    day=day,
                    prompt=prompt,
                    value=counter,
                )
        result = self.report()["CA-D1"]["C_state:A_state"]
        self.assertEqual(result["n_people_with_minimum_pairs"], 1)
        self.assertEqual(result["n_common_pairs"], 12)
        self.assertAlmostEqual(result["within_person_centered_r"], 1.0)

    def test_abandoned_duration_separate(self):
        """Do not treat time observed before abandonment as completion."""
        self.attempt(reason="abandoned")
        report = self.report()
        self.assertEqual(report["CA-F2"]["10:all_attempts:abandoned"][
            "median"], 55)
        self.assertEqual(report["CA-F2"]["10:selected:submitted"]["n"], 0)

    def test_partial_form_is_valid_submission(self):
        """A skipped item does not delete a timely form."""
        self.attempt()
        self.tables["items"][0].update(value="", response_status="skipped",
                                       answered_offset_s="")
        self.assertEqual(self.report()["attempt_counts"], {"selected": 1})
        self.assertEqual(self.report()["CA-M1_M2"]["C_state"][
            "missing"]["selected"]["proportion"], 1)

    def test_invalid_value_rejected(self):
        """Reject nonfinite values and values outside item scales."""
        self.attempt()
        for value in ("NaN", "inf", "101", "-1"):
            with self.subTest(value=value):
                self.tables["items"][0]["value"] = value
                with self.assertRaises(ValueError):
                    self.report()

    def test_invalid_binary_contact_rejected(self):
        """Reject numeric ratings on the binary contact item."""
        self.attempt()
        self.tables["items"][-1]["value"] = "50"
        with self.assertRaises(ValueError):
            self.report()

    def test_missing_schedule_rejected(self):
        """Prevent denominators being reduced by omitted unanswered prompts."""
        self.tables["prompts"].pop()
        with self.assertRaises(ValueError):
            self.report()

    def test_missing_item_rejected(self):
        """Require all item records, even missing/structural ones."""
        self.attempt()
        self.tables["items"].pop()
        with self.assertRaises(ValueError):
            self.report()

    def test_unknown_parent_rejected(self):
        """Prevent orphaned responses from entering the analysis."""
        self.attempt()
        self.tables["items"][0]["submission_id"] = "unknown"
        with self.assertRaises(ValueError):
            self.report()

    def test_duplicate_timestamp_rejected(self):
        """Avoid selecting an arbitrary first record from exact ties."""
        self.attempt("one")
        self.attempt("two")
        with self.assertRaises(ValueError):
            self.report()

    def test_chronology_rejected(self):
        """Reject item answers recorded before the display time."""
        self.attempt()
        self.tables["items"][0]["answered_offset_s"] = "7201"
        with self.assertRaises(ValueError):
            self.report()

    def test_synthetic_csv_roundtrip(self):
        """Exercise the actual CSV schemas rather than only dictionaries."""
        self.attempt()
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / "synthetic"
            write_export(self.tables, folder)
            data = validate(read_tables(folder), self.config)
            chosen, _ = select_attempts(data, self.config)
            self.assertEqual(len(chosen), 1)
            with self.assertRaises(FileExistsError):
                write_export(self.tables, folder)


if __name__ == "__main__":
    unittest.main()
