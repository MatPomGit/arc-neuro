"""Strict dependency-free reader for the flat PROJECT_STATE.yaml contract.

This intentionally supports the repository's documented YAML subset only:
unquoted top-level scalar values and a two-space-indented known_blockers list.
Unknown YAML syntax is rejected rather than silently misinterpreted.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
import re

FIELDS = frozenset({
    "schema_version", "repository_type", "template_version", "programme",
    "scientific_owner", "updated", "phase", "projects_registered",
    "papers_registered", "public_catalog_status", "pages_status",
    "hardware_validation_status", "last_live_audit", "known_blockers",
    "next_action",
})
SCALAR = re.compile(r"[A-Za-z0-9_.-]+(?: [A-Za-z0-9_.-]+)*")
KEY = re.compile(r"([a-z][a-z0-9_]*):(?: (.*))?")
LIST_ITEM = re.compile(r"  - ([a-z][a-z0-9_]*)")


def load_project_state(root: Path, issues: list[str]) -> dict:
    """Read state safely, rejecting unsupported structure and duplicate keys."""
    path = root / "PROJECT_STATE.yaml"
    try:
        data = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        issues.append("Cannot read PROJECT_STATE.yaml")
        return {}

    state: dict = {}
    list_active = False
    for number, raw in enumerate(data.splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        line = raw.rstrip()
        match = KEY.fullmatch(line)
        if match:
            key, value = match.groups()
            list_active = False
            if key not in FIELDS:
                issues.append(f"Unknown PROJECT_STATE.yaml key: {key}")
                continue
            if key in state:
                issues.append(f"Duplicate PROJECT_STATE.yaml key: {key}")
                continue
            if key == "known_blockers" and not value:
                state[key] = []
                list_active = True
            elif value is None or not value or not SCALAR.fullmatch(value):
                issues.append(f"Unsupported PROJECT_STATE.yaml value: {key} at line {number}")
            elif value == "null":
                state[key] = None
            elif value.isdecimal():
                state[key] = int(value)
            else:
                state[key] = value
            continue

        entry = LIST_ITEM.fullmatch(line)
        if entry and list_active:
            state["known_blockers"].append(entry.group(1))
        else:
            issues.append(f"Unsupported PROJECT_STATE.yaml syntax at line {number}")

    for key in sorted(FIELDS - state.keys()):
        issues.append(f"Missing PROJECT_STATE.yaml field: {key}")
    return state


def check_project_state(
    state: dict, programme: dict, projects: dict, papers: dict, issues: list[str]
) -> None:
    """Verify declared state against canonical public JSON registries."""
    if state.get("schema_version") != 1 or state.get("repository_type") != "research_program":
        issues.append("PROJECT_STATE.yaml schema_version/repository_type mismatch")
    for key, source_key in (
        ("programme", "programme"), ("template_version", "template_version"),
        ("scientific_owner", "owner"), ("pages_status", "pages_status"),
    ):
        if state.get(key) != programme.get(source_key):
            issues.append(f"PROJECT_STATE.yaml {key} disagrees with program.json")

    for field, source, list_key in (
        ("projects_registered", projects, "projects"),
        ("papers_registered", papers, "papers"),
    ):
        expected = source.get(list_key)
        actual = state.get(field)
        if type(actual) is not int or actual < 0:
            issues.append(f"PROJECT_STATE.yaml {field} must be a nonnegative integer")
        elif isinstance(expected, list) and actual != len(expected):
            issues.append(f"PROJECT_STATE.yaml {field} disagrees with {list_key} registry")

    for field in ("updated", "last_live_audit"):
        value = state.get(field)
        if field == "last_live_audit" and value is None:
            continue
        if not isinstance(value, str):
            issues.append(f"PROJECT_STATE.yaml {field} must be an ISO date")
            continue
        try:
            if date.fromisoformat(value).isoformat() != value:
                raise ValueError("Noncanonical date")
        except ValueError:
            issues.append(f"PROJECT_STATE.yaml {field} must be an ISO date")

    if not isinstance(state.get("known_blockers"), list):
        issues.append("PROJECT_STATE.yaml known_blockers must be a list")
    for field in ("phase", "public_catalog_status", "hardware_validation_status", "next_action"):
        if not isinstance(state.get(field), str) or not state[field]:
            issues.append(f"PROJECT_STATE.yaml {field} must be a nonempty string")

    records = projects.get("projects")
    if isinstance(records, list):
        public_listings = sum(
            p.get("public_listing") is True for p in records if isinstance(p, dict)
        )
        empty_status = state.get("public_catalog_status") == "empty_no_explicitly_approved_entries"
        if (public_listings == 0) != empty_status:
            issues.append("PROJECT_STATE.yaml public_catalog_status contradicts registry listings")
