# SignalOS

`SignalOS` is a public scaffold for building a personal second-brain system.

It is designed around a simple idea: incoming information should not stop at capture or summarization. A useful second brain should help turn daily inputs into reusable judgments, working memory, and durable operating rules.

This repository is the public-safe framework layer. It deliberately excludes private memory, account sessions, captured feeds, API keys, and machine-specific automation state.

> A self-learning second brain built on the ideas behind `karpathy/llm-wiki.md`, designed to turn information flow into durable memory.

## Positioning

This project is best understood as a personal second-brain operating system, not a note-taking app.

It builds on the direction behind `karpathy/llm-wiki.md`: LLM systems should do more than answer questions against static notes. They should help compile repeated inputs into reusable knowledge. `SignalOS` pushes that idea toward a practical local workflow: capture information, reflect on it, distill it, and promote the parts that matter into durable memory.

## What This Project Is

This project is a file-based operating system for knowledge work. It separates:

- intake from synthesis
- durable memory from temporary runtime state
- public framework code from private personal data
- markdown knowledge from generated dashboards

It is meant to be forked and adapted to an individual's workflow, not used as a hosted product.

## Core Idea

The model behind this repo is:

1. capture external inputs
2. distill them into notes, analyses, and decisions
3. promote stable patterns into durable memory
4. expose the current state through a local dashboard
5. let agents write back into the system in a controlled way

The goal is not to build a larger archive. The goal is to build a system that can reuse what it has already learned.

## Architecture

```text
raw/         immutable captured inputs
wiki/        durable knowledge, analyses, concepts, and operating notes
scripts/     local automation helpers and controlled writeback logic
automation/  generated runtime state, logs, scheduler artifacts
web/         generated local dashboards
config/      local settings templates
templates/   reusable markdown and structure templates
```

## Repository Principles

- Keep the framework public and the person private.
- Prefer concise, reusable judgments over verbose note dumps.
- Treat external content as a hypothesis until it changes local behavior.
- Make all sensitive paths and providers configurable.
- Use markdown as the durable source of truth.

## Included

- a clean repo structure for a second-brain system
- starter scripts for private local memory initialization and sync
- a public-safe Reddit learning demo flow using mock intake data
- a static demo dashboard generator
- sanitized wiki docs that explain architecture and publishing boundaries
- config templates instead of hard-coded personal paths

## Not Included

- personal memory contents
- browser profiles, cookies, or session state
- captured X, Reddit, or browser data
- API keys, tokens, or secrets
- private logs, launch agents, or machine-specific runtime files

## Quick Start

1. Copy [`config/settings.example.json`](config/settings.example.json) to `config/settings.local.json`.
2. Replace the example values with your own local paths if you want an external memory directory.
3. Run the starter scripts:

```bash
python3 scripts/init_memory.py
python3 scripts/memory_state_sync.py
python3 scripts/reddit_feed_refresh.py
python3 scripts/build_demo_dashboard.py
```

4. Open the generated dashboard at `web/assistant-dashboard.html`.
5. Read [`AGENTS.md`](AGENTS.md) and [`wiki/overview.md`](wiki/overview.md) before extending the repo.

If you skip local config, the scripts default to a private `.local-memory/` folder inside the repo.

## What Works Out Of The Box

This repository runs successfully as a public-safe demo.

Out of the box, a fresh clone can:

- initialize local memory files
- generate a memory-state dashboard
- run the Reddit learning demo from mock JSON input
- generate intelligence and learning-memory markdown pages

Out of the box, a fresh clone does not:

- log into X, Reddit, or any browser session
- capture live social feeds automatically
- ship cookies, browser profiles, or account state

## How To Use It

Use this repo as the public framework layer, then keep your real second brain in one of these patterns:

- a private sibling repository
- a private local directory outside Git
- ignored local files referenced through `config/settings.local.json`

The safe rule is simple: publish structure, prompts, templates, and generic scripts. Do not publish your actual memory.

## Project Status

This repository is a starter framework, not a finished product. It currently includes:

- a layered memory model
- local memory initialization
- memory-state sync
- a public-safe Reddit learning demo flow
- a demo dashboard build step

It does not yet ship production-grade ingestion connectors or hosted infrastructure.

## If You Want Real Capture

If someone wants to capture real Reddit, X, or other feeds instead of using the included mock demo, they need to add their own private runtime layer.

That usually means:

1. create `config/settings.local.json`
2. point it at a private local memory directory outside Git
3. prepare a private browser or export workflow
4. supply local input data such as JSON exports or a custom connector
5. keep sessions, cookies, browser profiles, and logs out of the public repository

The recommended open-source pattern is:

- keep `SignalOS` as the public framework
- keep live capture scripts and account sessions in a private local layer
- feed sanitized exports or derived notes back into the public workflow

This repository intentionally demonstrates the learning system without publishing anyone's personal browsing state.

## Reddit Learning Flow

`SignalOS` now includes a public-safe Reddit learning example.

The included script:

- reads a mock or local JSON export of visible Reddit posts
- scores and filters posts for AI-relevant signal
- writes an intelligence page and a compressed learning-memory page
- promotes a small number of reusable rules into volatile memory
- exposes the result in the local dashboard

The default input file is [`raw/inbox/reddit-ml-visible-posts.example.json`](raw/inbox/reddit-ml-visible-posts.example.json). Forks can replace it with a private local export through `config/settings.local.json`.

## Documentation Map

- [`AGENTS.md`](AGENTS.md): operating rules for agent maintenance
- [`wiki/overview.md`](wiki/overview.md): wiki structure
- [`wiki/analyses/memory-schema.md`](wiki/analyses/memory-schema.md): memory layer design
- [`wiki/analyses/open-source-boundaries.md`](wiki/analyses/open-source-boundaries.md): what stays public vs private
- [`wiki/analyses/publish-checklist.md`](wiki/analyses/publish-checklist.md): pre-release safety checklist
- [`CONTRIBUTING.md`](CONTRIBUTING.md): contribution rules
- [`ROADMAP.md`](ROADMAP.md): planned directions
- [`SECURITY.md`](SECURITY.md): reporting and privacy guidance

## Contributing

Contributions should improve the framework without introducing private user data assumptions. Before sending changes, read [`CONTRIBUTING.md`](CONTRIBUTING.md) and make sure the patch keeps the public/private split intact.

## License

Released under the MIT License. See [`LICENSE`](LICENSE).
