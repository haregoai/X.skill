#!/bin/sh

set -eu

ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
INPUT_PATH="${1:-}"

cd "$ROOT"

python3 scripts/init_memory.py
python3 scripts/memory_state_sync.py

if [ -n "$INPUT_PATH" ]; then
  python3 scripts/x_home_feed_refresh.py --input "$INPUT_PATH"
else
  python3 scripts/x_home_feed_refresh.py
fi

python3 scripts/memory_state_sync.py
python3 scripts/build_demo_dashboard.py

printf '\nX pipeline completed.\n'
printf 'Open: %s\n' "$ROOT/web/assistant-dashboard.html"
