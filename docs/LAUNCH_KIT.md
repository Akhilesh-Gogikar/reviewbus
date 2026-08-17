# Launch kit

Use this only after the repository owner approves public visibility.

## Positioning

**Short:** Reproducible reviewer-authority maps from public metadata.

**Long:** ReviewBus turns public pull-request files and submitted reviews into deterministic path/reviewer maps, concentration metrics, unowned-path evidence, and correction-friendly suggestions—without scoring employee performance.

## Reproducible demo

```sh
python3 -m pip install .
reviewbus analyze --input examples/public_repo.json --json /tmp/reviewbus.json --html /tmp/reviewbus.html --codeowners /tmp/CODEOWNERS.suggested
```

Expected result: three paths, two reviewers, one unowned path, and no network request.

## Launch checklist

- Ownership, MIT license, trademark, provenance, privacy, responsible-use, and security reviews recorded.
- CI green on all documented Python/platform combinations.
- `v0.1.0` tag, changelog, methodology, and fixture agree.
- Report checked with keyboard and screen-reader navigation.
- Public fetch tested using a read-only token without logging it.
- Every claim distinguishes observed history from formal ownership and performance.

Do not market ReviewBus as an employee ranking system, availability oracle, or governance authority.
