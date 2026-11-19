"""Fail-closed public catalog review manifest.

An offline manifest is an audit reference, not proof that the GitHub review
exists or the author approved publication. Human GitHub review is required.
"""
from __future__ import annotations

from datetime import date
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlparse

ID = re.compile(r"^[a-z][a-z0-9-]{2,63}$")
DIGEST = re.compile(r"^[0-9a-f]{64}$")
REVIEW_URL = re.compile(
    r"^https://github\.com/MatPomGit/arc-neuro/pull/[1-9][0-9]*"
    r"#pullrequestreview-[1-9][0-9]*$"
)
FIELDS = {"project_id", "project_sha256", "review_url", "reviewed_by", "approved_on"}
OWNER = "MatPomGit"


def project_digest(project: dict) -> str:
    serialized = json.dumps(
        project, ensure_ascii=False, sort_keys=True, allow_nan=False,
        separators=(",", ":"),
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def load_publication_approvals(root: Path) -> dict[str, dict]:
    """Invalid/missing manifests fail closed, including duplicate entries."""
    path = root / "portfolio/publication-approvals.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        raise ValueError("Cannot read public approval registry") from exc
    if not isinstance(data, dict) or set(data) != {"schema_version", "approvals"}:
        raise ValueError("Invalid public approval registry root")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("Invalid approval registry schema version")
    if not isinstance(data["approvals"], list):
        raise ValueError("Public approvals must be an array")
    records = {}
    for item in data["approvals"]:
        if not isinstance(item, dict) or set(item) != FIELDS:
            raise ValueError("Malformed public approval")
        ident, digest, url, reviewer, approved_on = (
            item["project_id"], item["project_sha256"],
            item["review_url"], item["reviewed_by"], item["approved_on"],
        )
        if not isinstance(ident, str) or not ID.fullmatch(ident) or ident in records:
            raise ValueError("Duplicate or invalid approved project ID")
        if not isinstance(digest, str) or not DIGEST.fullmatch(digest):
            raise ValueError("Invalid approved project digest")
        if not isinstance(url, str) or not REVIEW_URL.fullmatch(url):
            raise ValueError("Invalid GitHub review URL")
        if reviewer != OWNER:
            raise ValueError("Reviewer does not match the designated programme owner")
        if not isinstance(approved_on, str):
            raise ValueError("Invalid approval date")
        try:
            if date.fromisoformat(approved_on).isoformat() != approved_on:
                raise ValueError("Noncanonical ISO date")
        except ValueError as exc:
            raise ValueError("Invalid approval date") from exc
        records[ident] = item
    return records


def same_repo_github_pages(project: dict) -> bool:
    """Default allowlist permits only the declared repository's Pages URL."""
    repo, url = project.get("repository"), project.get("pages_url")
    if not isinstance(repo, str) or not isinstance(url, str) or repo.count("/") != 1:
        return False
    owner, name = repo.split("/")
    if not owner or not name:
        return False
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", owner) or not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
        return False
    try:
        page = urlparse(url)
        return (
            page.scheme == "https"
            and page.hostname == f"{owner.lower()}.github.io"
            and page.username is None and page.password is None
            and page.port is None and not page.query and not page.fragment
            and page.path.startswith(f"/{name}/")
            and not any(c.isspace() or c in "<>[]()\\" for c in url)
        )
    except ValueError:
        return False


def is_approved_project(project: dict, approvals: dict[str, dict]) -> bool:
    if project.get("visibility") != "public" or project.get("public_listing") is not True:
        return False
    if not same_repo_github_pages(project):
        return False
    record = approvals.get(project.get("id"))
    return (
        isinstance(record, dict)
        and record.get("project_sha256") == project_digest(project)
        and record.get("reviewed_by") == OWNER
        and isinstance(record.get("review_url"), str)
        and bool(REVIEW_URL.fullmatch(record["review_url"]))
    )


def check_publication_approvals(root: Path, projects: list, issues: list[str]) -> None:
    try:
        approvals = load_publication_approvals(root)
    except ValueError:
        issues.append("Invalid or unavailable public approval registry")
        return
    known = set()
    for project in projects:
        if not isinstance(project, dict):
            continue
        ident = project.get("id")
        if isinstance(ident, str):
            known.add(ident)
        if project.get("public_listing") is True and not is_approved_project(project, approvals):
            issues.append(f"Missing or stale public approval for project: {ident}")
    for ident in approvals:
        if ident not in known:
            issues.append(f"Orphan public approval for project: {ident}")
