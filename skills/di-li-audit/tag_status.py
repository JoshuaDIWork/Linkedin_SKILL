#!/usr/bin/env python3
"""
tag_status.py - tag every post, ad, campaign or page LIVE or ARCHIVED before
anyone draws a conclusion from it.

An audit that ranks an archived ad next to a live one, or a plan that sends
readers to "/campaign/ai-fast-start-archived-july-2026", is working from the
wrong evidence. This script reads rows from a LinkedIn Ads export, a Windsor.ai
pull, a GA4 or HubSpot page report, or a hand-made CSV, and adds three
columns: status, reason, warning.

Statuses
  LIVE      running or published now
  STALLED   marked active but delivered nothing in the window
  PAUSED    paused by someone, may come back
  ENDED     finished on schedule (a COMPLETED campaign)
  ARCHIVED  retired: archived or removed in the platform, or an
            "-archived-<month>-<year>" / "-archive-<month>-<year>" page
  VARIANT   an A/B test variant URL, not a page in its own right
  DRAFT     never went out
  DEAD      a 404
  UNKNOWN   nothing in the row says

Rules, in order
  1. The row's own URL, slug or title decides first. DI retires pages by
     renaming the slug ("-archived-july-2026", "-archive-sept-2026"), so a
     page with that slug is ARCHIVED whatever the platform status says.
  2. Otherwise the platform status decides (creative_status, campaign_status,
     campaign_group_status, status, state). When a row has several, the most
     retired wins: an ACTIVE creative in a COMPLETED campaign is ENDED. A page
     with a URL or title and no status or archive marker is LIVE.
  3. An active item with zero impressions in the window is STALLED.
  4. A LIVE item whose landing page is archived, a variant or a 404 stays
     LIVE and gets a warning, because money is being spent sending people
     somewhere retired.

Usage
  python3 tag_status.py export.csv                 # table
  python3 tag_status.py windsor.json --json        # rows with status added
  python3 tag_status.py export.csv --live-only     # only LIVE rows
  python3 tag_status.py export.csv --summary       # counts per status
"""

import argparse
import csv
import json
import re
import sys

ARCHIVE_RE = re.compile(r"(?i)(?:^|[-_/ (])archived?(?=$|[-_/ )])")
VARIANT_RE = re.compile(r"(?i)(?:^|/)-?ab-variant-")
DEAD_RE = re.compile(r"(?i)(?:^|/)404(?:$|[/?#])")

# Fields that name the item itself, and fields that point somewhere else.
SELF_FIELDS = ("url", "page_url", "page", "slug", "landing_page_path", "title", "page_title", "name")
POINTER_FIELDS = ("landing_page", "share_landing_page", "cta_url", "destination_url")
STATUS_FIELDS = ("creative_status", "campaign_status", "campaign_group_status", "status", "state")
DELIVERY_FIELDS = ("impressions_last_14d", "impressions_window", "delivered")

PLATFORM = {
    "ACTIVE": "LIVE", "PUBLISHED": "LIVE", "PUBLISHED_OR_SCHEDULED": "LIVE", "LIVE": "LIVE",
    "ENABLED": "LIVE", "SERVING": "LIVE",
    "ARCHIVED": "ARCHIVED", "REMOVED": "ARCHIVED", "DELETED": "ARCHIVED", "CANCELED": "ARCHIVED",
    "CANCELLED": "ARCHIVED", "UNPUBLISHED": "ARCHIVED",
    "COMPLETED": "ENDED", "ENDED": "ENDED", "FINISHED": "ENDED",
    "PAUSED": "PAUSED",
    "DRAFT": "DRAFT", "PENDING_DELETION": "ARCHIVED", "PENDING": "DRAFT",
}


# Order of retirement: when a row carries several statuses, the later wins.
RETIREMENT = ["UNKNOWN", "LIVE", "DRAFT", "PAUSED", "ENDED", "ARCHIVED"]


def _url_status(value):
    """Status implied by a URL, slug or title, or None."""
    if not value:
        return None
    v = str(value)
    if DEAD_RE.search(v):
        return "DEAD"
    if VARIANT_RE.search(v):
        return "VARIANT"
    if ARCHIVE_RE.search(v):
        return "ARCHIVED"
    return None


def _first(row, fields):
    for f in fields:
        if row.get(f) not in (None, ""):
            return f, row[f]
    return None, None


def tag(row):
    """Return {status, reason, warning} for one row (a dict)."""
    # 1. The item's own URL, slug or title.
    for f in SELF_FIELDS:
        s = _url_status(row.get(f))
        if s:
            return {"status": s, "reason": f"{f} is {s.lower()}", "warning": ""}

    # 2. The platform's own status. A creative can say ACTIVE inside a
    # campaign that has COMPLETED, so the most retired status in the row wins.
    status, reason = "UNKNOWN", "no status, URL or title in the row"
    best = None
    for f in STATUS_FIELDS:
        raw = row.get(f)
        if raw in (None, ""):
            continue
        s = PLATFORM.get(str(raw).strip().upper(), "UNKNOWN")
        if best is None or RETIREMENT.index(s) > RETIREMENT.index(best[0]):
            best = (s, f"{f} = {raw}")
    if best:
        status, reason = best
    elif any(row.get(f) for f in SELF_FIELDS):
        # A page in a report, with no platform status and no archive marker
        # in its URL or title, is live as far as anything can tell.
        status, reason = "LIVE", "URL and title carry no archive marker"

    # 3. Active but not delivering.
    if status == "LIVE":
        dfield, delivered = _first(row, DELIVERY_FIELDS)
        if delivered is not None:
            try:
                none_delivered = float(delivered) == 0
            except (TypeError, ValueError):
                none_delivered = str(delivered).strip().lower() in ("false", "no")
            if none_delivered:
                status, reason = "STALLED", f"{reason}, but {dfield} = {delivered}"

    # 4. Where a live item sends people.
    warning = ""
    if status in ("LIVE", "STALLED"):
        for f in POINTER_FIELDS:
            s = _url_status(row.get(f))
            if s:
                warning = f"{f} points at a {s.lower()} page: {row[f]}"
                break
    return {"status": status, "reason": reason, "warning": warning}


def load(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    text = raw.lstrip()
    if text.startswith("{") or text.startswith("["):
        data = json.loads(text)
        if isinstance(data, dict):
            data = data.get("result") or data.get("rows") or data.get("data") or [data]
        return data
    return list(csv.DictReader(raw.splitlines()))


def label(row):
    for f in ("title", "name", "campaign", "creative_content_data_share_ad_context_dsc_name",
              "sponsored_creative_content_title", "url", "landing_page", "creative_id"):
        if row.get(f):
            return str(row[f]).replace("\n", " ")[:60]
    return "(row)"


def main():
    ap = argparse.ArgumentParser(description="Tag rows LIVE / ARCHIVED before auditing them.")
    ap.add_argument("input", nargs="?", default="-", help="CSV or JSON file, or - for stdin")
    ap.add_argument("--json", action="store_true", help="emit rows with status, reason, warning added")
    ap.add_argument("--live-only", action="store_true", help="keep LIVE and STALLED rows only")
    ap.add_argument("--summary", action="store_true", help="print counts per status")
    args = ap.parse_args()

    rows = load(args.input)
    out = []
    for r in rows:
        t = tag(r)
        if args.live_only and t["status"] not in ("LIVE", "STALLED"):
            continue
        out.append({**r, **t})

    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return
    if args.summary:
        counts = {}
        for r in out:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
        for k in sorted(counts, key=lambda k: -counts[k]):
            print(f"  {k:<9} {counts[k]}")
        warns = sum(1 for r in out if r["warning"])
        if warns:
            print(f"  {warns} live item(s) point at a retired page")
        return
    for r in out:
        line = f"  {r['status']:<9} {label(r):<60}  {r['reason']}"
        print(line)
        if r["warning"]:
            print(f"  {'':<9} ! {r['warning']}")


if __name__ == "__main__":
    main()
