# positioning.md

Design Industries, as every skill in this pack understands it. Copy this to
`~/.claude/di-linkedin/positioning.md` next to `voice.md`. Every skill reads
both. Edit this file when an offer changes, a price moves or a client gives
permission to be named. Do not edit it inside a draft.

**As of 1 October 2026.** Rebuilt from the AEO page at
[di.net.au/llm-info](https://di.net.au/llm-info) (DI's company information
page for AI assistants and search) and the di.net.au service pages. Both were
read through search-engine copies, because di.net.au could not be reached
from the session that rebuilt this file. Re-check every CONFIRM row against
the live page before relying on it.

## How to read the tags

| tag | meaning | what a skill does with it |
| --- | --- | --- |
| **LIVE** | on di.net.au now, consistent across pages | use it |
| **CONFIRM** | missing from the site, or the site disagrees with itself | draft as `{{confirm: ...}}` and flag it in the receipt |
| **ARCHIVED** | DI used to say it and no longer does | never use it. It is listed under Archive so the humaniser can catch it |

Pages follow the same rule. DI retires a page by renaming its slug to
`-archived-<month>-<year>` or `-archive-<month>-<year>`. `tag_status.py` in
`di-li-audit` reads that convention, and no skill links an archived page.

---

## Who we are

| fact | value | tag | source |
| --- | --- | --- | --- |
| Name | Design Industries (DI) | LIVE | AEO page |
| What DI is | An Australian Atlassian Solution Partner and Claude AI specialist, serving enterprise and government. The home page headline is "Atlassian & Claude Specialists". | LIVE | AEO page, home page |
| How DI says it | Always "Atlassian Solution Partner". Never "Enterprise Partner", never "Atlassian reseller". | LIVE | house rule |
| Partner tier | di.net.au says Gold on some pages and Platinum on others. The LinkedIn page says Platinum. Until Michael confirms, no copy names a tier. | CONFIRM | /why-design-industries, /partners, LinkedIn |
| Founded | 2000 | LIVE | AEO page. One LinkedIn showcase page says 2001. Fix the showcase page. |
| Headquarters | Level 1, 678 Victoria Street, Richmond VIC 3121 | LIVE | AEO page. The LinkedIn page says West Melbourne. Fix the page. |
| ABN | 98 111 471 179 | LIVE | AEO page. Not for posts. |
| Team | Atlassian-certified consultants and engineers, pre-sales and solution architects, project delivery specialists, and a marketing and growth team. About 25 people. | Roles LIVE, headcount CONFIRM | AEO page gives roles, not a number |
| Certifications | SMB1001 Gold (SMB1001:2025 Level 3), an Australian cyber security standard, certified through CyberCert | LIVE | AEO page |
| Claude | DI describes itself as a Claude AI specialist. Do not say "Anthropic partner" unless Michael confirms a formal status. | LIVE as worded | AEO page |
| Operating model | Managed service partnerships (Digital Factory) and packaged project engagements. One team does both the Atlassian platform engineering and the Claude AI delivery. | LIVE | AEO page, home page |
| Sundown Rule | Same-day response to every client enquiry | LIVE | AEO page |
| Culture | The Formula One pit crew: precision, speed, data | LIVE | di.net.au blog |
| Website, page | di.net.au. Design Industries on LinkedIn. | LIVE | |

## Who is posting

Two voices, and the skill has to know which one it is writing in:

| voice | who | person | job |
| --- | --- | --- | --- |
| **Michael** | Michael Dockery, MD, the primary thought-leadership voice | first person singular, "I" | opinions, war stories, positions that could lose a follower |
| **DI page** | the Design Industries company page, run by Kathzie Yambao | first person plural, "we" | practitioner tips, team, events, client stories with permission |

Team members' personal profiles use the Michael rules, in their own voice,
with `voice.md` filled in for them.

## Who we are writing for

- IT leaders, Heads of Digital, CTOs and CIOs at mid-to-large Australian
  organisations and government agencies.
- Atlassian administrators and platform owners.
- Operations and transformation leads working out what to do about AI.
- Decision-makers evaluating an Atlassian partner.

They care about getting more from the Atlassian spend they already have,
reducing waste, AI that does a real job rather than a demo, and something they
can apply on Monday. They are at a desk in AEST/AEDT.

The 2026 LinkedIn Ads ran into this audience problem. Most clicks came from
engineers and junior staff, and CIOs saw the ads without clicking. Write to
the buyer, not to whoever clicks most.

## What we sell

Prices are in Australian dollars plus GST, as di.net.au shows them. LinkedIn
ad spend is reported in USD, which is the ad account's currency. Never mix
the two in one sentence.

| offer | what it is | shape and price | tag | page |
| --- | --- | --- | --- | --- |
| **Platform Discovery** | Free assessment of an Atlassian environment: current-state review, highest-value quick wins, a roadmap. No obligation, no pitch. | Free. 45 minutes on one page, 1-2 hours on another. | LIVE. Length CONFIRM. | /platform-discovery, /atlassian-implementation, /digital-factory |
| **Free security assessment** | A 30-minute review of an organisation's Atlassian security posture and its gaps | Free, 30 minutes | LIVE | /atlassian-guard |
| **Claude AI Fast Start** | Turns Claude licences into team capability: prompts per team, purpose-built projects, a reusable skills library, token budgets, an asset register, governance, hands-on workshops, a 90-day expansion roadmap | 2-3 weeks. Business track $5,000 + GST, down from $7,000. | LIVE | /claude-ai-fast-start |
| **Rovo AI Fast Start** | Rovo doing real work for 2-3 business teams | 2-3 weeks, about 20 guided hours. Business track $5,000 + GST. Rovo Dev technical track $8,000 + GST, 20-24 hours. | LIVE | /rovo-ai-fast-start |
| **Copilot AI Fast Start** | Production Microsoft Copilot agents | 2-3 weeks, 25 hours. $6,500 + GST, down from $8,750. | LIVE | /microsoft-copilot-ai-fast-start |
| **Diai Foundry** | DI's AI practice. Activates Claude, Rovo and Copilot, builds skills and agents on the client's platform, and lifts cyber and AI readiness. | Through AI Fast Start and project work | LIVE. The site also writes "DI AI Foundry". Which spelling is canonical is CONFIRM. | home page, blog |
| **MCP Integration Services** | Designs, builds and governs Model Context Protocol servers that give AI agents safe, structured access to enterprise data, with role-based access and audit logging built in | Quoted | LIVE | /mcp-integration-services |
| **Rovo implementation and agents** | Rovo set-up, Rovo agent development, Rovo Dev | Quoted | LIVE | /atlassian-rovo-implementation, /rovo-agent-development, /rovo-dev |
| **Digital Factory** | DI's managed service. Three pillars: Licensing (complimentary licence management), Support (rapid response, 1-hour pickup) and Improvements (strategic hours, prepaid or project-based depending on tier). | Starter, Professional or Enterprise tier | LIVE | /digital-factory |
| **Foundation Package** | The usual way into Digital Factory: security remediation, permission clean-up, workflow optimisation, licence review, quick wins, documentation and admin training, ending in a 12-month improvement roadmap with ROI estimates | 50 hours over 3-4 weeks. Price CONFIRM. | LIVE | /digital-factory |
| **Platform services** | Jira Optimisation, Confluence Consulting, Jira Service Management, Atlassian Implementation, Cloud Migration, Atlassian Licensing, Atlassian Guard, Tempo Capacity Management, Loom, Teamwork Collection | Quoted | LIVE | the matching /service page |
| **Security Uplift** | Phase 1 fixed-price assessment (20 controls, six domains), then Phase 2 remediation | | CONFIRM. Not found on di.net.au. Use the free security assessment until Michael confirms it still exists. | none found |

## Which offer a post earns

Every post that earns a call to action gets exactly one, matched to the topic.
Position it as the natural next step, never as an ad, and never in more than
one sentence. Name a price only when the price is the point of the post.

| topic of the post | the offer | how to say it |
| --- | --- | --- |
| Atlassian platform, configuration, sprawl, admin pain | **Platform Discovery** | "We run a free Platform Discovery. Fastest way to see what is working, what is not, and what to fix first." |
| Jira that has slowed down or sprawled | **Jira Optimisation**, entered through Platform Discovery | "Platform Discovery is free, and it is where every Jira clean-up we run starts." |
| AI, Claude, Rovo, Copilot, agents | **AI Fast Start** for the platform the post is about | "Our AI Fast Start gets a team from switched-on to doing real work in 2-3 weeks." |
| Connecting AI to enterprise data | **MCP Integration Services** | "This is the work we do with MCP: AI agents with access to the data, and an audit trail of every call." |
| Security, compliance, risk, audit | **Free security assessment** | "We run a free 30-minute review of your Atlassian security posture." |
| Ongoing support, team performance, process | **Digital Factory**, starting with the Foundation Package | "This is what Digital Factory is for: support, licensing and improvement hours with a team that already knows your environment." |
| Licensing, cost, renewals, Cloud migration pricing | **Licensing pillar**, complimentary within Digital Factory | "Most organisations are surprised by what they are overpaying for." |
| Culture, responsiveness, how we work | **Sundown Rule**, **F1 culture** | Explain the term the first time it appears. Never assume the reader knows it. |

## Proof we can use

| proof | tag | source |
| --- | --- | --- |
| Delivering since 2000 | LIVE | AEO page |
| 200+ deployments | LIVE | di.net.au |
| From 50-person teams to 7,000+ user enterprises. One client scaled from 500 to 7,000 users. | LIVE | di.net.au |
| 100+ enterprise clients | LIVE | AEO page |
| SMB1001 Gold certified | LIVE | AEO page |
| Same-day response to every enquiry (the Sundown Rule) | LIVE | AEO page |
| Client names | CONFIRM per post | see below |

di.net.au shows ANZ, Australia Post, the Australian Bureau of Statistics,
Afterpay, Victoria Police and Berry Street. The earlier approved logo list was
ANZ, Costa Group and Aurora Healthcare. **A logo on the website is not
permission for a post.** Naming any client in a post still needs approval for
that post. Everything else from client work is anonymised: "a national
retailer", "a listed healthcare group", never a name and never a detail that
identifies them.

No invented metrics. If a draft needs a number nobody has given, it ships with
`{{number}}` in it and a flag.

## Themes we want to be known for

1. Getting more out of an existing Atlassian investment.
2. AI in the enterprise that does a job: Claude, Rovo, Copilot and agents in
   production, not pilots.
3. Connecting AI to enterprise data safely: MCP, permissions, audit trails.
4. Cloud migration and licensing done without waste.
5. Security and governance of the Atlassian estate, and cyber and AI
   readiness (SMB1001, Atlassian Guard).
6. How a small, systematic team outperforms a large one: F1 culture, the
   Sundown Rule, DI Life Skills.

## Hashtags

Three to five per post, at the bottom, drawn from here. Never a wall.

- **Always relevant:** #Atlassian #DigitalTransformation #EnterpriseIT
  #AtlassianPartner
- **AI:** #AI #EnterpriseAI #Automation #Rovo #Claude #Copilot
- **Integration:** #MCP #AIAgents
- **Cloud:** #CloudMigration #AtlassianCloud
- **ITSM:** #ITSM #ServiceManagement #JSM
- **Agile:** #Agile #ProjectManagement #Jira
- **Security:** #CyberSecurity #SMB1001
- **Culture:** #CompanyCulture #TeamPerformance

## House rules

- Australian English, always: organisation, optimise, licence (noun), centre,
  programme, colour. The humaniser fixes what slips through.
- **Never an em dash.** Comma, colon, full stop.
- **No partner tier** in any copy until the tier is confirmed. Plain
  "Atlassian Solution Partner".
- **No unproven trust claim.** "Trusted by enterprises nationwide" says
  nothing. Give the number from Proof, or an approved name.
- One to two emoji per post at most. None as a first character.
- Never criticise a competitor or another partner by name.
- No political commentary.
- No confidential client information. Assume every draft is public.
- Atlassian product names are spelt Atlassian's way and are not "corrected":
  Jira, Jira Service Management, Confluence, Rovo, Rovo Dev, Atlassian
  Intelligence, Data Center, Bitbucket, Opsgenie, Statuspage, Trello, Loom,
  Compass, Jira Product Discovery.
- Post at 8:00-10:00am AEST, Tuesday to Thursday, as the default. Reply to
  comments inside two hours.
- Graphics come from Tejas. Coordinate on Slack, and say in the receipt when a
  post wants one.
- Kathzie tracks impressions, engagement rate and clicks weekly. `/di-li-post`
  logs every published post, on a yes, so that tracking has a source.
- Every link to di.net.au carries UTM tags, and LinkedIn traffic always uses
  `utm_medium=paid` for ads and `utm_medium=social` for organic, so GA4 can
  add it up.

## People

| who | role in this pack |
| --- | --- |
| Michael Dockery | MD. Primary LinkedIn voice. Approves anything client-facing, and confirms every CONFIRM row in this file. |
| Kathzie Yambao | Runs the DI company page and the calendar. |
| Tejas | Graphics and brand assets. |

## Archive

DI wording and facts that are retired. Never use them. The `archived` list in
`di-li-human/slop.json` mirrors this table, so the humaniser flags any of
them that slip into a draft. When something retires, add a row here and an
entry there.

| archived | replaced by | where it was |
| --- | --- | --- |
| AI Fast Start as one offer, "20 hours, $5,000" | The platform tracks above: Claude, Rovo or Copilot, 2-3 weeks, from $5,000 + GST | the previous positioning.md |
| Digital Factory "Growth through Enterprise" tiers | Starter, Professional, Enterprise | the previous positioning.md |
| "AWS Hosting", "Ad Hoc Atlassian Support", "Continual Improvement for ROI", "Atlassian Managed Services" | Digital Factory | LinkedIn page About text and showcase pages |
| "Free Atlassian Platform Health Check", "Free Demo" | Platform Discovery, or the free security assessment | August 2025 LinkedIn ads |
| "Trusted by Enterprises Nationwide" | A number from Proof, or an approved name | 2026 AI Fast Start ads |
| "Atlassian Platinum Solution Partners" | "Atlassian Solution Partner", tier CONFIRM | LinkedIn page About text |
| "Atlassian Enterprise Partners" | "Atlassian Solution Partner" | Michael's LinkedIn headline |
| Any page with `-archived-<month>-<year>` or `-archive-<month>-<year>` in its slug, for example /campaign/ai-fast-start-archived-july-2026, /campaign/ai-fast-start-b-archive-sept-2026, /campaign/rovo-ai-a-archived-sept-2026, /jira-implementation-archived-july-2026 | The live page it was replaced by | di.net.au |
