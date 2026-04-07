# Contributing

Thanks for contributing to `X.skill`.

This repository is a public framework for building local second-brain systems. Contributions should make the framework more reusable without baking in anyone's private memory, personal workflow assumptions, or account-specific automation state.

## Contribution Rules

- Keep the public/private split intact.
- Do not commit real personal memory, browser data, sessions, or secrets.
- Prefer config-driven paths over machine-specific paths.
- Prefer generic examples and mock data over real captured feeds.
- Update docs when architecture or workflow changes.

## Good Contributions

- reusable ingestion patterns with fake data
- memory-layer improvements
- dashboard templates and generators
- schema design and documentation
- local tooling that writes back into markdown in a controlled way

## Changes To Avoid

- hard-coded absolute paths
- bundled browser profiles or session artifacts
- embedded API keys, tokens, or secret material
- docs that imply personal example data is part of the framework
- patches that only work for one machine layout

## Development

Typical local sanity checks:

```bash
python3 -m py_compile scripts/*.py
python3 scripts/init_memory.py
python3 scripts/memory_state_sync.py
python3 scripts/build_demo_dashboard.py
```

## Pull Requests

Before opening a PR:

1. read [`wiki/analyses/open-source-boundaries.md`](wiki/analyses/open-source-boundaries.md)
2. read [`wiki/analyses/publish-checklist.md`](wiki/analyses/publish-checklist.md)
3. verify that generated private state is still ignored
4. explain the public value of the change in the PR description

## Design Standard

This project values durable usefulness over novelty. A good patch should make it easier for someone else to build their own second brain, not expose the maintainer's personal one.
