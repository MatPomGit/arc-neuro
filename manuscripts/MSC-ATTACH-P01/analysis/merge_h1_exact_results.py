"""Strict streaming merge for deterministic ARC H1 Monte Carlo chunks.

The merge path intentionally uses only the Python standard library. In
particular it does not import pandas/NumPy. This is important on Windows:
thousands of repeated pandas.read_csv calls previously exposed intermittent
native-stack corruption after otherwise successful Monte Carlo computation.

The merger validates:
- non-empty inputs;
- a consistent CSV schema;
- one row per scenario/replication key;
- exact replication coverage 0..N-1 when requested.

Rows are streamed directly to the merged CSV, so the 120,000-replication
full design does not need to be materialized as a pandas DataFrame.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

KEYS = (
    "couples",
    "compliance_target",
    "missingness_strength",
    "truth",
    "replication",
)
SCENARIO_KEYS = KEYS[:-1]
SUMMARY_KEYS = (
    "couples",
    "people",
    "compliance_target",
    "missingness_strength",
    "truth",
)


def json_scalar(value: object) -> object:
    """Convert NumPy-like scalar objects to JSON-native Python scalars."""

    item = getattr(value, "item", None)
    if callable(item):
        try:
            return item()
        except (ValueError, TypeError):
            pass
    return value


def _iter_records(data: object) -> Iterable[Mapping[str, Any]]:
    """Yield mappings from ordinary iterables or small DataFrame-like tests."""

    if hasattr(data, "to_dict"):
        # Compatibility for unit tests and callers passing a DataFrame.
        # Production merge never takes this branch.
        records = data.to_dict(orient="records")  # type: ignore[attr-defined]
        yield from records
        return
    yield from data  # type: ignore[misc]


def _parse_int(value: object, name: str) -> int:
    try:
        return int(float(str(value)))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid integer {name}={value!r}") from exc


def _parse_float(value: object, name: str) -> float:
    try:
        result = float(str(value))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid float {name}={value!r}") from exc
    if not math.isfinite(result):
        raise ValueError(f"non-finite merge key {name}={value!r}")
    return result


def replication_key(row: Mapping[str, Any]) -> tuple[int, float, float, str, int]:
    """Return the canonical merge key."""

    return (
        _parse_int(row["couples"], "couples"),
        _parse_float(row["compliance_target"], "compliance_target"),
        _parse_float(row["missingness_strength"], "missingness_strength"),
        str(row["truth"]),
        _parse_int(row["replication"], "replication"),
    )


def scenario_key(row: Mapping[str, Any]) -> tuple[int, float, float, str]:
    """Return the canonical scenario key."""

    key = replication_key(row)
    return key[:-1]


def validate_unique_replications(data: object) -> None:
    """Require one row per scenario and absolute replication index."""

    seen: set[tuple[int, float, float, str, int]] = set()
    examples: list[tuple[int, float, float, str, int]] = []
    for row in _iter_records(data):
        key = replication_key(row)
        if key in seen and len(examples) < 20:
            examples.append(key)
        seen.add(key)
    if examples:
        raise ValueError(
            "overlapping Monte Carlo replication keys detected; "
            f"examples: {examples}"
        )


def validate_expected_replications(
    data: object,
    expected: int | None,
) -> list[dict[str, object]]:
    """Return per-scenario coverage and optionally require exact 0..N-1."""

    scenario_reps: dict[
        tuple[int, float, float, str],
        list[int],
    ] = defaultdict(list)
    for row in _iter_records(data):
        key = replication_key(row)
        scenario_reps[key[:-1]].append(key[-1])
    return coverage_from_replications(scenario_reps, expected)


def coverage_from_replications(
    scenario_reps: Mapping[
        tuple[int, float, float, str],
        Iterable[int],
    ],
    expected: int | None,
) -> list[dict[str, object]]:
    """Build strict scenario coverage records."""

    coverage: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []
    expected_set = set(range(expected)) if expected is not None else None

    for scenario in sorted(scenario_reps):
        replications = sorted(int(value) for value in scenario_reps[scenario])
        if not replications:
            continue
        unique = set(replications)
        row: dict[str, object] = {
            key: value
            for key, value in zip(SCENARIO_KEYS, scenario, strict=True)
        }
        row.update(
            {
                "rows": len(replications),
                "min_replication": min(replications),
                "max_replication": max(replications),
                "unique_replications": len(unique),
            }
        )
        if expected_set is not None:
            missing = sorted(expected_set - unique)
            unexpected = sorted(value for value in unique if value >= expected)
            row["expected_replications"] = expected
            row["missing_count"] = len(missing)
            row["unexpected_count"] = len(unexpected)
            if missing:
                row["first_missing"] = missing[:20]
            if unexpected:
                row["first_unexpected"] = unexpected[:20]
            if (
                len(replications) != expected
                or len(unique) != expected
                or missing
                or unexpected
            ):
                failures.append(row)
        coverage.append(row)

    if failures:
        raise ValueError(
            "Monte Carlo scenario coverage is incomplete, duplicated, "
            "or out of range; first failures: "
            f"{failures[:5]}"
        )
    return coverage


def _numeric_value(value: object) -> float | None:
    """Parse one CSV scalar for summary averaging."""

    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"nan", "na", "none", "null"}:
        return None
    if text.lower() == "true":
        return 1.0
    if text.lower() == "false":
        return 0.0
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


class ScenarioSummary:
    """Streaming accumulator matching the historical scenario summary."""

    def __init__(self, row: Mapping[str, Any]) -> None:
        self.key_values: dict[str, Any] = {
            "couples": _parse_int(row["couples"], "couples"),
            "people": _parse_int(row["people"], "people"),
            "compliance_target": _parse_float(
                row["compliance_target"], "compliance_target"
            ),
            "missingness_strength": _parse_float(
                row["missingness_strength"], "missingness_strength"
            ),
            "truth": str(row["truth"]),
        }
        self.replications = 0
        self.sums: dict[str, float] = defaultdict(float)
        self.counts: dict[str, int] = defaultdict(int)
        self.representation_counts: dict[str, Counter[str]] = defaultdict(Counter)

    def add(self, row: Mapping[str, Any]) -> None:
        self.replications += 1
        for column, raw in row.items():
            if column in SUMMARY_KEYS:
                continue
            if column.startswith("representation_margin_"):
                label = str(raw).strip() or "nan"
                self.representation_counts[column][label] += 1
            number = _numeric_value(raw)
            if number is not None:
                self.sums[column] += number
                self.counts[column] += 1

    def finish(self) -> dict[str, Any]:
        result = dict(self.key_values)
        result["replications"] = self.replications
        for column in sorted(self.sums):
            count = self.counts[column]
            if count:
                result[f"mean_{column}"] = self.sums[column] / count
        for column in sorted(self.representation_counts):
            counts = self.representation_counts[column]
            total = sum(counts.values())
            if total:
                for label, count in counts.items():
                    result[f"p_{column}_{label}"] = count / total
        return result


def _summary_key(row: Mapping[str, Any]) -> tuple[int, int, float, float, str]:
    return (
        _parse_int(row["couples"], "couples"),
        _parse_int(row["people"], "people"),
        _parse_float(row["compliance_target"], "compliance_target"),
        _parse_float(row["missingness_strength"], "missingness_strength"),
        str(row["truth"]),
    )


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write compact rows using the union of observed fields."""

    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def merge_files(
    paths: list[Path],
    output_dir: Path,
    expected_replications: int | None,
) -> dict[str, Any]:
    """Stream input CSVs into one strict merged result without pandas."""

    if not paths:
        raise ValueError("no Monte Carlo inputs supplied")

    output_dir.mkdir(parents=True, exist_ok=True)
    merged_path = output_dir / "h1_exact_replications.csv"

    # First pass: inspect headers only. Individual one-replication files may
    # legitimately omit optional columns, so reproduce pandas' historical
    # union-of-columns behavior without importing pandas.
    field_union: set[str] = set()
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
        if path.stat().st_size <= 0:
            raise ValueError(f"empty Monte Carlo result file: {path}")
        with path.open("r", newline="", encoding="utf-8-sig") as handle:
            reader = csv.reader(handle)
            try:
                fields = next(reader)
            except StopIteration as exc:
                raise ValueError(f"missing CSV header: {path}") from exc
        missing = set(KEYS) - set(fields)
        if missing:
            raise ValueError(
                f"{path} missing merge keys: {sorted(missing)}"
            )
        if "people" not in fields:
            raise ValueError(f"{path} missing summary key: people")
        field_union.update(fields)

    canonical_fields = sorted(field_union)
    seen: set[tuple[int, float, float, str, int]] = set()
    scenario_reps: dict[
        tuple[int, float, float, str],
        list[int],
    ] = defaultdict(list)
    summaries: dict[
        tuple[int, int, float, float, str],
        ScenarioSummary,
    ] = {}
    input_rows = 0

    with merged_path.open("w", newline="", encoding="utf-8") as merged_handle:
        writer = csv.DictWriter(
            merged_handle,
            fieldnames=canonical_fields,
            extrasaction="raise",
        )
        writer.writeheader()

        for path in paths:
            with path.open("r", newline="", encoding="utf-8-sig") as handle:
                reader = csv.DictReader(handle)
                file_rows = 0
                for row in reader:
                    file_rows += 1
                    input_rows += 1
                    key = replication_key(row)
                    if key in seen:
                        raise ValueError(
                            "overlapping Monte Carlo replication key detected: "
                            f"{key} from {path}"
                        )
                    seen.add(key)
                    scenario_reps[key[:-1]].append(key[-1])

                    skey = _summary_key(row)
                    accumulator = summaries.get(skey)
                    if accumulator is None:
                        accumulator = ScenarioSummary(row)
                        summaries[skey] = accumulator
                    accumulator.add(row)

                    writer.writerow(row)

                if file_rows == 0:
                    raise ValueError(f"empty Monte Carlo result file: {path}")

    coverage = coverage_from_replications(
        scenario_reps,
        expected_replications,
    )
    summary_rows = [
        summaries[key].finish()
        for key in sorted(summaries)
    ]
    write_rows(
        output_dir / "h1_exact_summary.csv",
        summary_rows,
    )

    manifest = {
        "merge_engine": "python_stdlib_streaming_csv",
        "pandas_used_for_merge": False,
        "input_files": [str(path) for path in paths],
        "input_rows": input_rows,
        "scenario_count": len(coverage),
        "expected_replications": expected_replications,
        "coverage": coverage,
    }
    (
        output_dir / "h1_exact_merge_manifest.json"
    ).write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--inputs",
        type=Path,
        nargs="+",
        help="Replication CSV chunks.",
    )
    source.add_argument(
        "--input-list",
        type=Path,
        help="UTF-8 text file containing one replication CSV path per line.",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--expected-replications",
        type=int,
        default=None,
        help="Require exact replication IDs 0..N-1 in every scenario.",
    )
    args = parser.parse_args()

    if args.input_list is not None:
        paths = [
            Path(line.strip())
            for line in args.input_list.read_text(
                encoding="utf-8-sig"
            ).splitlines()
            if line.strip()
        ]
        if not paths:
            raise ValueError(f"input list is empty: {args.input_list}")
    else:
        paths = list(args.inputs)

    manifest = merge_files(
        paths,
        args.output_dir,
        args.expected_replications,
    )
    print(f"Merged rows: {manifest['input_rows']}")
    print(f"Scenarios: {manifest['scenario_count']}")
    print("Merge engine: Python stdlib streaming CSV (pandas-free)")


if __name__ == "__main__":
    main()
