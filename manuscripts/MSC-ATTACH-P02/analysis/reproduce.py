# SPDX-License-Identifier: Apache-2.0
"""Reproduce configured ARC simulation outputs and write provenance metadata."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess

from arc_model import MODEL_VERSION
from experiments import run_config


HERE = Path(__file__).resolve().parent
DEFAULT_CONFIGS = [
    HERE / "configs" / "phase_map.json",
    HERE / "configs" / "integration_surface.json",
    HERE / "configs" / "recovery_profiles.json",
    HERE / "configs" / "control_responsiveness.json",
    HERE / "configs" / "parameter_recovery.json",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=HERE,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduce ARC configured experiments.")
    parser.add_argument("--output", type=Path, default=HERE.parents[2] / "build/MSC-ATTACH-P02/experiments")
    parser.add_argument(
        "--configs",
        type=Path,
        nargs="*",
        default=DEFAULT_CONFIGS,
    )
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    generated: list[str] = []
    config_meta: list[dict] = []

    for config_path in args.configs:
        config_path = config_path.resolve()
        name = config_path.stem
        destination = args.output / name
        destination.mkdir(parents=True, exist_ok=True)
        before = {p.relative_to(args.output).as_posix() for p in args.output.rglob("*") if p.is_file()}
        run_config(config_path, destination)
        after = {p.relative_to(args.output).as_posix() for p in args.output.rglob("*") if p.is_file()}
        generated.extend(sorted(after - before))
        config_meta.append(
            {
                "path": config_path.relative_to(HERE.parent).as_posix()
                if HERE.parent in config_path.parents
                else str(config_path),
                "sha256": sha256(config_path),
            }
        )

    manifest = {
        "model": "ARC",
        "model_version": MODEL_VERSION,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "dependencies": {
            "numpy": importlib.metadata.version("numpy"),
            "matplotlib": importlib.metadata.version("matplotlib"),
        },
        "rng": "numpy.random.default_rng / PCG64 family",
        "configs": config_meta,
        "generated_outputs": generated,
        "interpretation": (
            "Synthetic outputs test consequences and identifiability of ARC assumptions; "
            "they are not empirical evidence of human attachment states."
        ),
    }
    (args.output / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
