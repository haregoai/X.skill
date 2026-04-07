#!/usr/bin/env python3

from __future__ import annotations

import html
import json
from pathlib import Path

from config import repo_root


ROOT = repo_root()
STATE = ROOT / "automation" / "memory-state.json"
REDDIT_STATE = ROOT / "automation" / "reddit-state.json"
OUTPUT = ROOT / "web" / "assistant-dashboard.html"
MEMORY_PAGE = ROOT / "wiki" / "analyses" / "memory-state-dashboard.md"
REDDIT_INTELLIGENCE = ROOT / "wiki" / "analyses" / "reddit-ml-intelligence.md"
REDDIT_LEARNING = ROOT / "wiki" / "analyses" / "reddit-ml-learning-memory.md"


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    state = load_json(STATE, {})
    timestamp = str(state.get("timestamp", "unknown"))
    stable = str(state.get("stable_preferences", 0))
    project = str(state.get("proven_capabilities", 0))
    volatile = str(state.get("volatile_priorities", 0))
    duplicate = str(state.get("volatile_duplicate_bullets", 0))
    page_ref = MEMORY_PAGE.relative_to(ROOT).as_posix()
    reddit = load_json(REDDIT_STATE, {})
    reddit_visible = str(reddit.get("visible_posts", 0))
    reddit_ai = str(reddit.get("ai_posts", 0))
    reddit_source_mode = str(reddit.get("source_mode", "disabled"))
    reddit_status = str(reddit.get("content_status", "not_built"))
    reddit_page_ref = REDDIT_INTELLIGENCE.relative_to(ROOT).as_posix()
    reddit_learning_ref = REDDIT_LEARNING.relative_to(ROOT).as_posix()
    doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SignalOS Dashboard</title>
  <style>
    :root {{
      --bg: #f5f1e8;
      --panel: #fffaf2;
      --ink: #1e1a16;
      --muted: #6f6458;
      --line: #d9cdbf;
      --accent: #166534;
      --accent-2: #a16207;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Georgia, serif; background: linear-gradient(180deg, #efe7d8 0%, var(--bg) 100%); color: var(--ink); }}
    .shell {{ max-width: 980px; margin: 0 auto; padding: 32px 20px 56px; }}
    .hero, .panel {{ background: var(--panel); border: 1px solid var(--line); border-radius: 18px; padding: 20px; box-shadow: 0 10px 30px rgba(60,40,20,0.06); }}
    .hero h1 {{ margin: 0 0 8px; font-size: 42px; }}
    .hero p {{ margin: 0; color: var(--muted); }}
    .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 18px; }}
    .metric {{ padding: 16px; border-radius: 14px; background: #fff; border: 1px solid var(--line); }}
    .metric .label {{ display: block; color: var(--muted); font-size: 13px; margin-bottom: 8px; }}
    .metric .value {{ font-size: 28px; font-weight: 700; }}
    .row {{ margin-top: 18px; }}
    .small {{ color: var(--muted); font-size: 14px; }}
    .link-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; margin-top: 12px; }}
    .link-card {{ padding: 16px; border-radius: 14px; background: #fff; border: 1px solid var(--line); }}
    .label {{ color: var(--muted); font-size: 13px; display: block; margin-bottom: 6px; }}
    a {{ color: var(--accent); text-decoration: none; }}
    @media (max-width: 900px) {{ .grid, .link-grid {{ grid-template-columns: repeat(2, 1fr); }} .hero h1 {{ font-size: 34px; }} }}
    @media (max-width: 640px) {{ .grid, .link-grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <div class="shell">
    <section class="hero">
      <h1>SignalOS</h1>
      <p>A public-safe starter dashboard for a local second-brain scaffold.</p>
      <div class="grid">
        <div class="metric"><span class="label">Last Sync</span><span class="value">{html.escape(timestamp)}</span></div>
        <div class="metric"><span class="label">Stable Rules</span><span class="value">{html.escape(stable)}</span></div>
        <div class="metric"><span class="label">Project Facts</span><span class="value">{html.escape(project)}</span></div>
        <div class="metric"><span class="label">Volatile Priorities</span><span class="value">{html.escape(volatile)}</span></div>
      </div>
    </section>
    <section class="panel row">
      <h2>Notes</h2>
      <p class="small">This dashboard is generated from sanitized local memory state. Duplicate volatile bullets: <strong>{html.escape(duplicate)}</strong>.</p>
      <p class="small">Detailed state page: <code>{html.escape(page_ref)}</code></p>
    </section>
    <section class="panel row">
      <h2>Reddit Learning</h2>
      <div class="grid">
        <div class="metric"><span class="label">Visible Posts</span><span class="value">{html.escape(reddit_visible)}</span></div>
        <div class="metric"><span class="label">AI-Relevant</span><span class="value">{html.escape(reddit_ai)}</span></div>
        <div class="metric"><span class="label">Source Mode</span><span class="value">{html.escape(reddit_source_mode)}</span></div>
        <div class="metric"><span class="label">Status</span><span class="value">{html.escape(reddit_status)}</span></div>
      </div>
      <div class="link-grid">
        <div class="link-card">
          <span class="label">Intelligence Page</span>
          <code>{html.escape(reddit_page_ref)}</code>
        </div>
        <div class="link-card">
          <span class="label">Learning Memory</span>
          <code>{html.escape(reddit_learning_ref)}</code>
        </div>
      </div>
    </section>
  </div>
</body>
</html>
"""
    OUTPUT.write_text(doc, encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
