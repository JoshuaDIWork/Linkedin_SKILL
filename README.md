# The Design Industries LinkedIn skill

Eleven Claude skills that run LinkedIn for Design Industries: Michael's
profile, the DI company page, and the team's own profiles. Free, MIT, no
signup, no API key, nothing to connect.

One of them writes posts off 21 hook formulas, in Michael's voice or the DI
page's, with the right DI offer as the one-line call to action. One comments
on other people's posts in the Atlassian ecosystem. One handles the replies
under DI's posts and flags the leads for HubSpot. One scores a team member's
profile out of 100 and rewrites what lost points. One plans the week: what
Michael posts, what the page posts, when in AEST, and who to engage with.

And one is the humaniser, which is the reason the rest are usable. It strips
the em dashes, the slop vocabulary and the invisible watermark characters out
of a draft, converts American spellings to Australian English, corrects
"Enterprise Partner" to "Atlassian Solution Partner", leaves "Data Center"
alone, and scores what is left against a six-check panel before anyone sees
it.

**Nothing gets posted until someone at DI says yes.** These skills write.
Michael, Kathzie and the team post.

This is a Design Industries adaptation of Jake Schincariol's
[linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill),
kept under the same MIT licence. The mechanics are his. The voice, the
positioning, the Australian English pass and the house-style check are DI's.

## Install

Paste this into Claude:

```
https://github.com/JoshuaDIWork/Linkedin_SKILL

Install this skill, then confirm /di-li-post works.
```

Or do it yourself, in Claude Code:

```bash
git clone https://github.com/JoshuaDIWork/Linkedin_SKILL.git
cp -r Linkedin_SKILL/skills/di-li-* ~/.claude/skills/
```

Or as a plugin:

```
/plugin marketplace add JoshuaDIWork/Linkedin_SKILL
/plugin install di-linkedin
```

Project-local instead of global: copy the same folders into your repo's
`.claude/skills/`. No Claude Code at all? Paste any single `SKILL.md` at the
top of a chat and it runs as a mode. You lose the two Python tools, which is
most of the point of `/di-li-human`, but the rest works.

Then set up the two files every skill reads:

```bash
mkdir -p ~/.claude/di-linkedin
cp Linkedin_SKILL/templates/positioning.md ~/.claude/di-linkedin/
cp Linkedin_SKILL/templates/voice.md ~/.claude/di-linkedin/
```

`positioning.md` is the company: who DI is, the two voices, the audience, the
offers and which topic earns which one, the hashtag library, the house rules.
It ships filled in. `voice.md` is the person. Michael's is pre-filled with
the calibration and the positions; the "three posts that sound like me"
section still wants three real posts. A team member setting up their own
profile copies the template, fills it in, and points the skills at it. Skip
this and everything comes out sounding like every other partner.

## The eleven

| command | what it does |
| --- | --- |
| `/di-li-post` | One idea into a post. Picks the voice (Michael or DI page), three hook options from [21 formulas](skills/di-li-post/hooks.json) with DI examples, one full draft, one DI offer as CTA if the topic earns it, humanised before you see it. |
| `/di-li-comment` | Comments on other people's posts. Nine types, picked by what the post actually is. Never "Great post!", never a pitch, never a dig at another partner. |
| `/di-li-reply` | The thread under a DI post. Sorts every comment into lead / substance / peer / support / noise, writes in that order, and flags the leads for HubSpot the same day. |
| `/di-li-profile` | Scores a team member's profile against a [13-part rubric](skills/di-li-profile/rubric.json) out of 100, including how it presents DI, then rewrites in fix-first order. |
| `/di-li-plan` | The week. Michael's three posts, the page's two, AEST times, and the 10 people in the Atlassian ecosystem to engage with. Writes `~/.claude/di-linkedin/plan.md`. |
| `/di-li-human` | The humaniser. Two scripts that actually run. See below. |
| `/di-li-carousel` | Document posts for the checklists and frameworks. Slide-by-slide copy, the cover that earns the swipe, and the PDF, with the brand pass left to Tejas. |
| `/di-li-repurpose` | One di.net.au article, webinar, case study or transcript into a week of posts that each stand alone, with client detail stripped first. |
| `/di-li-dm` | The 200-character invite, the first message, and the two follow-ups, for prospects, Atlassian contacts, partners and candidates. Two follow-ups. |
| `/di-li-inbox` | Triages the inbox into lead / partner / candidate / peer / ask / spam, and tells you which tell gave the vendor sequence away. |
| `/di-li-audit` | Post-mortem on what DI has already published. Ranks by engagement rate and reach multiple, not impressions, and prints Kathzie's weekly three numbers first. |

## The humaniser

`/di-li-human` ships two Python scripts with no dependencies. They run on your
machine, on your text, and nothing is uploaded.

```bash
python3 humanize.py draft.txt --report      # clean it, show every change
python3 detect.py draft.txt                  # score it, six checks
python3 detect.py before.txt after.txt       # prove the delta
```

**What comes out automatically:**

- **Invisible characters.** Zero-width spaces and joiners, word joiners, soft
  hyphens, byte-order marks, Unicode tag characters, non-breaking and narrow
  spaces. Your keyboard does not make these. They survive copy-paste and they
  are invisible in every editor you own.
- **Typography.** Em dash to comma, en dash to hyphen, curly quotes to
  straight, ellipsis to three dots. DI's house rule is that an em dash never
  ships, so this pass is not optional.
- **The lexicon.** 110 stock words and phrases with plain-English
  replacements: delve, leverage, robust, seamless, crucial, testament to, "in
  today's fast-paced world", "let that sink in". Capitalisation preserved and
  URLs untouched. It lives in [`slop.json`](skills/di-li-human/slop.json) and
  it is meant to be edited. "Ecosystem" is not in it, because DI says
  "Atlassian ecosystem" and means it.
- **Australian English.** 350 American spellings with their Australian forms:
  organization, optimize, center, behavior, catalog, fulfill, traveled and
  the rest of the family. A short list of ambiguous ones (license, program)
  is flagged rather than changed, because the noun and the verb differ.
- **DI house style.** "Enterprise Partner" and "Atlassian reseller" become
  "Atlassian Solution Partner". "It's important to note that" is deleted.
  "game-changer", "silver bullet", "synergy", "best-in-class" and
  "industry-leading" are flagged for a rewrite, because there is no safe
  word to swap in for a claim that should not have been made.
- **Protected terms.** Atlassian product names and DI offer names are
  stashed before any pass runs, so "Jira Data Center" is never "corrected"
  to "Data Centre" and "Jira Service Management" is never touched.

**What gets flagged instead of fixed:** "It's not just X, it's Y", rule-of-three
triads, one-word rhetorical questions, more than five hashtags, reflex
engagement bait, uniform sentence length, a US date, a dig at "other
partners", and a DI term ("Sundown Rule", "Digital Factory", "Diai Foundry")
used without being explained on first use. Changing the shape of a sentence
needs judgement, so those are handed back for a rewrite rather than mangled
by a regex.

**The six checks**, scored 0-100, higher is more human and more DI:

| check | what it measures |
| --- | --- |
| BURSTINESS | sentence-length variation. Models write even. |
| SPECIFICITY | numbers, names and concrete markers per 100 words |
| SLOP DENSITY | lexicon hits per 100 words |
| FINGERPRINT | invisible characters, em dashes, curly quotes per 1,000 |
| VOICE | contractions, person, structural tells |
| HOUSE STYLE | American spellings, banned DI phrases, hashtag count, unexplained DI terms |

The verdict weights the mean at 60% and the **weakest single check** at 40%,
because a detector only needs one signal to fire. HOUSE STYLE has nothing to
do with detectors. It is there because a post with "optimize" in it is a post
Kathzie has to fix after it goes up, and one with "Enterprise Partner" in it
is a post Michael has to take down.

Run against a deliberately terrible draft:

```
  BURSTINESS    ##################......  76.0
                variation 0.58 across 6 sentences (want 0.55+)
  SPECIFICITY   ######################## 100.0
                12 concrete markers, 17.9 per 100 words (want 4+)
  SLOP DENSITY  ........................   0.0
                5 stock terms, 7.5 per 100 words (in today's fast-paced world, let that sink in, leverage, robust, ...)
  FINGERPRINT   ........................   0.0
                1 invisible, 1 em dash, 0 curly quote, 0 ellipsis, 0 hard space
  VOICE         ###################.....  77.5
                6.0 contractions, 7.5 personal pronouns per 100 words, 3 structural tell(s) [not-just, rocket, engagement-bait]
  HOUSE STYLE   ........................   0.0
                4 American spelling(s) (analyze, centralize, optimize, organization), 2 banned phrase(s), 8 hashtag(s), 1 em dash [Enterprise Partner, game-changer, 8 hashtags] unexplained: Digital Factory
--------------------------------------------------------------
  HUMAN SCORE   ######..................  25.4   FLAGGED
  Weakest signal: SLOP DENSITY. Fix that first.
```

After `humanize.py`, with the flagged structures still unrewritten:

```
  25.4 FLAGGED  ->  60.4 REVIEW   (+35.0)
```

The last stretch to PASS is the part the script deliberately leaves to you.
A real DI post, written the way the skills write, comes in like this:

```
  HUMAN SCORE   ######################..  89.7   PASS
```

## The fine print, which is the honest part

**These skills do not post to LinkedIn, and they should not.** There is no
official API for posting to a personal profile without an approved partner
app, and automating the site with a browser or a third-party tool violates
[LinkedIn's User Agreement](https://www.linkedin.com/legal/user-agreement) and
gets accounts restricted. A restricted account with "Design Industries" in the
headline is a company problem. So every skill here ends the same way: a
copy-ready block, and a person pastes it. That is not a limitation bolted on
afterwards, it is the design. It is also why the approval gate is real rather
than a setting.

**The first five checks are local heuristics, not detector APIs.** They are
modelled on the signals public detectors key on, and they run entirely on
your machine. They are not GPTZero, Originality, Copyleaks, Winston or
Turnitin, they do not call those services, and they cannot promise those
verdicts. Fixing what they measure tends to move those numbers, because they
are measuring the same underlying things. That is the whole claim. Nobody can
honestly sell you "undetectable", and anybody who does is selling you
something.

**The invisible-character pass is real and it is narrow.** It removes the
zero-width and format characters that end up in generated text and survive a
copy-paste. That is a genuine, checkable fingerprint. It is not a claim about
defeating a cryptographic watermarking scheme, and this repo does not make
one.

**Nothing here fabricates, and nothing here names a client.** No invented
metrics, clients or outcomes go under Michael's name or DI's. If a draft
needs a number nobody has given, it comes back with `{{number}}` in it and a
flag, every time. Client work is anonymised by default, and naming one needs
approval recorded in the post's receipt, even for the clients on the approved
logo list.

## Files

```
skills/di-li-post/hooks.json       21 hook formulas with DI examples: template, example, what it is for, how it gets ruined
skills/di-li-human/slop.json       the lexicon: 110 terms, 350 spellings, 18 house phrases, 38 protected terms, 12 structural tells
skills/di-li-human/humanize.py     the five cleaning passes
skills/di-li-human/detect.py       the six-check panel
skills/di-li-profile/rubric.json   the 100-point profile score, with the DI alignment item
templates/positioning.md           Design Industries, as the skills understand it. Ships filled in.
templates/voice.md                 the voice profile. Michael's is pre-filled; each poster gets their own.
```

## Who does what

| who | role |
| --- | --- |
| Michael Dockery | Managing Director. Primary LinkedIn voice. Approves anything client-facing. |
| Kathzie Yambao | Runs the DI company page, the calendar and the weekly numbers. |
| Tejas | Graphics and brand assets, via Slack. |

## Credit

O
DI adaptation by Design Industries, [di.net.au](https://di.net.au).

## Licence

MIT. Take it, change it, ship it.
