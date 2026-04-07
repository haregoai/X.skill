#!/usr/bin/env python3

from __future__ import annotations

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
STATE = AUTOMATION / "reddit-state.json"
INTELLIGENCE = ANALYSES / "reddit-ml-intelligence.md"
LEARNING = ANALYSES / "reddit-ml-learning-memory.md"
HISTORY = WEB / "reddit-history.json"
ARCHIVE = WEB / "reddit-archive.json"

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
    "benchmark",
    "reasoning",
    "research",
    "automation",
    "model",
    "models",
    "inference",
    "training",
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


def settings_input_path() -> Path:
    settings = load_settings()
    raw_value = (
        settings.get("reddit", {}).get("mock_input")
        or "raw/inbox/reddit-ml-visible-posts.example.json"
    )
    candidate = Path(raw_value).expanduser()
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate


def load_posts() -> list[dict]:
    path = settings_input_path()
    data = load_json(path, [])
    if not isinstance(data, list):
        raise RuntimeError(f"reddit mock input is not a JSON list: {path}")
    posts: list[dict] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        title = clean_text(item.get("title", ""))
        text = clean_text(item.get("text", ""))
        link = clean_text(item.get("link", ""))
        hrefs = [clean_text(href) for href in item.get("hrefs", []) if clean_text(href)]
        if not (title or text):
            continue
        posts.append({"title": title, "text": text, "link": link, "hrefs": hrefs})
    return posts


def english_gist(text: str) -> str:
    return clean_text(text)[:220]


def reflection_for_post(post: dict) -> str:
    text = (post.get("title", "") + " " + post.get("text", "")).lower()
    if "memory" in text or "retrieval" in text:
        return "Worth absorbing if it changes how memory promotion or retrieval should work, not if it only adds another summary pattern."
    if "benchmark" in text or "evaluation" in text:
        return "Useful when it adds a way to verify whether the system is actually learning instead of only storing more text."
    if "workflow" in text or "agent" in text:
        return "High-signal when the idea can become a default workflow rule or a reusable operator pattern."
    return "Keep only the part that transfers into behavior, tooling, or judgment."


def memory_rule_for_post(post: dict) -> str:
    text = (post.get("title", "") + " " + post.get("text", "")).lower()
    if "memory" in text:
        return "Promote Reddit ideas only when they strengthen durable memory or retrieval behavior."
    if "benchmark" in text:
        return "Prefer external ideas that improve evaluation, not just feature count."
    if "workflow" in text or "agent" in text:
        return "Convert workflow discussions into explicit operating rules, not loose inspiration."
    return "Keep only Reddit signals that change defaults, tooling, or judgment."


def score_post(post: dict) -> dict:
    text = clean_text(post.get("text", ""))
    lowered = f"{post.get('title', '')} {text}".lower()
    ai_score = sum(1 for keyword in AI_KEYWORDS if keyword in lowered)
    github_links = [href for href in post.get("hrefs", []) if "github.com/" in href]
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
        bullet = f"Reddit reflection: {post['memory_rule']}"
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
                        f"- title: `{post['title']}`",
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
title: Reddit MachineLearning Intelligence
type: analysis
status: active
created: 2026-04-07
updated: 2026-04-07
source_files:
  - {source_rel}
tags:
  - analysis
  - reddit
  - learning
  - intelligence
---

This page is generated from a public-safe Reddit mock feed or a locally supplied Reddit export.

## Last Refresh

- timestamp: `{captured_at}`
- visible posts: `{len(posts)}`

{body}
"""
    INTELLIGENCE.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_learning_memory(posts: list[dict], source_path: Path) -> None:
    source_rel = source_path.relative_to(ROOT).as_posix()
    items = "\n".join(
        f"- `{post['title']}` | {post['memory_rule']}"
        for post in posts[:6]
    )
    content = f"""---
title: Reddit MachineLearning Learning Memory
type: analysis
status: active
created: 2026-04-07
updated: 2026-04-07
source_files:
  - {source_rel}
tags:
  - analysis
  - reddit
  - ai
  - learning
---

This page compresses Reddit inputs into reusable learning rules.

## Distilled Rules

{items if items else "- none yet"}
"""
    LEARNING.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    source_path = settings_input_path()
    posts = [score_post(post) for post in load_posts()]
    posts.sort(key=lambda item: (item["useful_score"], item["ai_score"]), reverse=True)
    captured_at = now_iso()
    new_posts = update_archive(posts, captured_at)
    snapshot = {
        "timestamp": captured_at,
        "checked_at": captured_at,
        "read_status": "read_ok",
        "content_status": "mock_demo_ready" if source_path.name.endswith(".example.json") else "read_ok",
        "visible_posts": len(posts),
        "ai_posts": len([post for post in posts if post["ai_score"] > 0]),
        "github_posts": len([post for post in posts if post["github_links"]]),
        "new_posts": new_posts,
        "last_error": "",
        "source_mode": "mock" if source_path.name.endswith(".example.json") else "local",
    }
    save_json(STATE, snapshot)
    update_history(snapshot)
    write_intelligence(posts, captured_at, source_path)
    write_learning_memory(posts, source_path)
    append_memory_rules(posts)
    print(STATE)


if __name__ == "__main__":
    main()
