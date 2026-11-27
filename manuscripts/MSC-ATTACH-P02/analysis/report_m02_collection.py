# SPDX-License-Identifier: Apache-2.0
# ARC Neuro migration: share the collector's default output location.
"""Validate M02 development shard manifests and create a descriptive progress report."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from collect_m02_data import DEFAULT_OUTPUT, manifest_paths


def summarize(collection: Path) -> dict:
    index_path = collection / "collection_index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if index.get("evidence_status") != "development_only":
        raise ValueError("Only development data may be summarized")
    shards = sorted(p for p in collection.iterdir() if p.is_dir())
    expected = index["shards_total"]
    completed_attempts = 0
    failures = 0
    nominal_correct = 0
    paired_available = 0
    for shard in shards:
        manifest = json.loads((shard / "collection_manifest.json").read_text(encoding="utf-8"))
        if manifest["files"] != manifest_paths(shard):
            raise RuntimeError(f"Integrity failure: {shard}")
        identity = manifest["identity"]
        lines = (shard / "trajectories.jsonl").read_text(encoding="utf-8").splitlines()
        if len(lines) != identity["replicate_count"]:
            raise RuntimeError(f"Replicate count mismatch: {shard}")
        for line in lines:
            record = json.loads(line)
            if record["generator"] != identity["generator"] or record["condition"] != identity["condition"]:
                raise RuntimeError(f"Row identity mismatch: {shard}")
            completed_attempts += 1
            failures += record["selected"] is None
            nominal_correct += record["selected"] == record["generator"]
            paired_available += record["paired_delta"] is not None
    if len(shards) > expected or completed_attempts > index["configured_attempts"]:
        raise RuntimeError("Collection contains more data than configured")
    return {
        "status": "development_only_descriptive_not_confirmatory",
        "collection_id": index["collection_id"],
        "source_commit": index["source_commit"],
        "shards_completed": len(shards),
        "shards_expected": expected,
        "attempts_completed": completed_attempts,
        "attempts_expected": index["configured_attempts"],
        "selection_failures": failures,
        "nominal_correct": nominal_correct,
        "nominal_recovery_descriptive": (nominal_correct / completed_attempts
                                          if completed_attempts else None),
        "paired_evaluable": paired_available,
        "complete": len(shards) == expected and completed_attempts == index["configured_attempts"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    root = args.output.resolve()
    collections = [p for p in root.iterdir()
                   if p.is_dir() and (p / "collection_index.json").exists()]
    if not collections:
        raise SystemExit("No completed M02 shard indexes found")
    for collection in sorted(collections):
        report = summarize(collection)
        path = collection / "COLLECTION_REPORT.md"
        content = ("# M02 collection report\n\n"
                   "**Development-only descriptive status. Not confirmatory evidence.**\n\n"
                   f"- Collection: `{report['collection_id']}`\n"
                   f"- Source commit: `{report['source_commit']}`\n"
                   f"- Shards: {report['shards_completed']}/{report['shards_expected']}\n"
                   f"- Attempted triads: {report['attempts_completed']}/{report['attempts_expected']}\n"
                   f"- Selection failures: {report['selection_failures']}\n"
                   f"- Nominal recovery: {report['nominal_correct']} / {report['attempts_completed']}\n"
                   f"- Paired-evaluable: {report['paired_evaluable']}\n"
                   f"- Complete: {report['complete']}\n\n"
                   "These pooled descriptive counts do not adjust for paired experimental "
                   "conditions, multiplicity or selection. No hypothesis test is implied.\n")
        path.write_text(content, encoding="utf-8")
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
