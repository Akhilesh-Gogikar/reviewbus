# Accessibility

ReviewBus treats its CLI and generated HTML as functional interfaces.

## Baseline

- Reports use `header`, `main`, and labeled `section` landmarks with a single page-level heading.
- A visible-on-focus skip link supports keyboard navigation.
- Tables have captions, scoped column headers, and text labels; unowned state is never communicated by color alone.
- Links and focus targets retain a high-contrast visible outline.
- Suggested CODEOWNERS text remains selectable and copyable.
- Reports contain no scripts, animation, or remote assets. CLI data can be separated between stdout and stderr.

## Release checks

Before a tag, inspect the fixture report with keyboard-only navigation, browser zoom at 200%, a screen reader's landmark/heading/table navigation, and light plus forced-color/high-contrast modes. Check reading order, captions, focus, link contrast, and long path wrapping.

## Known limits

Wide tables may scroll horizontally at narrow widths, and dense reviewer lists can be verbose for screen readers. The static report has no interactive filtering. These tradeoffs avoid scripts and remote dependencies.

Report accessibility bugs with a synthetic fixture through the bug template. If the artifact includes sensitive person or repository data, use [SECURITY.md](../SECURITY.md).
