# Daily Wire

A daily morning briefing on Pakistan's strategic affairs: geopolitics, conflict, defence, economy, finance and sovereignty.

- `editions/` — one JSON file per day (the content)
- `scripts/build.py` — turns editions into the website (`python3 scripts/build.py`)
- `docs/` — the generated site served by GitHub Pages (don't edit by hand)
- `CLAUDE.md` — the daily publishing routine, source rules and editorial rules
- `feeds.json` — the RSS feeds collected every two hours by GitHub Actions
- `feeds/` — collected feed items (last 14 days) and `status.json` showing which feeds worked

A new edition is written and published automatically every morning at about 07:00 Pakistan time. Yesterday's edition moves to the archive automatically.

## Editing an edition yourself
Open `editions/<date>.json` on GitHub, tap the pencil, change the text between the quotes and commit. The site rebuilds automatically within a minute or two (see the Actions tab). Keep the quotes and commas intact — if the build fails, the Actions tab shows why and the live site stays as it was.

## Hosting
GitHub → Settings → Pages → Source: *Deploy from a branch* → Branch `main`, folder `/docs`.
