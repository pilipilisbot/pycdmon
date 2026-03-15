# Contributing

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Quality checks

```bash
ruff check .
pytest
```

## Pull requests

- Keep PRs focused and small
- Add/adjust tests for behavior changes
- Document public API changes in README/docs
