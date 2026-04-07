# X.skill

`X.skill` is an X-first self-learning and self-distillation system built on top of the core ideas in `karpathy/llm-wiki.md`.

It is centered on capturing signals from your personal X `For You` feed, filtering and distilling high-value content, and promoting the useful parts into durable memory.

In one line: it extends Karpathy's wiki-maintenance pattern into a personal X-based self-learning loop for memory formation.

This repository is the public-safe framework layer of that system. It deliberately excludes private memory, account sessions, captured feeds, API keys, and machine-specific automation state.

## Positioning

This project is best understood as a personal second-brain framework for X-driven learning, not a note-taking app or a generic feed reader.

## What Makes It Different

Most note systems stop at saving information. Most feed readers stop at helping you consume more.

`X.skill` is built around a different loop:

1. capture signals from your real X `For You` flow
2. compress strong posts into intelligence pages and learning notes
3. extract durable rules from repeated high-signal inputs
4. promote those rules into memory
5. reuse that memory in future work

The point is not to build a larger archive. The point is to build a system that learns from your feed and remembers what matters.

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
- starter scripts for local memory initialization and sync
- a public-safe learning demo flow using mock intake data
- a static dashboard generator
- docs for private X capture and dedicated-browser setup
- config templates instead of hard-coded personal paths

## Not Included

- personal memory contents
- browser profiles, cookies, or session state
- captured X, Reddit, or browser data
- API keys, tokens, or secrets
- private logs, launch agents, or machine-specific runtime files

## Quick Start

```bash
python3 scripts/init_memory.py
python3 scripts/memory_state_sync.py
python3 scripts/reddit_feed_refresh.py
python3 scripts/build_demo_dashboard.py
```

This runs the public-safe demo flow. It initializes local memory, generates learning pages from mock social-feed input, and builds a local dashboard.

If you want external paths, copy [`config/settings.example.json`](config/settings.example.json) to `config/settings.local.json` and replace the example values with your own local directories. If you skip local config, the scripts default to a private `.local-memory/` folder inside the repo.

The public repo does not ship real X sessions, browser profiles, or live capture scripts. Real X capture belongs in a private local runtime layer.

## Who This Is For

`X.skill` is for people who do ongoing knowledge work and want more than a note archive:

- builders who learn heavily from their own X `For You` timeline
- people who want a system that absorbs strong posts into memory instead of just bookmarking them
- people who want memory to affect later decisions, not just store old text
- users who prefer local files, markdown, and inspectable workflows over opaque hosted systems

## X-First Learning Model

`X.skill` is X-first in its intended design.

The core product idea is:

- observe your own X `For You` feed
- identify the posts that are actually worth keeping
- compress them into reflections, rules, and learning memory
- move the durable parts into your second brain

That makes it closer to a self-learning memory system than a generic feed reader or note vault.

In one line: Karpathy's `LLM Wiki` compiles static sources into a maintained wiki; `X.skill` extends that pattern into X-driven memory formation.

## X Capture And Memory Flow

In a real private setup, the X loop looks like this:

1. read your own X `For You` feed
2. identify the posts worth keeping
3. write intelligence, reflection, and learning-memory pages
4. promote durable judgments into memory
5. surface the current state in a local dashboard

The goal is not to save more tweets. The goal is to absorb the right tweets into your brain.

## X Dashboard

[`x-dashboard.html`](/Users/dengz/llm-wiki/web/x-dashboard.html) is the live learning dashboard for the personal X `For You` feed.

It sits between raw X input and durable memory, and shows:

- capture health and read status
- feed composition and topic density
- high-value learning candidates
- GitHub follow-up signals
- reflection notes and current conclusions
- a bilingual timeline of absorbed posts

It is not a normal feed reader. It is the learning surface where X posts are turned into memory candidates.

## How To Use X Capture

The public repository does not ship your real X session or private browser automation. Instead, the intended setup is:

1. create `config/settings.local.json`
2. point `memory_root` and `browser_profile_root` to private local directories outside Git
3. launch a dedicated automation browser with a separate profile
4. log into your own X account in that dedicated browser
5. keep the browser focused on the `For You` / home timeline
6. use your private capture layer to export visible posts into a local JSON file
7. feed that JSON into the same learning and memory workflow used by the public demo

The dedicated browser exists for one reason: keep your personal X login and automation state separate from the public repository and from your everyday browsing session.

For a fuller private-setup walkthrough, see [`wiki/analyses/x-private-capture-setup.md`](wiki/analyses/x-private-capture-setup.md).

## Public Demo

The public demo uses mock social-feed input because it is safe to publish. In a real private setup, the same learning loop is intended to run primarily on your own X `For You` capture stream.

## Documentation Map

- [`AGENTS.md`](AGENTS.md): operating rules for agent maintenance
- [`wiki/overview.md`](wiki/overview.md): wiki structure
- [`wiki/analyses/x-private-capture-setup.md`](wiki/analyses/x-private-capture-setup.md): how to run X capture with a private browser layer
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
