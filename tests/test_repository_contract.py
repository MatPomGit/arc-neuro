"""Offline tests for ARC template structure, privacy and data ownership."""
from __future__ import annotations
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from validate_repository import validate, github_repo_url, safe_public_page_url, load_json
from build_public_catalog import render
from check_freshness import inspect_project


def candidate():
    return {
        "id":"msc-example", "title":"Private project", "repository":"MatPomGit/msc-example",
        "url":"https://github.com/MatPomGit/msc-example", "role":"primary",
        "primary_program":"arc-neuro", "line":"ndd", "status":"active",
        "visibility":"private", "public_listing":False, "default_branch":"main",
        "snapshot_sha":"a"*40, "pages_url":None, "submodule_path":None
    }

class ARCContractTests(unittest.TestCase):
    def test_scaffold_passes(self):
        self.assertEqual(validate(ROOT,"scaffold"),[])

    def test_license_metadata_is_consistent(self):
        meta = json.loads((ROOT / "program.json").read_text(encoding="utf-8"))
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        self.assertEqual(meta["license_spdx"], "MIT")
        self.assertTrue(license_text.startswith("MIT License\n\nCopyright (c) 2026 Mateusz Pomianek"))
        self.assertIn("Permission is hereby granted, free of charge", license_text)
        self.assertIn("THE SOFTWARE IS PROVIDED", license_text)
        self.assertIn("license: MIT", citation)

    def test_unconfigured_publish_is_blocked(self):
        issues=validate(ROOT,"publish")
        self.assertIn("Program publishing requires at least one project and research line", issues)
        self.assertIn("No reviewed public Pages configuration", issues)

    def test_github_url_forbids_token_and_untrusted_host(self):
        self.assertTrue(github_repo_url("MatPomGit/example","https://github.com/MatPomGit/example"))
        self.assertFalse(github_repo_url("MatPomGit/example","https://token@github.com/MatPomGit/example"))
        self.assertFalse(github_repo_url("MatPomGit/example","https://example.org/MatPomGit/example"))

    def test_private_project_never_in_public_pages(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"portfolio").mkdir()
            (root/"portfolio/projects.json").write_text(json.dumps({"projects":[{
                **candidate(),"public_listing":True,"pages_url":"https://internal.example/private"
            }]}),encoding="utf-8")
            result=render(root)
            self.assertNotIn("Private project",result)
            self.assertNotIn("internal.example",result)

    def test_duplicate_project_ids_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            # Clone only required lightweight fixture files to the temporary root.
            import shutil
            dst=Path(d)
            for f in ROOT.rglob("*"):
                if f.is_file() and "__pycache__" not in f.parts:
                    dest=dst/f.relative_to(ROOT)
                    dest.parent.mkdir(parents=True,exist_ok=True)
                    shutil.copyfile(f,dest)
            meta=json.loads((dst/"program.json").read_text(encoding="utf-8"))
            meta["programme"]="arc-neuro"
            (dst/"program.json").write_text(json.dumps(meta),encoding="utf-8")
            (dst/"areas/index.json").write_text(json.dumps({"lines":[{"id":"ndd","title":"NDD"}]}),encoding="utf-8")
            (dst/"portfolio/projects.json").write_text(json.dumps({"projects":[candidate(),candidate()]}),encoding="utf-8")
            self.assertTrue(any("duplicate project" in x.lower() for x in validate(dst,"scaffold")))

    def test_public_source_rejects_unlisted_private_repo(self):
        with tempfile.TemporaryDirectory() as d:
            import shutil
            dst = Path(d)
            for file in ROOT.rglob("*"):
                if file.is_file() and "__pycache__" not in file.parts:
                    copy_to = dst / file.relative_to(ROOT)
                    copy_to.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(file, copy_to)
            (dst / "areas/index.json").write_text(
                json.dumps({"lines": [{"id": "ndd", "title": "Neurodiversity"}]}),
                encoding="utf-8",
            )
            (dst / "portfolio/projects.json").write_text(
                json.dumps({"projects": [candidate()]}), encoding="utf-8",
            )
            issues = validate(dst, "scaffold")
            self.assertTrue(any("Private repository recorded in public ARC" in x for x in issues))

    def test_public_source_cannot_disable_privacy_gate(self):
        for declared in ("private", None):
            with self.subTest(declared_visibility=declared):
                def tampered_load(root, relative, issues):
                    data = load_json(root, relative, issues)
                    if relative == "program.json":
                        if declared is None:
                            data.pop("repository_visibility", None)
                        else:
                            data["repository_visibility"] = declared
                    if relative == "portfolio/projects.json":
                        data["projects"] = [candidate()]
                    return data

                with patch("validate_repository.load_json", side_effect=tampered_load):
                    issues = validate(ROOT, "scaffold")
                self.assertTrue(any("ARC Neuro repository must remain public" in x for x in issues))
                self.assertTrue(any("Private repository recorded in public ARC" in x for x in issues))

    def test_public_programme_identity_is_fixed(self):
        def tampered_load(root, relative, issues):
            data = load_json(root, relative, issues)
            if relative == "program.json":
                data["programme"] = "arc-ai"
            return data

        with patch("validate_repository.load_json", side_effect=tampered_load):
            issues = validate(ROOT, "scaffold")
        self.assertIn("ARC Neuro repository identity mismatch", issues)


    def test_non_object_json_roots_fail_cleanly(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for invalid in ([], None, "not an object"):
                (root/"broken.json").write_text(json.dumps(invalid), encoding="utf-8")
                issues = []
                self.assertEqual(load_json(root, "broken.json", issues), {})
                self.assertTrue(any("Invalid JSON root" in x for x in issues))

    def test_non_string_repo_fails_validation_without_crash(self):
        self.assertFalse(github_repo_url(None, "https://github.com/owner/repo"))
        self.assertFalse(github_repo_url(42, "https://github.com/owner/repo"))

    def test_duplicate_repo_with_distinct_project_ids_is_rejected(self):
        def injected(root, relative, issues):
            data = load_json(root, relative, issues)
            if relative == "portfolio/projects.json":
                first = {**candidate(), "visibility": "public"}
                second = {**first, "id": "msc-second"}
                data["projects"] = [first, second]
            return data
        with patch("validate_repository.load_json", side_effect=injected):
            issues = validate(ROOT, "scaffold")
        self.assertTrue(any("Duplicated project repository" in x for x in issues))

    def test_catalog_fails_closed_for_malformed_projects(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/"portfolio").mkdir()
            path = root/"portfolio/projects.json"
            for invalid in ([], {"projects": "unexpected"}, {"projects": [5]}):
                path.write_text(json.dumps(invalid), encoding="utf-8")
                with self.assertRaises(ValueError):
                    render(root)

    def test_public_pages_urls_reject_markup_injection(self):
        self.assertTrue(safe_public_page_url("https://matpomgit.github.io/msc-example/"))
        self.assertFalse(safe_public_page_url("https://host.example/)[malicious](x"))
        self.assertFalse(safe_public_page_url("https://user:pw@host.example/path"))

    def test_freshness_produces_stale_without_modification(self):
        fake=type("Result", (),{"returncode":0,"stdout": "b"*40+"\trefs/heads/main\n"})
        with patch("check_freshness.subprocess.run",return_value=fake):
            r=inspect_project(candidate())
        self.assertEqual(r["status"],"STALE")
        self.assertEqual(r["snapshot_sha"],"a"*40)

    def test_remote_unavailable_not_success(self):
        fake=type("Result", (),{"returncode":128,"stdout":"","stderr":"TOKEN MUST NOT BE LOGGED"})
        with patch("check_freshness.subprocess.run",return_value=fake):
            r=inspect_project(candidate())
        self.assertEqual(r["status"],"UNAVAILABLE")
        self.assertNotIn("TOKEN",json.dumps(r))

if __name__=="__main__": unittest.main()
