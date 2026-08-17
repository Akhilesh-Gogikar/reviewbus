# ReviewBus

[![CI](https://github.com/akigogikar/reviewbus/actions/workflows/ci.yml/badge.svg)](https://github.com/akigogikar/reviewbus/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/github/license/akigogikar/reviewbus)](LICENSE)

ReviewBus turns public pull-request files and submitted reviews into reproducible path ↔ reviewer maps. It highlights review concentration and unowned paths while keeping every suggestion inspectable and correctable.

**Status:** 0.1.0 alpha and private prelaunch. Historical public activity is not formal ownership, availability, employment, expertise, or performance.

## One-command usage

```sh
reviewbus analyze --input examples/public_repo.json --json report.json --html report.html --codeowners CODEOWNERS.suggested
```

## Install from source

ReviewBus supports Python 3.10–3.14 and has no runtime dependencies. CI tests every supported Python version on Linux and Python 3.14 on macOS and Windows.

```sh
git clone https://github.com/akigogikar/reviewbus.git
cd reviewbus
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
reviewbus --help
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

## Offline reproducible demo

```sh
python3 reviewbus.py analyze \
  --input examples/public_repo.json \
  --json /tmp/reviewbus.json \
  --html /tmp/reviewbus.html \
  --codeowners /tmp/CODEOWNERS.suggested
```

Expected output has three paths, two reviewers, and one unowned path. JSON and HTML omit generation timestamps and sort entities for reproducibility.

## Optional public fetch

```sh
# GITHUB_TOKEN is optional; when used, give it read-only public access.
python3 reviewbus.py fetch owner/repository --limit 25 --output /tmp/public-snapshot.json
python3 reviewbus.py analyze --input /tmp/public-snapshot.json --json /tmp/reviewbus.json --html /tmp/reviewbus.html
```

`fetch` rejects repositories reported as private. It reads the optional token from `GITHUB_TOKEN` (or the variable selected by `--token-env`) and never writes the token to an artifact. Fetching is bounded to one page of at most 100 items per endpoint.

## Metrics in 0.1

- latest qualifying `APPROVED` or `CHANGES_REQUESTED` review by a non-author, attributed to each changed path;
- minimum reviewers accounting for 80% of qualifying path-review events;
- reviewer/path counts, approval/change-request counts, average response time, and UTC activity span;
- paths with no qualifying event in the sample; and
- deterministic top-two reviewer and CODEOWNERS suggestions.

## Documentation and community

- Design: [architecture](docs/ARCHITECTURE.md), [API stability](docs/API_STABILITY.md), [privacy](docs/PRIVACY.md), and [accessibility](docs/ACCESSIBILITY.md)
- Use: [troubleshooting](docs/TROUBLESHOOTING.md) and [launch kit](docs/LAUNCH_KIT.md)
- Direction: [roadmap](ROADMAP.md), [changelog](CHANGELOG.md), and [governance](GOVERNANCE.md)
- Participate: [contributing](CONTRIBUTING.md), [code of conduct](CODE_OF_CONDUCT.md), and [support](SUPPORT.md)
- Safety: [security policy](SECURITY.md), [scope](SCOPE.md), and [provenance](PROVENANCE.md)
- Related optional projects: [ecosystem](ECOSYSTEM.md)

## Test

```sh
python3 -m unittest discover -s tests -v
```

## Honest limitations and non-goals

One qualifying review is attributed to every changed path, so large pull requests carry more path events. v0 does not model renames, teams, branch protection, review dismissal, merge authority, or complete pagination. UTC activity is not a location inference. “Unowned” means only that the analyzed sample has no qualifying event.

Do not use ReviewBus for employee ranking, maintainer shaming, automatic assignment, issue closure, or governance decisions. Private repositories are out of scope.

Released under the [MIT License](LICENSE).
