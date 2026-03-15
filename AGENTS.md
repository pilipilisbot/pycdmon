# AGENTS.md

## Goal
Build and maintain a robust Python SDK for cdmon Domains & DNS API.

## Constraints
- Python >= 3.10
- Keep public API backward compatible in minor versions
- Prefer explicit, typed methods over generic wrappers
- No network-dependent tests (use mocking)

## Definition of done
- Public methods documented
- Tests cover success + failure paths
- `ruff check .` and `pytest` pass
- Changelog entry added (when `CHANGELOG.md` exists)

## Commit style
- feat: new capability
- fix: bug fix
- refactor: internal only
- docs: documentation only
- test: tests only

## Safety
Never print or hardcode API keys in code, docs, examples, tests, or logs.
