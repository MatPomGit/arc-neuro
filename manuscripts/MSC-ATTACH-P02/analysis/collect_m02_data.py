# SPDX-License-Identifier: Apache-2.0
# ARC Neuro migration: repository-relative paths; generated outputs under ignored build/.
"""Resumable, integrity-checked collection of M02 *development* simulation data.

Default is a dry run. A completed shard is immutable and is rechecked via
SHA-256 on resume. No exploratory run can be relabelled confirmatory here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG = Path(__file__).resolve().parent / "configs/m02_standardized_development.json"
DEFAULT_OUTPUT = ROOT / "build/MSC-ATTACH-P02/m02-collection"
SIMULATOR = Path(__file__).with_name("controller_identifiability_suite.py")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_atomic(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                     prefix=".tmp-", delete=False) as f:
        f.write(data)
        tmp = Path(f.name)
    os.replace(tmp, path)


def manifest_paths(shard: Path) -> dict[str, str]:
    return {p.name: digest(p) for p in sorted(shard.iterdir())
            if p.is_file() and p.name != "collection_manifest.json"}


def validate_completed(shard: Path, identity: dict) -> None:
    meta = shard / "collection_manifest.json"
    if not meta.is_file():
        raise RuntimeError(f"Partial shard requires manual inspection: {shard}")
    record = json.loads(meta.read_text(encoding="utf-8"))
    if record["identity"] != identity or record["files"] != manifest_paths(shard):
        raise RuntimeError(f"Shard identity/checksum mismatch: {shard}")
    if not {"trajectories.jsonl", "summary.csv", "metadata.json", "config.json"}.issubset(record["files"]):
        raise RuntimeError(f"Missing mandatory shard outputs: {shard}")


def git_commit() -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                            capture_output=True, text=True, check=True)
    return result.stdout.strip()


def collect(config: Path, output: Path, chunk: int, execute: bool,
            max_shards: int | None = None) -> dict:
    if chunk < 2 or (max_shards is not None and max_shards < 1):
        raise ValueError("chunk >= 2 and max_shards >= 1 required")
    spec = json.loads(config.read_text(encoding="utf-8"))
    if spec.get("evidence_status") != "development_only":
        raise ValueError("Only development_only configs are accepted")
    if not isinstance(spec.get("seed"), int) or not isinstance(spec.get("replications"), int):
        raise ValueError("Integer base seed and replications required")
    if spec["replications"] < 2:
        raise ValueError("At least two replicates required")
    if output.resolve() == ROOT.resolve() or output.resolve() == config.parent.resolve():
        raise ValueError("Unsafe output directory")
    source = git_commit()
    config_hash = digest(config)
    collection_id = hashlib.sha256((config_hash + ":" + source).encode()).hexdigest()[:20]
    base = output / collection_id
    tasks = []
    for ci, condition in enumerate(spec["conditions"]):
        for gi, generator in enumerate(spec["generators"]):
            for start in range(0, spec["replications"], chunk):
                count = min(chunk, spec["replications"] - start)
                # One-replicate tails are merged into the preceding chunk.
                if count == 1 and tasks and tasks[-1]["ci"] == ci and tasks[-1]["gi"] == gi:
                    tasks[-1]["count"] += 1
                    continue
                tasks.append({"ci": ci, "gi": gi, "start": start, "count": count,
                              "condition": condition, "generator": generator})
    # A one-replicate final tail is included in a previous shard for each cell.
    # The chunk offset is incorporated into the seed, preserving distinct draws.
    overview = {"collection_id": collection_id, "evidence_status": "development_only",
                "source_commit": source, "config_sha256": config_hash,
                "configured_attempts": len(spec["conditions"]) * len(spec["generators"]) * spec["replications"],
                "shards_total": len(tasks), "executed": 0, "reused": 0,
                "planned": 0, "shards": []}
    for i, task in enumerate(tasks):
        if max_shards is not None and i >= max_shards:
            break
        name = f"c{task['ci']:03d}-g{task['gi']:02d}-r{task['start']:07d}"
        shard = base / name
        identity = {"source_commit": source, "original_config_sha256": config_hash,
                    "condition": task["condition"]["id"], "generator": task["generator"],
                    "replicate_start": task["start"], "replicate_count": task["count"]}
        if shard.exists():
            validate_completed(shard, identity)
            overview["reused"] += 1
            state = "verified_reused"
        elif execute:
            shard.mkdir(parents=True, exist_ok=False)
            local = dict(spec)
            local["conditions"] = [task["condition"]]
            local["generators"] = [task["generator"]]
            local["replications"] = task["count"]
            local["seed"] = spec["seed"] + task["start"]
            local["evidence_id"] = f"{spec.get('evidence_id', 'M02-DEV')}-{name}"
            shard_config = shard / "input_spec.json"
            write_atomic(shard_config, json.dumps(local, indent=2) + "\n")
            try:
                subprocess.run([sys.executable, str(SIMULATOR), "--config",
                                str(shard_config), "--output", str(shard),
                                "--source-commit", source], check=True, cwd=ROOT)
                files = manifest_paths(shard)
                if not {"trajectories.jsonl", "summary.csv", "metadata.json", "config.json"}.issubset(files):
                    raise RuntimeError("Incomplete simulator outputs")
                write_atomic(shard / "collection_manifest.json",
                             json.dumps({"identity": identity, "files": files,
                                         "completed_utc": datetime.now(timezone.utc).isoformat()},
                                        indent=2) + "\n")
            except Exception:
                # Fail closed; an incomplete shard will never be silently reused.
                raise
            overview["executed"] += 1
            state = "collected"
        else:
            overview["planned"] += 1
            state = "planned"
        overview["shards"].append({"name": name, "state": state,
                                   "replicate_count": task["count"]})
        if execute:
            write_atomic(base / "collection_index.json",
                         json.dumps(overview, indent=2) + "\n")
    return overview


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path,
                   default=DEFAULT_CONFIG)
    p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--chunk-size", type=int, default=10)
    p.add_argument("--execute", action="store_true", help="Actually run development simulations")
    p.add_argument("--max-shards", type=int)
    args = p.parse_args()
    result = collect(args.config.resolve(), args.output.resolve(), args.chunk_size,
                     args.execute, args.max_shards)
    print(json.dumps({k: v for k, v in result.items() if k != "shards"}, indent=2))


if __name__ == "__main__":
    main()
