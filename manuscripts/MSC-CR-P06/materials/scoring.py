"""Reference scorer for the public P06 pilot bank; no empirical data."""
from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean

CATEGORIES = ("U", "S", "N")
BANK_PATH = Path(__file__).with_name("pilot-bank.json")


def load_bank(path=BANK_PATH):
    """Read and validate the versioned, public pilot bank."""
    bank = json.loads(Path(path).read_text(encoding="utf-8"))
    if bank.get("schema_version") != 1:
        raise ValueError("Unsupported bank schema")
    forms = {}
    for form in bank["forms"]:
        fid = form["form"]
        if fid in forms:
            raise ValueError("Duplicate form")
        items = {}
        for item in form["items"]:
            iid = item["id"]
            if iid in items or item["key"] not in CATEGORIES:
                raise ValueError("Invalid item ID or key")
            if type(item["justify"]) is not bool:
                raise ValueError("Invalid justification flag")
            items[iid] = item
        if len(items) != 24 or sum(i["justify"] for i in items.values()) != 6:
            raise ValueError("Unexpected form structure")
        if any(sum(i["key"] == key for i in items.values()) != 8 for key in CATEGORIES):
            raise ValueError("Unbalanced answer key")
        forms[fid] = items
    if set(forms) != {"A", "B", "C"}:
        raise ValueError("Unexpected forms")
    if len({iid for f in forms.values() for iid in f}) != 72:
        raise ValueError("Item IDs must be globally unique")
    return forms


def score_form(items, rows):
    """Score one participant/time/form. Rows may omit unanswered items.

    Required row field: item_id. Optional fields: response (U/S/N or None),
    confidence (finite 0..100 or None), justification_score (0/1/2 or None,
    adjudicated human rating, not automated text assessment).
    All missing outcomes are returned as None, never as zero.
    """
    seen = set()
    accuracy, paired, ratings = [], [], []
    matrix = {k: {r: 0 for r in CATEGORIES} for k in CATEGORIES}
    missing_by_key = dict.fromkeys(CATEGORIES, 0)
    for row in rows:
        iid = row["item_id"]
        if iid not in items or iid in seen:
            raise ValueError(f"Unknown or duplicate item: {iid}")
        seen.add(iid)
        item = items[iid]
        key = item["key"]
        response = row.get("response")
        confidence = row.get("confidence")
        rating = row.get("justification_score")
        if response is not None and response not in CATEGORIES:
            raise ValueError("Invalid response category")
        if confidence is not None:
            if (type(confidence) not in (int, float) or
                    not math.isfinite(confidence) or not 0 <= confidence <= 100):
                raise ValueError("Invalid confidence")
            if response is None:
                raise ValueError("Confidence without a response")
        if rating is not None:
            if not item["justify"] or type(rating) is not int or rating not in (0, 1, 2):
                raise ValueError("Invalid human justification rating")
            ratings.append(rating)
        if response is None:
            missing_by_key[key] += 1
            continue
        correct = int(response == key)
        accuracy.append(correct)
        matrix[key][response] += 1
        if confidence is not None:
            paired.append((confidence / 100, correct))
    for iid, item in items.items():
        if iid not in seen:
            missing_by_key[item["key"]] += 1
    n, p, j = len(accuracy), len(paired), len(ratings)
    return {
        "n_answered": n,
        "n_confidence_pairs": p,
        "n_justifications_rated": j,
        "accuracy": mean(accuracy) if n >= 20 else None,
        "brier": mean((c-y)**2 for c, y in paired) if p >= 20 else None,
        "confidence_bias": mean(c-y for c, y in paired) if p >= 20 else None,
        "mean_confidence_paired": mean(c for c, y in paired) if p >= 20 else None,
        "accuracy_paired": mean(y for c, y in paired) if p >= 20 else None,
        "justification_mean": mean(ratings) if j >= 5 else None,
        "confusion": matrix,
        "missing_by_key": missing_by_key,
    }


def quadratic_kappa(pairs):
    """Quadratically weighted Cohen kappa on complete paired human ratings.

    None denotes missing; returns None for zero pairs or zero expected
    disagreement. Does not estimate a confidence interval; clustered
    resampling by participant is a separate planned analysis.
    """
    table = [[0]*3 for _ in range(3)]
    for a, b in pairs:
        for value in (a, b):
            if value is not None and (type(value) is not int or value not in (0, 1, 2)):
                raise ValueError("Invalid rater score")
        if a is not None and b is not None:
            table[a][b] += 1
    n = sum(map(sum, table))
    if not n:
        return None
    marg_a = list(map(sum, table))
    marg_b = [sum(table[a][b] for a in range(3)) for b in range(3)]
    observed = sum((a-b)**2 * table[a][b] for a in range(3) for b in range(3)) / n
    expected = sum((a-b)**2 * marg_a[a] * marg_b[b] for a in range(3) for b in range(3)) / n**2
    return 1 - observed/expected if expected else None
