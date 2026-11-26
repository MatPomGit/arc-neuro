"""Prospective reference design, not an acquisition application."""
from collections import Counter
from itertools import product
from random import Random

VERSION = "0.4.0"
STIMULUS_VERSION = "0.4.1"
NUMBERS = (1, 2, 3, 4, 6, 7, 8, 9)


def category(rule, number):
    if rule not in (0, 1) or number not in NUMBERS:
        raise ValueError("invalid rule or stimulus")
    return number % 2 if rule == 0 else int(number > 5)


def _candidate(seed, attempt):
    rng = Random(seed if attempt == 0 else f'{seed}:{attempt}')
    mapping = [seed % 2, (seed // 2) % 2]
    rows = []
    first_rule = (seed // 4) % 2
    mixed_counts = Counter()
    repeat_plan = {}
    for change in (True, False):
        flags = [True] * 12 + [False] * 82
        rng.shuffle(flags)
        repeat_plan[change] = iter(flags)
    for block in range(6):
        mixed = block >= 2
        n = 48 if mixed else 24
        rule = rng.randrange(2) if mixed else (first_rule + block) % 2
        flags = ([True] * (24 if block % 2 == 0 else 23)
                 + [False] * (23 if block % 2 == 0 else 24)) if mixed else [False] * (n - 1)
        rng.shuffle(flags)
        prev = None
        counts = mixed_counts if mixed else Counter()
        for t in range(n):
            change = None if t == 0 else flags[t - 1]
            if change:
                rule = 1 - rule
            # Every mixed-block transition changes the cue, including repeat.
            cues = [2 * rule, 2 * rule + 1]
            if prev is not None and prev["cue"] in cues:
                cues.remove(prev["cue"])
            cue = rng.choice(cues)
            def strata(number):
                congruent = (category(0, number) ^ mapping[0]) == (category(1, number) ^ mapping[1])
                repeat = prev is not None and number == prev["stimulus"]
                response_repeat = prev is not None and (category(rule, number) ^ mapping[rule]) == prev["correct_key"]
                return [(change, "stimulus", number), (change, "congruence", congruent),
                        (change, "repeat", repeat), (change, "response_repeat", response_repeat),
                        (change, "rule", rule, "key", category(rule, number) ^ mapping[rule])]
            candidates = list(NUMBERS)
            rng.shuffle(candidates)
            if mixed and prev is not None:
                repeat_stimulus = next(repeat_plan[change])
                candidates = [x for x in candidates if (x == prev["stimulus"]) == repeat_stimulus]
            # Balance global marginal strata; the explicit repeat schedule has
            # exactly twelve identical-stimulus transitions in each condition.
            number = min(candidates, key=lambda x: sum(counts[k] for k in strata(x) if k[1] != "repeat"))
            counts.update(strata(number))
            row = dict(task="switching", block=block, trial_index=t, mixed=mixed,
                       rule=rule, cue=cue, stimulus=number, mapping=list(mapping),
                       transition="undefined" if change is None else "switch" if change else "repeat",
                       correct_key=category(rule, number) ^ mapping[rule])
            rows.append(row)
            prev = row
    return rows


def balance_metrics(rows):
    """Report mixed-block margins, excluding initial trials."""
    c = {k: Counter() for k in ("switch", "repeat")}
    for a, b in zip(rows, rows[1:]):
        if not b["mixed"] or a["block"] != b["block"]:
            continue
        d = c[b["transition"]]
        n, m = b["stimulus"], b["mapping"]
        d.update([("stimulus", n), ("rule", b["rule"]), ("key", b["correct_key"]),
                  ("cue", b["cue"]), ("congruence", (category(0, n) ^ m[0]) == (category(1, n) ^ m[1])),
                  ("stimulus_repeat", a["stimulus"] == n),
                  ("response_repeat", a["correct_key"] == b["correct_key"])])
    return {k: dict(n=sum(d["stimulus", n] for n in NUMBERS),
                    stimulus=[d["stimulus", n] for n in NUMBERS],
                    rule=[d["rule", n] for n in range(2)],
                    key=[d["key", n] for n in range(2)],
                    cue=[d["cue", n] for n in range(4)],
                    congruence=d["congruence", True],
                    stimulus_repeat=d["stimulus_repeat", True],
                    response_repeat=d["response_repeat", True])
            for k, d in c.items()}


def balance_violations(metrics):
    """Provisional engineering tolerances, not validated psychometric cutoffs."""
    errors = []
    for condition, m in metrics.items():
        if m["n"] != 94:
            errors.append(f"{condition}:n")
        if m["stimulus_repeat"] != 12:
            errors.append(f"{condition}:stimulus_repeat")
        for field, lo, hi in (("stimulus", 6, 18), ("rule", 35, 59),
                              ("key", 35, 59), ("cue", 10, 37)):
            if not all(lo <= n <= hi for n in m[field]):
                errors.append(f"{condition}:{field}")
        for field in ("congruence", "response_repeat"):
            if not 35 <= m[field] <= 59:
                errors.append(f"{condition}:{field}")
    a, b = metrics["switch"], metrics["repeat"]
    for field in ("congruence", "response_repeat"):
        if abs(a[field] - b[field]) > 8:
            errors.append(f"contrast:{field}")
    for field, limit in (("stimulus", 6), ("rule", 8), ("key", 8), ("cue", 12)):
        if any(abs(x-y) > limit for x,y in zip(a[field], b[field])):
            errors.append(f"contrast:{field}")
    return errors


def switching(seed):
    if type(seed) is not int or seed < 0:
        raise ValueError("seed must be a nonnegative integer")
    for attempt in range(128):
        rows = _candidate(seed, attempt)
        if not balance_violations(balance_metrics(rows)):
            return rows
    raise RuntimeError(f"No valid switching schedule for seed {seed} within 128 attempts")


def decision_trials(seed):
    rng = Random(seed)
    rows = []
    for task in ("risk", "ambiguity"):
        block = []
        for delta, level, rep in product((-2, 0, 2), range(4), range(4)):
            side = "left" if rep % 2 == 0 else "right"
            row = dict(task=task, block=0, target_side=side, contrast=delta, level=level)
            if task == "risk":
                spread = level + 3
                row.update(reference_outcomes=[10, 14], target_outcomes=[12+delta-spread, 12+delta+spread],
                           reference_p=.5, target_p=.5, ev_difference=delta,
                           variance_difference=spread**2 - 4)
            else:
                halfwidth = (1 + level) / 10
                row.update(reference_outcomes=[8, 16], target_outcomes=[8+delta, 16+delta],
                           reference_p=.5, target_p=None,
                           ambiguity_bounds=[round(.5-halfwidth, 2), round(.5+halfwidth, 2)],
                           nominal_payoff_contrast=delta, ambiguity_width=round(2*halfwidth, 2))
            block.append(row)
        rng.shuffle(block)
        for t, row in enumerate(block):
            rows.append(dict(row, trial_index=t))
    return rows


def manifest(seed):
    if type(seed) is not int or seed < 0:
        raise ValueError("seed must be a nonnegative integer")
    tasks = ["switching", "decision"] if (seed // 8) % 2 == 0 else ["decision", "switching"]
    return dict(protocol_version=VERSION, stimulus_version=STIMULUS_VERSION, seed=seed,
                task_order=tasks, switching=switching(seed), decisions=decision_trials(seed))
