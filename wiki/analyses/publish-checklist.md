---
title: Publish Checklist
type: analysis
status: active
created: 2026-04-07
updated: 2026-04-07
tags:
  - analysis
  - release
  - privacy
---

## Checklist

- remove absolute personal paths
- remove private memory contents
- remove runtime state and generated logs
- remove browser profiles and session artifacts
- replace real data with mock examples
- replace machine-specific LaunchAgents with templates or docs
- verify `.gitignore` excludes local config and runtime files
- verify README does not imply the included data is real user memory
