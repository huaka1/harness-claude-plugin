# Project Memory

`.harness/context/` is the durable project memory. It is more important than cross-project personal memory for engineering work.

Use it to avoid repeating research and mistakes.

## Files

- `facts.md`: verified durable facts.
- `architecture.md`: current architecture and important coupling points.
- `commands.md`: commands that are known to work, with cwd/env if needed.
- `constraints.md`: project/user constraints.
- `decisions.md`: accepted/rejected decisions and rationale.
- `pitfalls.md`: failure patterns and corrections.
- `links.md`: authoritative links and when to re-check them.
- `glossary.md`: project terms.
- `lessons/`: dated deeper lessons when a short pitfall is not enough.

## Link Entry Template

```text
## <Topic>

- URL: <url>
- Why: <why this source matters>
- Applies to: <keywords>
- Last checked: YYYY-MM-DD
- Rule: <when future agents must re-open this link>
```

Prefer storing current links over copied external content when freshness matters.
