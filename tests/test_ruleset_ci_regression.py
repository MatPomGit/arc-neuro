"""Read-only main-branch ruleset contract; live API audit requires opt-in."""
import json
import os
import unittest
from urllib.request import Request, urlopen

URL = "https://api.github.com/repos/MatPomGit/arc-neuro/rulesets/27658007"
REQUIRED = "contract (head)"
MAIN_REFS = {"~DEFAULT_BRANCH", "~ALL", "refs/heads/main", "main"}


def ci_required(ruleset):
    """Presence of a check is insufficient: it must protect main without bypass."""
    if not isinstance(ruleset, dict):
        return False
    if ruleset.get("enforcement") != "active" or ruleset.get("target") != "branch":
        return False
    conditions = ruleset.get("conditions", {})
    if not isinstance(conditions, dict):
        return False
    refs = conditions.get("ref_name", {})
    if not isinstance(refs, dict):
        return False
    included = refs.get("include", [])
    excluded = refs.get("exclude", [])
    if not isinstance(included, list) or not isinstance(excluded, list):
        return False
    if not all(isinstance(ref, str) for ref in included + excluded):
        return False
    if not (set(included) & MAIN_REFS) or (set(excluded) & MAIN_REFS):
        return False
    bypass = ruleset.get("bypass_actors", [])
    if not isinstance(bypass, list) or any(
        not isinstance(actor, dict) or actor.get("bypass_mode") in {"always", "pull_request"}
        for actor in bypass
    ):
        return False
    rules = ruleset.get("rules", [])
    if not isinstance(rules, list):
        return False
    for rule in rules:
        if not isinstance(rule, dict) or rule.get("type") != "required_status_checks":
            continue
        parameters = rule.get("parameters", {})
        if not isinstance(parameters, dict):
            continue
        checks = parameters.get("required_status_checks", [])
        if not isinstance(checks, list):
            continue
        if any(isinstance(check, dict) and check.get("context") == REQUIRED
               for check in checks):
            return True
    return False


def example_ruleset(checks=None):
    return {
        "enforcement": "active", "target": "branch",
        "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
        "bypass_actors": [],
        "rules": [{"type": "required_status_checks", "parameters": {
            "required_status_checks": checks if checks is not None else [{"context": REQUIRED}]
        }}],
    }


class MainRulesetRegression(unittest.TestCase):
    def test_ruleset_contract_examples(self):
        self.assertTrue(ci_required(example_ruleset()))
        self.assertFalse(ci_required(example_ruleset([])))
        self.assertFalse(ci_required(example_ruleset([{"context": "not-the-required-check"}])))
        for key, value in [
            ("enforcement", "disabled"), ("enforcement", "evaluate"),
            ("target", "tag"),
            ("conditions", {"ref_name": {"include": ["refs/heads/develop"], "exclude": []}}),
            ("conditions", {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": ["~DEFAULT_BRANCH"]}}),
            ("bypass_actors", [{"actor_type": "RepositoryRole", "actor_id": 5, "bypass_mode": "always"}]),
        ]:
            with self.subTest(key=key, value=value):
                record = example_ruleset()
                record[key] = value
                self.assertFalse(ci_required(record))
        record = example_ruleset([])
        record["rules"].append(example_ruleset()["rules"][0])
        self.assertTrue(ci_required(record), "Required checks may be split across rules")

    @unittest.skipUnless(os.environ.get("ARC_RULESET_LIVE") == "1",
                         "Live GitHub audit requires explicit opt-in")
    def test_live_main_ruleset_requires_ci(self):
        request = Request(URL, headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "arc-neuro-read-only-security-audit",
        })
        with urlopen(request, timeout=10) as response:
            ruleset = json.load(response)
        self.assertTrue(ci_required(ruleset), f"CI_NOT_ENFORCED: {URL}")


if __name__ == "__main__":
    unittest.main()
