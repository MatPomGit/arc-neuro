"""Prospective reference design, not an acquisition application."""
from collections import Counter
from itertools import product
from random import Random

VERSION = "0.4.0"
NUMBERS = (1, 2, 3, 4, 6, 7, 8, 9)


def category(rule, number):
    if rule not in (0, 1) or number not in NUMBERS:
        raise ValueError("invalid rule or stimulus")
    return number % 2 if rule == 0 else int(number > 5)


def switching(seed):
    rng = Random(seed)
    mapping = [seed % 2, (seed // 2) % 2]
    rows = []
    first_rule = (seed // 4) % 2
    for block in range(6):
        mixed = block >= 2
        n = 48 if mixed else 24
        rule = rng.randrange(2) if mixed else (first_rule + block) % 2
        flags = ([True] * (24 if block % 2 == 0 else 23)
                 + [False] * (23 if block % 2 == 0 else 24)) if mixed else [False] * (n - 1)
        rng.shuffle(flags)
        prev = None
        counts = Counter()
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
            # Balance marginal strata greedily, not a proof of factorial balance.
            number = min(candidates, key=lambda x: sum(counts[k] for k in strata(x) if k[1] != "repeat")
                         + (4 if prev and x == prev["stimulus"] and counts[(change, "repeat", True)] >=
                            max(1, counts[(change, "repeat", False)] // 7) else 0))
            counts.update(strata(number))
            row = dict(task="switching", block=block, trial_index=t, mixed=mixed,
                       rule=rule, cue=cue, stimulus=number, mapping=list(mapping),
                       transition="undefined" if change is None else "switch" if change else "repeat",
                       correct_key=category(rule, number) ^ mapping[rule])
            rows.append(row)
            prev = row
    return rows


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
    return dict(protocol_version=VERSION, stimulus_version=VERSION, seed=seed,
                task_order=tasks, switching=switching(seed), decisions=decision_trials(seed))
