#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
DEFAULT_SETTINGS = CONFIG_DIR / "settings.example.json"
LOCAL_SETTINGS = CONFIG_DIR / "settings.local.json"


def load_settings() -> dict:
    path = LOCAL_SETTINGS if LOCAL_SETTINGS.exists() else DEFAULT_SETTINGS
    return json.loads(path.read_text(encoding="utf-8"))


def repo_root() -> Path:
    return ROOT


def local_memory_root() -> Path:
    settings = load_settings()
    candidate = settings.get("paths", {}).get("memory_root") or str(ROOT / ".local-memory")
    if candidate.startswith("/absolute/path/to/"):
        candidate = str(ROOT / ".local-memory")
    return Path(candidate).expanduser()
