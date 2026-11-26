"""Deterministic seed-sweep audit for the prospective stimulus reference."""
import argparse
import json
from design import switching, balance_metrics, balance_violations, STIMULUS_VERSION


def sweep(start, count):
    if type(start) is not int or type(count) is not int or start < 0 or count < 1:
        raise ValueError("invalid seed range")
    ranges = {}
    failures = []
    for seed in range(start, start + count):
        try:
            metrics = balance_metrics(switching(seed))
            errors = balance_violations(metrics)
            if errors:
                failures.append(dict(seed=seed, violations=errors))
            for condition, m in metrics.items():
                for field, value in m.items():
                    key = f"{condition}.{field}"
                    values = value if isinstance(value, list) else [value]
                    lo, hi = ranges.get(key, (min(values), max(values)))
                    ranges[key] = [min(lo, *values), max(hi, *values)]
        except RuntimeError as exc:
            failures.append(dict(seed=seed, error=str(exc)))
    return dict(stimulus_version=STIMULUS_VERSION, start=start, count=count,
                passed=count-len(failures), failures=failures, ranges=ranges)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=2048)
    args = parser.parse_args()
    report = sweep(args.start, args.count)
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(bool(report["failures"]))
