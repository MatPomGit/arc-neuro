"""Verify the public owner's explicit GitHub review of catalog metadata.

No credentials, privileged runner or private API is used. An empty approval
manifest performs zero network requests. A malformed or unavailable review
fails closed so syntax-only attestations cannot authorize catalog entries.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen

from public_approvals import (
    check_publication_approvals,
    load_publication_approvals,
    strict_json_loads,
)

REVIEW_REF = re.compile(
    r"https://github\.com/MatPomGit/arc-neuro/pull/([1-9][0-9]*)"
    r"#pullrequestreview-([1-9][0-9]*)"
)


def fetch_review(pr_number: int, review_id: int) -> dict:
    url = (
        "https://api.github.com/repos/MatPomGit/arc-neuro/"
        f"pulls/{pr_number}/reviews/{review_id}"
    )
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "arc-neuro-public-review-verifier",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urlopen(request, timeout=10) as response:
        body = response.read(262145)
    if len(body) > 262144:
        raise ValueError("Oversized GitHub review response")
    data = strict_json_loads(body.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Invalid GitHub review response")
    return data


def verify_public_reviews(root: Path, fetcher=fetch_review) -> list[str]:
    issues: list[str] = []
    try:
        approvals = load_publication_approvals(root)
        data = strict_json_loads(
            (root / "portfolio/projects.json").read_text(encoding="utf-8")
        )
        if not isinstance(data, dict) or not isinstance(data.get("projects"), list):
            raise ValueError("Invalid projects registry")
        check_publication_approvals(root, data["projects"], issues)
    except (OSError, UnicodeError, ValueError):
        return ["Invalid public review evidence inputs"]
    if issues:
        return issues
    for ident, record in approvals.items():
        match = REVIEW_REF.fullmatch(record["review_url"])
        if not match:
            issues.append(f"Invalid review URL for project: {ident}")
            continue
        pr, review_id = map(int, match.groups())
        try:
            review = fetcher(pr, review_id)
        except (OSError, URLError, ValueError, TimeoutError):
            issues.append(f"GitHub public review unavailable for project: {ident}")
            continue
        if not isinstance(review, dict):
            issues.append(f"Invalid GitHub review response for project: {ident}")
            continue
        user = review.get("user")
        reviewer = user.get("login") if isinstance(user, dict) else None
        body = review.get("body")
        expected = (
            f"APPROVE_PUBLIC_LISTING {ident} "
            f"sha256:{record['project_sha256']}"
        )
        if not (
            review.get("id") == review_id
            and review.get("html_url") == record["review_url"]
            and reviewer == "MatPomGit"
            and review.get("state") in ("COMMENTED", "APPROVED")
            and isinstance(body, str) and body.strip() == expected
            and isinstance(review.get("submitted_at"), str)
            and review["submitted_at"][:10] == record["approved_on"]
        ):
            issues.append(f"Review evidence mismatch for project: {ident}")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    issues = verify_public_reviews(args.root)
    for issue in issues:
        print("FAIL:", issue)
    print(
        "public-review-evidence: "
        f"{'FAIL' if issues else 'PASS'}; findings={len(issues)}"
    )
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
