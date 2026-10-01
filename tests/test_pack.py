#!/usr/bin/env python3
"""
test_pack.py - regression tests for the di-linkedin pack.

Plain Python, no dependencies. Run from the repo root:

    python3 tests/test_pack.py

Every case here is a defect found by running the pack against Design
Industries' real LinkedIn copy and ads. A case that fails means the pack has
regressed on something it once let through to a live post.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HUMAN = os.path.join(ROOT, "skills", "di-li-human")
AUDIT = os.path.join(ROOT, "skills", "di-li-audit")
sys.path.insert(0, HUMAN)
sys.path.insert(0, AUDIT)

import detect  # noqa: E402
import humanize  # noqa: E402
import tag_status  # noqa: E402

LEX = humanize.load_lexicon()
FAILS = []


def check(name, cond, detail=""):
    if cond:
        print(f"  ok    {name}")
    else:
        print(f"  FAIL  {name}  {detail}")
        FAILS.append(name)


def clean(text):
    return humanize.humanize(text, LEX)


def house(text):
    return detect.check_house(text, LEX)


def flag_names(report):
    return " | ".join(f["name"] for f in report["structures"])


def section(title):
    print(f"\n{title}")


# --------------------------------------------------------------------------
section("Partner wording")

out, rep = clean("We are Atlassian Enterprise Partners in Melbourne.\n")
check("plural 'Enterprise Partners' is replaced, plural kept",
      "Atlassian Solution Partners" in out and "Enterprise" not in out, repr(out))

out, _ = clean("Founder - Design Industries - Atlassian Enterprise Partners\n")
check("Michael's headline wording is replaced",
      out.strip().endswith("Atlassian Solution Partners"), repr(out))

out, _ = clean("We are an Atlassian Enterprise Partner.\n")
check("singular still replaced, singular kept",
      "an Atlassian Solution Partner." in out, repr(out))

out, _ = clean("We are Atlassian resellers.\n")
check("plural 'resellers' is replaced", "Atlassian Solution Partners" in out, repr(out))

score, detail = house("We are Atlassian Enterprise Partners in Melbourne, and proud of it.")
check("detect.py fails HOUSE STYLE on the plural", score < 60, f"{score} {detail}")

score, detail = house("Design Industries are Atlassian Platinum Solution Partners in Melbourne.")
check("tier wording 'Platinum Solution Partners' is penalised", score < 60, f"{score} {detail}")

_, rep = clean("We are an Atlassian Gold Solution Partner.\n")
check("tier wording is flagged for rewrite", "Gold Solution Partner" in flag_names(rep), flag_names(rep))

# --------------------------------------------------------------------------
section("Atlassian product casing and misspellings")

out, _ = clean("We support JIRA, BitBucket, OpsGenie and StatusPage.\n")
check("miscased products corrected",
      "Jira, Bitbucket, Opsgenie and Statuspage" in out, repr(out))

out, _ = clean("See https://example.com/JIRA/BitBucket for the JIRA-123 ticket.\n")
check("URLs and issue keys are left alone",
      "https://example.com/JIRA/BitBucket" in out and "JIRA-123" in out, repr(out))

out, _ = clean("Atlassian Licencing and licenced seats.\n")
check("'Licencing' corrected to 'Licensing'",
      "Atlassian Licensing and licensed seats." in out, repr(out))

score, detail = house("We deliver Atlassian Licencing for JIRA and BitBucket customers across Australia.")
check("detect.py penalises casing and 'Licencing'", score < 70, f"{score} {detail}")

out, _ = clean("Jira Data Center and Jira Service Management stay as they are.\n")
check("protected terms still untouched",
      "Jira Data Center and Jira Service Management" in out, repr(out))

# --------------------------------------------------------------------------
section("Claims, lexicon gaps and structures from the live ads")

_, rep = clean("Four platforms. Trusted by Enterprises Nationwide.\n")
check("unproven trust claim flagged", "trust claim" in flag_names(rep).lower(), flag_names(rep))

_, rep = clean("Trusted by 40 Australian enterprises since 2019.\n")
check("trust claim with a number is not flagged",
      "trust claim" not in flag_names(rep).lower(), flag_names(rep))

out, _ = clean("Rovo transforms your workflow with an AI-powered assistant.\n")
check("'transforms' and 'AI-powered' replaced",
      "transforms" not in out and "AI-powered" not in out, repr(out))

_, rep = clean("Search, learn and act in one place. Ready to get smarter?\n")
check("'Ready to ...?' engagement bait flagged", "engagement bait" in flag_names(rep).lower(), flag_names(rep))

_, rep = clean("Working AI Agents. In Production. This Month.\n")
check("staccato fragment triad flagged", "staccato" in flag_names(rep).lower(), flag_names(rep))

# --------------------------------------------------------------------------
section("SPECIFICITY no longer paid for product names")

names_only = ("We work with Jira, Confluence, Jira Service Management, Bitbucket, Rovo, Loom, "
              "Trello and Compass across Atlassian Cloud and Data Center for every team we meet.")
numbers = ("We cut 312 unused seats, saved $42,000 a year and moved 4 instances in 9 weeks "
           "for a team of 1,800 people across 3 states and 2 time zones last year, then "
           "closed 640 stale tickets in the first 10 days after go-live.")
s_names, _ = detect.check_specificity(names_only, LEX)
s_nums, _ = detect.check_specificity(numbers, LEX)
check("product-name list scores low on SPECIFICITY", s_names < 50, str(s_names))
check("a numbers paragraph still scores high", s_nums >= 90, str(s_nums))

# --------------------------------------------------------------------------
section("Archived DI facts")

score, detail = house("Our Growth tier includes AWS Hosting and Ad Hoc Atlassian Support for every client.")
check("archived offer names penalised in HOUSE STYLE", score < 70, f"{score} {detail}")

_, rep = clean("Ask about our Growth tier and AWS Hosting.\n")
check("archived offer names flagged with replacement", "archived" in flag_names(rep).lower(), flag_names(rep))

# --------------------------------------------------------------------------
section("Live / archive tagging")

T = tag_status.tag
check("ACTIVE creative on a live page is LIVE",
      T({"creative_status": "ACTIVE", "landing_page": "https://di.net.au/campaign/ai-fast-start-a"})["status"] == "LIVE")
check("ARCHIVED creative is ARCHIVED", T({"creative_status": "ARCHIVED"})["status"] == "ARCHIVED")
check("REMOVED creative is ARCHIVED", T({"creative_status": "REMOVED"})["status"] == "ARCHIVED")
check("COMPLETED campaign is ENDED", T({"campaign_status": "COMPLETED"})["status"] == "ENDED")
check("'-archived-july-2026' slug is ARCHIVED",
      T({"url": "https://di.net.au/campaign/ai-fast-start-archived-july-2026"})["status"] == "ARCHIVED")
check("'-archive-sept-2026' slug is ARCHIVED",
      T({"url": "https://di.net.au/campaign/ai-fast-start-b-archive-sept-2026"})["status"] == "ARCHIVED")
check("title '(archived-july-2026)' is ARCHIVED",
      T({"title": "campaign/ai-fast-start-a (archived-july-2026)"})["status"] == "ARCHIVED")
check("A/B variant URL is VARIANT",
      T({"url": "https://di.net.au/-ab-variant-c41ef2a3-9501-45a7-a753-7408c6799e59"})["status"] == "VARIANT")
check("404 is DEAD", T({"url": "https://di.net.au/404"})["status"] == "DEAD")
r = T({"creative_status": "ACTIVE", "landing_page": "https://di.net.au/campaign/rovo-ai-a-archived-sept-2026"})
check("live ad pointing at an archived page is flagged", r["status"] == "LIVE" and r["warning"], str(r))
check("ACTIVE creative in a COMPLETED campaign is ENDED",
      T({"creative_status": "ACTIVE", "campaign_status": "COMPLETED"})["status"] == "ENDED")
check("a plain page URL with no status is LIVE",
      T({"url": "https://di.net.au/platform-discovery"})["status"] == "LIVE")
check("a row with nothing in it is UNKNOWN", T({"impressions": 10})["status"] == "UNKNOWN")
check("ACTIVE campaign with no delivery is STALLED",
      T({"campaign_status": "ACTIVE", "impressions_last_14d": 0})["status"] == "STALLED")

# --------------------------------------------------------------------------
section("Pack structure and the read-only rule")

skills = sorted(d for d in os.listdir(os.path.join(ROOT, "skills")) if d.startswith("di-li-"))
check("eleven skills", len(skills) == 11, str(skills))
MARK = "## Hard rule: read-only"
for s in skills:
    text = open(os.path.join(ROOT, "skills", s, "SKILL.md"), encoding="utf-8").read()
    check(f"{s} carries the read-only rule", MARK in text)
    fm = re.search(r"^name:\s*(\S+)", text, re.M)
    check(f"{s} frontmatter name matches folder", fm and fm.group(1) == s)
readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
check("README states the read-only rule", "read-only" in readme.lower())

for rel in ("rubric.json", "page_rubric.json"):
    r = json.load(open(os.path.join(ROOT, "skills", "di-li-profile", rel), encoding="utf-8"))
    total = sum(i["points"] for i in r["items"])
    check(f"{rel} sums to 100", total == 100 == r["total"], str(total))
    ids = [i["id"] for i in r["items"]]
    check(f"{rel} ids are unique", len(ids) == len(set(ids)))

hooks = json.load(open(os.path.join(ROOT, "skills", "di-li-post", "hooks.json"), encoding="utf-8"))
check("21 hook formulas", len(hooks["hooks"]) == 21)

pos = open(os.path.join(ROOT, "templates", "positioning.md"), encoding="utf-8").read()
check("positioning.md has an as-of date", re.search(r"As of \d{1,2} \w+ 20\d\d", pos) is not None)
check("positioning.md has an Archive section", "## Archive" in pos)
check("positioning.md carries no em dash", "\u2014" not in pos)
for s in skills:
    text = open(os.path.join(ROOT, "skills", s, "SKILL.md"), encoding="utf-8").read()
    prose = re.sub(r"`[^`\n]*`", "", text)  # a code span may show the character it handles
    check(f"{s} carries no em dash", "\u2014" not in prose)

# --------------------------------------------------------------------------
print()
if FAILS:
    print(f"{len(FAILS)} failing")
    sys.exit(1)
print("all passing")
