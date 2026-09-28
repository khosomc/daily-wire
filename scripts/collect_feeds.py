#!/usr/bin/env python3
"""Collect headlines and summaries from the RSS/Atom feeds in feeds.json.

Runs on GitHub Actions every two hours. Items are merged into
feeds/YYYY-MM-DD.json (date in Pakistan time) and de-duplicated by link.
feeds/status.json records which feeds worked on the latest run.
Only what publishers put in their feeds is stored: title, short
description, date and link. Standard library only.
"""
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "feeds"
PKT = timezone(timedelta(hours=5))
KEEP_DAYS = 14
SUMMARY_MAX = 320
UA = "DailyWireFeedReader/1.0 (+https://github.com/khosomc/daily-wire)"

KEYWORDS = re.compile(
    r"pakistan|islamabad|karachi|lahore|peshawar|quetta|rawalpindi|balochistan|baluchistan|"
    r"khyber|pakhtunkhwa|sindh|gilgit|kashmir|imran khan|shehbaz|sharif|bilawal|\bpti\b|"
    r"پاکستان|اسلام آباد|کراچی|لاہور|پشاور|کوئٹہ|بلوچستان|خیبر|سندھ", re.I)

NS = {"atom": "http://www.w3.org/2005/Atom", "rss1": "http://purl.org/rss/1.0/",
      "dc": "http://purl.org/dc/elements/1.1/", "content": "http://purl.org/rss/1.0/modules/content/"}


def clean(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(re.sub(r"\s+", " ", text)).strip()
    if len(text) > SUMMARY_MAX:
        text = text[:SUMMARY_MAX].rsplit(" ", 1)[0] + "…"
    return text


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    try:
        d = parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(PKT)


def text_of(el, *paths):
    for p in paths:
        found = el.find(p, NS)
        if found is not None:
            if found.text and found.text.strip():
                return found.text
            if found.get("href"):
                return found.get("href")
    return ""


def parse_feed(xml_bytes):
    root = ET.fromstring(xml_bytes)
    items = []
    # RSS 2.0
    for it in root.iter("item"):
        items.append((text_of(it, "title"), text_of(it, "link", "guid"),
                      text_of(it, "description", "content:encoded"),
                      text_of(it, "pubDate", "dc:date")))
    # RSS 1.0 / RDF
    for it in root.iter(f"{{{NS['rss1']}}}item"):
        items.append((text_of(it, "rss1:title"), text_of(it, "rss1:link"),
                      text_of(it, "rss1:description"), text_of(it, "dc:date")))
    # Atom
    for it in root.iter(f"{{{NS['atom']}}}entry"):
        link = ""
        for l in it.findall("atom:link", NS):
            if l.get("rel") in (None, "alternate"):
                link = l.get("href", "")
                break
        items.append((text_of(it, "atom:title"), link,
                      text_of(it, "atom:summary", "atom:content"),
                      text_of(it, "atom:published", "atom:updated")))
    return items


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml, text/xml, */*"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def collect(feed, now):
    raw = parse_feed(fetch(feed["url"]))
    out = []
    for title, link, desc, date in raw:
        title, link = clean(title), (link or "").strip()
        if not title or not link.startswith("http"):
            continue
        summary = clean(desc)
        if feed.get("filter") and not KEYWORDS.search(f"{title} {summary}"):
            continue
        published = parse_date(date)
        if published and published < now - timedelta(days=2):
            continue
        out.append({
            "source": feed["name"], "lang": feed.get("lang", "en"), "title": title,
            "summary": summary, "link": link,
            "published": published.isoformat() if published else None,
            "collected": now.isoformat(timespec="minutes"),
        })
    return out, len(raw)


def main():
    now = datetime.now(PKT)
    config = json.loads((ROOT / "feeds.json").read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    day_file = OUT / f"{now:%Y-%m-%d}.json"
    existing = json.loads(day_file.read_text(encoding="utf-8")) if day_file.exists() else []
    seen = {i["link"] for i in existing}

    status, added = [], 0
    for feed in config["feeds"]:
        if not feed.get("enabled", True):
            continue
        try:
            items, total = collect(feed, now)
            new = [i for i in items if i["link"] not in seen]
            seen.update(i["link"] for i in new)
            existing.extend(new)
            added += len(new)
            status.append({"feed": feed["name"], "ok": True, "items_in_feed": total, "kept": len(items), "new": len(new)})
        except Exception as e:  # one broken feed must not stop the rest
            status.append({"feed": feed["name"], "ok": False, "error": f"{type(e).__name__}: {e}"[:200]})

    existing.sort(key=lambda i: i.get("published") or i["collected"], reverse=True)
    day_file.write_text(json.dumps(existing, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "status.json").write_text(json.dumps(
        {"run": now.isoformat(timespec="minutes"), "feeds": status}, ensure_ascii=False, indent=1), encoding="utf-8")

    cutoff = (now - timedelta(days=KEEP_DAYS)).strftime("%Y-%m-%d")
    for f in OUT.glob("20??-??-??.json"):
        if f.stem < cutoff:
            f.unlink()

    ok = sum(s["ok"] for s in status)
    print(f"{ok}/{len(status)} feeds OK, {added} new items -> {day_file.name}")
    for s in status:
        if not s["ok"]:
            print(f"  FAILED {s['feed']}: {s['error']}")
    if ok == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
