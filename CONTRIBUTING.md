# Contributing to ReviewBus

ReviewBus maps historical public review activity without ranking people or declaring formal ownership. Contributions must preserve that distinction.

## Before opening a change

1. Read [SCOPE.md](SCOPE.md), [GOVERNANCE.md](GOVERNANCE.md), and [API stability](docs/API_STABILITY.md).
2. Explain how a metric can be inspected and corrected, and identify bias or false-inference risks.
3. Use only public specifications and synthetic review fixtures. Log every new source or fixture in [PROVENANCE.md](PROVENANCE.md).
4. Never submit private repository metadata, employment data, customer/partner material, access tokens, or identifiable incident records.

## Development check

```sh
python3 -m unittest discover -s tests -v
python3 reviewbus.py analyze --input examples/public_repo.json --json /tmp/reviewbus.json --html /tmp/reviewbus.html --codeowners /tmp/CODEOWNERS.suggested
```

Use Python 3.10–3.14 and standard-library runtime code. Keep reports deterministic and script-free. A new metric needs a definition, a focused test, and an explicit limitation.

## Pull requests

Keep the change narrow, describe compatibility and responsible-use effects, and list exact validation commands. By contributing, you agree that your contribution is provided under the MIT License and that you have the right to submit it.
