# SPDX-License-Identifier: Apache-2.0
# Modified in ARC Neuro: resolve the migrated protocol configuration locally.
"""Generate a small deterministic SYNTHETIC CA export for integration checks.

This fixture tests export handling, not psychological effects or study power.
"""

import argparse
import csv
import json
from pathlib import Path

from analysis import SCHEMAS


def fixture(config: dict) -> dict:
    """Create one synthetic person with a complete, unanswered schedule."""
    version = config["instrument_version"]
    tables = {name: [] for name in SCHEMAS}
    tables["participants"].append(dict(
        participant_code="SYNTHETIC_001", instrument_version=version,
        schedule_started="true", start_offset="0", withdrawal_offset="",
        completion_status="completed",
    ))
    for day in range(1, config["esm"]["days"] + 1):
        for prompt in range(1, config["esm"]["prompts_per_day"] + 1):
            time = (day - 1) * 86400 + (prompt - 1) * 7200
            tables["prompts"].append(dict(
                participant_code="SYNTHETIC_001", day=str(day),
                prompt=str(prompt), planned_offset_s=str(time),
                enabled_before_withdrawal="true", delivery_status="unknown",
                delivered_offset_s="",
            ))
    return tables


def add_attempt(tables: dict, config: dict, sid: str, prompt: int = 2,
                day: int = 1, delay: int = 60, value: int = 50,
                reason: str = "submitted") -> None:
    """Add a synthetic attempt with explicit structural missing records."""
    planned = (day - 1) * 86400 + (prompt - 1) * 7200
    closed = planned + delay
    tables["submissions"].append(dict(
        submission_id=sid, participant_code="SYNTHETIC_001", day=str(day),
        prompt=str(prompt), opened_offset_s=str(planned + 5),
        submitted_offset_s=str(closed) if reason == "submitted" else "",
        closed_offset_s=str(closed), end_reason=reason,
        instrument_version=config["instrument_version"], help_open_count="0",
    ))
    for name in config["current_items"] + config["interval_items"]:
        structural = prompt == 1 and name in config["interval_items"]
        tables["items"].append(dict(
            submission_id=sid, item_id=name,
            displayed="false" if structural else "true",
            value="" if structural else str(1 if name == "K_contact"
                                             else value),
            response_status="structural" if structural else "answered",
            displayed_offset_s="" if structural else str(planned + 10),
            answered_offset_s="" if structural else str(planned + 20),
        ))


def write_export(tables: dict, folder: Path) -> None:
    """Create a new explicitly synthetic export without overwriting files."""
    folder.mkdir(parents=True, exist_ok=False)
    for name, columns in SCHEMAS.items():
        with (folder / f"{name}.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=columns)
            writer.writeheader()
            writer.writerows(tables[name])
    (folder / "SYNTHETIC.txt").write_text(
        "SYNTHETIC software fixture. No human participants or findings.\n",
        encoding="utf-8",
    )


def main() -> None:
    """Write a reproducible mix of valid, duplicate and late attempts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--config", type=Path,
        default=Path(__file__).resolve().parents[1] / "protocol/design_config.json",
    )
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    tables = fixture(config)
    add_attempt(tables, config, "SYNTHETIC_FIRST", prompt=1, value=100)
    add_attempt(tables, config, "SYNTHETIC_VALID", value=0)
    add_attempt(tables, config, "SYNTHETIC_DUPLICATE", delay=120, value=100)
    add_attempt(tables, config, "SYNTHETIC_LATE", prompt=3, delay=1300)
    add_attempt(tables, config, "SYNTHETIC_ABANDONED", prompt=4,
                reason="abandoned")
    write_export(tables, args.output)
    print("SYNTHETIC export created; not human study data.")


if __name__ == "__main__":
    main()
