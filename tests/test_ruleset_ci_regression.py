"""Read-only security contract for main ruleset; live check is opt-in."""
import json
import os
import unittest
from urllib.request import Request, urlopen

URL = "https://api.github.com/repos/MatPomGit/arc-neuro/rulesets/27658007"
REQUIRED = "contract (head)"


def ci_required(ruleset):
    rules = ruleset.get("rules", [])
    for rule in rules:
        if rule.get("type") != "required_status_checks":
            continue
        checks = rule.get("parameters", {}).get("required_status_checks", [])
        return any(check.get("context") == REQUIRED for check in checks)
    return False


class MainRulesetRegression(unittest.TestCase):
    def test_security_contract_examples(self):
        self.assertFalse(ci_required({"rules": [{"type": "required_status_checks", "parameters": {"required_status_checks": []}}]}))
        self.assertTrue(ci_required({"rules": [{"type": "required_status_checks", "parameters": {"required_status_checks": [{"context": REQUIRED}]}}]}))

    @unittest.skipUnless(os.environ.get("ARC_RULESET_LIVE") == "1", "Live GitHub audit requires explicit opt-in")
    def test_live_main_ruleset_requires_ci(self):
        request = Request(URL, headers={"Accept": "application/vnd.github+json", "User-Agent": "arc-neuro-read-only-security-audit"})
        with urlopen(request, timeout=10) as response:
            ruleset = json.load(response)
        self.assertTrue(ci_required(ruleset), f"CI_NOT_ENFORCED: {URL}")


if __name__ == "__main__":
    unittest.main()
