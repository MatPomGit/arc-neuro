"""Import explicit proposed dependencies from manuscript study cards.

Never infer readiness, canonical ownership, or actual hardware from a station ID.
Existing manually curated dependencies are preserved; conflicts require review.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = re.compile(r'^- \*\*`(app-[a-z0-9-]+)`\*\*.*?rola `([A-Z_]+)`.*?status repozytorium `([A-Z_]+)`')
LIB = re.compile(r'^- \*\*`(lib-[a-z0-9-]+)`\*\*: status `([A-Z_]+)`')


def proposed_tools(text, source):
    section = None
    result = {}
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        match = APP.match(line) if section == "Aplikacje" else None
        lib = LIB.match(line) if section == "Biblioteki" else None
        if match:
            ref, role, status = match.groups()
        elif lib:
            ref, status = lib.groups()
            role = "PROPOSED_LIBRARY"
        else:
            continue
        entry = {"ref": ref, "role": role, "contract_path": source,
                 "validation_status": "NOT_VERIFIED",
                 "notes": f"Source repository status: {status}; proposed dependency only."}
        if ref in result and result[ref] != entry:
            raise ValueError(f"Conflicting source entries: {source}: {ref}")
        result[ref] = entry
    return list(result.values())


def migrate(root, write=False):
    changed, missing, conflicts = [], [], []
    for path in sorted((root / "manuscripts").glob("MSC-*/paper.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        study = path.parent / "study.md"
        if not study.is_file():
            missing.append(path.parent.name)
            continue
        if study.is_symlink() or path.is_symlink() or path.parent.is_symlink():
            raise ValueError(f"Symlink denied: {path}")
        source = study.relative_to(root).as_posix()
        tools = record["dependencies"]["tools"]
        existing = {entry["ref"] for entry in tools}
        proposed = proposed_tools(study.read_text(encoding="utf-8"), source)
        for entry in proposed:
            if entry["ref"] not in existing:
                tools.append(entry)
                existing.add(entry["ref"])
        if record["study_plan"] is None:
            record["study_plan"] = source
        elif record["study_plan"] != source:
            conflicts.append(path.parent.name)
        updated = json.dumps(record, ensure_ascii=False, indent=2) + "\n"
        if json.loads(updated) != json.loads(path.read_text(encoding="utf-8")):
            changed.append(path.parent.name)
            if write:
                path.write_text(updated, encoding="utf-8")
    return {"changed": changed, "missing_study": missing, "existing_plan_review": conflicts}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    print(json.dumps(migrate(ROOT, args.write), indent=2))
