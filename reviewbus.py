#!/usr/bin/env python3
"""ReviewBus: reproducible reviewer-authority maps from public GitHub metadata."""

from __future__ import annotations

import argparse
import html
import json
import math
import os
import re
import tempfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

VERSION = "0.1.0"
API_ROOT = "https://api.github.com"
AUTHORITY_STATES = {"APPROVED", "CHANGES_REQUESTED"}
LOGIN_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")


class ReviewBusError(ValueError):
    """Raised for invalid inputs or unavailable public GitHub data."""


def _parse_time(value: object, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ReviewBusError(f"{label} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ReviewBusError(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ReviewBusError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _login(node: object) -> str | None:
    if isinstance(node, dict):
        value = node.get("login")
    else:
        value = node
    return value if isinstance(value, str) and LOGIN_RE.fullmatch(value) else None


def _path(file_node: object) -> str | None:
    value = file_node.get("filename") if isinstance(file_node, dict) else file_node
    if not isinstance(value, str):
        return None
    normalized = value.strip().replace("\\", "/").lstrip("/")
    if not normalized or normalized.startswith("../") or "/../" in normalized or normalized == "..":
        return None
    return normalized


def _bus_factor_80(counts: Counter[str]) -> int:
    total = sum(counts.values())
    if not total:
        return 0
    target = math.ceil(total * 0.8)
    running = 0
    for index, count in enumerate(sorted(counts.values(), reverse=True), 1):
        running += count
        if running >= target:
            return index
    return len(counts)


def _mean(values: list[float]) -> float | None:
    return round(sum(values) / len(values), 2) if values else None


def _utc_span(hours: list[int]) -> int:
    unique = sorted(set(hours))
    if len(unique) < 2:
        return 0
    gaps = [(unique[(index + 1) % len(unique)] - hour) % 24 for index, hour in enumerate(unique)]
    return 24 - max(gaps)


def _validate_public_bundle(data: object) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not isinstance(data, dict):
        raise ReviewBusError("input must be a JSON object")
    repository = data.get("repository")
    pulls = data.get("pull_requests")
    if not isinstance(repository, dict) or not isinstance(pulls, list):
        raise ReviewBusError("input requires repository and pull_requests")
    full_name = repository.get("full_name")
    if not isinstance(full_name, str) or full_name.count("/") != 1:
        raise ReviewBusError("repository.full_name must be owner/name")
    if repository.get("private") is True or repository.get("visibility") not in (None, "public"):
        raise ReviewBusError("ReviewBus v0 accepts public repositories only")
    if repository.get("visibility") is None and repository.get("private") is not False:
        raise ReviewBusError("repository must explicitly declare visibility=public or private=false")
    if not all(isinstance(pull, dict) for pull in pulls):
        raise ReviewBusError("every pull request must be an object")
    return repository, pulls


def analyze_bundle(data: object) -> dict[str, object]:
    repository, pulls = _validate_public_bundle(data)
    path_events: dict[str, list[dict[str, object]]] = defaultdict(list)
    all_paths: set[str] = set()
    accepted_pulls = 0

    def pull_key(pull: dict[str, Any]) -> tuple[int, str]:
        number = pull.get("number")
        return (number if isinstance(number, int) else 2**31, str(number))

    for pull in sorted(pulls, key=pull_key):
        number = pull.get("number")
        if not isinstance(number, int):
            raise ReviewBusError("pull request number must be an integer")
        created = _parse_time(pull.get("created_at"), f"pull request {number}.created_at")
        files = pull.get("files", [])
        reviews = pull.get("reviews", [])
        if not isinstance(files, list) or not isinstance(reviews, list):
            raise ReviewBusError(f"pull request {number} files/reviews must be arrays")
        paths = sorted({candidate for item in files if (candidate := _path(item)) is not None})
        all_paths.update(paths)
        accepted_pulls += 1
        author = _login(pull.get("user"))
        latest: dict[str, tuple[datetime, str]] = {}
        for review in reviews:
            if not isinstance(review, dict):
                continue
            reviewer = _login(review.get("user"))
            state = str(review.get("state", "")).upper()
            if reviewer is None or reviewer == author or state not in AUTHORITY_STATES:
                continue
            submitted = _parse_time(review.get("submitted_at"), f"pull request {number} review submitted_at")
            if reviewer not in latest or submitted >= latest[reviewer][0]:
                latest[reviewer] = (submitted, state)
        for path in paths:
            for reviewer, (submitted, state) in sorted(latest.items()):
                path_events[path].append(
                    {
                        "reviewer": reviewer,
                        "state": state,
                        "latency_hours": max(0.0, (submitted - created).total_seconds() / 3600),
                        "utc_hour": submitted.hour,
                    }
                )

    reviewer_stats: dict[str, dict[str, object]] = defaultdict(
        lambda: {"events": 0, "approvals": 0, "change_requests": 0, "paths": set(), "latencies": [], "utc_hours": []}
    )
    path_rows: list[dict[str, object]] = []
    codeowners: list[str] = []
    total_counts: Counter[str] = Counter()
    unowned = 0
    for path in sorted(all_paths):
        events = path_events.get(path, [])
        counts = Counter(str(event["reviewer"]) for event in events)
        total = sum(counts.values())
        total_counts.update(counts)
        reviewer_rows = []
        for reviewer, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
            selected = [event for event in events if event["reviewer"] == reviewer]
            approvals = sum(event["state"] == "APPROVED" for event in selected)
            changes = sum(event["state"] == "CHANGES_REQUESTED" for event in selected)
            latencies = [float(event["latency_hours"]) for event in selected]
            hours = [int(event["utc_hour"]) for event in selected]
            reviewer_rows.append(
                {
                    "login": reviewer,
                    "authority_events": count,
                    "approvals": approvals,
                    "change_requests": changes,
                    "average_response_hours": _mean(latencies),
                    "review_hours_utc": sorted(Counter(hours).items()),
                }
            )
            aggregate = reviewer_stats[reviewer]
            aggregate["events"] = int(aggregate["events"]) + count
            aggregate["approvals"] = int(aggregate["approvals"]) + approvals
            aggregate["change_requests"] = int(aggregate["change_requests"]) + changes
            aggregate["paths"].add(path)
            aggregate["latencies"].extend(latencies)
            aggregate["utc_hours"].extend(hours)
        is_unowned = total == 0
        if is_unowned:
            unowned += 1
            suggestion: list[str] = []
            codeowners.append(f"# /{path} needs an owner")
        else:
            suggestion = [row["login"] for row in reviewer_rows[:2]]
            codeowners.append(f"/{path} " + " ".join("@" + login for login in suggestion))
        shares = [count / total for count in counts.values()] if total else []
        path_rows.append(
            {
                "path": path,
                "authority_events": total,
                "reviewer_count": len(counts),
                "review_authority_bus_factor_80": _bus_factor_80(counts),
                "top_reviewer_share": round(max(shares), 4) if shares else None,
                "concentration_hhi": round(sum(share * share for share in shares), 4) if shares else None,
                "unowned": is_unowned,
                "suggested_reviewers": suggestion,
                "reviewers": reviewer_rows,
            }
        )

    reviewers = []
    for login, stats in sorted(reviewer_stats.items()):
        reviewers.append(
            {
                "login": login,
                "authority_events": stats["events"],
                "approvals": stats["approvals"],
                "change_requests": stats["change_requests"],
                "paths_reviewed": sorted(stats["paths"]),
                "average_response_hours": _mean(stats["latencies"]),
                "review_hours_utc": sorted(Counter(stats["utc_hours"]).items()),
                "handoff_span_utc_hours": _utc_span(stats["utc_hours"]),
            }
        )
    path_count = len(path_rows)
    return {
        "schema_version": 1,
        "tool": "reviewbus",
        "tool_version": VERSION,
        "repository": {"full_name": repository["full_name"], "visibility": "public"},
        "summary": {
            "pull_requests": accepted_pulls,
            "paths": path_count,
            "reviewers": len(reviewers),
            "authority_events": sum(total_counts.values()),
            "unowned_paths": unowned,
            "owned_path_percentage": round(100 * (path_count - unowned) / path_count, 2) if path_count else 0.0,
            "review_authority_bus_factor_80": _bus_factor_80(total_counts),
        },
        "paths": path_rows,
        "reviewers": reviewers,
        "suggested_codeowners": codeowners,
        "methodology": {
            "authority_states": sorted(AUTHORITY_STATES),
            "bus_factor": "minimum reviewers accounting for at least 80% of qualifying path-review events",
            "warning": "Historical public review activity is not formal ownership, availability, employment, or performance.",
        },
    }


def json_text(report: dict[str, object]) -> str:
    return json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def codeowners_text(report: dict[str, object]) -> str:
    lines = [
        "# ReviewBus suggestions — review and correct before use.",
        "# Historical review activity is not formal ownership or availability.",
        *report["suggested_codeowners"],
    ]
    return "\n".join(lines) + "\n"


def html_text(report: dict[str, object]) -> str:
    path_rows = []
    for row in report["paths"]:
        reviewers = ", ".join("@" + str(login) for login in row["suggested_reviewers"]) or "Needs owner"
        path_rows.append(
            "<tr><th scope=\"row\"><code>" + html.escape(str(row["path"])) + "</code></th>"
            + f"<td>{row['authority_events']}</td><td>{row['review_authority_bus_factor_80']}</td>"
            + f"<td>{html.escape(reviewers)}</td><td>{'yes' if row['unowned'] else 'no'}</td></tr>"
        )
    reviewer_rows = []
    for row in report["reviewers"]:
        reviewer_rows.append(
            f"<tr><th scope=\"row\">@{html.escape(str(row['login']))}</th><td>{row['authority_events']}</td>"
            f"<td>{len(row['paths_reviewed'])}</td><td>{row['average_response_hours']}</td>"
            f"<td>{row['handoff_span_utc_hours']}</td></tr>"
        )
    summary = report["summary"]
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ReviewBus report</title><style>
body{{font:16px/1.5 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#17202a;background:#fff}}table{{border-collapse:collapse;width:100%;margin:0}}th,td{{border:1px solid #697176;padding:.45rem;text-align:left}}th{{background:#e8edef}}code,pre{{background:#f1f3f4;padding:.2rem .35rem;overflow:auto}}a{{color:#174f78}}a:focus-visible,.table-wrap:focus-visible{{outline:3px solid #6c3483;outline-offset:3px}}.warning{{border-left:.4rem solid #8a6d00;padding:.7rem;background:#fffbea}}.skip-link{{position:absolute;left:-10000px;top:auto}}.skip-link:focus{{left:1rem;top:1rem;background:#fff;padding:.5rem;z-index:1}}.table-wrap{{overflow-x:auto;margin:1rem 0}}@media(forced-colors:active){{.warning{{border-left-color:CanvasText}}}}
</style></head><body><a class="skip-link" href="#content">Skip to report content</a><header><h1>ReviewBus: {html.escape(str(report['repository']['full_name']))}</h1></header><main id="content">
<p>{summary['pull_requests']} pull requests · {summary['paths']} paths · {summary['reviewers']} reviewers · {summary['unowned_paths']} unowned paths</p>
<p>Repository review-authority bus factor (80%): <strong>{summary['review_authority_bus_factor_80']}</strong></p>
<p class="warning">Historical public review activity is not formal ownership, availability, employment, or performance. Correct these suggestions before use.</p>
<section aria-labelledby="path-map-heading"><h2 id="path-map-heading">Path ↔ reviewer map</h2><div class="table-wrap" role="region" aria-label="Scrollable path and reviewer metrics" tabindex="0"><table><caption>Observed review authority by changed path</caption><thead><tr><th scope="col">Path</th><th scope="col">Events</th><th scope="col">Bus factor</th><th scope="col">Suggestions</th><th scope="col">Unowned</th></tr></thead><tbody>{''.join(path_rows)}</tbody></table></div></section>
<section aria-labelledby="reviewer-heading"><h2 id="reviewer-heading">Reviewer metrics</h2><div class="table-wrap" role="region" aria-label="Scrollable reviewer metrics" tabindex="0"><table><caption>Observed reviewer activity in the analyzed sample</caption><thead><tr><th scope="col">Reviewer</th><th scope="col">Events</th><th scope="col">Paths</th><th scope="col">Avg response hours</th><th scope="col">UTC activity span</th></tr></thead><tbody>{''.join(reviewer_rows)}</tbody></table></div></section>
<section aria-labelledby="owners-heading"><h2 id="owners-heading">Suggested CODEOWNERS</h2><pre><code>{html.escape(codeowners_text(report))}</code></pre></section>
</main></body></html>
"""


def _write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def _github_json(url: str, token: str | None) -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"reviewbus/{VERSION}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    try:
        with urlopen(Request(url, headers=headers), timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReviewBusError(f"GitHub request failed: {type(exc).__name__}") from exc


def fetch_public_repository(full_name: str, limit: int = 25, token: str | None = None) -> dict[str, object]:
    if full_name.count("/") != 1 or not 1 <= limit <= 100:
        raise ReviewBusError("repository must be owner/name and limit must be 1..100")
    owner, name = full_name.split("/")
    slug = quote(owner, safe="") + "/" + quote(name, safe="")
    repository = _github_json(f"{API_ROOT}/repos/{slug}", token)
    if not isinstance(repository, dict) or repository.get("private") is not False:
        raise ReviewBusError("ReviewBus v0 fetches public repositories only")
    pulls = _github_json(
        f"{API_ROOT}/repos/{slug}/pulls?state=closed&sort=updated&direction=desc&per_page={limit}", token
    )
    if not isinstance(pulls, list):
        raise ReviewBusError("GitHub pull request response was not an array")
    normalized = []
    for pull in pulls[:limit]:
        if not isinstance(pull, dict) or not isinstance(pull.get("number"), int):
            continue
        number = pull["number"]
        files = _github_json(f"{API_ROOT}/repos/{slug}/pulls/{number}/files?per_page=100", token)
        reviews = _github_json(f"{API_ROOT}/repos/{slug}/pulls/{number}/reviews?per_page=100", token)
        normalized.append(
            {
                "number": number,
                "created_at": pull.get("created_at"),
                "user": {"login": _login(pull.get("user"))},
                "files": [
                    {"filename": item.get("filename")}
                    for item in files if isinstance(files, list) and isinstance(item, dict) and isinstance(item.get("filename"), str)
                ] if isinstance(files, list) else [],
                "reviews": [
                    {
                        "user": {"login": _login(item.get("user"))},
                        "state": item.get("state"),
                        "submitted_at": item.get("submitted_at"),
                    }
                    for item in reviews if isinstance(reviews, list) and isinstance(item, dict)
                ] if isinstance(reviews, list) else [],
            }
        )
    return {
        "repository": {"full_name": repository.get("full_name", full_name), "visibility": "public", "private": False},
        "pull_requests": sorted(normalized, key=lambda pull: pull["number"]),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="reviewbus", description=__doc__)
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze = subparsers.add_parser("analyze", help="analyze an offline GitHub-shaped JSON bundle")
    analyze.add_argument("--input", required=True, help="input path, or - for stdin")
    analyze.add_argument("--json", dest="json_path", default="-", help="report path, or - for stdout")
    analyze.add_argument("--html", dest="html_path", help="static HTML output path")
    analyze.add_argument("--codeowners", help="suggested CODEOWNERS output path")
    fetch = subparsers.add_parser("fetch", help="fetch a bounded snapshot from a public GitHub repository")
    fetch.add_argument("repository", help="owner/name")
    fetch.add_argument("--limit", type=int, default=25, help="closed pull requests to fetch (1..100)")
    fetch.add_argument("--output", default="-", help="snapshot path, or - for stdout")
    fetch.add_argument("--token-env", default="GITHUB_TOKEN", help="environment variable containing an optional token")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "fetch":
            snapshot = fetch_public_repository(args.repository, args.limit, os.environ.get(args.token_env))
            content = json.dumps(snapshot, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
            if args.output == "-":
                print(content, end="")
            else:
                _write_atomic(Path(args.output), content)
            return 0
        if args.input == "-":
            data = json.load(os.sys.stdin)
        else:
            data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        report = analyze_bundle(data)
        content = json_text(report)
        if args.json_path == "-":
            print(content, end="")
        else:
            _write_atomic(Path(args.json_path), content)
        if args.html_path:
            _write_atomic(Path(args.html_path), html_text(report))
        if args.codeowners:
            _write_atomic(Path(args.codeowners), codeowners_text(report))
        return 0
    except (OSError, json.JSONDecodeError, ReviewBusError) as exc:
        print(f"reviewbus: {exc}", file=os.sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
