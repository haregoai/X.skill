---
title: X Private Capture Setup
type: analysis
status: active
created: 2026-04-07
updated: 2026-04-07
tags:
  - analysis
  - x
  - capture
  - private-runtime
---

This page explains how `X.skill` is intended to connect to a real personal X home feed without publishing private browser state.

## Design Rule

The public repository contains the learning framework.

Your real X session, browser profile, cookies, and capture runtime belong in a private local layer outside Git.

## Recommended Setup

1. Copy `config/settings.example.json` to `config/settings.local.json`.
2. Set `paths.memory_root` to a private local directory.
3. Set `paths.browser_profile_root` to a private local browser-profile directory.
4. Keep all live session data outside the repository.

## Dedicated Browser Pattern

Use a dedicated browser profile for X capture.

Why:

- it keeps your automation session separate from daily browsing
- it makes failures easier to debug
- it reduces the chance of leaking personal browser state into the repo

Minimum pattern:

1. create a private browser profile directory
2. launch Chrome or Chromium with that profile
3. expose a local remote-debugging port
4. log into X in that dedicated profile
5. open `https://x.com/home`

Example on macOS:

```bash
open -n -a "Google Chrome" --args \
  --user-data-dir="/private/path/to/x-browser-profile" \
  --remote-debugging-port=9223 \
  --remote-debugging-address=127.0.0.1 \
  --no-first-run \
  --no-default-browser-check \
  "https://x.com/home"
```

This command is only an example. The important part is the pattern: private profile, private session, local debugging port.

## Live Capture Workflow

The intended private X loop is:

1. open the dedicated browser on the X home timeline
2. keep that session logged in
3. use a private extractor to read visible posts from the page
4. export the visible posts to a local JSON file
5. pass that JSON into the learning and memory pipeline

The public repo does not include your real extractor or session. It only defines the learning side of the workflow.

## Local JSON Handoff

The clean boundary between private capture and public learning is a local JSON export.

For example:

- private runtime captures visible X posts
- private runtime writes `raw/inbox/x-home-visible-posts.json`
- `X.skill` reads the file and produces intelligence pages, reflection pages, and memory updates

This handoff keeps the public repository reusable without bundling anyone's private account state.

## Manual Login And Recovery

In practice, X capture often requires manual intervention:

- initial login
- password re-entry
- suspicious-login checks
- email or phone verification
- timeline not rendering correctly

That is normal. A real X setup should support two modes:

- background automation mode for routine capture
- visible browser mode for login, recovery, and debugging

## Public Safety Rule

Do not commit any of the following:

- browser profile directories
- cookies or session files
- raw captured X posts tied to a real person
- machine-specific launch agents
- private logs that reveal browsing behavior

Publish the framework. Keep the person private.
