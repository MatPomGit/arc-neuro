"""Compile all ARC Neuro LaTeX drafts using an isolated temporary directory.

Smoke test only: successful PDF creation is not scientific peer review.
Runs on GitHub-hosted CI, never on persistent research runners.
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AREAS = {"ndd": 16, "affect": 4, "cognition": 13, "social": 25, "psychometrics": 8}

def compile_all(root: Path = ROOT, timeout: int = 40) -> list[str]:
    errors: list[str] = []
    latex = shutil.which("pdflatex")
    if latex is None:
        return ["pdflatex is unavailable; compilation NOT_RUN"]
    with tempfile.TemporaryDirectory(prefix="arc-neuro-pdf-") as tmp:
        for area, count in AREAS.items():
            files = sorted((root / "papers" / area).glob("MSC-*/main.tex"))
            if len(files) != count:
                errors.append(f"{area}: expected {count} sources; found {len(files)}")
            for src in files:
                rel = src.relative_to(root).as_posix()
                dest = Path(tmp) / area / src.parent.name
                dest.mkdir(parents=True, exist_ok=True)
                if src.is_symlink():
                    errors.append(f"{rel}: symlink denied")
                    continue
                try:
                    result = subprocess.run(
                        [latex, "-halt-on-error", "-interaction=nonstopmode",
                         "-no-shell-escape", f"-output-directory={dest}", "main.tex"],
                        cwd=src.parent, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        text=True, errors="replace", timeout=timeout, check=False,
                    )
                    pdf = dest / "main.pdf"
                    if result.returncode != 0 or not pdf.is_file() or pdf.stat().st_size < 300:
                        lines = result.stdout.splitlines()
                        detail = next((line.strip() for line in lines if line.startswith("!")), "")
                        errors.append(f"{rel}: LaTeX FAIL exit={result.returncode} {detail}")
                    else:
                        print(f"PASS PDF: {rel}")
                except (subprocess.TimeoutExpired, OSError) as exc:
                    errors.append(f"{rel}: {type(exc).__name__}")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = compile_all(args.root)
    for err in errors:
        print("FAIL:", err)
    print("arc-neuro-latex:", "FAIL" if errors else "PASS (63 PDFs)")
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
