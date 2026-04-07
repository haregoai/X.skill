---
title: Open Source Boundaries
type: analysis
status: active
created: 2026-04-07
updated: 2026-04-07
tags:
  - analysis
  - privacy
  - publishing
---

This page defines what belongs in the public repository versus the private second-brain layer.

## Safe To Publish

- repo structure
- generic prompts and operating rules
- template scripts with config-driven paths
- fake or mock example data
- dashboard layouts that do not contain real captured content

## Keep Private

- personal memory files
- user profile, decisions, and private notes
- browser profiles, cookies, sessions, and captured social feeds
- tokens, API keys, secrets, proxy settings, and auth materials
- machine-specific scheduler files and private logs

## Design Rule

The open repository should export the framework, not the person.
