# AGENTS

This repository is a public scaffold for a file-based second-brain system. It is intended to be maintained by coding agents and humans without leaking private memory into version control.

## Core Rule

Do not treat chat history as durable memory when the information belongs in the repository. Durable knowledge should be written into markdown or generated state files with clear ownership.

## Durable Layers

- `raw/`: immutable captured inputs and mock examples
- `wiki/`: distilled knowledge, architecture notes, and reusable judgments
- `scripts/`: controlled writeback logic and local helpers
- `automation/`: generated runtime state that is usually private and ignored
- `web/`: generated dashboard output

## Operating Principles

- promote durable findings into markdown
- prefer concise rules over archival sprawl
- separate framework code from personal data
- treat external signals as provisional until they transfer into behavior
- keep public examples generic and privacy-safe
- make local paths configurable instead of hard-coded

## Public / Private Split

Public:

- repository structure
- prompts, schemas, and workflow patterns
- generic scripts and templates
- sanitized example dashboards and docs

Private:

- memory contents tied to a real person
- browser profiles, cookies, and sessions
- captured social feeds or account-specific raw data
- API keys, secrets, proxies, and private automation logs

## Working Rules

- Update docs when the architecture changes.
- Keep generated local state out of Git.
- Prefer small, composable scripts over opaque automation.
- When adding ingestion examples, use mock data unless the source is explicitly public-safe.
- Before publishing, verify that no machine-specific or personal data paths remain.

## Resume Order

1. `README.md`
2. `AGENTS.md`
3. `wiki/overview.md`
4. `wiki/analyses/open-source-boundaries.md`
5. `wiki/analyses/publish-checklist.md`
6. `index.md`

## Publish Safety

Before open-sourcing changes, read [`wiki/analyses/publish-checklist.md`](wiki/analyses/publish-checklist.md).
