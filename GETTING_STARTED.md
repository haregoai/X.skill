# Getting Started

This guide has two paths:

- `Demo Mode`: run the repo in a few minutes with the included example data
- `Private X Mode`: process your own local X home export safely

## Privacy First

Never commit:

- browser profiles
- cookies or session files
- real X exports
- API keys
- private logs

Keep your real X session and export workflow outside Git.

## Demo Mode

Run:

```bash
./setup.sh
```

What it does:

- initializes local memory
- processes the included X home example JSON
- processes the included Reddit example JSON
- builds the local dashboard

Then open:

- `web/assistant-dashboard.html`
- `wiki/analyses/x-home-intelligence.md`
- `wiki/analyses/x-home-learning-memory.md`

## Private X Mode

1. Copy `config/settings.example.json` to `config/settings.local.json`.
2. Point `memory_root` and `browser_profile_root` to private local directories.
3. Launch your dedicated X browser profile.
4. Log into X and keep the browser on the home timeline.
5. Export visible posts to a local JSON file.
6. Run:

```bash
./scripts/run_x_pipeline.sh /absolute/path/to/x-home-visible-posts.json
```

This updates:

- `wiki/analyses/x-home-intelligence.md`
- `wiki/analyses/x-home-learning-memory.md`
- `web/assistant-dashboard.html`

## Expected JSON Shape

Your local X export should be a JSON list. Each item can contain:

```json
{
  "author": "Author Name",
  "handle": "@handle",
  "text": "Visible post text",
  "link": "https://x.com/.../status/...",
  "hrefs": ["https://x.com/..."]
}
```

See `raw/inbox/x-home-visible-posts.example.json` for a public-safe example.

## Dedicated Browser

Use a separate browser profile for X automation. The pattern is documented in:

- `wiki/analyses/x-private-capture-setup.md`

## Troubleshooting

- If the pipeline runs but pages stay unchanged, check whether your JSON export path is correct.
- If you are debugging login, do it in the visible dedicated browser first.
- If you are handling real X data, keep it in a private local directory and do not move it into the public repo.
