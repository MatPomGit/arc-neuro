"""Collect an explicit allowlist of reproducibility metadata, no secrets."""
import argparse
import hashlib
import importlib.metadata
import json
import platform
from pathlib import Path
import subprocess
from design import VERSION,STIMULUS_VERSION


def cmd(*args):
    try:
        return subprocess.check_output(args,stderr=subprocess.DEVNULL,text=True,timeout=10).strip()
    except (OSError,subprocess.SubprocessError):
        return None


def collect(report=None):
    root=Path(__file__).resolve().parent
    files=sorted(p for p in root.rglob("*") if p.is_file() and p.suffix in (".py",".mjs",".html",".css",".txt"))
    dirty=cmd("git","-C",str(root),"status","--porcelain","--untracked-files=no")
    return dict(protocol_version=VERSION,stimulus_version=STIMULUS_VERSION,
                git_sha=cmd("git","-C",str(root),"rev-parse","HEAD"),
                git_tracked_dirty=None if dirty is None else bool(dirty),
                python=platform.python_version(),os=platform.system(),machine=platform.machine(),
                node=cmd("node","--version"),chrome=cmd("google-chrome","--version"),
                packages={d.metadata["Name"]:d.version for d in sorted(importlib.metadata.distributions(),
                    key=lambda x:x.metadata["Name"].lower()) if d.metadata["Name"]},
                source_sha256={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
                report_sha256=hashlib.sha256(Path(report).read_bytes()).hexdigest() if report else None)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report")
    a=p.parse_args()
    print(json.dumps(collect(a.report),sort_keys=True,indent=2,allow_nan=False))
