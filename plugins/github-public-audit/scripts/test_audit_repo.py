#!/usr/bin/env python3
"""Regression tests for public-readiness detection rules."""

from pathlib import Path
import unittest

from audit_repo import Auditor


class DetectionRuleTests(unittest.TestCase):
    def rules_for(self, line: str) -> set[str]:
        auditor = Auditor(Path("/"), "full")
        auditor.scan_line(line, scope="test", path="fixture.txt", number=1)
        return {finding.rule for finding in auditor.findings}

    def test_lowercase_users_namespace_is_not_a_local_path(self) -> None:
        self.assertNotIn("local_path", self.rules_for('namespace = "/users/{actorId}/facts"'))

    def test_macos_user_path_is_detected_case_sensitively(self) -> None:
        self.assertIn("local_path", self.rules_for('path = "/Users/alice/project/file.txt"'))
        self.assertNotIn("local_path", self.rules_for('path = "/users/alice/project/file.txt"'))

    def test_linux_and_windows_user_paths_are_detected(self) -> None:
        self.assertIn("local_path", self.rules_for('path = "/home/alice/project/file.txt"'))
        self.assertIn("local_path", self.rules_for(r'path = "C:\users\alice\project\file.txt"'))
        self.assertIn("local_path", self.rules_for(r'json = "C:\\Users\\alice\\project\\file.txt"'))

    def test_dependency_distribution_domains_are_not_url_findings(self) -> None:
        self.assertFalse(self.rules_for('resolved = "https://registry.npmjs.org/pkg/-/pkg.tgz"')
                         & {"internal_url", "direct_ip_url"})
        self.assertFalse(self.rules_for('url = "https://files.pythonhosted.org/packages/archive.whl"')
                         & {"internal_url", "direct_ip_url"})

    def test_internal_and_private_endpoints_are_detected(self) -> None:
        self.assertIn("internal_url", self.rules_for("http://localhost:8787/api"))
        self.assertIn("internal_url", self.rules_for("https://10.0.0.8/private"))
        self.assertIn("internal_url", self.rules_for("https://service.internal/api"))
        self.assertIn("internal_url", self.rules_for("http://169.254.1.2/metadata"))

    def test_direct_public_ip_endpoint_is_detected_once(self) -> None:
        rules = self.rules_for("https://203.0.113.10/api")
        self.assertEqual({"direct_ip_url"}, rules & {"internal_url", "direct_ip_url"})


if __name__ == "__main__":
    unittest.main()
