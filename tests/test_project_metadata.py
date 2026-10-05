import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import reviewbus  # noqa: E402


class ProjectMetadataTests(unittest.TestCase):
    def test_packaging_and_community_baseline(self):
        required = {
            "LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "SUPPORT.md",
            "GOVERNANCE.md", "ROADMAP.md", "CHANGELOG.md", "ECOSYSTEM.md", "docs/ARCHITECTURE.md",
            "docs/TROUBLESHOOTING.md", "docs/API_STABILITY.md", "docs/PRIVACY.md", "docs/ACCESSIBILITY.md",
            "docs/ISSUE_SEEDS.md", ".github/dependabot.yml", ".github/workflows/ci.yml",
            ".github/workflows/release.yml", ".github/pull_request_template.md",
            ".github/CODEOWNERS",
        }
        self.assertFalse([name for name in sorted(required) if not (ROOT / name).is_file()])
        metadata = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertRegex(metadata, rf'(?m)^version = "{re.escape(reviewbus.VERSION)}"$')
        self.assertRegex(metadata, r'(?m)^requires-python = ">=3\.10,<3\.15"$')
        self.assertIn('"Programming Language :: Python :: 3.14"', metadata)
        self.assertRegex(metadata, r"(?m)^dependencies = \[\]$")
        self.assertRegex(metadata, r'(?m)^license = "MIT"$')
        self.assertRegex(metadata, r'(?m)^reviewbus = "reviewbus:main"$')
        self.assertEqual("* @Akhilesh-Gogikar\n", (ROOT / ".github/CODEOWNERS").read_text(encoding="utf-8"))
        release_workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
        ci_workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn('"3.14"', ci_workflow)
        self.assertEqual(5, ci_workflow.count("os: ubuntu-latest"))
        self.assertEqual(1, ci_workflow.count("os: macos-latest"))
        self.assertEqual(1, ci_workflow.count("os: windows-latest"))
        self.assertIn("fail-fast: false", ci_workflow)
        self.assertIn("name: Python ${{ matrix.python }} on ${{ matrix.os }}", ci_workflow)
        self.assertIn('"3.14"', release_workflow)
        self.assertIn('tags: ["v*"]', release_workflow)
        self.assertIn("needs: test", release_workflow)
        self.assertNotIn("publish", release_workflow.lower())

    def test_relative_markdown_links_resolve(self):
        missing = []
        pattern = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)#]+)(?:#[^)]+)?\)")
        for document in sorted(ROOT.rglob("*.md")):
            if ".git" in document.parts:
                continue
            for target in pattern.findall(document.read_text(encoding="utf-8")):
                if not (document.parent / target).resolve().exists():
                    missing.append(f"{document.relative_to(ROOT)} -> {target}")
        self.assertEqual([], missing)

    def test_ecosystem_lists_only_public_tools(self):
        public = {"reviewbus", "releasefence"}
        text = (ROOT / "ECOSYSTEM.md").read_text(encoding="utf-8")
        self.assertIn("optional and informational", text)
        listed = re.findall(r"(?m)^- \[([^\]]+)\]\(https://github\.com/Akhilesh-Gogikar/([^)/]+)\)", text)
        self.assertEqual(public, {name for name, _ in listed})
        self.assertEqual(public, {repo for _, repo in listed})
        self.assertEqual(len(public), text.count("\n- "))
        # Unreleased sibling tools must not be named until they are public, so this guard uses an
        # allowlist of owner repositories instead of naming the unreleased ones.
        # ponytail: catches links and ECOSYSTEM entries, not a bare unlinked name elsewhere.
        linked = set()
        for document in sorted(ROOT.rglob("*")):
            folders = document.relative_to(ROOT).parts[:-1]
            if not document.is_file() or {"venv", "build", "dist", "node_modules"} & set(folders):
                continue
            if any(part.startswith(".") and part != ".github" for part in folders):
                continue
            if document.suffix in {".md", ".py", ".toml", ".yml", ".yaml", ".json", ".svg", ".txt", ".html", ".rst"}:
                body = document.read_text(encoding="utf-8")
                linked |= set(re.findall(r"(?i)github\.com/Akhilesh-Gogikar/([A-Za-z0-9_.-]+)", body))
        self.assertEqual(set(), {repo.lower().rstrip(".").removesuffix(".git") for repo in linked} - public)

    def test_issue_seeds_are_actionable(self):
        text = (ROOT / "docs/ISSUE_SEEDS.md").read_text(encoding="utf-8")
        self.assertEqual(5, text.count("**Issue:** [#"))
        for field in ("**Labels:**", "**Rationale:**", "**Acceptance criteria:**", "**Test plan:**", "**Skills:**", "**Estimated scope:**", "**Likely files:**"):
            self.assertEqual(5, text.count(field), field)


if __name__ == "__main__":
    unittest.main()
