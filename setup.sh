#!/bin/sh

set -eu

ROOT="$(CDPATH= cd -- "$(dirname "$0")" && pwd)"

cd "$ROOT"

if [ ! -f config/settings.local.json ]; then
  cp config/settings.example.json config/settings.local.json
fi

python3 scripts/init_memory.py
python3 scripts/memory_state_sync.py
python3 scripts/x_home_feed_refresh.py
python3 scripts/reddit_feed_refresh.py
python3 scripts/build_demo_dashboard.py

printf '\nSetup complete.\n'
printf 'Demo dashboard: %s\n' "$ROOT/web/assistant-dashboard.html"
printf 'To process your own X home export:\n'
printf '  ./scripts/run_x_pipeline.sh /absolute/path/to/x-home-visible-posts.json\n'
