"""Validate every v3 manuscript record using JSON Schema Draft 2020-12."""
from pathlib import Path
import sys
import json
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from public_approvals import strict_json_loads


def validate(root=ROOT):
    schema = strict_json_loads((root / "schemas/paper.v3.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    paths = sorted((root / "manuscripts").glob("MSC-*/paper.json"))
    catalog = strict_json_loads((root / "manuscripts/catalog.json").read_text(encoding="utf-8"))
    expected = {p["id"] for p in catalog["papers"]}
    if {p.parent.name for p in paths} != expected or len(expected) != len(catalog["papers"]):
        errors.append("Metadata coverage differs from catalog")
    for path in paths:
        if path.is_symlink() or path.parent.is_symlink():
            errors.append(f"{path.relative_to(root)}: symlink denied")
            continue
        try:
            record = strict_json_loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            errors.append(f"{path.relative_to(root)}: {type(exc).__name__}")
            continue
        for error in validator.iter_errors(record):
            errors.append(f"{path.relative_to(root)}:{list(error.absolute_path)}: {error.message}")
    return errors, len(paths)


if __name__ == "__main__":
    errors, count = validate()
    for error in errors:
        print("FAIL:", error)
    print(f"v3 paper schema: {'FAIL' if errors else 'PASS'}; records={count}")
    raise SystemExit(bool(errors))
