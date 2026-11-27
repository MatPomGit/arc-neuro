# SPDX-License-Identifier: Apache-2.0
# Modified in ARC Neuro: resolve the migrated protocol configuration locally.
"""Validate CA CSV exports and report descriptive feasibility diagnostics.

No hypothesis tests or automatic collection-readiness decisions are made.
Usage: python manuscripts/MSC-ATTACH-P06/analysis/analysis.py --input DIR --output NEW_DIR
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
import math
import random
from pathlib import Path
from statistics import mean, median, stdev

SCHEMAS = {
    "participants": (
        "participant_code instrument_version schedule_started start_offset "
        "withdrawal_offset completion_status"
    ).split(),
    "prompts": (
        "participant_code day prompt planned_offset_s "
        "enabled_before_withdrawal delivery_status delivered_offset_s"
    ).split(),
    "submissions": (
        "submission_id participant_code day prompt opened_offset_s "
        "submitted_offset_s closed_offset_s end_reason instrument_version "
        "help_open_count"
    ).split(),
    "items": (
        "submission_id item_id displayed value response_status "
        "displayed_offset_s answered_offset_s"
    ).split(),
}


def require(condition: bool, message: str) -> None:
    """Reject an invalid export without silently repairing source data."""
    if not condition:
        raise ValueError(message)


def number(value: str, nullable: bool = False) -> float | None:
    """Parse finite nonnegative numbers; only an empty cell means missing."""
    if nullable and value == "":
        return None
    try:
        result = float(value)
    except ValueError:
        raise ValueError("Expected a finite numeric cell") from None
    require(math.isfinite(result) and result >= 0, "Invalid numeric field")
    return result


def boolean(value: str) -> bool:
    """Parse only explicit lowercase true/false flags."""
    require(value in {"true", "false"}, "Invalid boolean field")
    return value == "true"


def key(row: dict) -> tuple:
    """Return a participant-day-prompt key with strict integer coordinates."""
    day, prompt = row["day"], row["prompt"]
    require(day.isdecimal() and prompt.isdecimal(), "Invalid prompt key")
    return row["participant_code"], int(day), int(prompt)


def read_tables(folder: Path) -> dict[str, list[dict]]:
    """Read exact UTF-8 CSV schemas, including empty header-only tables."""
    tables = {}
    for name, columns in SCHEMAS.items():
        with (folder / f"{name}.csv").open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            reader = csv.DictReader(handle)
            require(reader.fieldnames == columns, f"{name}: invalid header")
            rows = list(reader)
            require(all(None not in row and None not in row.values()
                        for row in rows), f"{name}: malformed row")
            tables[name] = rows
    return tables


def validate(tables: dict, config: dict) -> dict:
    """Validate keys, chronology, schedules, scales and structural missingness.

    Return typed indexes, preserving every attempt. This is structural
    validation, not verification that reported events occurred on a phone.
    """
    people, prompts, submissions, items = {}, {}, {}, {}
    item_names = config["current_items"] + config["interval_items"]
    days = config["esm"]["days"]
    per_day = config["esm"]["prompts_per_day"]
    for row in tables["participants"]:
        pid = row["participant_code"]
        require(bool(pid) and pid not in people, "Duplicate/empty person key")
        require(row["instrument_version"] == config["instrument_version"],
                "Instrument version mismatch")
        started = boolean(row["schedule_started"])
        start = number(row["start_offset"], nullable=not started)
        withdrawal = number(row["withdrawal_offset"], nullable=True)
        status = row["completion_status"]
        require(status in {"completed", "withdrawn", "ongoing", "not_started"},
                "Invalid participant status")
        require(started == (status != "not_started"), "Start/status mismatch")
        require((withdrawal is not None) == (status == "withdrawn"),
                "Withdrawal/status mismatch")
        require(withdrawal is None or withdrawal >= start,
                "Withdrawal before start")
        people[pid] = dict(started=started, start=start, withdrawal=withdrawal)
    for row in tables["prompts"]:
        prompt_key = key(row)
        pid, day, prompt = prompt_key
        require(pid in people and people[pid]["started"], "Unknown person")
        require(1 <= day <= days and 1 <= prompt <= per_day,
                "Prompt outside design")
        require(prompt_key not in prompts, "Duplicate prompt")
        planned = number(row["planned_offset_s"])
        withdrawal = people[pid]["withdrawal"]
        enabled = boolean(row["enabled_before_withdrawal"])
        require(enabled == (withdrawal is None or planned <= withdrawal),
                "Withdrawal flag contradicts schedule")
        delivery = row["delivery_status"]
        delivered = number(row["delivered_offset_s"], nullable=True)
        require(delivery in {"confirmed", "failed", "unknown"},
                "Invalid delivery status")
        require((delivery == "confirmed") == (delivered is not None),
                "Delivery timestamp/status mismatch")
        require(delivered is None or delivered >= planned,
                "Delivery before schedule")
        require(planned >= people[pid]["start"], "Prompt before start")
        prompts[prompt_key] = dict(planned=planned, enabled=enabled,
                                  delivery=delivery)
    for pid, person in people.items():
        schedule = [prompts[k]["planned"] for k in sorted(prompts)
                    if k[0] == pid]
        expected = days * per_day if person["started"] else 0
        require(len(schedule) == expected, "Incomplete planned schedule")
        require(all(b > a for a, b in zip(schedule, schedule[1:])),
                "Non-increasing schedule")
    for row in tables["submissions"]:
        sid = row["submission_id"]
        require(bool(sid) and sid not in submissions, "Duplicate attempt ID")
        pk = key(row)
        require(pk in prompts, "Attempt without planned prompt")
        require(row["instrument_version"] == config["instrument_version"],
                "Attempt version mismatch")
        opened = number(row["opened_offset_s"])
        submitted = number(row["submitted_offset_s"], nullable=True)
        closed = number(row["closed_offset_s"], nullable=True)
        reason = row["end_reason"]
        require(reason in {"submitted", "abandoned", "technical_error"},
                "Invalid end reason")
        require((reason == "submitted") == (submitted is not None),
                "Submission timestamp/status mismatch")
        require(opened >= prompts[pk]["planned"], "Opened before schedule")
        require(closed is None or closed >= opened, "Closed before opening")
        require(submitted is None or (submitted >= opened
                                      and closed == submitted),
                "Invalid submission chronology")
        require(row["help_open_count"].isdecimal(), "Invalid help count")
        submissions[sid] = dict(key=pk, opened=opened, submitted=submitted,
                                closed=closed, reason=reason)
    for row in tables["items"]:
        sid, item = row["submission_id"], row["item_id"]
        require(sid in submissions and item in item_names,
                "Unknown attempt/item reference")
        require((sid, item) not in items, "Duplicate item record")
        displayed = boolean(row["displayed"])
        state = row["response_status"]
        require(state in {"answered", "skipped", "structural", "not_reached",
                          "technical_error"}, "Invalid response status")
        structural = (submissions[sid]["key"][2] == 1
                      and item in config["interval_items"])
        require((state == "structural") == structural,
                "Incorrect structural missingness")
        value = number(row["value"], nullable=True)
        shown = number(row["displayed_offset_s"], nullable=True)
        answered = number(row["answered_offset_s"], nullable=True)
        require((state == "answered") == (value is not None),
                "Missingness/value contradiction")
        require(displayed == (shown is not None), "Display/time mismatch")
        require(state not in {"answered", "skipped"} or displayed,
                "Response to undisplayed item")
        require(state not in {"structural", "not_reached"} or not displayed,
                "Undisplayed status contradiction")
        require((state == "answered") == (answered is not None),
                "Answer/time mismatch")
        require(value is None or (value in {0, 1} if item == "K_contact"
                                   else value <= 100), "Value outside scale")
        start, end = submissions[sid]["opened"], submissions[sid]["closed"]
        require(shown is None or (shown >= start
                                  and (end is None or shown <= end)),
                "Display outside attempt")
        require(answered is None or (answered >= shown
                                     and (end is None or answered <= end)),
                "Answer outside display interval")
        items[sid, item] = dict(
            value=value,
            displayed=displayed,
            status=state,
            shown=shown,
            answered=answered,
        )
    require(len(items) == len(submissions) * len(item_names),
            "Missing item records; export all ten records per attempt")
    return dict(people=people, prompts=prompts, submissions=submissions,
                items=items)


def select_attempts(data: dict, config: dict) -> tuple[dict, dict]:
    """Select the first timely submission and audit every other attempt."""
    eligible = defaultdict(list)
    audit = {}
    window = config["esm"]["response_window_minutes"] * 60
    for sid, attempt in data["submissions"].items():
        pk, submitted = attempt["key"], attempt["submitted"]
        prompt = data["prompts"][pk]
        withdrawal = data["people"][pk[0]]["withdrawal"]
        if submitted is None:
            audit[sid] = attempt["reason"]
        elif not prompt["enabled"] or (withdrawal is not None
                                       and submitted > withdrawal):
            audit[sid] = "after_withdrawal"
        elif submitted > prompt["planned"] + window:
            audit[sid] = "late"
        else:
            eligible[pk].append((submitted, sid))
    chosen = {}
    for pk, attempts in eligible.items():
        attempts.sort()
        require(len({time for time, _ in attempts}) == len(attempts),
                "Ambiguous duplicate submission timestamps")
        chosen[pk] = attempts[0][1]
        for index, (_, sid) in enumerate(attempts):
            audit[sid] = "selected" if index == 0 else "duplicate"
    return chosen, audit


def fraction(numerator: int, denominator: int) -> dict:
    """Retain exact denominators; undefined rates are null, never zero."""
    return dict(numerator=numerator, denominator=denominator,
                proportion=numerator / denominator if denominator else None)


def distribution(values: list[float]) -> dict:
    """Return sample size and linearly interpolated descriptive quantiles."""
    values = sorted(values)
    def quantile(probability):
        if not values:
            return None
        position = (len(values) - 1) * probability
        lower = int(position)
        upper = min(lower + 1, len(values) - 1)
        return values[lower] + (position - lower) * (
            values[upper] - values[lower]
        )
    q1, q3 = quantile(0.25), quantile(0.75)
    return dict(n=len(values), median=quantile(0.5), p90=quantile(0.9),
                iqr=q3 - q1 if values else None)


def pearson(values_x: list[float], values_y: list[float]) -> float | None:
    """Return Pearson r, or null when the coefficient is not estimable."""
    require(len(values_x) == len(values_y), "Correlation vectors differ")
    if len(values_x) < 2:
        return None
    mean_x, mean_y = mean(values_x), mean(values_y)
    centered_x = [value - mean_x for value in values_x]
    centered_y = [value - mean_y for value in values_y]
    denominator = math.sqrt(
        sum(value * value for value in centered_x)
        * sum(value * value for value in centered_y)
    )
    if denominator == 0:
        return None
    return sum(x * y for x, y in zip(centered_x, centered_y)) / denominator


def bootstrap_median(values: list[float], config: dict) -> dict:
    """Bootstrap whole-person medians using the frozen reporting settings."""
    values = [value for value in values if value is not None]
    result = {
        "n_people": len(values),
        "point": median(values) if values else None,
        "range": [min(values), max(values)] if values else None,
        "interval": None,
        "degenerate": None,
    }
    settings = config["reporting_bootstrap"]
    if len(values) < settings["minimum_eligible_persons"]:
        return result
    rng = random.Random(settings["seed"])
    estimates = []
    for _ in range(settings["replications"]):
        sample = [values[rng.randrange(len(values))] for _ in values]
        estimates.append(median(sample))
    estimates.sort()
    alpha = 1 - settings["confidence_level"]

    def percentile(probability: float) -> float:
        position = (len(estimates) - 1) * probability
        lower = int(position)
        upper = min(lower + 1, len(estimates) - 1)
        return estimates[lower] + (position - lower) * (
            estimates[upper] - estimates[lower]
        )

    low = percentile(alpha / 2)
    high = percentile(1 - alpha / 2)
    result["interval"] = {
        "method": settings["method"],
        "confidence_level": settings["confidence_level"],
        "replications": settings["replications"],
        "seed": settings["seed"],
        "low": low,
        "high": high,
    }
    result["degenerate"] = low == high
    return result


def ca_d1_report(data: dict, selected: set[str]) -> dict:
    """Compute the three prespecified descriptive CA-D1 correlations."""
    pairs = (
        ("C_state", "A_state"),
        ("A_state", "W_solitude"),
        ("A_state", "X_distance"),
    )
    output = {}
    for item_x, item_y in pairs:
        by_person = defaultdict(list)
        for sid in selected:
            left = data["items"].get((sid, item_x))
            right = data["items"].get((sid, item_y))
            if not left or not right:
                continue
            if left["value"] is None or right["value"] is None:
                continue
            pid = data["submissions"][sid]["key"][0]
            by_person[pid].append((left["value"], right["value"]))

        eligible = {
            pid: values for pid, values in by_person.items()
            if len(values) >= 10
        }
        person_x = [mean(x for x, _ in values) for values in eligible.values()]
        person_y = [mean(y for _, y in values) for values in eligible.values()]

        centered_x = []
        centered_y = []
        centered_people = 0
        for values in eligible.values():
            xs = [x for x, _ in values]
            ys = [y for _, y in values]
            if len(set(xs)) < 2 or len(set(ys)) < 2:
                continue
            centered_people += 1
            mean_x, mean_y = mean(xs), mean(ys)
            centered_x.extend(x - mean_x for x in xs)
            centered_y.extend(y - mean_y for y in ys)

        output[f"{item_x}:{item_y}"] = {
            "minimum_pairs_per_person": 10,
            "n_people_with_minimum_pairs": len(eligible),
            "n_common_pairs": sum(len(values) for values in eligible.values()),
            "between_person_mean_r": pearson(person_x, person_y),
            "within_person_centered_r": pearson(centered_x, centered_y),
            "n_people_in_centered_r": centered_people,
            "n_pairs_in_centered_r": len(centered_x),
            "interpretation": (
                "descriptive_only; correlation does not establish construct "
                "validity, prediction or causality"
            ),
        }
    return output


def summarize(data: dict, config: dict) -> dict:
    """Report prespecified ESM feasibility outputs without inferential claims.

    The private output contains pseudonymous IDs for auditable selection.
    CA-Q1 cognitive-interview coding remains a separate input/workflow.
    """
    chosen, audit = select_attempts(data, config)
    selected = set(chosen.values())
    rates = {}
    for pid, person in data["people"].items():
        if not person["started"]:
            continue
        planned = [k for k in data["prompts"] if k[0] == pid]
        active = [k for k in planned if data["prompts"][k]["enabled"]]
        confirmed = [k for k in active
                     if data["prompts"][k]["delivery"] == "confirmed"]
        rates[pid] = {
            "full_plan": fraction(sum(k in chosen for k in planned),
                                  len(planned)),
            "until_withdrawal": fraction(sum(k in chosen for k in active),
                                         len(active)),
            "confirmed_delivery": fraction(sum(k in chosen for k in confirmed),
                                           len(confirmed)),
        }
    duration = {}
    for form in (6, 10):
        for scope in ("all_attempts", "selected"):
            for reason in ("submitted", "abandoned", "technical_error"):
                attempts = [a for sid, a in data["submissions"].items()
                            if (6 if a["key"][2] == 1 else 10) == form
                            and (scope == "all_attempts" or sid in selected)
                            and a["reason"] == reason]
                observed = [a["closed"] - a["opened"] for a in attempts
                            if a["closed"] is not None]
                duration[f"{form}:{scope}:{reason}"] = {
                    **distribution(observed),
                    "missing_duration": len(attempts) - len(observed),
                }

    item_dwell = {}
    for item in config["current_items"] + config["interval_items"]:
        item_dwell[item] = {}
        for scope in ("all_attempts", "selected"):
            item_rows = [
                row for (sid, name), row in data["items"].items()
                if name == item and (scope == "all_attempts" or sid in selected)
            ]
            observed = [
                row["answered"] - row["shown"] for row in item_rows
                if row["shown"] is not None and row["answered"] is not None
            ]
            item_dwell[item][scope] = {
                **distribution(observed),
                "missing_dwell": sum(
                    row["displayed"] and row["answered"] is None
                    for row in item_rows
                ),
            }

    measurements = {}
    threshold = config["diagnostic_thresholds"]
    for item in config["current_items"] + config["interval_items"]:
        rows = [(sid, row) for (sid, name), row in data["items"].items()
                if name == item]
        missing = {}
        for scope in ("all_attempts", "selected"):
            shown = [row for sid, row in rows if row["displayed"]
                     and (scope == "all_attempts" or sid in selected)]
            missing[scope] = fraction(sum(r["value"] is None for r in shown),
                                      len(shown))
        values = defaultdict(list)
        for sid, row in rows:
            if sid in selected and row["value"] is not None:
                values[data["submissions"][sid]["key"][0]].append(row["value"])
        people = {}
        for pid in rates:
            vals = values[pid]
            people[pid] = {
                **distribution(vals),
                "floor": fraction(sum(v <= threshold["floor_at_or_below"]
                                      for v in vals), len(vals)),
                "ceiling": fraction(sum(v >= threshold["ceiling_at_or_above"]
                                        for v in vals), len(vals)),
                "boundary": fraction(
                    sum(
                        v <= threshold["floor_at_or_below"]
                        or v >= threshold["ceiling_at_or_above"]
                        for v in vals
                    ),
                    len(vals),
                ),
                "sd": stdev(vals) if len(vals) >= threshold[
                    "minimum_observations_for_person_sd"] else None,
            }
        measurements[item] = {"missing": missing, "by_person": people}

    bootstrap = {}
    for metric in ("full_plan", "until_withdrawal", "confirmed_delivery"):
        bootstrap[f"CA-F1:{metric}"] = bootstrap_median(
            [
                person[metric]["proportion"] for person in rates.values()
                if person[metric]["proportion"] is not None
            ],
            config,
        )
    for item, report in measurements.items():
        bootstrap[f"CA-M2:{item}:boundary_fraction"] = bootstrap_median(
            [
                person["boundary"]["proportion"]
                for person in report["by_person"].values()
                if person["boundary"]["proportion"] is not None
            ],
            config,
        )
        bootstrap[f"CA-M2:{item}:within_person_sd"] = bootstrap_median(
            [
                person["sd"] for person in report["by_person"].values()
                if person["sd"] is not None
            ],
            config,
        )

    return {
        "status": "esm_descriptive_pipeline_complete_no_readiness_decision",
        "not_implemented": ["CA-Q1 cognitive-interview coding and analysis"],
        "readiness_decision": (
            "not_computed_by_design; interpret each prespecified domain "
            "separately and combine with CA-Q1 plus governance gates"
        ),
        "instrument_version": config["instrument_version"],
        "plan_version": config["plan_version"],
        "CA-F1": rates,
        "CA-F2": duration,
        "CA-F2_item_dwell": item_dwell,
        "CA-M1_M2": measurements,
        "CA-D1": ca_d1_report(data, selected),
        "person_bootstrap": bootstrap,
        "attempt_counts": dict(Counter(audit.values())),
        "selection_audit_private": audit,
    }


def main() -> None:
    """Validate before creating a new private output directory."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--config", type=Path,
        default=Path(__file__).resolve().parents[1] / "protocol/design_config.json",
    )
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        data = validate(read_tables(args.input), config)
        report = summarize(data, config)
        sources = [args.input / f"{name}.csv" for name in SCHEMAS]
        sources.extend([args.config, Path(__file__)])
        report["input_sha256"] = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sources
        }
        args.output.mkdir(parents=True, exist_ok=False)
        (args.output / "report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)
            + "\n", encoding="utf-8",
        )
        print("Validated; private descriptive report written. No theory test.")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"CA analysis failed: {exc}\n")


if __name__ == "__main__":
    main()
