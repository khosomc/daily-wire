# Daily Wire

A short, daily digest of Pakistan's news, published each morning.

- `editions/` — one JSON file per day (the content)
- `scripts/build.py` — turns editions into the website (`python3 scripts/build.py`)
- `docs/` — the generated site served by GitHub Pages (don't edit by hand)
- `CLAUDE.md` — the daily publishing routine, source rules and editorial rules
- `feeds.json` — the RSS feeds collected every two hours by GitHub Actions
- `feeds/` — collected feed items (last 14 days) and `status.json` showing which feeds worked

A new edition is written and published automatically every morning at about 07:00 Pakistan time. Yesterday's edition moves to the archive automatically.

## Hosting
GitHub → Settings → Pages → Source: *Deploy from a branch* → Branch `main`, folder `/docs`.
