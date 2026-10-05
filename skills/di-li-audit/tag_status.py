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
  2. Otherwise the platform status decides, read from the top of the
     hierarchy down: campaign_group_status first, then campaign_status, then
     creative_status, status, state. When a row has several, the most
     retired wins: an ACTIVE creative in a COMPLETED campaign is ENDED, and
     an ACTIVE campaign in a PAUSED campaign group is PAUSED. Pausing a group
     leaves the campaigns under it showing ACTIVE, so a campaign row with no
     group status is filled in from any row in the input (or --groups file)
     that carries the same campaign_group_id or campaign_group_name. A page
     with a URL or title and no status or archive marker is LIVE.
  3. An active item with zero impressions in the window is STALLED. A
     STALLED campaign whose group status was never read gets a warning,
     because it may be a paused group rather than a broken campaign.
  4. A LIVE item whose landing page is archived, a variant or a 404 stays
     LIVE and gets a warning, because money is being spent sending people
     somewhere retired.

Usage
  python3 tag_status.py export.csv                 # table
  python3 tag_status.py windsor.json --json        # rows with status added
  python3 tag_status.py export.csv --live-only     # only LIVE rows
  python3 tag_status.py export.csv --summary       # counts per status
  python3 tag_status.py campaigns.json --groups groups.json
                                                   # add group status from a
                                                   # campaign-group pull
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
# Top of the hierarchy first. In the LinkedIn API a campaign group is what
# Campaign Manager calls a "Campaign", and a campaign is an "Ad set".
STATUS_FIELDS = ("campaign_group_status", "campaign_status", "creative_status", "status", "state")
GROUP_KEYS = ("campaign_group_id", "campaign_group_name", "campaign_group")
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
        under = row.get("campaign_status")
        if reason.startswith("campaign_group_status") and under not in (None, "") \
                and PLATFORM.get(str(under).strip().upper()) != status:
            reason += f" (campaign_status = {under} underneath)"
        if row.get("campaign_group_status_from") and "campaign_group_status" in reason:
            reason += f", group status matched on {row['campaign_group_status_from']}"
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
    if status == "STALLED" and row.get("campaign_status") not in (None, "") \
            and row.get("campaign_group_status") in (None, ""):
        warning = ("campaign_group_status not read: a paused campaign group leaves its "
                   "campaigns ACTIVE. Read the group status before reporting this as broken")
    if status in ("LIVE", "STALLED") and not warning:
        for f in POINTER_FIELDS:
            s = _url_status(row.get(f))
            if s:
                warning = f"{f} points at a {s.lower()} page: {row[f]}"
                break
    return {"status": status, "reason": reason, "warning": warning}


def inherit_group_status(rows, groups=()):
    """Copy campaign_group_status onto rows that lack it, matched by group id
    or name, from any row in rows or groups that carries it. Rows are changed
    in place, and an inherited value is marked in campaign_group_status_from."""
    known = {}
    for r in list(groups) + list(rows):
        st = r.get("campaign_group_status")
        if st in (None, ""):
            continue
        for k in GROUP_KEYS:
            if r.get(k) not in (None, ""):
                known.setdefault((k, str(r[k]).strip()), st)
    for r in rows:
        if r.get("campaign_group_status") not in (None, ""):
            continue
        for k in GROUP_KEYS:
            hit = known.get((k, str(r.get(k, "")).strip()))
            if hit is not None:
                r["campaign_group_status"] = hit
                r["campaign_group_status_from"] = k
                break
    return rows


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
    ap.add_argument("--groups", help="CSV or JSON campaign-group pull to read group status from")
    args = ap.parse_args()

    rows = inherit_group_status(load(args.input), load(args.groups) if args.groups else ())
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
