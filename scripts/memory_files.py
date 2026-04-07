#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from config import local_memory_root, repo_root


ROOT = repo_root()
MEM = local_memory_root()
GLOBAL = MEM / "global-memory.md"
STABLE = MEM / "stable-memory.md"
PROJECT = MEM / "project-memory.md"
VOLATILE = MEM / "volatile-memory.md"

DEFAULT_GLOBAL = f"""# Global Memory

This file is intended to be loaded at session start as a concise cross-project memory index.

## Memory Layers

- Stable memory: `{STABLE}`
- Project memory: `{PROJECT}`
- Volatile memory: `{VOLATILE}`

## Distilled Knowledge

- Memory state dashboard: `{ROOT / "wiki" / "analyses" / "memory-state-dashboard.md"}`
"""

DEFAULT_STABLE = """# Stable Memory

These are durable user preferences and long-lived working assumptions.

## User Preferences

## Practical Constraints

## Working Style

## System Rules
"""

DEFAULT_PROJECT = """# Project Memory

This layer stores durable facts about the current system.

## Assistant System Status

## Proven Capabilities

## Current Experimental Areas

## Default Direction
"""

DEFAULT_VOLATILE = """# Volatile Memory

These are current priorities and active working states that may change often.

## Dual Core Focus

## Current Operating Rules

## Current System Priorities
"""

MEMORY_DEFAULTS = {
    GLOBAL: DEFAULT_GLOBAL,
    STABLE: DEFAULT_STABLE,
    PROJECT: DEFAULT_PROJECT,
    VOLATILE: DEFAULT_VOLATILE,
}


def ensure_memory_files() -> None:
    MEM.mkdir(parents=True, exist_ok=True)
    for path, content in MEMORY_DEFAULTS.items():
        if path.exists():
            continue
        path.write_text(content.strip() + "\n", encoding="utf-8")
