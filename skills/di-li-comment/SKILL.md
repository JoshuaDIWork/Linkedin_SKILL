---
name: di-li-comment
description: >-
  Write comments on other people's LinkedIn posts, from Michael or the DI
  company page, that read as a practitioner with an opinion rather than a bot.
  Use when someone at DI pastes a post and wants a comment, says "comment on
  this", "engage with this", "what do I say here", or wants a batch of
  comments for the engagement round in the weekly plan.
---

# di-li-comment

Commenting is the highest-leverage thing on LinkedIn and the easiest to do
badly. A comment on an Atlassian product manager's post with 400 reactions
gets seen by more Australian IT leaders than most of DI's own posts. A generic
one gets seen by nobody and costs credibility with the author.

## Before you write

Read `~/.claude/di-linkedin/positioning.md` and `voice.md`. Decide the voice
and say it: Michael comments as "I". The DI page comments as "we", and does
so less often, because a company page arguing in someone's comments reads
oddly.

## Input

The user pastes the post text, and the author's name and role if they have
it. If they paste a screenshot, read it. If they give you a URL you cannot
open, ask them to paste the text. Do not guess what the post said, and do not
use browser automation to scrape the feed.

## The nine comment types

Pick by what the post actually is. Never default to type 1.

| # | type | when | shape |
| --- | --- | --- | --- |
| 1 | **Add a datum** | post makes a claim you can support with a number | "We see the same thing: roughly 30% of the seats in a first Platform Discovery are..." |
| 2 | **Add the missing case** | post is right but incomplete | "This holds until {condition}. Then..." |
| 3 | **Respectful disagree** | you genuinely think it is wrong | name the agreement first, then the fork |
| 4 | **Extend one line** | one sentence in the post is the good one | quote it, then build on it |
| 5 | **Ask the real question** | post skipped the hard part | one question, specific, no "curious to hear" |
| 6 | **The receipt** | DI has done the thing they described | what happened, anonymised, in two sentences |
| 7 | **The correction** | there is a factual error | be right, be brief, be kind, be sure. Atlassian licensing facts especially. |
| 8 | **The reframe** | the post has the right facts and the wrong frame | "Another way to read this:" |
| 9 | **The one-liner** | the post needs nothing, you want presence | under 12 words, must be funny or true |

## Rules

- **2 to 4 sentences.** Longer reads as a hijack. Shorter reads as filler.
- **Never open with "Great post"**, "Love this", "So true", "Couldn't agree
  more", "This resonates", or the author's first name followed by an
  exclamation mark. All six are invisible.
- **No emoji openers.** No 🔥 or 👏 as a first character.
- **Never restate the post.** The author knows what they wrote and so does
  everyone reading.
- **One idea.** A comment with two points reads as a blog attempt.
- **Say the specific thing.** If the comment could sit under any post on the
  topic, it is not a comment, it is noise.
- **Disagreement is allowed and works**, but the agreement has to come first
  and be real.
- **Never pitch in a comment.** No offer, no "DM me", no link to di.net.au.
  The comment earns the profile visit. The profile does the selling.
- **Never criticise a competitor or another Atlassian partner**, in a comment
  on their post or anyone else's. If the post is a partner's and it is wrong,
  type 2 or type 5, never type 3 or 7.
- **On Atlassian's own posts and Atlassian staff posts**, be useful and
  brief. This is the room DI most wants to be seen in, and it is watched.
- **Clients stay anonymous**, even when the client is the author. Especially
  then.
- **Australian English, no em dashes**, same as everything else.

## Output

Give **two options of different types**, labelled, plus a one-line reason for
the one you would post. Run both through `/di-li-human` first. A comment with
an em dash in it is more obviously machine-written than a post, because
comments are short and people read them closely.

```
COMMENT OPTIONS  (Michael, on @author's post about Cloud migration timelines)

[6 · Receipt]
We ran a 4,000-seat Data Center to Cloud move for a listed group last year
and the migration itself was the easy month. The eleven months before it,
getting six teams to agree what to leave behind, was the project.

[2 · Missing case]
Holds for a single-instance estate. Once there are three Jira instances
with overlapping projects, the timeline is set by the consolidation, not
the migration, and no tooling shortens that part.

Post the first. It is our own experience and it concedes the hard part,
which is what people reply to.
```

## Batch mode

If the user wants the engagement round from `/di-li-plan`, ask for the 5-10
posts as pasted text in one message, return one comment each in a single
block, and keep a running note of who has been commented on this week in
`~/.claude/di-linkedin/log.md`. Commenting on the same three people every day
is visible and it looks like what it is.

## Never

Do not auto-post. Do not use a browser tool to publish comments on anyone's
behalf. Automated posting and scraping both violate LinkedIn's User Agreement
and put the account at risk, and a restricted MD account is a company
problem. This skill writes the comment. The person posts it.
