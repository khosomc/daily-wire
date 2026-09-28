# Daily Wire — instructions for Claude

Daily Wire is a static daily briefing on **Pakistan's strategic affairs** — where Pakistan sits in the world and how it pays its way — published every morning to GitHub Pages from the `docs/` folder. Written in British English.

## Editorial focus
Readers are analysts, diplomats, investors, journalists, students and diaspora professionals. Cover:
- **Geopolitics & Diplomacy** — Pakistan's relations with China, the US, the Gulf, Iran, Afghanistan, India, Central Asia, Europe; the SCO, UN, OIC and other bodies; visits, agreements, statements.
- **Conflict & Security** — regional and global conflicts Pakistan is part of or affected by (e.g. US–Iran, Afghanistan, India–Pakistan), militancy and insurgency, border incidents.
- **Defence** — armed forces, procurement, exercises, doctrine, defence agreements and cooperation.
- **Economy** — growth, inflation, trade, energy, the IMF programme, budgets and fiscal policy.
- **Finance & Capital** — markets (PSX), the rupee, FX reserves, debt and rollovers, credit ratings, FDI and investment flows, remittances.
- **Sovereignty** — borders and airspace, Kashmir, territorial and legal disputes, and economic sovereignty (lender conditions, debt dependence, foreign control of strategic assets).
- **Also today** — 3–4 one-line items of major domestic news (big political developments, mass-casualty events) so readers aren't blindsided.

Leave out sport, weather, entertainment and general crime unless they have a clear strategic or economic angle. For each story, the test is: *does this change Pakistan's position, security, money or room for manoeuvre?*

## How the site works
- Each edition is one file: `editions/YYYY-MM-DD.json` (date in Pakistan time, PKT/UTC+5).
- `python3 scripts/build.py` regenerates everything in `docs/`: the newest edition becomes the homepage, every edition gets a permanent page in `docs/archive/`, and `docs/archive/index.html` lists them all. **Never edit `docs/` by hand** — it is overwritten on each build.
- Archiving is automatic: adding today's JSON pushes yesterday's edition into the archive.
- A GitHub Actions job (`.github/workflows/collect-feeds.yml`) runs `scripts/collect_feeds.py` every two hours. It reads the publisher RSS feeds listed in `feeds.json` and saves each item's title, feed summary, date and link to `feeds/YYYY-MM-DD.json`. `feeds/status.json` shows which feeds worked on the last run.

## Sources

### Core — scan every day
- English (Pakistan): Dawn, The News, The Express Tribune, Business Recorder
- Urdu: Daily Jang (jang.com.pk), Daily Express (express.pk)
- International: Arab News Pakistan, Al Jazeera
- Regional: Khyber News (Khyber Pakhtunkhwa)
- Analysis/context (not breaking news): The Friday Times

### Use with care — second sources, or for stories the core misses
- Geo News: rewrite official labels neutrally (e.g. say "militants", attributing any "India-backed" claim to ISPR).
- Daily Times, The Nation, Samaa: fine as extra sources; ignore sensational wording.
- Nawa-i-Waqt: skip its crime and soft stories.
- Awami Awaz (Sindhi): use for Sindh politics and provincial news only.
- Profit (Pakistan Today): free articles only; skip anything marked premium.

### Feed-only sources (from `feeds/`)
BBC News, BBC Urdu, DW, DW Urdu, France 24, The Guardian and Independent Urdu block direct reading. Use them **only** through what their own RSS feeds provide in `feeds/<date>.json`. Never try to open their article pages another way (no mirrors, caches or alternative download tools). Summarise only from the feed's title and summary, attribute the claim to the outlet, and link to the original.

### Indian sources — short allowlist only
- News: The Hindu, The Indian Express, Scroll.in, The Wire.
- Research: Carnegie India, Takshashila Institution.
- Government-linked (label them, e.g. `"MP-IDSA (Indian govt-funded)"`, `"ORF (close to Indian govt)"`): use only to show Delhi's view.
- Use mainly for the Indian side of a story (Indian government statements, Indian data, India–Pakistan relations). **Never the only source for a claim about Pakistan's internal affairs.** Always attribute ("The Hindu reported…").
- Every other Indian outlet is excluded, including all TV news channels and their websites.

### Research institutes and data — for context, not daily news
Use these for storyline/background pages, fuller articles and figures that explain a story (e.g. "PIPS recorded X attacks in KP last year").
- Pakistani: PIDE, SDPI, Tabadlab, LUMS research centres, PIPS, CRSS, PILDAT, FAFEN, HRCP, Gallup Pakistan.
- International: International Crisis Group, Wilson Center (South Asia), Carnegie Endowment, USIP, Chatham House, Stimson Center, Atlantic Council (South Asia Center), ACLED, World Bank, IMF, ADB, UNDP, Human Rights Watch, Amnesty International, Freedom House, RSF, CPJ.
- Official data (allowed, not state media): Pakistan Bureau of Statistics, State Bank of Pakistan, Election Commission of Pakistan.
- Label government-linked Pakistani think tanks, e.g. `"ISSI (govt-linked)"`, `"IPRI (govt-linked)"`.
- Where it matters, say whose research it is (advocacy groups and government-funded institutes have perspectives).
- Always give the report's year ("a 2024 PIPS report found…"); don't present old findings as current.
- Summarise findings in your own words with a link to the report; no long quotes. Free-to-read reports only.

### Excluded
- Paywalled outlets and journals (e.g. FT, Bloomberg, The Economist, Nikkei, NYT, SCMP, paywalled parts of IISS).
- Indian outlets not on the allowlist above.
- State media (APP, Radio Pakistan, PTV) may be used only for official statements and must be labelled, e.g. `"name": "APP (state media)"`.

### Wire services
Reuters, AP and AFP stories that appear, credited, in a core outlet (e.g. "Reuters report in Dawn") may be used. Link to the article you read and mention the agency in the summary.

## Daily routine (the scheduled run)
1. Work out today's date in Asia/Karachi. If `editions/<today>.json` already exists, stop — the edition is already out.
2. `git pull` to get the latest collected feeds. Read `feeds/<today>.json` and `feeds/<yesterday>.json` and note which stories appear across several outlets.
3. Check the homepage of **every core source** (for this focus, lean especially on Dawn, Business Recorder, Profit, Arab News Pakistan, Al Jazeera and The Friday Times), then the "use with care" sources for anything big the core missed. Major casualty events, security incidents and major political developments must not be missed — if they have no strategic angle, they go in "Also today".
4. Pick **10–16 stories** that pass the focus test above, plus 3–4 "Also today" items. Sections, in this order, dropping any that are empty: Geopolitics & Diplomacy, Conflict & Security, Defence, Economy, Finance & Capital, Sovereignty, Also today. Where a story fits several sections, put it where its main consequence lies. "Also today" items are one sentence each.
5. Write each story as:
   - `headline`: your own wording, under ~12 words.
   - `summary`: 1–2 factual sentences **in your own words**. Never copy sentences from the source. No quotes longer than a few words.
   - `sources`: one or more `{"name", "url"}` pointing to the original article (not a homepage). For major political and security stories, prefer two outlets from different media groups (e.g. Dawn plus Jang or Express).
   - For non-English sources, translate into English and put the language in the source name, e.g. `"Jang (Urdu)"`, `"Awami Awaz (Sindhi)"`.
6. Write a 2–3 sentence `lead` on the day's main strategic themes — what moved in Pakistan's position abroad, its security and its money.
7. Save `editions/<today>.json` matching the schema of existing editions, then run `python3 scripts/build.py`. Fix any build errors it reports.
8. Commit (`Edition YYYY-MM-DD`), `git pull --rebase`, then push to `main`.
9. If `feeds/status.json` shows a feed failing, mention it in the final summary.

## Editorial rules
- Neutral, factual tone. Attribute claims ("ISPR said", "the ministry said"); don't state contested claims as fact.
- Apply the same bar to Pakistani and Indian sources: rewrite loaded labels from either side neutrally (e.g. "Indian-administered Kashmir" rather than "IIOJK", and "Pakistan-administered Kashmir" or "Azad Jammu and Kashmir" rather than "PoK"; "militants" rather than "India-backed terrorists" or "Pakistan-sponsored terrorists", attributing such claims to whoever made them).
- Skip celebrity gossip, sensational crime details and anything about identifiable victims of sexual violence.
- If a headline and its URL look mismatched on an outlet's page, open the article to confirm before using it, or leave it out.
- Don't invent URLs. If a story can't be linked to a real article, drop it.
