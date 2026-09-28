#!/usr/bin/env python3
"""Build the Daily Wire static site from editions/*.json into docs/.

- docs/index.html            -> newest edition
- docs/archive/YYYY-MM-DD.html -> every edition (permanent links)
- docs/archive/index.html    -> list of all editions

Archiving is automatic: add a new JSON file, run this script, and the
previous edition drops off the homepage into the archive.
Standard library only.
"""
import json
import sys
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDITIONS = ROOT / "editions"
OUT = ROOT / "docs"
SITE_NAME = "Daily Wire"
TAGLINE = "Pakistan's news, briefly — every morning"

CSS = """
:root{--bg:#faf8f3;--fg:#1c1b19;--muted:#6b675e;--line:#e3ded2;--accent:#01411c;--accent-soft:#e6efe8;--card:#fff}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121412;--fg:#ecebe6;--muted:#a19d93;--line:#2c302c;--accent:#6fcf8f;--accent-soft:#1b2a1f;--card:#191c19}}
:root[data-theme="dark"]{--bg:#121412;--fg:#ecebe6;--muted:#a19d93;--line:#2c302c;--accent:#6fcf8f;--accent-soft:#1b2a1f;--card:#191c19}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 "Source Serif 4",Georgia,serif}
a{color:inherit}
.wrap{max-width:760px;margin:0 auto;padding:0 16px}
header.mast{border-bottom:3px double var(--line);padding:28px 0 18px;text-align:center}
.mast .name{font:700 clamp(2.2rem,8vw,3.4rem)/1 "Playfair Display",Georgia,serif;letter-spacing:-.01em;margin:0;text-decoration:none;display:inline-block}
.mast .name span{color:var(--accent)}
.mast .tag{font:500 .8rem/1.4 Inter,system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-top:10px}
.dateline{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font:500 .82rem/1.4 Inter,system-ui,sans-serif;color:var(--muted);padding:10px 0;border-bottom:1px solid var(--line)}
.dateline a{color:var(--accent);text-decoration:none;font-weight:600}
.lead{font-size:1.12rem;margin:26px 0 8px;padding:16px 18px;background:var(--accent-soft);border-left:4px solid var(--accent);border-radius:2px}
section h2{font:700 .78rem/1 Inter,system-ui,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin:34px 0 4px;padding-bottom:8px;border-bottom:1px solid var(--line)}
article{padding:16px 0;border-bottom:1px solid var(--line)}
article:last-child{border-bottom:0}
article h3{font:700 1.22rem/1.3 "Playfair Display",Georgia,serif;margin:0 0 6px}
article p{margin:0 0 8px}
.src{font:500 .8rem/1.5 Inter,system-ui,sans-serif;color:var(--muted)}
.src a{color:var(--accent);text-decoration:none;border-bottom:1px solid transparent}
.src a:hover{border-bottom-color:var(--accent)}
ul.arch{list-style:none;padding:0;margin:24px 0}
ul.arch li{border-bottom:1px solid var(--line)}
ul.arch a{display:flex;justify-content:space-between;gap:12px;padding:14px 2px;text-decoration:none}
ul.arch .d{font:700 1.08rem/1.3 "Playfair Display",Georgia,serif}
ul.arch .n{font:500 .8rem/1.3 Inter,system-ui,sans-serif;color:var(--muted);white-space:nowrap;align-self:center}
footer{margin:40px 0 32px;padding-top:16px;border-top:3px double var(--line);font:400 .8rem/1.6 Inter,system-ui,sans-serif;color:var(--muted)}
footer a{color:var(--accent)}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700'
         '&family=Playfair+Display:wght@700&family=Source+Serif+4:wght@400;600&display=swap" rel="stylesheet">')


def fail(msg):
    sys.exit(f"build error: {msg}")


def load(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"{path.name}: invalid JSON ({e})")
    d = data.get("date")
    if d != path.stem:
        fail(f"{path.name}: 'date' must equal the file name ({path.stem})")
    try:
        date.fromisoformat(d)
    except ValueError:
        fail(f"{path.name}: bad date {d!r}")
    if not data.get("sections"):
        fail(f"{path.name}: no sections")
    for s in data["sections"]:
        if not s.get("name") or not s.get("stories"):
            fail(f"{path.name}: every section needs a name and stories")
        for st in s["stories"]:
            for key in ("headline", "summary", "sources"):
                if not st.get(key):
                    fail(f"{path.name}: story missing {key!r}: {st.get('headline')}")
            for src in st["sources"]:
                if not src.get("name") or not str(src.get("url", "")).startswith("http"):
                    fail(f"{path.name}: bad source in {st['headline']!r}")
    return data


def long_date(d):
    x = date.fromisoformat(d)
    return f"{x:%A} {x.day} {x:%B %Y}"


def story_count(ed):
    return sum(len(s["stories"]) for s in ed["sections"])


def page(title, body, prefix):
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(TAGLINE)}">
{FONTS}
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="mast">
<a class="name" href="{prefix}index.html">Daily <span>Wire</span></a>
<div class="tag">{escape(TAGLINE)}</div>
</header>
{body}
<footer>
Headlines are summarised in our own words with links to the original reporting. Read the full stories at their sources.
· <a href="{prefix}archive/index.html">Archive</a>
</footer>
</div>
</body>
</html>
"""


def edition_body(ed, prefix, is_latest):
    right = (f'<a href="{prefix}archive/index.html">Past editions →</a>' if is_latest
             else f'<a href="{prefix}index.html">Today\'s edition →</a>')
    parts = [f'<div class="dateline"><span>{long_date(ed["date"])} · {story_count(ed)} stories</span>{right}</div>']
    if ed.get("lead"):
        parts.append(f'<p class="lead">{escape(ed["lead"])}</p>')
    for s in ed["sections"]:
        parts.append(f'<section><h2>{escape(s["name"])}</h2>')
        for st in s["stories"]:
            links = " · ".join(
                f'<a href="{escape(src["url"])}" rel="noopener" target="_blank">{escape(src["name"])}</a>'
                for src in st["sources"])
            parts.append(f'<article><h3>{escape(st["headline"])}</h3>'
                         f'<p>{escape(st["summary"])}</p><div class="src">Source: {links}</div></article>')
        parts.append("</section>")
    return "\n".join(parts)


def main():
    files = sorted(EDITIONS.glob("*.json"))
    if not files:
        fail("no editions found in editions/")
    eds = [load(f) for f in files]
    eds.sort(key=lambda e: e["date"], reverse=True)
    latest = eds[0]

    (OUT / "archive").mkdir(parents=True, exist_ok=True)
    (OUT / ".nojekyll").write_text("")

    (OUT / "index.html").write_text(
        page(f"{SITE_NAME} — {long_date(latest['date'])}", edition_body(latest, "", True), ""), encoding="utf-8")

    for ed in eds:
        (OUT / "archive" / f"{ed['date']}.html").write_text(
            page(f"{SITE_NAME} — {long_date(ed['date'])}", edition_body(ed, "../", ed is latest), "../"),
            encoding="utf-8")

    items = "\n".join(
        f'<li><a href="{ed["date"]}.html"><span class="d">{long_date(ed["date"])}</span>'
        f'<span class="n">{story_count(ed)} stories</span></a></li>' for ed in eds)
    arch = (f'<div class="dateline"><span>Archive · {len(eds)} editions</span>'
            f'<a href="../index.html">Today\'s edition →</a></div><ul class="arch">{items}</ul>')
    (OUT / "archive" / "index.html").write_text(page(f"{SITE_NAME} — Archive", arch, "../"), encoding="utf-8")

    print(f"Built {len(eds)} edition(s); homepage = {latest['date']}")


if __name__ == "__main__":
    main()
