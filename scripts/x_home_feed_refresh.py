#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from config import load_settings, repo_root
from memory_files import VOLATILE, ensure_memory_files


ROOT = repo_root()
ANALYSES = ROOT / "wiki" / "analyses"
AUTOMATION = ROOT / "automation"
WEB = ROOT / "web"
STATE = AUTOMATION / "x-home-state.json"
INTELLIGENCE = ANALYSES / "x-home-intelligence.md"
LEARNING = ANALYSES / "x-home-learning-memory.md"
HISTORY = WEB / "x-home-history.json"
ARCHIVE = WEB / "x-home-archive.json"

AI_KEYWORDS = [
    "agent",
    "agents",
    "ai",
    "llm",
    "gpt",
    "claude",
    "codex",
    "openai",
    "anthropic",
    "gemini",
    "memory",
    "retrieval",
    "workflow",
    "reasoning",
    "automation",
    "model",
    "models",
    "inference",
    "prompt",
    "wiki",
    "obsidian",
    "local",
]


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def save_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def default_input_path() -> Path:
    settings = load_settings()
    raw_value = settings.get("x", {}).get("export_input") or "raw/inbox/x-home-visible-posts.example.json"
    candidate = Path(raw_value).expanduser()
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process a local X home export into intelligence and memory pages.")
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Optional path to a local JSON export of visible X home posts.",
    )
    return parser.parse_args()


def normalize_post(item: dict) -> dict | None:
    author = clean_text(item.get("author", ""))
    handle = clean_text(item.get("handle", ""))
    title = clean_text(item.get("title", "")) or clean_text(f"{author} {handle}".strip())
    text = clean_text(item.get("text", ""))
    link = clean_text(item.get("link", ""))
    hrefs = [clean_text(href) for href in item.get("hrefs", []) if clean_text(href)]
    if not (title or text):
        return None
    return {
        "author": author,
        "handle": handle,
        "title": title,
        "text": text,
        "link": link,
        "hrefs": hrefs,
    }


def load_posts(input_path: Path) -> list[dict]:
    data = load_json(input_path, [])
    if not isinstance(data, list):
        raise RuntimeError(f"x home input is not a JSON list: {input_path}")
    posts: list[dict] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        normalized = normalize_post(item)
        if normalized:
            posts.append(normalized)
    return posts


def english_gist(text: str) -> str:
    return clean_text(text)[:220]


def reflection_for_post(post: dict) -> str:
    text = f"{post.get('title', '')} {post.get('text', '')}".lower()
    if "obsidian" in text or "second brain" in text or "memory" in text:
        return "Absorb only the part that changes how the second-brain system stores, promotes, or reuses knowledge."
    if "workflow" in text or "agent" in text or "automation" in text:
        return "Worth keeping when it can become a repeatable workflow rule instead of a one-off tactic."
    if "github.com/" in " ".join(post.get("hrefs", [])):
        return "Good candidate for local validation because there is code or a concrete artifact behind the claim."
    return "Keep only the transferable judgment, not the entire post."


def memory_rule_for_post(post: dict) -> str:
    text = f"{post.get('title', '')} {post.get('text', '')}".lower()
    if "memory" in text or "wiki" in text or "obsidian" in text:
        return "Promote X ideas only when they improve memory structure, retrieval, or durable reuse."
    if "workflow" in text or "agent" in text or "automation" in text:
        return "Convert X workflow ideas into explicit operating rules, not inspiration-only notes."
    if any("github.com/" in href for href in post.get("hrefs", [])):
        return "Validate code-backed X ideas locally before promoting them into durable memory."
    return "Keep only X signals that change defaults, judgment, or tooling."


def score_post(post: dict) -> dict:
    text = clean_text(post.get("text", ""))
    lowered = f"{post.get('title', '')} {text}".lower()
    ai_score = sum(1 for keyword in AI_KEYWORDS if keyword in lowered)
    github_links = [href for href in post.get("hrefs", []) if "github.com/" in href or "gist.github.com/" in href]
    useful_score = ai_score * 4 + len(github_links) * 5
    return {
        **post,
        "cleaned_text": text,
        "english_gist": english_gist(text),
        "ai_score": ai_score,
        "github_links": github_links,
        "useful_score": useful_score,
        "reflection": reflection_for_post(post),
        "memory_rule": memory_rule_for_post(post),
    }


def update_archive(posts: list[dict], captured_at: str) -> int:
    archive = load_json(ARCHIVE, [])
    by_link = {item.get("link"): item for item in archive if item.get("link")}
    new_posts = 0
    for post in posts:
        link = post.get("link") or f"synthetic:{post.get('title', '')[:80]}"
        existing = by_link.get(link)
        if existing:
            existing["seen_count"] = int(existing.get("seen_count", 1)) + 1
            existing["last_seen"] = captured_at
            continue
        by_link[link] = {
            "title": post.get("title", ""),
            "link": link,
            "english_gist": post.get("english_gist", ""),
            "ai_score": post.get("ai_score", 0),
            "useful_score": post.get("useful_score", 0),
            "first_seen": captured_at,
            "last_seen": captured_at,
            "seen_count": 1,
        }
        new_posts += 1
    merged = sorted(by_link.values(), key=lambda item: item.get("last_seen", ""), reverse=True)[:120]
    save_json(ARCHIVE, merged)
    return new_posts


def update_history(snapshot: dict) -> None:
    history = load_json(HISTORY, [])
    history.append(snapshot)
    save_json(HISTORY, history[-60:])


def append_memory_rules(posts: list[dict]) -> None:
    ensure_memory_files()
    lines = VOLATILE.read_text(encoding="utf-8").splitlines()
    heading = "## Current Operating Rules"
    if heading not in lines:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend([heading, ""])
    index = lines.index(heading) + 1
    while index < len(lines) and not lines[index].startswith("## "):
        index += 1
    existing = {line.strip()[2:] for line in lines if line.strip().startswith("- ")}
    additions = []
    for post in posts[:3]:
        bullet = f"X reflection: {post['memory_rule']}"
        if bullet not in existing:
            additions.append(f"- {bullet}")
    if additions:
        block_start = lines.index(heading) + 1
        block = lines[block_start:index]
        if block and block[-1].strip():
            block.append("")
        block.extend(additions)
        lines[block_start:index] = block
        VOLATILE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_intelligence(posts: list[dict], captured_at: str, source_path: Path) -> None:
    source_rel = source_path.relative_to(ROOT).as_posix()
    body = "\n".join(
        [
            "## Visible Posts",
            "",
            *[
                "\n".join(
                    [
                        f"- author: `{post.get('author', '')} {post.get('handle', '')}`".rstrip(),
                        f"  - link: `{post['link'] or 'mock-no-link'}`",
                        f"  - gist: {post['english_gist']}",
                        f"  - reflection: {post['reflection']}",
                    ]
                )
                for post in posts[:8]
            ],
        ]
    )
    content = f"""---
title: X Home Intelligence
type: analysis
status: active
created: 2026-04-07
updated: 2026-04-07
source_files:
  - {source_rel}
tags:
  - analysis
  - x
  - learning
  - intelligence
---

This page is generated from a local X home export.

## Last Refresh

- timestamp: `{captured_at}`
- visible posts: `{len(posts)}`

{body}
"""
    INTELLIGENCE.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_learning_memory(posts: list[dict], source_path: Path) -> None:
    source_rel = source_path.relative_to(ROOT).as_posix()
    items = "\n".join(
        f"- `{post.get('author', '')} {post.get('handle', '')}` | {post['memory_rule']}"
        for post in posts[:6]
    )
    content = f"""---
title: X Home Learning Memory
type: analysis
status: active
created: 2026-04-07
updated: 2026-04-07
source_files:
  - {source_rel}
tags:
  - analysis
  - x
  - learning
  - memory
---

This page compresses X home inputs into reusable learning rules.

## Distilled Rules

{items if items else "- none yet"}
"""
    LEARNING.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_path = args.input.expanduser() if args.input else default_input_path()
    if not input_path.is_absolute():
        input_path = (ROOT / input_path).resolve()
    posts = [score_post(post) for post in load_posts(input_path)]
    posts.sort(key=lambda item: (item["useful_score"], item["ai_score"]), reverse=True)
    captured_at = now_iso()
    new_posts = update_archive(posts, captured_at)
    snapshot = {
        "timestamp": captured_at,
        "checked_at": captured_at,
        "read_status": "read_ok",
        "content_status": "mock_demo_ready" if input_path.name.endswith(".example.json") else "read_ok",
        "visible_posts": len(posts),
        "ai_posts": len([post for post in posts if post["ai_score"] > 0]),
        "github_posts": len([post for post in posts if post["github_links"]]),
        "new_posts": new_posts,
        "last_error": "",
        "source_mode": "mock" if input_path.name.endswith(".example.json") else "local",
        "input_path": str(input_path),
    }
    save_json(STATE, snapshot)
    update_history(snapshot)
    write_intelligence(posts, captured_at, input_path)
    write_learning_memory(posts, input_path)
    append_memory_rules(posts)
    print(STATE)


if __name__ == "__main__":
    main()
