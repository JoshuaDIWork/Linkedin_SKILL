#!/usr/bin/env python3
"""
humanize.py - strip the machine fingerprint out of a Design Industries draft.

Five passes, in this order:

  0. PROTECT     stash URLs, email addresses and the protected terms in
                 slop.json (Atlassian product names, DI offer names) so no
                 later pass rewrites inside them. "Data Center" stays
                 "Data Center". "Jira Service Management" is never touched.
  1. INVISIBLE   delete or normalise the characters a human keyboard never
                 produces: zero-width joiners, word joiners, soft hyphens,
                 BOMs, Unicode tag characters, non-breaking and narrow spaces.
                 These survive copy-paste and are the most mechanical tell in
                 any generated text.
  2. TYPOGRAPHIC em dash -> comma, en dash -> hyphen, curly quotes -> straight,
                 ellipsis -> three dots, bullet -> hyphen. DI's house rule is
                 that an em dash never ships.
  3. LEXICAL     replace the slop lexicon in slop.json with plain words,
                 preserving capitalisation.
  4. SPELLING    American to Australian English: organization -> organisation,
                 optimize -> optimise, center -> centre, and 300-odd more,
                 preserving capitalisation. Then the misspellings that are
                 wrong in both systems: "Licencing" -> "Licensing".
  5. HOUSE       DI's own phrasing: "Enterprise Partner(s)" becomes "Atlassian
                 Solution Partner(s)", plural kept. Filler is deleted, and
                 banned phrases with no safe replacement ("game-changer",
                 "Platinum Solution Partner") are flagged for a rewrite.
  6. CASING      Atlassian's own capitalisation, case-sensitive: JIRA -> Jira,
                 BitBucket -> Bitbucket, OpsGenie -> Opsgenie. URLs and issue
                 keys such as JIRA-123 are left alone.

Retired DI wording listed under "archived" in slop.json ("Growth tier",
"AWS Hosting") is flagged with what replaced it, never auto-swapped, because
the right replacement depends on the sentence.

Structural tells (rule-of-three, "not just X, it's Y", hashtag walls, a DI
term used without explanation) are REPORTED, never auto-rewritten - rewriting
a sentence's shape needs judgement, so that is the model's job, not a regex's.

Usage
  python3 humanize.py draft.txt
  python3 humanize.py draft.txt --report
  pbpaste | python3 humanize.py - --report
  python3 humanize.py draft.txt --json
  python3 humanize.py draft.txt -o clean.txt
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")

# What counts as explaining a DI term on first use: a bracket, a colon, a
# ", which is", ", our", "is our", "means", or "is a/an X that/which/where".
# "Digital Factory is a game-changer" does not count.
EXPLAINED = re.compile(
    r"^\s*(?:\(|:|,\s*(?:which|our|the|DI's)\b|\s*is\s+(?:our|DI's|the way|how|what)\b"
    r"|\s*means\b|\s*is\s+an?\s+[\w-]+(?:\s+[\w-]+){0,3}\s+(?:that|which|where)\b)",
    re.IGNORECASE)


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    """'U+200B' -> '\\u200b';  'U+E0000-U+E007F' -> (start, end)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def _word_pattern(find, flags=re.IGNORECASE, plural=False):
    """Whole-word pattern for a lexicon entry. With plural=True the entry
    also matches its plural, captured as group 1, so "Enterprise Partner"
    catches "Enterprise Partners" and the replacement can keep the s."""
    body = re.escape(find).replace(r"\ ", r"\s+")
    tail = r"(s)?\b" if plural else r"\b"
    return re.compile(r"\b" + body + tail, flags)


def _outside_urls(text, fn):
    """Apply fn to every stretch of text that is not a URL or email."""
    out, last = [], 0
    for m in URL_RE.finditer(text):
        out.append(fn(text[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(fn(text[last:]))
    return "".join(out)


def protect(text, lex):
    """Swap URLs, emails and protected terms for placeholders so no pass
    rewrites inside them. Protected terms match case-sensitively, longest
    first, so 'Jira Data Center' wins over 'Jira' and 'Data Center'."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00P{len(found) - 1}\x00"

    text = URL_RE.sub(stash, text)
    terms = sorted(lex.get("protected", []), key=len, reverse=True)
    for term in terms:
        text = _word_pattern(term, 0).sub(stash, text)
    return text, found


def restore(text, found):
    for i, item in enumerate(found):
        text = text.replace(f"\x00P{i}\x00", item)
    return text


def pass_invisible(text, lex):
    """Delete or space-normalise invisible characters. Returns (text, hits)."""
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": entry["action"]})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Any remaining Cf (format) character is invisible by definition.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "other invisible format chars", "count": len(stray),
                     "action": "delete"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n, "to": entry["to"].strip() or "(space)"})
        if ch == "—":
            # " word — word " and "word—word" both collapse to a comma + space.
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)      # 5–10  -> 5-10
            text = re.sub(r"\s+–\s+", ", ", text)            # used as em dash
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    # A comma inserted before existing punctuation reads wrong.
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def _replace_entries(text, entries, key_find="find", key_replace="replace", family=None):
    """Longest-first replacement of a list of {find, replace} entries.
    Entries whose replace is None are skipped (flag-only)."""
    hits = []
    entries = sorted([e for e in entries if e.get(key_replace) is not None],
                     key=lambda e: len(e[key_find]), reverse=True)
    for entry in entries:
        find = entry[key_find]
        plural = bool(entry.get("plural"))
        pattern = _word_pattern(find, plural=plural)
        found = list(pattern.finditer(text))
        if not found:
            continue
        hits.append({"find": find + ("(s)" if plural else ""),
                     "replace": entry[key_replace] or "(deleted)",
                     "count": len(found),
                     "family": entry.get("family", family or "")})

        def swap(m, repl=entry[key_replace], plural=plural):
            out = _match_case(m.group(0), repl)
            if plural and m.group(1) and out:
                out += m.group(1)
            return out

        text = pattern.sub(swap, text)
    return text, hits


def _tidy(text):
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*([,.;:])\s*", "", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # A deleted phrase can leave ". ." behind. Collapse it, but leave "..." alone.
    text = re.sub(r"(?<!\.)\.\s*\.(?!\.)", ".", text)
    return text


def pass_lexical(text, lex):
    """Replace slop words and phrases. Longest first so phrases win."""
    text, hits = _replace_entries(text, lex["phrases"] + lex["words"])
    text = _tidy(text)
    # An em dash that became a comma, followed by a sentence connective, leaves
    # a splice ("is important, also, it's proof"). Promote it to a full stop.
    text = re.sub(r",\s*(also|so|still|basically|in the end)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def pass_spelling(text, lex):
    """American to Australian English, then misspellings that are wrong in
    both systems. Protected terms were stashed already, so 'Data Center'
    never reaches this pass."""
    text, hits = _replace_entries(text, lex.get("spelling", []), family="spelling")
    text, fixes = _replace_entries(text, lex.get("corrections", []), family="correction")
    return text, hits + fixes


def casing_pattern(find):
    """Case-sensitive whole-word match that skips issue keys like JIRA-123."""
    return re.compile(r"\b" + re.escape(find).replace(r"\ ", r"\s+") + r"\b(?!-\d)")


def pass_casing(text, lex):
    """Atlassian's own capitalisation. Runs before protection, because
    'Jira service management' starts with the protected word 'Jira', and
    skips URLs itself."""
    hits = []
    for entry in sorted(lex.get("casing", []), key=lambda e: len(e["find"]), reverse=True):
        pattern = casing_pattern(entry["find"])
        n = sum(len(pattern.findall(seg)) for seg in URL_RE.split(text))
        if not n:
            continue
        hits.append({"find": entry["find"], "replace": entry["replace"], "count": n})
        text = _outside_urls(text, lambda seg, p=pattern, r=entry["replace"]: p.sub(r, seg))
    return text, hits


CLAIM_RE = re.compile(
    r"(?i)\b\d[\d,]*\+?\s+(?:enterprise\s+|australian\s+|government\s+)?"
    r"(?:clients|customers|enterprises|organi[sz]ations|deployments|implementations|projects|partners)\b")


def scan_claims(text, lex):
    """House rules that need more than a regex: scale claims that are not
    in the sourced list, client names that are not on Michael's approved
    list, and a '2-3 weeks' that does not name the Claude or Rovo track."""
    flags = []
    sourced = [p.lower() for p in lex.get("sourced_claims", {}).get("phrases", [])]
    for m in CLAIM_RE.finditer(text):
        claim = m.group(0)
        if not any(claim.lower().startswith(p) or p.startswith(claim.lower()) for p in sourced):
            flags.append({"name": f'Unsourced scale claim "{claim}"', "count": 1,
                          "fix": "Use a sourced number from positioning.md Proof, or add this one to "
                                 "sourced_claims in slop.json with its source."})
    for name in lex.get("unapproved_clients", {}).get("names", []):
        n = len(_word_pattern(name, 0).findall(text))
        if n:
            flags.append({"name": f'"{name}" is not on the approved client list', "count": n,
                          "fix": "Only ANZ, Australia Post, Viva Energy, Bunnings, Honda, La Trobe "
                                 "University and Hume City Council may be named. Anonymise."})
    tl = lex.get("timeline")
    if tl:
        for m in re.finditer(tl["regex"], text):
            window = text[max(0, m.start() - 120):m.end() + 120]
            named = lambda words: [w for w in words
                                   if re.search(r"\b" + re.escape(w) + r"(?!\s+Dev)\b", window)]
            outside = [w for w in tl.get("out_of_scope", [])
                       if re.search(r"\b" + re.escape(w) + r"\b", window)]
            if not named(tl["scope"]):
                flags.append({"name": f'"{m.group(0)}" without the Claude or Rovo track', "count": 1,
                              "fix": tl["fix"]})
            elif outside:
                flags.append({"name": f'"{m.group(0)}" next to {", ".join(outside)}', "count": 1,
                              "fix": tl["fix"]})
    return flags


def scan_archived(text, lex):
    """Retired DI wording. Flagged with what replaced it, never swapped."""
    flags = []
    for entry in lex.get("archived", []):
        n = len(_word_pattern(entry["find"]).findall(text))
        if n:
            flags.append({"name": f'"{entry["find"]}" is archived DI wording', "count": n,
                          "fix": f'Use {entry["replace_with"]}. {entry["why"]}'})
    return flags


def pass_house(text, lex):
    """DI house phrasing. Entries with a replacement are swapped; entries
    without one are returned as flags for the model to rewrite."""
    house = lex.get("house", [])
    text, hits = _replace_entries(text, house, family="house")
    text = _tidy(text)
    flags = []
    work = text
    # Longest first, blanking each match, so "Atlassian Platinum Solution
    # Partners" is one flag and not three.
    for entry in sorted(house, key=lambda e: len(e["find"]), reverse=True):
        if entry.get("replace") is not None:
            continue
        pattern = _word_pattern(entry["find"], plural=bool(entry.get("plural")))
        n = len(pattern.findall(work))
        if n:
            flags.append({"name": f'"{entry["find"]}"', "count": n, "fix": entry["why"]})
            work = pattern.sub(lambda m: " " * len(m.group(0)), work)
    for entry in lex.get("spelling_flag", []):
        n = len(_word_pattern(entry["find"]).findall(text))
        if n:
            flags.append({"name": f'"{entry["find"]}" (check noun/verb)', "count": n,
                          "fix": entry["why"]})
    return text, hits, flags


def scan_di_terms(text, lex):
    """A DI term used without an explanation nearby is a tell to the reader
    that the post was written for insiders. Heuristic: the first occurrence
    must be followed within 160 characters by 'is', 'means', ':', 'we call'
    or brackets."""
    flags = []
    for entry in lex.get("di_terms", []):
        m = _word_pattern(entry["term"], 0).search(text)
        if not m:
            continue
        window = text[m.end():m.end() + 160]
        before = text[max(0, m.start() - 40):m.start()]
        if re.search(EXPLAINED, window) \
           or re.search(r"\bwe call (?:it|this)\s*$", before, re.IGNORECASE):
            continue
        flags.append({"name": f'"{entry["term"]}" used without explanation', "count": 1,
                      "fix": f'Say what it is on first use: {entry["explain"]}.'})
    return flags


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    limit = lex.get("hashtag_limit", 5)
    tags = re.findall(r"(?<!\w)#\w+", text)
    if len(tags) > limit:
        flags.append({"name": f"{len(tags)} hashtags (DI limit is {limit})", "count": len(tags),
                      "fix": "Keep three to five from the library in positioning.md. Delete the rest."})
    # Sentence-length uniformity is structural too.
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "name": f"Uniform sentence length (variation {cv:.2f})",
                "count": len(lens),
                "fix": "Break one sentence in half. Let another run long. Machines write even.",
            })
    return flags


def humanize(text, lex):
    # House replacements run on the raw text, before protection, because
    # "Atlassian Enterprise Partner" overlaps the protected word "Atlassian".
    text, house, _ = pass_house(text, lex)
    text, casing = pass_casing(text, lex)
    text, stash = protect(text, lex)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex)
    text, spell = pass_spelling(text, lex)
    text = restore(text, stash)
    _, _, house_flags = pass_house(text, lex)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "spelling": spell,
        "house": house,
        "casing": casing,
        "structures": (scan_structures(text, lex) + house_flags
                       + scan_archived(text, lex) + scan_claims(text, lex)
                       + scan_di_terms(text, lex)),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for k in ("invisible", "typographic", "lexical", "spelling", "house", "casing")
                for h in report[k])

    head("HUMANISE REPORT")
    print(f"{total} machine and house-style artefacts removed, "
          f"{len(report['structures'])} tells flagged for rewrite", file=out)

    if report["invisible"]:
        head("1. INVISIBLE CHARACTERS")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['action']}", file=out)
    if report["typographic"]:
        head("2. TYPOGRAPHY")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. SLOP LEXICON")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["spelling"]:
        head("4. AUSTRALIAN ENGLISH")
        for h in report["spelling"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}", file=out)
    if report["house"]:
        head("5. DI HOUSE STYLE")
        for h in report["house"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}", file=out)
    if report["casing"]:
        head("6. ATLASSIAN CASING")
        for h in report["casing"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}", file=out)
    if report["structures"]:
        head("7. FLAGGED FOR REWRITE  (not auto-fixed - rewrite these yourself)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("CLEAN")
        print("  Nothing to strip.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Strip the machine fingerprint out of a DI draft.")
    ap.add_argument("input", nargs="?", default="-", help="file, or - for stdin")
    ap.add_argument("-o", "--out", help="write cleaned text here instead of stdout")
    ap.add_argument("--report", action="store_true", help="print what changed, to stderr")
    ap.add_argument("--json", action="store_true", help="emit {text, report} as JSON")
    ap.add_argument("--lexicon", default=LEX, help="path to slop.json")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
