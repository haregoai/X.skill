#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from config import repo_root
from memory_files import GLOBAL, PROJECT, STABLE, VOLATILE, ensure_memory_files


ROOT = repo_root()
OUTPUT = ROOT / "wiki" / "analyses" / "memory-state-dashboard.md"
STATE = ROOT / "automation" / "memory-state.json"
GLOBAL_REL = GLOBAL.relative_to(ROOT)
STABLE_REL = STABLE.relative_to(ROOT)
PROJECT_REL = PROJECT.relative_to(ROOT)
VOLATILE_REL = VOLATILE.relative_to(ROOT)

PROMOTIONS = {
    STABLE: {
        "## User Preferences": [
            "Promote durable conclusions into memory instead of leaving them only in chat.",
            "Prefer reusable rules over one-off summaries.",
        ],
        "## System Rules": [
            "Treat external signals as hypotheses until they transfer into local behavior.",
        ],
    },
    PROJECT: {
        "## Proven Capabilities": [
            "The system can maintain layered memory in markdown files.",
            "The system can publish a sanitized framework while keeping personal memory private.",
        ],
    },
    VOLATILE: {
        "## Current Operating Rules": [
            "Keep the public framework generic and config-driven.",
        ],
        "## Current System Priorities": [
            "Turn useful patterns into templates, scripts, or checklists.",
        ],
    },
}


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def ensure_section(lines: list[str], heading: str) -> list[str]:
    if any(line.strip() == heading for line in lines):
        return lines
    if lines and lines[-1].strip():
        lines.append("")
    lines.extend([heading, ""])
    return lines


def add_bullets_to_section(lines: list[str], heading: str, bullets: list[str]) -> list[str]:
    lines = ensure_section(lines, heading)
    heading_index = next(i for i, line in enumerate(lines) if line.strip() == heading)
    insert_at = heading_index + 1
    while insert_at < len(lines) and not lines[insert_at].startswith("## "):
        insert_at += 1
    existing = {
        line.strip()[2:]
        for line in lines[heading_index + 1:insert_at]
        if line.strip().startswith("- ")
    }
    additions = [f"- {bullet}" for bullet in bullets if bullet not in existing]
    if not additions:
        return lines
    block = lines[heading_index + 1:insert_at]
    if block and block[-1].strip():
        block.append("")
    block.extend(additions)
    lines[heading_index + 1:insert_at] = block
    return lines


def normalize_blank_lines(lines: list[str]) -> list[str]:
    normalized: list[str] = []
    previous_blank = False
    for line in lines:
        blank = not line.strip()
        if blank and previous_blank:
            continue
        normalized.append(line)
        previous_blank = blank
    return normalized


def dedupe_bullet_lines(lines: list[str]) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            bullet = stripped[2:]
            if bullet in seen:
                continue
            seen.add(bullet)
        output.append(line)
    return output


def collect_bullets(lines: list[str], heading: str) -> list[str]:
    active = False
    items: list[str] = []
    for line in lines:
        if line.startswith("## "):
            active = line.strip() == heading
            continue
        if not active:
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:])
            continue
        match = re.match(r"^\d+\.\s+(.*)$", stripped)
        if match:
            items.append(match.group(1))
    return items


def file_age_hours(path: Path) -> float:
    modified = datetime.fromtimestamp(path.stat().st_mtime).astimezone()
    return round((datetime.now().astimezone() - modified).total_seconds() / 3600, 2)


def promote_memory_rules() -> None:
    ensure_memory_files()
    for path, sections in PROMOTIONS.items():
        lines = read_lines(path)
        for heading, bullets in sections.items():
            lines = add_bullets_to_section(lines, heading, bullets)
        lines = dedupe_bullet_lines(lines)
        path.write_text("\n".join(normalize_blank_lines(lines)).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    promote_memory_rules()
    stable_lines = read_lines(STABLE)
    project_lines = read_lines(PROJECT)
    volatile_lines = read_lines(VOLATILE)

    stable_prefs = collect_bullets(stable_lines, "## User Preferences")
    project_status = collect_bullets(project_lines, "## Proven Capabilities")
    volatile_priorities = collect_bullets(volatile_lines, "## Current System Priorities")
    volatile_bullets = [line.strip()[2:] for line in volatile_lines if line.strip().startswith("- ")]
    duplicate_count = len(volatile_bullets) - len(set(volatile_bullets))

    snapshot = {
        "timestamp": now_iso(),
        "stable_preferences": len(stable_prefs),
        "proven_capabilities": len(project_status),
        "volatile_priorities": len(volatile_priorities),
        "volatile_duplicate_bullets": duplicate_count,
        "ages_hours": {
            "global": file_age_hours(GLOBAL),
            "stable": file_age_hours(STABLE),
            "project": file_age_hours(PROJECT),
            "volatile": file_age_hours(VOLATILE),
        },
    }
    STATE.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    content = f"""---
title: Memory State Dashboard
type: analysis
status: active
created: 2026-04-07
updated: 2026-04-07
source_files:
  - {GLOBAL_REL}
  - {STABLE_REL}
  - {PROJECT_REL}
  - {VOLATILE_REL}
tags:
  - analysis
  - memory
  - dashboard
---

This page is generated by `scripts/memory_state_sync.py`.

## Last Sync

- timestamp: `{snapshot['timestamp']}`
- volatile duplicate bullets: `{snapshot['volatile_duplicate_bullets']}`

## Stable Layer

{chr(10).join(f"- {item}" for item in stable_prefs) if stable_prefs else "- none yet"}

## Project Layer

{chr(10).join(f"- {item}" for item in project_status) if project_status else "- none yet"}

## Volatile Priorities

{chr(10).join(f"- {item}" for item in volatile_priorities) if volatile_priorities else "- none yet"}

## Freshness

- global memory: `{snapshot['ages_hours']['global']}h`
- stable memory: `{snapshot['ages_hours']['stable']}h`
- project memory: `{snapshot['ages_hours']['project']}h`
- volatile memory: `{snapshot['ages_hours']['volatile']}h`
"""
    OUTPUT.write_text(content.rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
