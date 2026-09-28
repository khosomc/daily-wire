# Daily Wire — instructions for Claude

Daily Wire is a static news digest for Pakistan, published every morning to GitHub Pages from the `docs/` folder. Written in British English.

## How the site works
- Each edition is one file: `editions/YYYY-MM-DD.json` (date in Pakistan time, PKT/UTC+5).
- `python3 scripts/build.py` regenerates everything in `docs/`: the newest edition becomes the homepage, every edition gets a permanent page in `docs/archive/`, and `docs/archive/index.html` lists them all. **Never edit `docs/` by hand** — it is overwritten on each build.
- Archiving is automatic: adding today's JSON pushes yesterday's edition into the archive.

## Daily routine (the scheduled run)
1. Work out today's date in Asia/Karachi. If `editions/<today>.json` already exists, stop — the edition is already out.
2. Gather news from roughly the last 24 hours using web search and by fetching outlet homepages: Dawn, The Express Tribune, The News, Geo, Business Recorder, The Nation, plus Reuters/AP/Al Jazeera for international angles.
3. Pick **12–20 stories** that matter to Pakistan. Use these sections in this order, dropping any that are empty: Politics, Security, Economy, Weather, Society, Region & World, Sport. Prefer stories with a confirmed article URL.
4. Write each story as:
   - `headline`: your own wording, under ~12 words.
   - `summary`: 1–2 factual sentences **in your own words**. Never copy sentences from the source. No quotes longer than a few words.
   - `sources`: one or more `{"name", "url"}` pointing to the original article (not a homepage), ideally from two outlets for major stories.
5. Write a 2–3 sentence `lead` summarising the day's main themes.
6. Save `editions/<today>.json` matching the schema of existing editions, then run `python3 scripts/build.py`. Fix any build errors it reports.
7. Commit (`Edition YYYY-MM-DD`) and push to `main`.

## Editorial rules
- Neutral, factual tone. Attribute claims ("ISPR said", "the ministry said"); don't state contested claims as fact.
- Skip celebrity gossip, sensational crime details and anything about identifiable victims of sexual violence.
- If a headline and its URL look mismatched on an outlet's page, open the article to confirm before using it, or leave it out.
- Don't invent URLs. If a story can't be linked to a real article, drop it.
