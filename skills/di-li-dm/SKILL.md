---
name: di-li-dm
description: >-
  Write LinkedIn connection notes and DM follow-ups for Design Industries that
  get replies: the 200-character invite, the first message, and the two
  follow-ups. Use when someone at DI says "write a connection request", "DM
  this person", "outreach message", "how do I follow up", "reach out to this
  CIO", or is contacting a specific prospect, Atlassian contact or partner on
  LinkedIn.
---

# di-li-dm

The invite note is 200 characters. The first DM decides whether there is a
second one. Neither is a pitch. DI's inbox is full of the other kind, and
`/di-li-inbox` marks them as spam, so do not write them.

## Before writing, get the specifics

Read `~/.claude/di-linkedin/positioning.md` and `voice.md`, then ask for, in
one batched question:

1. **Who**: name, role, company. And which kind of person: a **prospect** (a
   Head of Digital with an Atlassian estate), an **Atlassian contact**
   (partner manager, product lead), a **partner or vendor**, or a
   **candidate** DI wants to hire.
2. **The hook**: the actual reason to reach out now. A post they wrote, a
   Cloud migration their company announced, a renewal coming up that DI knows
   about legitimately, a talk they gave at an Atlassian event, a mutual
   connection who has agreed to be named. Not "they fit our ICP".
3. **What DI wants**: a conversation, a Platform Discovery, a partner intro,
   a hire. Be honest internally, even if the message does not lead with it.

If there is no specific reason to message this person today, say so. A
message with no reason is what everyone else sends, and it is why their reply
rate is 2%.

## The invite note (200 characters)

```
{one specific reference to them} + {one line of who you are} + {no ask}
```

The note asks for nothing. It exists to make the accept obvious. Under 200
characters including spaces. Count them and show the count.

```
Your post on the 18-month Cloud migration was the most honest one I have
read on it. I run Design Industries, an Atlassian partner in Melbourne.
Would like to follow along.
                                                                    [186/200]
```

## The first message, after they accept

Wait a day. Then:

- **Two to four sentences.** A screen of text is a delete.
- **Reference the specific thing** from the note. Continuity is the whole
  reason the note was specific.
- **Give something before asking.** The most useful thing DI can give a
  prospect in one message is a fact about their own estate they did not
  have: the last-login versus licence-count test, a renewal date pattern, a
  Rovo setting that is off by default. A template, a number, a name, an
  answer. Never a brochure.
- **One ask, and make it small.** "Worth 20 minutes?" beats "let me walk you
  through Digital Factory".
- **No calendar link in message one.** It reads as a funnel, because it is.
- **Platform Discovery is not mentioned in message one.** It is free, which
  is exactly why it sounds like a pitch when it arrives too early.

## Follow-ups

Two. That is the number.

- **+4 days**: add something new. An article from di.net.au that answers the
  thing they posted about counts, if it genuinely does. Never "just bumping
  this" or "following up on my last message". If you have nothing new, you
  have no follow-up.
- **+10 days**: the close-the-loop message. Say you will stop, and mean it.
  This one gets a surprising share of the total replies, because it removes
  the pressure.

Then stop. A third follow-up converts nobody and costs the relationship, and
in a market the size of Australian enterprise IT, the relationship is the
asset.

## Never

- Never send an automated connection or message sequence. Automated outreach
  tools violate LinkedIn's User Agreement and get accounts restricted, and a
  restricted account with "Design Industries" in the headline is a company
  problem.
- Never fabricate a mutual connection, a shared event, or having read
  something the sender has not read.
- Never mention a client by name, even an approved one, in a DM to a
  prospect. "A listed healthcare group" is the ceiling.
- Never write the message that opens "I hope this message finds you well".
- Never send more than 20 invites a day from one account. Beyond that,
  LinkedIn throttles it, and a throttled account is a dead one.
- Never contact someone at a current client about switching partners. DI
  already is their partner.

## Output

The invite note with its character count, the first message, and both
follow-ups with the day they go out. All humanised through `/di-li-human`,
all in Australian English. The person sends every one of them by hand, and
logs the conversation in HubSpot themselves.
