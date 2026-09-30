---
name: di-li-carousel
description: >-
  Build a LinkedIn document post (carousel) for Design Industries:
  slide-by-slide copy, the cover that earns the swipe, and the PDF to upload
  on DI's brand. Use when someone at DI says "carousel", "document post",
  "slides for LinkedIn", "turn this into a carousel", "make the checklist a
  carousel", or has a list-shaped idea that would die as a text post.
---

# di-li-carousel

Document posts are the highest-dwell format on LinkedIn, because a swipe is
counted and a scroll is not. The format rewards one idea broken into steps.
It punishes a text post cut into pieces. For DI it is the natural home of the
teach post: a migration checklist, the six security domains, the five things
to check before a renewal.

## Before you write

Read `~/.claude/di-linkedin/positioning.md` and `voice.md`. Carousels
usually go out on the DI page in the "we" voice, but Michael can carry one
when the idea is his.

## When to use it instead of a text post

Use a carousel when the idea has **sequence**: steps, a countdown, a
before/after progression, a framework with parts. Use a text post when the
idea is one claim. Splitting one claim across eight slides is the most common
way carousels fail, and if that is what the user has, say so and hand them to
`/di-li-post`.

## Structure

8-12 slides. Under 8 is a text post. Over 12 and the completion rate falls off
a cliff.

```
1        COVER      the hook, 6 words or fewer, plus one line of promise
2        THE STAKE  why this matters, in one sentence, with a number if there is one
3-N      ONE IDEA PER SLIDE. A headline of 3-7 words, and at most 25 words
                    under it. If a slide needs a paragraph, it is two slides.
N+1      RECAP      the whole thing as a list, so the screenshot is useful
LAST     CTA        one action. Follow the DI page, comment a keyword, or the
                    one DI offer the topic earns. One.
```

## Slide copy rules

- **Slide 1 is 80% of the result.** Six words. Big. The rest of the deck
  cannot save a cover nobody swipes.
- **Number every slide** (3/10). Completion goes up when people can see the
  end.
- **No slide is a paragraph.** If you cannot say it in 25 words, split it.
- **The recap slide is the one people screenshot.** Make it standalone, and
  make sure it carries the DI mark.
- **Design Industries and di.net.au on every slide**, small, bottom corner.
  Screenshots travel without you.
- **Australian English, no em dashes**, spelt the way the humaniser leaves
  it. A carousel with "optimize" on slide 4 is a carousel Kathzie has to
  rebuild.
- **Atlassian product names spelt Atlassian's way**, and no Atlassian logo
  unless the partner brand guidelines allow it in that placement. If in
  doubt, the word, not the mark.

## Making the PDF

LinkedIn wants a PDF, 1080x1350 (4:5) for maximum feed real estate, under
100MB, under 300 pages. Build it as HTML and print to PDF:

```bash
# one page per slide, 1080x1350, no margins
# then: Chrome headless --print-to-pdf, or any HTML-to-PDF you already use
```

Write the HTML with one `<section>` per slide, `width:1080px; height:1350px;
page-break-after:always`, and type no smaller than 28px, because people read
these on a phone at thumbnail size.

**Do not invent a DI palette.** If a DI brand skill or design system is in
this project, use it. If not, build the deck in neutral greys with a single
placeholder accent, mark it DRAFT on the cover, and put "Tejas to apply DI
brand (Slack)" in the receipt. Tejas owns the brand assets and the final
tiles come from him.

## Output

The slide-by-slide copy first, as a numbered list the user can read in ten
seconds. Then the accompanying **post text**: a carousel still needs 2-3
lines above it, which is the actual hook in the feed, plus three to five
hashtags from the library. Run both through `/di-li-human`. Then build the
PDF only if the user approves the copy.

Nothing is uploaded to LinkedIn. The person posts the PDF themselves.
