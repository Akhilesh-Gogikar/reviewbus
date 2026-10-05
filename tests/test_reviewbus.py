import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import reviewbus  # noqa: E402


class ReviewBusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads((ROOT / "examples" / "public_repo.json").read_text(encoding="utf-8"))

    def test_builds_path_reviewer_graph_and_bus_factor(self):
        report = reviewbus.analyze_bundle(self.fixture)
        self.assertEqual(3, report["summary"]["paths"])
        self.assertEqual(1, report["summary"]["unowned_paths"])
        self.assertEqual(2, report["summary"]["review_authority_bus_factor_80"])
        paths = {row["path"]: row for row in report["paths"]}
        self.assertEqual(2, paths["src/core.py"]["review_authority_bus_factor_80"])
        self.assertEqual(["fixture-reviewer-a", "fixture-reviewer-b"], paths["src/core.py"]["suggested_reviewers"])
        self.assertTrue(paths["scripts/release.py"]["unowned"])
        self.assertIn("# /scripts/release.py needs an owner", report["suggested_codeowners"])

    def test_output_is_stable_when_pull_order_changes(self):
        reversed_fixture = copy.deepcopy(self.fixture)
        reversed_fixture["pull_requests"].reverse()
        first = reviewbus.json_text(reviewbus.analyze_bundle(self.fixture))
        second = reviewbus.json_text(reviewbus.analyze_bundle(reversed_fixture))
        self.assertEqual(first, second)

    def test_rejects_private_or_ambiguous_visibility(self):
        private = copy.deepcopy(self.fixture)
        private["repository"]["private"] = True
        with self.assertRaises(reviewbus.ReviewBusError):
            reviewbus.analyze_bundle(private)
        ambiguous = copy.deepcopy(self.fixture)
        ambiguous["repository"].pop("private")
        ambiguous["repository"].pop("visibility")
        with self.assertRaises(reviewbus.ReviewBusError):
            reviewbus.analyze_bundle(ambiguous)

    @patch("reviewbus._github_json")
    def test_fetch_normalizes_public_github_responses(self, github_json):
        github_json.side_effect = [
            {"full_name": "octocat/Hello-World", "private": False},
            [{"number": 7, "created_at": "2026-01-01T00:00:00Z", "user": {"login": "octocat"}}],
            [{"filename": "README.md"}],
            [
                {"user": {"login": "fixture-reviewer-c"}, "state": "APPROVED", "submitted_at": "2026-01-01T01:00:00Z"},
                {"user": {"login": "fixture-reviewer-a"}, "state": "COMMENTED", "submitted_at": "2026-01-01T02:00:00Z"},
            ],
        ]
        snapshot = reviewbus.fetch_public_repository("octocat/Hello-World", limit=1)
        self.assertEqual("octocat/Hello-World", snapshot["repository"]["full_name"])
        self.assertEqual("README.md", snapshot["pull_requests"][0]["files"][0]["filename"])
        # Comment-only reviews are not analyzed, so the snapshot does not keep them.
        self.assertEqual(["fixture-reviewer-c"], [review["user"]["login"] for review in snapshot["pull_requests"][0]["reviews"]])
        self.assertEqual(4, github_json.call_count)

    def test_cli_writes_all_static_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            json_path, html_path, owners_path = root / "report.json", root / "report.html", root / "CODEOWNERS.suggested"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "reviewbus.py"),
                    "analyze",
                    "--input",
                    str(ROOT / "examples" / "public_repo.json"),
                    "--json",
                    str(json_path),
                    "--html",
                    str(html_path),
                    "--codeowners",
                    str(owners_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(3, json.loads(json_path.read_text(encoding="utf-8"))["summary"]["paths"])
            rendered = html_path.read_text(encoding="utf-8")
            self.assertIn("Path ↔ reviewer map", rendered)
            self.assertIn('class="skip-link"', rendered)
            self.assertIn("<caption>", rendered)
            self.assertNotIn("<script", rendered.lower())
            self.assertIn("not a performance, responsiveness, or availability measure", rendered)
            self.assertIn("/src/core.py @fixture-reviewer-a @fixture-reviewer-b", owners_path.read_text(encoding="utf-8"))

    def test_top_level_version_does_not_require_a_subcommand(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "reviewbus.py"), "--version"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("reviewbus 0.1.1\n", result.stdout)


if __name__ == "__main__":
    unittest.main()
