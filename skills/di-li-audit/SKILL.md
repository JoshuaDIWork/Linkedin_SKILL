---
name: di-li-audit
description: >-
  Post-mortem on what Design Industries has already published on LinkedIn,
  Michael's profile or the company page: which posts actually worked, why,
  and what to stop doing. Use when someone at DI pastes LinkedIn analytics or
  past posts and asks "what's working", "why did this flop", "read my
  analytics", "audit my content", "weekly numbers", or wants to know what to
  double down on.
---

# di-li-audit

The only honest source of what works for an account is that account. Every
rule in every LinkedIn guide, including the ones in this pack, is a prior.
Michael's own last 30 posts, and the DI page's, are the evidence.

## Input

Ask for whichever the user has:

- The post analytics export (LinkedIn: Analytics, Content, Export). CSV. For
  the company page: Page analytics, Content, Export.
- Or a screenshot per post with impressions, reactions, comments, reposts.
- Or just the posts and their reaction counts, which is enough for a first
  pass.

Also read `~/.claude/di-linkedin/log.md` if it exists, since it records which
voice and which hook formula each post used and whether it had a graphic.

Audit Michael and the DI page **separately**. A company page has a different
baseline and mixing them hides both patterns.

## What to actually measure

Raw impressions are the least useful number on the page, because they are
mostly a function of how many people already follow the account. Compute
these instead, and show the working:

| metric | how | what it tells you |
| --- | --- | --- |
| **Engagement rate** | (reactions + comments + reposts) / impressions | whether the post earned its reach |
| **Comment ratio** | comments / reactions | whether it started something or just got a nod |
| **Reach multiple** | impressions / follower count | whether it travelled past the existing audience |
| **Click rate** | clicks / impressions, if available | whether the first-comment link did its job |
| **Save/send rate** | if available | the strongest single predictor of future reach |

Rank by engagement rate and reach multiple, not impressions. A post with 900
impressions and 40 comments beat the one with 12,000 impressions and 6.

Kathzie tracks impressions, engagement rate and clicks weekly. When this
skill is run weekly, print those three for the week first, per profile, in a
form she can paste straight into the tracker.

## Then find the pattern

With the top 5 and bottom 5 side by side, look for what actually separates
them, and be willing to conclude something the user will not like:

- Hook formula. Which numbers from `hooks.json` are in the top 5?
- Voice. Did Michael's posts or the DI page's do the work?
- Theme. Which of the five positioning themes is carrying the account, and
  which is dead weight?
- Format. Text, document, image, video. Did the Tejas graphics earn their
  turnaround?
- Length.
- Whether an offer or CTA was in the post, and what it did to comments.
- Day and time: check this **last**, and only if the others show nothing. It
  is almost never the cause, and it is where people want it to be.
- First-two-hour replies. Posts DI replied to inside two hours versus not.

State the finding as a claim with the evidence attached, and say how confident
it is. With 30 posts you can see a pattern; with 6 you cannot, and you should
say that instead of inventing one.

## Output

```
AUDIT  ·  Michael  ·  31 posts  ·  12 Jun - 5 Sep

WEEKLY  (for Kathzie's tracker, w/c 1 Sep)
  impressions 14,200  ·  engagement rate 3.1%  ·  clicks 212

TOP 5 BY ENGAGEMENT RATE
  8.1%  #3  Mistake      "$18,000 is what one unread renewal notice cost"    1,940 imp
  6.4%  #20 Walk-Away    "We turned down a 2,000-seat migration"             2,210 imp
  ...

BOTTOM 5
  0.4%  #5  List         "7 Jira plugins every admin needs"                11,400 imp
  ...

WHAT THE DATA SAYS
1. Posts where DI was the one who looked bad: mean 6.2% vs 1.1% for
   everything else. n=6. This is your strongest signal and it is not close.
2. Tool listicles get impressions and nothing else. High reach, no comments,
   no clicks. Three of your bottom five.
3. Posts with a Platform Discovery line in them: no drop in engagement.
   Posts with a price in them: comments halve. n=4, low confidence.
4. Day of week shows nothing. Tuesday mean and Friday mean are inside the
   noise. Stop optimising it.

STOP: listicles about plugins.
DO MORE: the ones with a cost DI paid, and a number.
```

Then hand the conclusions to `/di-li-plan` so next week's plan is built on
DI's own evidence rather than on defaults.
