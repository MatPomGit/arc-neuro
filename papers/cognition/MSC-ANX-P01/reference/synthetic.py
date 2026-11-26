"""Synthetic-only reference for QA and participant-level H1 summaries."""
from statistics import median
from random import Random
from math import exp, isfinite
from design import manifest


def summarize(rows):
    mixed = [r for r in rows if r["mixed"] and r["transition"] != "undefined"]
    def technically_valid(r):
        return not r["focus_lost"] and not r["technical_error"] and (
            r["timeout"] or (r["rt_ms"] is not None and isfinite(r["rt_ms"]) and 150 <= r["rt_ms"] <= 2000))
    def correct(r):
        return technically_valid(r) and not r["timeout"] and r["correct"]
    valid = [r for r in mixed if technically_valid(r)]
    groups = {c: [r["rt_ms"] for r in valid if r["transition"] == c and correct(r)]
              for c in ("switch", "repeat")}
    accuracy = sum(correct(r) for r in valid) / len(valid) if valid else None
    baseline = [r["rt_ms"] for r in rows if not r["mixed"] and correct(r)]
    eligible = (accuracy is not None and accuracy >= .75 and
                all(len(g) >= 50 for g in groups.values()) and len(baseline) >= 24)
    return dict(eligible=eligible, accuracy=accuracy,
                n_switch=len(groups["switch"]), n_repeat=len(groups["repeat"]),
                baseline_rt_ms=median(baseline) if baseline else None,
                switch_cost_ms=median(groups["switch"])-median(groups["repeat"]) if eligible else None)


def logistic(x):
    return 1 / (1 + exp(-x))


def synthetic(seed, n):
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")
    rng = Random(seed)
    for i in range(n):
        pid = f"SYN-{i+1:06d}"
        m = manifest(rng.randrange(2**31))
        gad = max(0, min(21, round(rng.gauss(7, 5))))
        depression = max(0, min(27, round(.6*gad+rng.gauss(3, 3))))
        baseline = rng.gauss(600, 60)
        cost = rng.gauss(75+2*gad, 35)
        trials = []
        for r in m["switching"]:
            rt = max(150, rng.gauss(baseline+(cost if r["transition"] == "switch" and r["mixed"] else 0), 90))
            timeout = rt > 2000 or rng.random() < .01
            trials.append(dict(r, participant_id=pid, rt_ms=None if timeout else rt,
                               timeout=timeout, correct=not timeout and rng.random() < .94,
                               focus_lost=rng.random() < .01, technical_error=False))
        decisions = []
        for r in m["decisions"]:
            x = (-.03*gad+.15*r["ev_difference"]-.02*r["variance_difference"] if r["task"] == "risk"
                 else -.03*gad+.15*r["nominal_payoff_contrast"]-.5*r["ambiguity_width"])
            decisions.append(dict(r, participant_id=pid, target_chosen=rng.random() < logistic(x),
                                  focus_lost=False, technical_error=False))
        yield dict(data_origin="synthetic", participant_id=pid, protocol_version=m["protocol_version"],
                   stimulus_version=m["stimulus_version"], seed=m["seed"], task_order=m["task_order"],
                   comprehension_passed=True, gad7_total=gad, depression_total=depression, age_years=rng.randint(18, 70),
                   sleep_hours=round(max(2, min(12, rng.gauss(7, 1))), 1),
                   os_family="synthetic", browser_family="synthetic",
                   switching=trials, decisions=decisions, summary=summarize(trials))
