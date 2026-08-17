# Contributing to ReviewBus

ReviewBus maps historical public review activity without ranking people or declaring formal ownership. Contributions must make results easier to reproduce, inspect, correct, or interpret while preserving that boundary.

## Pick a pathway

1. **First contribution — fixtures, docs, and report clarity.** Add a synthetic edge case, improve a diagnostic, or strengthen an accessibility assertion.
2. **Metric contributor — bounded computation.** Define the question, event unit, denominator, sample limitation, false inference, and correction path before writing code.
3. **Acquisition contributor — public fetch and normalization.** Preserve public-only validation, bounded requests, token privacy, snapshot reproducibility, and zero remote writes.
4. **Reviewer — sustained project care.** Contributors who repeatedly ship accurate, responsible work may be invited to triage or review related areas. Commit access is never automatic.

The current [issue seeds](docs/ISSUE_SEEDS.md) span all four pathways. Comment with a short approach before starting a multi-day item; assignment coordinates work but does not grant ownership of an idea.

## Before opening a change

1. Read [SCOPE.md](SCOPE.md), [GOVERNANCE.md](GOVERNANCE.md), and [API stability](docs/API_STABILITY.md).
2. Explain how a metric can be inspected and corrected, and identify bias or false-inference risks.
3. Use only public specifications and synthetic review fixtures. Log every source or fixture in [PROVENANCE.md](PROVENANCE.md).
4. Never submit private repository metadata, employment data, partner/customer material, access tokens, or identifiable incident records.

## Development check

Use Python 3.10–3.14 and standard-library runtime code.

```sh
python3 -m unittest discover -s tests -v
python3 reviewbus.py analyze --input examples/public_repo.json --json /tmp/reviewbus.json --html /tmp/reviewbus.html --codeowners /tmp/CODEOWNERS.suggested
```

Keep reports deterministic and script-free. A new metric needs a definition, focused test, and explicit limitation.

## Triage and review expectations

- A maintainer aims to acknowledge a well-scoped issue or pull request within seven days; this is a best-effort target, not an SLA.
- `good first issue` means the design is understood and localized. `help wanted` means the outcome is scoped but discussion may remain. `advanced` means privacy, bias, schema, pagination, or compatibility needs agreement first.
- Triage may request invented fixture data, split unrelated changes, or close proposals that score people or depend on private metadata.
- If there is no response after seven days, one concise follow-up is welcome. Do not post duplicate issues or contact people named in a report.

## Pull requests and recognition

Keep changes small. Link the issue, define metric/input/schema impact, explain privacy and false-inference controls, list provenance, and provide exact validation commands.

Merged contributors are credited in the next release notes unless they opt out. Sustained contributors may be invited to review related code and will be acknowledged for that work. No contribution volume guarantees a role.

By contributing, you agree that your work is provided under the MIT License and that you have the right to submit it.
