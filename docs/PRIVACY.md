# Privacy

Offline analysis reads only the selected JSON bundle and writes requested artifacts. It sends no telemetry and loads no remote assets.

Optional `fetch` makes read-only HTTPS requests for public repository and pull-request metadata. A token is read from the selected environment variable and sent only as an authorization header; it is not serialized. Use the least-privilege token available and prefer no token when rate limits allow.

Public metadata can still identify people and expose sensitive social patterns. Minimize the sample, store snapshots/reports according to your retention policy, and do not combine output with employment or private-repository data. Review HTML/JSON before sharing.

Generated HTML is self-contained and script-free. CODEOWNERS suggestions are historical heuristics; correct them before use.
