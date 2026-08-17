# Troubleshooting

## The command is not found

Run `python3 -m pip install .` inside the checkout and activate that virtual environment. Without installation, use `python3 reviewbus.py --help`.

## Public fetch receives an HTTP error

Confirm the repository is public and the `owner/name` spelling is correct. Anonymous requests have low rate limits; set a read-only `GITHUB_TOKEN` in the environment. Never put the token in a command argument, snapshot, or issue.

## A path is marked unowned

“Unowned” means no qualifying approval/change-request event was observed for that path in this sample. It does not mean nobody maintains the file. Expand the public sample or correct the suggestion manually.

## Reviewer counts look inflated

One qualifying review is attributed to each changed path. Large pull requests therefore contribute multiple path-review events by design. Inspect `paths[].reviewers` rather than treating the repository total as a count of review submissions.

## Times do not match a person's timezone

ReviewBus reports UTC submission hours only. It does not infer a location or timezone. Timestamps without an explicit timezone are rejected.
