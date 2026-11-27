"""Build and fit the prespecified crossed-effects probit model in Python."""
import argparse
import csv
from pathlib import Path

import numpy as np


DOMAINS = ("mobilnosc", "ekologia", "wyposazenie")
WAVES = ("T0", "T1", "T2")
ARMS = ("control", "training")


def encode(rows):
    subjects = sorted({row["participant_id"] for row in rows})
    scenarios = sorted({row["item_id"] for row in rows})
    person_index = {key: index for index, key in enumerate(subjects)}
    item_index = {key: index for index, key in enumerate(scenarios)}
    columns = {
        "arm": [ARMS.index(row["arm"]) for row in rows],
        "wave": [WAVES.index(row["phase"]) for row in rows],
        "domain": [DOMAINS.index(row["domain"]) for row in rows],
        "form": [int(row["form"]) for row in rows],
        "person": [person_index[row["participant_id"]] for row in rows],
        "item": [item_index[row["item_id"]] for row in rows],
        "signal": [0.5 if row["correct_option"] != row["ai_option"] else -0.5 for row in rows],
        "knowledge": [float(row["knowledge_score"]) - 2 for row in rows],
        "reject": [1 - int(row["accepted"]) for row in rows],
    }
    return {key: np.asarray(value) for key, value in columns.items()}, subjects, scenarios


def primary_contrast(sensitivity):
    """Average the two far-domain differences in change on the probit scale."""
    return (
        sensitivity[1, 2, 1:] - sensitivity[1, 0, 1:]
        - sensitivity[0, 2, 1:] + sensitivity[0, 0, 1:]
    ).mean()


def build_model(rows):
    import pymc as pm

    data, subjects, scenarios = encode(rows)
    coords = dict(arm=ARMS, wave=WAVES, domain=DOMAINS, person=subjects,
                  item=scenarios, component=("criterion", "sensitivity"), form=("A", "B", "C"))
    with pm.Model(coords=coords) as model:
        dimensions = ("arm", "wave", "domain")
        intercept = pm.Normal("intercept", 0, 1.25, dims=dimensions)
        sensitivity = pm.Normal("sensitivity", 0, 1.5, dims=dimensions)
        knowledge = pm.Normal("knowledge", 0, 0.5, dims=("domain", "component"))
        form_raw = pm.Normal("form_raw", 0, 0.4, dims=("form", "component"))
        form = form_raw - form_raw.mean(axis=0)
        varying = {}
        for name in ("person", "item"):
            scale = pm.HalfNormal(f"{name}_sd", 0.65, dims="component")
            z = pm.Normal(f"{name}_z", 0, 1, dims=(name, "component"))
            varying[name] = z[data[name], :] * scale
        cell = data["arm"], data["wave"], data["domain"]
        shifts = (varying["person"] + varying["item"] + form[data["form"]]
                  + knowledge[data["domain"]] * data["knowledge"][:, None])
        eta = intercept[cell] + shifts[:, 0] + data["signal"] * (sensitivity[cell] + shifts[:, 1])
        from pytensor.tensor import erfc
        pm.Bernoulli("rejected", p=0.5 * erfc(-eta / np.sqrt(2)), observed=data["reject"])
        pm.Deterministic("primary_delta", primary_contrast(sensitivity))
    return model


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--seed", type=int, default=27112026)
    args = parser.parse_args()
    with args.input.open(encoding="utf-8", newline="") as source:
        rows = [row for row in csv.DictReader(source)
                if row["phase"] in WAVES and row["accepted"] in {"0", "1"}
                and row.get("window_status") != "outside"]
    if not rows:
        parser.error("no valid test trials")
    import pymc as pm

    with build_model(rows):
        trace = pm.sample(draws=2000, tune=2000, chains=4, cores=2,
                          target_accept=0.95, random_seed=args.seed)
    trace.to_netcdf(args.output)


if __name__ == "__main__":
    main()
