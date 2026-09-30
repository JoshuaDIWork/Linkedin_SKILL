---
name: di-li-inbox
description: >-
  Triage a Design Industries LinkedIn inbox, Michael's or a team member's:
  sort connection requests and DMs into leads, partners, candidates, peers,
  asks and spam, and draft the replies worth sending. Use when someone at DI
  says "my inbox is a mess", "triage my DMs", "should I reply to this",
  pastes a batch of LinkedIn messages, or is drowning in connection requests
  and vendor pitches.
---

# di-li-inbox

Most LinkedIn inboxes are 80% noise, and the cost of that noise is that the
20% goes unanswered for a week. For an MD of an Atlassian partner the noise
is specific: Marketplace vendors, offshore dev shops, lead-gen agencies
selling lead-gen. This skill separates them, then writes only what is worth
writing.

## Before you write

Read `~/.claude/di-linkedin/positioning.md` and `voice.md`. Reply as the
person whose inbox it is.

## Input

The user pastes the messages. Screenshots are fine. Do not log into their
account or read their inbox with a browser tool.

## Sort into six

| bucket | signal | action |
| --- | --- | --- |
| **LEAD** | describes a problem DI solves, asks about Atlassian licensing, Cloud, AI, security, or about working together | reply today, full answer, flag for HubSpot. Sundown Rule applies. |
| **PARTNER** | Atlassian staff, another Solution Partner, a Marketplace vendor with a real reason to talk | reply this week, warm, no commitments in writing |
| **CANDIDATE** | wants to work at DI, or is a recruiter with a candidate | reply if there is or might be a role, one warm line and a pointer to careers if not |
| **PEER** | someone in the field with something genuine to say | reply this week, keep it human |
| **ASK** | wants advice, time, an intro, a favour, a "quick chat" | reply if it is cheap and specific, decline cleanly if not |
| **SPAM** | lead-gen sequence, offshore dev shop, "quick question" with no question, a vendor pitch with no reason DI specifically | archive, no reply |

Print the counts first. Seeing "3 leads, 1 partner, 2 candidates, 41 spam" is
most of the value.

## Detecting a sequence

Automated outreach has a shape: an invite note with no specifics, a message
that arrives within minutes of the accept, "quick question", "I noticed you
work in {IT consulting}", a calendar link in message one, then a bump exactly
four days later. When you see it, mark it SPAM and say which tell gave it
away. Nobody at DI owes a reply to a script. And note the irony: the shape
this skill detects is the shape `/di-li-dm` refuses to write.

## Replies

- **LEAD**: answer the actual question in the message, in full, for free. If
  it is a fit, the offer is one sentence at the end, from the positioning
  map. If it is not, say so and point them somewhere useful. Both outcomes
  are good. Flag the message in the receipt so it lands in HubSpot the same
  day.
- **PARTNER**: Atlassian staff get a reply the same day, always. Other
  partners get warmth and no detail about DI's clients or pipeline. A vendor
  with a genuine reason gets a "send me the one-pager" and nothing more until
  Michael has seen it.
- **CANDIDATE**: DI is a 25-person team and hires carefully. If there is a
  role, ask for the CV and say who will be in touch. If not, one warm line,
  and keep the door open honestly rather than with "we'll keep you on file".
- **ASK**: if it costs under ten minutes and is specific, do it. If it is
  "can I pick your brain", decline in one warm sentence and give them the one
  answer you would have given on the call. That is the polite version and it
  is also the more useful one.
- **DECLINES** are short, warm and final. No "let's revisit in Q3" if there
  is no Q3.
- **Australian English, no em dashes.** Everything through `/di-li-human`.

## Output

Grouped by bucket, counts first, drafts only for the buckets that get replies,
each one humanised. Then the gate: the person sends them.

```
INBOX  ·  Michael  ·  52 items  ·  3 LEAD, 1 PARTNER, 2 CANDIDATE, 3 PEER, 2 ASK, 41 SPAM

LEAD  (3, flag all for HubSpot today)
...

SPAM  (41) - archive. 34 are the same sequence: no-specifics invite,
"quick question" within 4 minutes of accept, calendar link in message one.
6 are offshore dev shops. 1 is a lead-gen agency selling lead-gen.
```
