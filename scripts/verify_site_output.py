"""Inspect curated generated HTML after a strict MkDocs build."""
from __future__ import annotations
import re
import sys
from pathlib import Path

def validate(site: Path) -> list[str]:
    if not site.is_dir() or site.is_symlink():
        return ["site directory missing or symlink"]
    html = sorted(site.rglob("*.html"))
    if not html or not (site / "index.html").is_file() or not (site / "projects" / "index.html").is_file():
        return ["required output HTML missing"]
    required = ["articles", "ndd", "affect", "cognition", "social", "psychometrics"]
    if any(not (site / name / "index.html").is_file() for name in required):
        return ["curated article HTML missing"]
    forbidden = re.compile(
        r"AGENT_WORKFLOW|CONTRIBUTING\.md|agents\.md|MatPomGit/devices|"
        r"neuro_paper_slots|research-autopilot|instructions to agent|"
        r"notatk\\w* dla autora|/docs/security/|/papers/(?:ndd|affect|cognition|social|psychometrics)/",
        re.IGNORECASE,
    )
    errors = []
    for p in html:
        if p.is_symlink():
            errors.append(f"symlink: {p.relative_to(site)}")
            continue
        txt = p.read_text(encoding="utf-8")
        if forbidden.search(txt):
            errors.append(f"internal text found in {p.relative_to(site)}")
    return errors

if __name__ == "__main__":
    errs = validate(Path(sys.argv[1] if len(sys.argv) > 1 else "site"))
    for e in errs:
        print("FAIL:", e)
    print("arc-site-output:", "FAIL" if errs else "PASS")
    raise SystemExit(bool(errs))
