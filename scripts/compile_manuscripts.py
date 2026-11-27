"""Compile all ARC Neuro LaTeX drafts using an isolated temporary directory.

Smoke test only: successful PDF creation is not scientific peer review.
Runs on GitHub-hosted CI, never on persistent research runners.
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def compile_all(root: Path = ROOT, timeout: int = 40) -> list[str]:
    errors: list[str] = []
    latex = shutil.which("pdflatex")
    if latex is None:
        return ["pdflatex is unavailable; compilation NOT_RUN"]
    with tempfile.TemporaryDirectory(prefix="arc-neuro-pdf-") as tmp:
        catalog = json.loads((root / "manuscripts/catalog.json").read_text(encoding="utf-8"))
        expected = {p["id"] for p in catalog["papers"]}
        files = sorted((root / "manuscripts").glob("MSC-*/main.tex"))
        actual = {src.parent.name for src in files}
        if actual != expected or len(expected) != len(catalog["papers"]):
            errors.append(f"Catalog mismatch: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}")
        for src in files:
            rel = src.relative_to(root).as_posix()
            dest = Path(tmp) / src.parent.name
            dest.mkdir(parents=True, exist_ok=True)
            if src.is_symlink():
                errors.append(f"{rel}: symlink denied")
                continue
            try:
                source = src.read_text(encoding="utf-8")
                apa = bool(re.search(r"\\documentclass\s*(?:\[[^\]]*\])?\s*\{apa7\}", source))
                bibliography = apa or r"\bibliography{" in source or r"\addbibresource{" in source
                if bibliography:
                    latexmk = shutil.which("latexmk")
                    if latexmk is None or (apa and shutil.which("biber") is None):
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
                    text=True, errors="replace", timeout=max(timeout, 180) if bibliography else timeout, check=False,
                )
                pdf = dest / "main.pdf"
                if result.returncode != 0 or not pdf.is_file() or pdf.stat().st_size < 300:
                    lines = result.stdout.splitlines()
                    detail = next((line.strip() for line in lines if line.startswith("!") or re.search(r":\d+:\s*(?:LaTeX|Package|Undefined|Missing|Extra|Emergency)", line) or "ERROR -" in line), "")
                    if not detail:
                        detail = "\n".join(lines[-25:])
                    errors.append(f"{rel}: LaTeX FAIL exit={result.returncode} {detail}")
                elif bibliography and (
                    not (dest / "main.blg").is_file()
                    or (apa and "ERROR -" in (dest / "main.blg").read_text(errors="replace"))
                    or re.search(
                        r"(?:Citation .* undefined|There were undefined (?:references|citations))",
                        (dest / "main.log").read_text(errors="replace"),
                    )
                ):
                    errors.append(f"{rel}: bibliography/reference validation failed")
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
    print("arc-neuro-latex:", "FAIL" if errors else "PASS")
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
