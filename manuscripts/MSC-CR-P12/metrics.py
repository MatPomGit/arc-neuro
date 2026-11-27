"""Secondary outcomes for trial records using the protocol data dictionary."""
from math import nan


def behavior_metrics(rows):
    """Return Brier, RAIR and RSR with explicit eligible-trial denominators."""
    squared_errors = []
    ai_adopted = []
    self_retained = []
    for row in rows:
        ai_correct = row["ai_option"] == row["correct_option"]
        if row["accepted"] is not None and row["confidence"] is not None:
            accurate = bool(int(row["accepted"])) == ai_correct
            squared_errors.append((float(row["confidence"]) - accurate) ** 2)
        if row["initial"] == row["ai_option"] or row["final"] is None:
            continue
        if ai_correct:
            ai_adopted.append(row["final"] == row["ai_option"])
        elif row["initial"] == row["correct_option"]:
            self_retained.append(row["final"] == row["initial"])
    values = dict(brier=squared_errors, rair=ai_adopted, rsr=self_retained)
    return {key: (sum(series) / len(series) if series else nan, len(series))
            for key, series in values.items()}
