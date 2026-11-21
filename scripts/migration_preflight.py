"""Read-only ARC Neuro registry migration preflight; never assigns ownership."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MSC = re.compile(r"^MSC-[A-Z0-9]+-[PRS][0-9]{2,}$")
KINDS = {"MANUSCRIPT", "IDEA"}


def audit(root: Path = ROOT) -> dict:
    root = Path(root)
    catalog = json.loads((root / "papers/catalog.json").read_text(encoding="utf-8"))
    areas = json.loads((root / "areas/index.json").read_text(encoding="utf-8"))
    program = json.loads((root / "program.json").read_text(encoding="utf-8"))
    registry = json.loads((root / "portfolio/papers.json").read_text(encoding="utf-8"))
    records = catalog["papers"]
    valid_areas = {x["id"] for x in areas["lines"]}
    identifiers = set()
    findings = []
    kinds, lines = Counter(), Counter()
    for row in records:
        ident = row.get("id")
        if not isinstance(ident, str) or not MSC.fullmatch(ident):
            findings.append("invalid_msc:" + str(ident))
            continue
        if ident in identifiers:
            findings.append("duplicate_msc:" + ident)
        identifiers.add(ident)
        area = row.get("area")
        if area not in valid_areas:
            findings.append("unknown_area:" + ident)
            continue
        lines[area] += 1
        kind = row.get("record_kind")
        if kind not in KINDS:
            findings.append("unknown_record_kind:" + ident)
        else:
            kinds[kind] += 1
        if not isinstance(row.get("stage"), str) or not row["stage"].strip():
            findings.append("missing_historic_stage:" + ident)
        folder = Path("papers") / area / ident
        if row.get("manuscript_path") != (folder / "main.tex").as_posix():
            findings.append("inconsistent_tex_path:" + ident)
        if row.get("readme_path") != (folder / "README.md").as_posix():
            findings.append("inconsistent_readme_path:" + ident)
        if not (root / folder / "main.tex").is_file():
            findings.append("missing_tex:" + ident)
        if not (root / folder / "README.md").is_file():
            findings.append("missing_readme:" + ident)

    if len(records) != 63 or len(identifiers) != 63:
        findings.append("expected_63_unique_msc")
    if kinds != Counter({"MANUSCRIPT": 32, "IDEA": 31}):
        findings.append("unexpected_manuscript_idea_split")
    if program.get("schema_version") != 1 or registry.get("schema_version") != 1:
        findings.append("unexpected_legacy_schema")
    if registry.get("papers") != []:
        findings.append("legacy_public_registry_is_not_empty")

    return {
        "inventory_status": "PASS" if not findings else "FAIL",
        "migration_status": "BLOCKED",
        "migration_ready": False,
        "schema_version": program.get("schema_version"),
        "record_count": len(records),
        "record_kinds": dict(sorted(kinds.items())),
        "research_lines": dict(sorted(lines.items())),
        "historical_stage_values": sorted({x.get("stage") for x in records
                                            if isinstance(x.get("stage"), str)}),
        "unresolved_decisions": [
            "canonical_owner_for_each_msc",
            "mapping_of_historical_stage_to_v2_research_state_and_publication_stage",
            "approval_of_public_listing_is_separate",
        ],
        "findings": sorted(set(findings)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        result = audit(args.root)
    except (OSError, KeyError, ValueError, TypeError) as exc:
        print(json.dumps({"inventory_status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["inventory_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
