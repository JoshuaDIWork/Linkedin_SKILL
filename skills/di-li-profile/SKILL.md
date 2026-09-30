---
name: di-li-profile
description: >-
  Score a Design Industries team member's LinkedIn profile out of 100 against
  a 13-part rubric and rewrite the parts that lose points: headline, about,
  experience, featured, banner, and how the profile presents DI. Use when
  someone at DI says "optimise my profile", "score my LinkedIn", "rewrite my
  headline", "fix my about section", "get the team's profiles consistent", or
  pastes a profile and asks how it reads.
---

# di-li-profile

A profile is not a resume. A resume answers "what have you done". A profile
answers "should I message this person", and it answers it in about four
seconds, from the headline and the first two lines of the about.

For DI there is a second question the profile answers: "is this the Atlassian
partner I should talk to". Every DI profile is a landing page for the company,
whether the person wants it to be or not, so the rubric scores that too.

## Input

Ask the user to paste: headline, about section, current role and the last two
experience entries, plus whether they have a banner and featured section. A
screenshot of the top card is enough for the first pass. Do not log into
LinkedIn on their behalf.

Read `~/.claude/di-linkedin/positioning.md` for how DI is described. Read the
person's `voice.md` if one exists; a profile in the wrong voice is a profile
nobody messages.

## Score it

Read `rubric.json` in this folder. Thirteen items, 100 points, each with what
full marks looks like. Score every item, show the table, and give the total.
Be honest. Most profiles land in the 30s and 40s on the first pass, and a
generous score is useless.

```
PROFILE SCORE  41/100

  headline            3/12   job title only, no outcome, no audience
  about first 2 lines 2/10   opens with "passionate about"
  about body          4/10   history, not offer
  featured            0/8    empty
  banner              0/6    default blue
  DI alignment        1/4    says "Atlassian Enterprise Partner"
  ...
```

## Then rewrite, in this order

Fix in descending order of points lost. Do not rewrite everything at once.
The person has to actually paste each of these in.

**1. Headline (220 characters).** The formula that works:
`{what you do for whom} | {proof} | {how to start}`. Not the job title. Not
"Helping X do Y" as the first three words, which every second profile now
opens with. "Atlassian Solution Partner" or "Design Industries" appears once,
and "Enterprise Partner" never. Give three options.

**2. About, first two lines.** Everything after line 2 is behind "see more" on
mobile, so those two lines are the whole about section for most readers. They
must state who you help and what changes. No "passionate", no
"results-driven", no third-person bio, no opening with your own name.

**3. About body.** Written to one reader, in the second person. Structure:
the problem they have, what you do about it, one piece of proof with a
number, what to do next. Under 1,400 characters even though the limit is
2,600. The "what to do next" is the DI entry point that fits the person's
role, from the positioning map: Platform Discovery for consultants, AI Fast
Start for the Diai Foundry team, and so on.

**4. Featured.** Three items: the best post, the proof asset (a DI case study
or di.net.au article), the way to contact. An empty featured section is
eight points and the only place on the profile the person fully controls.

**5. Experience.** Each role gets one line of scope and two to three bullets
that are outcomes with numbers, not duties. Client outcomes are anonymised
unless the client is on the approved list in `positioning.md`. Cut anything
older than ten years to a single line. The Design Industries entry reads the
same way across the whole team: same company description, same spelling of
the offers.

**6. Banner.** One sentence of positioning and one way to reach you. The
default blue gradient is the clearest signal on the page that nobody is home.
Tejas has a DI banner; ask for it on Slack rather than making one.

## Output

Score table, then the rewrites as copy-ready blocks in fix-first order, each
one already run through `/di-li-human` so the spelling is Australian and no
em dash survives. Re-score at the end and show the delta honestly. If the
rewrite gets to 88 and not 98, say 88, and say what the remaining points need
(usually recommendations, a real banner and posting history, none of which a
rewrite can create).

Nothing is saved to LinkedIn by this skill. The person pastes each section in.
