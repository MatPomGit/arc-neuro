"""Read-only ARC Neuro registry migration preflight; never assigns ownership."""
from __future__ import annotations

import argparse
import json
import re
from hashlib import sha1
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MSC = re.compile(r"^MSC-[A-Z0-9]+-[PRS][0-9]{2,}$")
KINDS = {"MANUSCRIPT", "IDEA"}
HISTORICAL_IDS_PATH = "config/historical-manuscripts-63.txt"
HISTORICAL_MANIFEST_GIT_BLOB_SHA = "ff5e5eb7ecf46049300944e168b1dff06abcb68d"


def audit(root: Path = ROOT) -> dict:
    root = Path(root)
    catalog = json.loads((root / "manuscripts/catalog.json").read_text(encoding="utf-8"))
    areas = json.loads((root / "config/research-lines.json").read_text(encoding="utf-8"))
    program = json.loads((root / "program.json").read_text(encoding="utf-8"))
    registry = {"schema_version": 1, "papers": []}
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
        folder = Path("manuscripts") / ident
        if row.get("manuscript_path") != (folder / "main.tex").as_posix():
            findings.append("inconsistent_tex_path:" + ident)
        if row.get("readme_path") != (folder / "README.md").as_posix():
            findings.append("inconsistent_readme_path:" + ident)
        if (root / folder).is_symlink():
            findings.append("symlink_manuscript_folder:" + ident)
        if (root / folder / "main.tex").is_symlink():
            findings.append("symlink_tex:" + ident)
        if (root / folder / "README.md").is_symlink():
            findings.append("symlink_readme:" + ident)
        if not (root / folder / "main.tex").is_file():
            findings.append("missing_tex:" + ident)
        if not (root / folder / "README.md").is_file():
            findings.append("missing_readme:" + ident)

    # Historical 63-item cohort is pinned independently of newer IDEA entries.
    # Neither the migration status nor public approvals are changed here.
    # Freeze the ID list to the original Git blob, not only a 63-ID count.
    # Any edited list requires an explicit new migration decision.
    historical_bytes = (root / HISTORICAL_IDS_PATH).read_bytes()
    blob_header = f"blob {len(historical_bytes)}\0".encode("ascii")
    manifest_git_blob = sha1(blob_header + historical_bytes).hexdigest()
    if manifest_git_blob != HISTORICAL_MANIFEST_GIT_BLOB_SHA:
        findings.append("historical_63_snapshot_modified")
    historical_lines = [
        line.strip() for line in historical_bytes.decode("utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    historical_ids = set(historical_lines)
    if (len(historical_lines) != 63 or len(historical_ids) != 63
            or any(not MSC.fullmatch(ident) for ident in historical_ids)):
        findings.append("invalid_historical_63_snapshot")
    historical = [row for row in records if row.get("id") in historical_ids]
    present_ids = {row.get("id") for row in historical}
    historical_kinds = Counter(row.get("record_kind") for row in historical)
    if len(historical) != 63 or len(present_ids) != 63 or present_ids != historical_ids:
        findings.append("expected_63_historical_unique_msc")
    if historical_kinds != Counter({"MANUSCRIPT": 32, "IDEA": 31}):
        findings.append("unexpected_historical_manuscript_idea_split")
    if len(records) != len(identifiers):
        findings.append("non_unique_new_msc")
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
        "historical_record_count": len(historical),
        "historical_record_kinds": dict(sorted(historical_kinds.items())),
        "later_record_ids": sorted(identifiers - historical_ids),
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
