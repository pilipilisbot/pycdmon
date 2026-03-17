---
name: pycdmon-agent
description: Maintain and use the pycdmon repository and SDK (sync/async client, CLI, tests, docs). Use when implementing features, fixing bugs, updating endpoints, adding examples, or helping an agent execute repository tasks end-to-end with project-specific commands and quality checks.
---

# pycdmon Agent Skill

Follow this workflow to work safely and consistently in this repository.

## 1) Understand scope before editing

- Read `README.md` for supported operations and CLI examples.
- Read `src/pycdmon/` to locate the relevant client/service code.
- Read `tests/` to mirror existing testing style.
- Keep API key handling safe: never print or hardcode secrets.

## 2) Implement changes in package code

- Add or modify behavior in `src/pycdmon`.
- Preserve backward compatibility for existing public methods in minor updates.
- Prefer explicit typed methods and clear exceptions.

## 3) Keep tests aligned with behavior

- Add or update tests in `tests/` for success and failure paths.
- Keep tests deterministic and network-independent (mock HTTP).
- Cover both sync and async paths when the change affects both.

## 4) Keep docs and examples in sync

When behavior changes, update all impacted files in the same PR/commit set:

- `README.md` (quickstart, supported operations, CLI usage)
- `examples/` snippets
- `docs/` notes
- This skill file (`skills/pycdmon-agent/SKILL.md`) when workflow, commands, or supported features change

## 5) Validate before finishing

Run:

```bash
ruff check .
pytest
```

If a new command or feature is added, include at least one usage example (README or `examples/`).

## 6) Commit style

Use conventional commit prefixes defined in `AGENTS.md`:

- `feat:` new capability
- `fix:` bug fix
- `refactor:` internal only
- `docs:` documentation only
- `test:` tests only

Keep commits focused and descriptive.
