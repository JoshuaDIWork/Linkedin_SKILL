#!/usr/bin/env python3
"""
detect.py - a six-check panel that scores how machine-written, and how
un-DI, a draft looks.

What this is:  five local heuristics modelled on the signals public AI
detectors actually measure - sentence-length variation, concreteness, stock
vocabulary, typographic fingerprint, and voice - plus a sixth, HOUSE STYLE,
that has nothing to do with detectors and everything to do with whether the
post reads as Design Industries: Australian English, no banned phrases, no
hashtag wall, no DI term left unexplained. Every score is computed on your
machine from the text alone. Nothing is uploaded.

What this is NOT:  GPTZero, Originality, Copyleaks, Winston or Turnitin.
It does not call their APIs and it cannot promise their verdict. It catches
the things they all key on, which is why fixing them tends to move their
numbers too - but the only honest claim is the one on this line.

Each check returns a HUMAN score from 0 to 100. Higher is better.

Usage
  python3 detect.py draft.txt
  pbpaste | python3 detect.py -
  python3 detect.py draft.txt --json
  python3 detect.py before.txt after.txt      # compare two drafts
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[A-Za-z']+")
CONTRACTIONS = re.compile(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", re.IGNORECASE)
PRONOUNS = re.compile(r"\b(i|me|my|mine|we|us|our|you|your)\b", re.IGNORECASE)
NUMBERS = re.compile(r"\b\d[\d,.]*%?\b|\$\d")
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]{2,}\b", re.MULTILINE)

# What counts as explaining a DI term on first use: a bracket, a colon, a
# ", which is", ", our", "is our", "means", or "is a/an X that/which/where".
# "Digital Factory is a game-changer" does not count.
EXPLAINED = re.compile(
    r"^\s*(?:\(|:|,\s*(?:which|our|the|DI's)\b|\s*is\s+(?:our|DI's|the way|how|what)\b"
    r"|\s*means\b|\s*is\s+an?\s+[\w-]+(?:\s+[\w-]+){0,3}\s+(?:that|which|where)\b)",
    re.IGNORECASE)


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Map value onto 0-100 where `human` -> 100 and `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")


def _word_pattern(find, flags=re.IGNORECASE, plural=False):
    body = re.escape(find).replace(r"\ ", r"\s+")
    return re.compile(r"\b" + body + (r"(?:s)?\b" if plural else r"\b"), flags)


def _count_consuming(text, entries, plural_key="plural"):
    """Count lexicon hits longest-first, blanking each match so that
    'Atlassian Enterprise Partners' is one hit, not two."""
    found = []
    for entry in sorted(entries, key=lambda e: len(e["find"]), reverse=True):
        pattern = _word_pattern(entry["find"], plural=bool(entry.get(plural_key)))
        n = len(pattern.findall(text))
        if n:
            found.append((entry, n))
            text = pattern.sub(lambda m: " " * len(m.group(0)), text)
    return found


def strip_protected(text, lex):
    """Blank out protected terms so 'Data Center' is not an American spelling."""
    for term in sorted(lex.get("protected", []), key=len, reverse=True):
        text = _word_pattern(term, 0).sub(" ", text)
    return text


def check_burstiness(text):
    """Humans vary sentence length hard. Models write even."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "too short to judge"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variation {cv:.2f} across {len(lens)} sentences (want 0.55+)"


def check_specificity(text, lex=None):
    """Numbers, names and concrete nouns. Slop is abstract. Atlassian
    product names and DI offer names do not count as names here: a list of
    products is not a fact, and every DI paragraph is full of them."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "too short to judge"
    per100 = 100 / len(w)
    named = strip_protected(text, lex) if lex else text
    hits = len(NUMBERS.findall(text)) + len(set(PROPER.findall(named)))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, f"{hits} concrete markers, {density:.1f} per 100 words (want 4+)"


def check_slop(text, lex):
    """Stock vocabulary density against the lexicon."""
    w = words(text)
    if not w:
        return 50.0, "empty"
    hits, found = 0, []
    for entry in lex["words"] + lex["phrases"]:
        n = len(_word_pattern(entry["find"]).findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} stock terms, {density:.1f} per 100 words"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Characters a phone keyboard does not produce."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "\u00a0\u202f\u2009")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisible, {em} em dash, {curly} curly quote, "
              f"{ellip} ellipsis, {nbsp} hard space")
    return score, detail


def check_voice(text, lex):
    """Contractions, person, and the shapes models default to."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "too short to judge"
    per100 = 100 / len(w)
    contractions = len(CONTRACTIONS.findall(text)) * per100
    person = len(PRONOUNS.findall(text)) * per100
    tells = 0
    names = []
    for s in lex["structures"]:
        if s.get("kind") == "house":
            continue  # house rules are scored in HOUSE STYLE
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(contractions, human=3.0, machine=0.0) * 0.35
             + scale(person, human=8.0, machine=1.0) * 0.35
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("uniform-bullets")
    detail = (f"{contractions:.1f} contractions, {person:.1f} personal pronouns "
              f"per 100 words, {tells} structural tell(s)")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


def check_house(text, lex):
    """Does it read as Design Industries. American spellings, banned
    phrases, hashtag count, DI terms left unexplained, em dashes. Starts at
    100 and loses points; a single 'Enterprise Partner' fails it."""
    w = words(text)
    if not w:
        return 50.0, "empty"
    body = strip_protected(text, lex)
    per100 = 100 / len(w)
    problems = []

    us = 0
    us_found = []
    for entry in lex.get("spelling", []):
        n = len(_word_pattern(entry["find"]).findall(body))
        if n:
            us += n
            us_found.append(entry["find"])

    # Corrections ("Licencing") are misspellings in both systems.
    for entry, n in _count_consuming(body, lex.get("corrections", [])):
        us += n
        us_found.append(entry["find"])
    spelling_score = scale(us * per100, human=0.0, machine=1.5)

    # House phrases match the raw text, longest first, so the protected word
    # "Atlassian" inside "Atlassian reseller" still counts and one phrase is
    # never penalised twice. Partner wording matches plurals too.
    banned = 0
    penalty = 0
    for entry, n in _count_consuming(text, lex.get("house", [])):
        banned += n
        problems.append(entry["find"])
        penalty += 45 if "Partner" in entry["find"] or "reseller" in entry["find"] else 20

    # Atlassian's own capitalisation, case-sensitive, URLs and issue keys
    # excluded. Miscased product names are a house-style problem, not a
    # detector one.
    plain = URL_RE.sub(" ", text)
    casing = 0
    for entry in lex.get("casing", []):
        n = len(re.findall(r"\b" + re.escape(entry["find"]) + r"\b(?!-\d)", plain))
        if n:
            casing += n
            problems.append(entry["find"])
    penalty += 10 * casing

    archived = 0
    for entry, n in _count_consuming(text, lex.get("archived", []), plural_key="_none"):
        archived += n
        problems.append(f'archived: {entry["find"]}')
    penalty += 15 * archived

    # House rules written as patterns: unproven trust claims, discounts,
    # offer prices or hours, IRAP / ISO 27001 / SOC 2, Community of Practice
    # as training, digs at other partners.
    for st in lex.get("structures", []):
        if st.get("kind") != "house":
            continue
        n = len(re.findall(st["regex"], text, re.MULTILINE))
        if n:
            banned += n
            penalty += 20 * n
            problems.append(st["id"])

    # Rules that need code: unsourced scale claims, unapproved client names,
    # an unscoped "2-3 weeks". Shared with humanize.py.
    import humanize as _h
    claim_flags = _h.scan_claims(text, lex)
    penalty += 15 * len(claim_flags)
    for f in claim_flags:
        problems.append(f["name"][:40])

    limit = lex.get("hashtag_limit", 5)
    tags = len(re.findall(r"(?<!\w)#\w+", text))
    if tags > limit:
        penalty += 10 * (tags - limit)
        problems.append(f"{tags} hashtags")

    unexplained = []
    for entry in lex.get("di_terms", []):
        m = _word_pattern(entry["term"], 0).search(text)
        if not m:
            continue
        window = text[m.end():m.end() + 160]
        before = text[max(0, m.start() - 40):m.start()]
        if re.search(EXPLAINED, window) \
           or re.search(r"\bwe call (?:it|this)\s*$", before, re.IGNORECASE):
            continue
        unexplained.append(entry["term"])
    penalty += 15 * len(unexplained)

    em = text.count("—")
    penalty += 15 * em

    score = clamp(spelling_score - penalty)
    detail = f"{us} American spelling(s)"
    if us_found:
        detail += " (" + ", ".join(sorted(set(us_found))[:4]) + (", ..." if len(set(us_found)) > 4 else "") + ")"
    detail += (f", {banned} banned phrase(s), {casing} miscased, {archived} archived, "
               f"{tags} hashtag(s), {em} em dash")
    if problems:
        detail += " [" + ", ".join(problems[:4]) + "]"
    if unexplained:
        detail += " unexplained: " + ", ".join(unexplained)
    return score, detail


CHECKS = ["BURSTINESS", "SPECIFICITY", "SLOP DENSITY", "FINGERPRINT", "VOICE", "HOUSE STYLE"]


def run(text, lex):
    results = {}
    results["BURSTINESS"] = check_burstiness(text)
    results["SPECIFICITY"] = check_specificity(text, lex)
    results["SLOP DENSITY"] = check_slop(text, lex)
    results["FINGERPRINT"] = check_fingerprint(text)
    results["VOICE"] = check_voice(text, lex)
    results["HOUSE STYLE"] = check_house(text, lex)
    scores = [results[c][0] for c in CHECKS]
    # The weakest check drags the verdict: a detector only needs one signal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "PASS" if overall >= 70 and min(scores) >= 55 else (
        "REVIEW" if overall >= 50 else "FLAGGED")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "AI DETECTION + HOUSE STYLE PANEL" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'HUMAN SCORE':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "PASS":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Weakest signal: {weakest}. Fix that first.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Score how machine-written, and how un-DI, a draft looks.")
    ap.add_argument("input", nargs="?", default="-", help="file, or - for stdin")
    ap.add_argument("compare", nargs="?", help="second file, to show before/after")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    args = ap.parse_args()

    lex = json.load(open(args.lexicon, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex)
        payload.append({
            "source": name,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
              f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
