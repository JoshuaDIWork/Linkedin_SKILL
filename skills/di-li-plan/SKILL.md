---
name: di-li-plan
description: >-
  Build the week on LinkedIn for Design Industries: what Michael posts, what
  the DI company page posts, when in AEST, and who to engage with in the
  Atlassian ecosystem. Use when someone at DI says "plan my week", "what
  should I post", "content calendar", "I have nothing to post about", "plan
  the company page", or wants a posting schedule and an engagement list.
---

# di-li-plan

The control room. Everything else in this pack executes; this decides what
gets executed. Run it once a week, on the same day. Monday morning AEST is the
working default, so Tuesday's post is drafted before Tuesday.

## Input

Read `~/.claude/di-linkedin/positioning.md`, `voice.md` and `log.md` if they
exist. The plan should not repeat a theme from the last fortnight, and it
should not put a hook formula that flopped in `/di-li-audit` back on the
schedule. Then ask for one thing only, because it is the thing that changes
each week:

**What actually happened this week.** A client call, a number, a mistake, a
thing the team built, a licensing surprise, an Atlassian announcement, an
argument. This is where posts come from. "AI" is not a plan. "The Rovo agent
that answered 40 service desk tickets on its first day" is a post.

The themes, audience and engagement targets live in `positioning.md` and do
not need asking again.

## Two calendars, one plan

| profile | posts a week | voice | who ships it |
| --- | --- | --- | --- |
| **Michael** | 3, sometimes 4 | first person, opinions, proof, stories | Michael pastes it |
| **DI page** | 2 | "we", practitioner tips, team, events, approved client stories | Kathzie pastes it |

Never both on the same day. Never the same theme in the same week. The DI
page can repost Michael's best post of the week two days later with one new
line on top, and that counts as one of its two.

Four posts a week on a personal profile beats seven. Consistency is a floor,
not a target, and the fifth post is almost always the weak one.

## What to post

Mix across the week, never two of the same type back to back:

| type | share | job | usually lands on |
| --- | --- | --- | --- |
| **Proof** | 1 per week | something that happened, anonymised, with a number | Michael |
| **Opinion** | 1 per week | a position that could lose a follower | Michael |
| **Teach** | 1 per week | one Atlassian thing the reader can do today | DI page |
| **Story** | 1 per fortnight | a scene with dialogue and a cost | Michael |
| **Team / culture** | 1 per fortnight | F1 culture, DI Life Skills, a hire, an event | DI page |
| **Offer** | 1 per fortnight | one DI offer, said plainly, no apology, from the positioning map | either |

For each slot give: the theme (from the five in `positioning.md`), the
specific angle drawn from what actually happened, the voice, and the hook
formula number from `di-li-post/hooks.json` that fits it. Not a topic, an
angle.

Each slot also says whether it wants a graphic, so Tejas gets the Slack
request on Monday rather than Thursday morning.

## When to post

DI's audience is at a desk in Melbourne, Sydney and Brisbane. The default is
**Tuesday to Thursday, 8:00-10:00am AEST**, with Monday afternoon and Friday
morning as the second tier. Weekends are for a personal story or nothing.
Perth and Auckland readers are a minority; do not shift the schedule for
them.

But state this plainly: **the day and hour matter far less than whether the
first line is good.** If someone is optimising posting times before their
hooks work, they are polishing the wrong thing, and you should say so.

Whoever posts replies to comments inside two hours. Put that in the plan as a
calendar block, not as a hope.

## Who to engage with

Build a list of 10, split three ways, from the Atlassian ecosystem and DI's
market:

- **5 reach**: Atlassian product leads and evangelists, Australian CIO
  commentators, well-followed Atlassian Community voices. People with the
  audience DI wants, whose posts DI can genuinely add to. Comment before they
  have 20 comments or nobody sees it.
- **3 peers**: other Solution Partners and Marketplace vendors DI respects.
  This is the group that reciprocates. Never a dig, ever.
- **2 buyers**: Heads of Digital and platform owners at organisations DI
  wants. Comment on their posts for weeks before any DM, and never pitch in a
  comment.

20 minutes a day, before posting, not after. Comments on other people's posts
are what makes DI's own post land.

## Output

```
WEEK OF 6 OCT  (AEST)

MON  engage only  (20 min, list below)  ·  brief Tejas: THU tile
TUE  8:15am  MICHAEL  PROOF    #17 Time Anchor    - licensing proposal, 5 hrs to 20 min
WED  engage only
THU  8:00am  DI PAGE  TEACH    #21 Direct Value   - the Jira automation rule that closes stale tickets. Give it away.
FRI  8:30am  MICHAEL  OPINION  #1  Contrarian     - why a 3-month AI pilot is a delay, not a pilot
SAT  -
SUN  4:00pm  MICHAEL  STORY    #9  Cold Open      - "can we just add 200 more licences"
next week: DI PAGE culture post (new hire), MICHAEL offer post (Security Uplift Phase 1)

ENGAGE  (5 reach / 3 peers / 2 buyers)
  ...

Say "write Tuesday" and I will draft it.
```

Write the plan to `~/.claude/di-linkedin/plan.md` so the other skills can
read it, and say who owns each row. Nothing is scheduled or posted anywhere.
This is a plan, and Michael and Kathzie run it.
