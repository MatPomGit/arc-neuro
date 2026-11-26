"""Compile all ARC Neuro LaTeX drafts using an isolated temporary directory.

Smoke test only: successful PDF creation is not scientific peer review.
Runs on GitHub-hosted CI, never on persistent research runners.
"""
from __future__ import annotations
import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AREAS = {"ndd": 16, "affect": 5, "cognition": 15, "social": 25, "psychometrics": 8}

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
                    apa = r"\documentclass[man]{apa7}" in src.read_text(encoding="utf-8")
                    if apa:
                        latexmk = shutil.which("latexmk")
                        if latexmk is None or shutil.which("biber") is None:
                            errors.append(f"{rel}: latexmk or biber unavailable")
                            continue
                        command = [latexmk, "-norc", "-pdf", "-halt-on-error",
                                   "-interaction=nonstopmode",
                                   "-pdflatex=pdflatex -no-shell-escape -file-line-error %O %S",
                                   f"-outdir={dest}", "main.tex"]
                    else:
                        command = [latex, "-halt-on-error", "-interaction=nonstopmode",
                                   "-no-shell-escape", f"-output-directory={dest}", "main.tex"]
                    result = subprocess.run(
                        command,
                        cwd=src.parent, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        text=True, errors="replace", timeout=max(timeout, 180) if apa else timeout, check=False,
                    )
                    pdf = dest / "main.pdf"
                    if result.returncode != 0 or not pdf.is_file() or pdf.stat().st_size < 300:
                        lines = result.stdout.splitlines()
                        detail = next((line.strip() for line in lines if line.startswith("!")), "")
                        errors.append(f"{rel}: LaTeX FAIL exit={result.returncode} {detail}")
                    elif apa and (
                        not (dest / "main.blg").is_file()
                        or "ERROR -" in (dest / "main.blg").read_text(errors="replace")
                        or re.search(
                            r"(?:Citation .* undefined|There were undefined (?:references|citations))",
                            (dest / "main.log").read_text(errors="replace"),
                        )
                    ):
                        errors.append(f"{rel}: APA7 bibliography/reference validation failed")
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
    print("arc-neuro-latex:", "FAIL" if errors else "PASS (69 PDFs)")
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
