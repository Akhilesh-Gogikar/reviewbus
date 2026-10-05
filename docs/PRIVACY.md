# Privacy

ReviewBus analyzes people's public review activity, so it collects as little as the metrics need and asks you to share even less.

## Network and storage

Offline analysis reads only the selected JSON bundle and writes requested artifacts. It sends no telemetry and loads no remote assets.

Optional `fetch` makes read-only HTTPS requests for public repository and pull-request metadata. A token is read from the selected environment variable and sent only as an authorization header; it is not serialized. Use the least-privilege token available and prefer no token when rate limits allow.

## Personal data in artifacts

- **Snapshots** from `fetch` contain, per pull request: number, creation time, author login, changed file paths, and each `APPROVED` or `CHANGES_REQUESTED` review's login, state, and submission time. Comment-only and pending reviews, names, emails, avatars, and review or comment text are not stored.
- **JSON and HTML reports** contain reviewer logins with per-reviewer event counts, approvals, change requests, reviewed paths, average response hours (from pull-request creation, not from a review request), UTC submission-hour counts, and UTC activity span.
- **CODEOWNERS suggestions** contain `@` mentions of reviewer logins.

ReviewBus does not pseudonymize logins. Remove or replace them before sharing if the audience does not need them.

## Responsible use

Do not use ReviewBus output for individual performance evaluation, hiring, compensation, promotion, discipline, or availability monitoring, and do not publish rankings or leaderboards of people. Per-reviewer figures describe one bounded sample of public activity; they are not a measure of anyone's performance, responsiveness, or working hours, and UTC submission hours can hint at a person's routine. Prefer sharing path-level results, which carry the review-coverage signal, over reviewer tables.

Public metadata can still identify people and expose sensitive social patterns. Minimize the sample, store snapshots and reports according to your retention policy, and do not combine output with employment or private-repository data. Review HTML and JSON before sharing.

Adding people to a real CODEOWNERS file makes GitHub request their reviews. Ask the people named before committing a suggestion.

Generated HTML is self-contained and script-free. CODEOWNERS suggestions are historical heuristics; correct them before use.
