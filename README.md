# ReviewBus

> **Private incubation repository. Do not publish or announce yet.**

ReviewBus turns public GitHub pull-request files and submitted reviews into a reproducible path ↔ reviewer map. It highlights review concentration and unowned paths, and emits suggestions—not governance decisions.

## Quickstart: offline fixture

Requires Python 3.10+ and no third-party packages.

```sh
cd /path/to/reviewbus
python3 reviewbus.py analyze \
  --input examples/public_repo.json \
  --json /tmp/reviewbus.json \
  --html /tmp/reviewbus.html \
  --codeowners /tmp/CODEOWNERS.suggested
```

The input is an offline, public-GitHub-shaped JSON bundle: `repository` plus `pull_requests`, each containing `files` and `reviews`. Output JSON and HTML intentionally omit generation timestamps and sort all entities for reproducibility.

## Optional public GitHub fetch

```sh
# GITHUB_TOKEN is optional but improves public API rate limits.
python3 reviewbus.py fetch octocat/Hello-World --limit 25 --output /tmp/github-snapshot.json
python3 reviewbus.py analyze --input /tmp/github-snapshot.json --json /tmp/reviewbus.json --html /tmp/reviewbus.html
```

The fetch command rejects repositories GitHub reports as private. It reads the optional token from `GITHUB_TOKEN` (or the environment variable named by `--token-env`) and never writes the token to an artifact.

## Metrics

- qualifying authority events: the latest `APPROVED` or `CHANGES_REQUESTED` review by a non-author on a pull request, attributed to each changed path;
- path and repository bus factor: the minimum reviewers accounting for at least 80% of qualifying path-review events;
- reviewer/path counts, approval/change-request counts, average response time, and UTC review-hour activity;
- unowned paths with no qualifying events;
- deterministic top-two reviewer and CODEOWNERS suggestions.

## Test

```sh
python3 -m unittest discover -s tests -v
```

## Limitations and responsible use

- Historical public activity is not formal ownership, current availability, employment, expertise, or performance. Review and correct every suggestion.
- Do not use this report to rank employees, shame maintainers, automatically assign work, or make governance decisions.
- v0 is file-path based; renames, deleted paths, branch protection, teams, CODEOWNERS history, review dismissal, and merge permissions are not modeled.
- GitHub fetch reads only one page (at most 100) of PRs, files, and reviews per endpoint. Large PRs can therefore be incomplete.
- UTC activity span is descriptive timing evidence, not a timezone or location inference.
- Unreviewed paths are “unowned” only within the analyzed sample.
- v0 accepts public repositories only and makes no attempt to scan private repositories.

See [SCOPE.md](SCOPE.md) and [PROVENANCE.md](PROVENANCE.md). No public license is granted while this repository is private.
