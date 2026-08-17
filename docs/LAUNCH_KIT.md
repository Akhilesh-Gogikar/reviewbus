# Launch kit

Use this only after the owner approves public visibility and every launch-day gate below passes. Copy describes 0.1.0 as it exists; never add adoption, benchmark, authority, or people-performance claims.

## Positioning

**One line:** Contributor count is not review coverage. Map paths that depend on too few reviewers.

**Short:** ReviewBus builds reproducible path ↔ reviewer maps from public review metadata and emits inspectable metrics plus correction-friendly suggestions.

**Differentiators:** offline-first analysis, path-level evidence instead of a contributor leaderboard, deterministic output, and explicit responsible-use limits around ownership, employment, location, and performance.

## Three-minute demo script

1. Say: “This describes one public metadata sample; it does not score people or declare owners.”
2. Run the offline fixture:

   ```sh
   python3 -m pip install .
   reviewbus analyze --input examples/public_repo.json --json /tmp/reviewbus.json --html /tmp/reviewbus.html --codeowners /tmp/CODEOWNERS.suggested
   ```

3. Show the summary: three paths, two reviewers, one unowned path.
4. In HTML, inspect `src/core.py` and explain the minimum reviewers covering 80% of qualifying events.
5. Open the CODEOWNERS suggestion and point out the correction warning plus the unowned-path comment.
6. End with limitations: bounded sample, path-event weighting, no teams/renames/merge authority, and no location or performance inference.

## Launch copy

### Hacker News

**Title:** Show HN: ReviewBus – reproducible path-to-reviewer maps from public metadata

**Text:** I built ReviewBus to test a narrower question than “how many contributors does this repository have?”: which changed paths repeatedly depend on the same reviewers in a defined public sample? The 0.1 CLI analyzes an offline JSON snapshot or optionally fetches bounded public metadata. It emits deterministic JSON, script-free HTML, and correction-friendly CODEOWNERS suggestions. It does not scan private repos, rank employees, infer location, or make assignments. The repository includes a synthetic three-path fixture; I would value feedback on metric definitions, missing sample context, and ways to make corrections clearer.

### Reddit

**Title:** I made an offline-first tool for mapping review bottlenecks by path

**Body:** ReviewBus 0.1 connects qualifying public review events to changed paths, then reports concentration, response time, an 80% review-authority bus factor, and paths with no observed reviewer in the sample. The output is deterministic and inspectable; suggestions are not ownership claims. I am looking for feedback on false inference risks, fixture coverage, and five scoped contributor issues.

### LinkedIn

Contributor totals can hide a smaller operational question: who has actually reviewed changes in each path of a public sample? ReviewBus 0.1 creates reproducible path/reviewer maps, concentration metrics, and correction-friendly suggestions from public review metadata. It is offline-first and deliberately does not score employees, infer location, scan private repositories, or automate assignments. The initial release includes a synthetic demo and clearly scoped contribution paths.

### X

ReviewBus 0.1 maps qualifying public review events to changed paths: deterministic JSON/HTML, concentration + 80% bus factor, unowned-path evidence, and correctable suggestions. Offline-first; no private repos, people ranking, location inference, or automatic assignment.

## FAQ

**Does a suggested reviewer own the path?** No. Suggestions summarize qualifying events in the selected sample and must be corrected before use.

**Does it scan private repositories?** No. 0.1 rejects inputs/fetches reported as private.

**Why attribute one review to every changed path?** The unit is a path-review event, not a review-submission count. This makes path coverage inspectable but gives larger changes more events.

**Does UTC activity reveal timezone or location?** No. It is a timestamp description only; location inference is an explicit non-goal.

**How do I contribute responsibly?** Start with synthetic data and one of the [issue seeds](ISSUE_SEEDS.md). Define the denominator, sample limit, false inference, and correction path for every metric.

## Launch-day checklist

- [ ] Public visibility explicitly approved after ownership, license, trademark, provenance, privacy, responsible-use, and security review.
- [ ] CI green on the documented Python/platform matrix; pinned actions and least-privilege permissions rechecked.
- [ ] Tag, version, changelog, package metadata, metric definitions, and fixture output agree on 0.1.0.
- [ ] Offline demo outputs exactly three paths, two reviewers, and one unowned path.
- [ ] HTML reviewed for keyboard, contrast, screen-reader, and wide-table behavior.
- [ ] Security advisory, issue forms, contributor links, and five issue seeds work from a signed-out view.
- [ ] Launch copy contains no adoption, performance, authority, or location claim not demonstrated by code.

## First 30 days

- **Days 1–2:** reproduce metric/output bugs with invented data; acknowledge well-scoped reports without debating lived maintainer experience.
- **Days 3–7:** summarize recurring sample-context and false-inference questions; fix wording before adding metrics.
- **Week 2:** guide contributors toward good-first fixtures/summary work, recognize merged work, and retire stale seeds.
- **Week 3:** review privacy, accessibility, fetch rate-limit behavior, and correction requests from public feedback.
- **Week 4:** publish a transparent note covering fixes, open risks, contributor credits, and unresolved metric questions. Traffic is not evidence of metric validity.

## Social preview and media

- Upload [the 1280 × 640 PNG](assets/social-preview.png) in **Settings → General → Social preview** immediately before the visibility change; GitHub does not read this repository file automatically.
- Keep the adjacent SVG as the editable source and follow the [asset notes](assets/README.md).
- Capture demos with synthetic inputs only. Remove usernames, home paths, tokens, partner names, and unrelated windows.
- Provide captions, a transcript, and descriptive alt text. Verify the README image, generated HTML, and demo at 200% zoom, by keyboard, and with a real screen reader before posting.
- Do not place download, adoption, company, performance, or compatibility counts on an asset unless the source and date are public and reproducible.

## Ethical cross-promotion

Cross-link only the seven related OSS tools named in ECOSYSTEM.md, and only where a link answers the reader's next technical question. Links stay optional, disclosed, and outside runtime output. Commercial products require exact owner-approved names, URLs, relationship wording, and trademark or partner permission before inclusion.
