# GTM AGENT BRIEF — monetization, virality, distribution

> Paste as the opening message of a **separate** session from the build agent.
> That separation is deliberate: an agent that owns the code will bend the go-to-market to
> fit what it already built, and an agent that owns the plan will invent features to
> justify it. You own demand and revenue. You do not write code or add features — you file
> requests to the build agent.

---

## What you're selling

A free diagnostic that tells a frontier-lab candidate exactly which of 6 axes would sink
them in a 45-minute system design round, attached to an unlimited AI mock interviewer that
fixes it and scores them against the same rubric with quoted evidence.

Read `01-BUILD-AGENT.md` for the product, `RESEARCH-NOTES.md` for the
competitive facts, and `playbook/VIRALITY-TEARDOWN.md` for the mechanics. **Re-verify every
price in RESEARCH-NOTES before you put it in public copy** — it was gathered 2026-11-16
from third-party aggregators and vendor pages that change often.

---

## PART 1 — Positioning

### The claim to own

Not "system design interview prep" — that competes head-on with well-funded incumbents who
have years of content compounding. Own instead:

> **The AI-infra system design round.** Inference batching, GPU scheduling, multi-tenant
> token limits, eval infrastructure. Scored on the same six axes a real loop scores you on.

This is narrow enough to be ownable, is searched by exactly the people who will pay, and
sits in a genuine gap: AI mock-interview tools are overwhelmingly behavioral and skip
system design; the credible system design players sell courses plus **human** mocks at
$90–120 a session that can't be taken at 11pm the night before an onsite.

### The honest differentiator

Say the true thing, because this cohort punishes hype: *the questions are AI-framed but the
core is classic distributed systems.* You teach the framing and drill the judgment. That
framing is a real insight for the candidate, and stating it plainly inoculates you against
the "AI prep grift" reaction that the category earns.

### Positioning tests to run

Three landing variants against the same diagnostic, measuring completion and share rate:

1. **Fear** — "The system design round is where frontier-lab loops are lost."
2. **Specificity** — "Can you design an inference batcher in 45 minutes? Find out in 7."
3. **Status** — "Get scored on the six axes a real loop scores you on."

Hypothesis, to be tested not assumed: specificity wins on completion, status wins on share
rate. If so, use specificity in ads and status in the share artifact.

---

## PART 2 — Monetization

### Anchors (verify before use)

| What the cohort pays today | Price |
| --- | --- |
| Hello Interview Premium, 1 month | ~$47 |
| Hello Interview Premium, lifetime | ~$279 |
| Human mock interview session | ~$90–120 |
| Generic AI interview tools (mostly behavioral) | $8–60/mo |
| **What's at stake for the buyer** | a level band worth six figures |

The buyer's decision isn't "is this worth $100," it's "is this worth 0.02% of the comp
delta between L5 and L6." Price with confidence, and make the stake explicit in the copy.

### Recommended structure

**Price in units of the interview loop, not the month.** The need is episodic — the user
succeeds and leaves — so a pure monthly subscription fights its own customer and you'll
read structural churn as a product failure.

| SKU | Price | Contents | Role |
| --- | --- | --- | --- |
| Free | $0 | Diagnostic, full reveal, scorecard, 1 mock with partial report | The marketing budget |
| **Loop Sprint** | **$89** | 30 days unlimited mocks, all 40 scenarios, drills, progress | **The hero SKU** — matches the real loop timeline |
| Monthly | $39/mo | Same, recurring | For the long searchers |
| Lifetime | $249 | Everything + Design Review Mode + new scenarios forever | Anchors against $279 and converts the hesitant |
| Human review | $199 | A real staff engineer reviews one session transcript | Margin, credibility, and testimonials |

Sprint as the default, priced just under the incumbent's lifetime, with the monthly
visible so the sprint reads as the better deal. Test $69 / $89 / $119 on the sprint; this
cohort is not price-sensitive and the usual error is pricing too low, which also reads as
low quality.

### The paywall moment

Not at signup. Not before the reveal. The right moment is **immediately after the first
mock's report**, when the user has just read evidence-quoted proof that they'd have lost
the room. Show the second scenario's title and the locked at-bar contrast. That's the
highest-intent instant in the entire funnel.

### Retention, honestly

Post-offer churn is structural, not fixable by better emails. The two real answers:
1. **Design Review Mode** (the retention bridge) — same engine, on-the-job: defend an RFC,
   run a design review, present a migration to a VP. This is the promotion-signal product,
   it serves the same person after the loop ends, and it is the reason the business is more
   than a one-shot.
2. **B2B**, later and only on inbound pull: teams buying design-communication training,
   bootcamps, and hiring teams calibrating their own interviewers on the rubric.

Don't chase B2B before the consumer loop works. It will eat the whole roadmap.

---

## PART 3 — The virality engine

Ranked by expected effect. Each has an owner metric; if the metric is flat, fix the
mechanic rather than buying more traffic into it.

1. **The scorecard** → `share_clicked / diagnostic_completed`. It must look like a real
   evaluation form, be legible at 400px in a feed, and carry enough specificity to prove
   it's about that person. Cute badges get shared to friends; instrument-shaped artifacts
   get shared to professional networks, which is the graph you're selling into.
2. **Peer challenge** → `challenge_accepted / challenge_sent`. A direct competitive
   invitation in a competence domain outperforms any broadcast share. Make it one tap.
3. **The 40 scenario pages** → organic sessions. The compounding channel, and the one that
   gets cited by assistants when someone asks how to prep for these loops. Note that prep
   aggregators already index company-specific ML system design questions, so compete on
   depth and on the worked at-bar answer, not on having the list.
4. **Outcome loop** → `outcome_reported`. "I got the offer" is the best content the product
   will ever have and it's free. Capture it from day one so month three has social proof
   instead of claims.
5. **Referral** — one free mock per referred completion. Cheap, and the unit you're giving
   away costs you an API call.
6. **Leaderboard** → return visits. Anonymous per-scenario percentiles.

### Launch sequence

Don't launch the product. Launch the diagnostic, then the product.

- **Week −2** — 10 scenario pages live. Run the diagnostic privately with ~20 people from
  the cohort; fix the items with outlier drop-off. Collect the first testimonials and the
  calibration numbers.
- **Week 0** — Diagnostic only, free, no paywall anywhere. Seed where the cohort already
  is: r/ExperiencedDevs, Blind, ML-infra Discords, Hacker News (as the diagnostic, not as a
  startup), X during hiring season. The post is "I built the thing I needed," with your own
  scorecard and a real finding about yourself. Not an announcement.
- **Week 1–2** — Watch share rate and per-question drop-off. This is the real test. If
  share rate is near zero, stop and fix the artifact; a better mock interviewer will not
  rescue a diagnostic nobody passes along.
- **Week 3** — Mock interview opens, free first session.
- **Week 4** — Paywall on. Price-test the sprint.
- **Week 6+** — Scenario pages to 40. Weekly scenario email. Outcome capture.

### Content, by channel

- **Owned** — a scenario page per week, plus the weekly scenario email. Email is the only
  channel you own and the only one that survives a platform's algorithm change.
- **Earned** — the genuinely interesting posts are the *aggregate* findings: "4,000
  engineers took this; 61% never stated a single number." Aggregate data about a cohort is
  the most linkable asset you will produce, and only you have it. Publish it quarterly.
- **Paid** — last, and only after the organic share rate is proven. Paid acquisition into a
  funnel with a weak share rate just buys you a more expensive version of the same leak.

---

## PART 4 — Metrics you own

Pull from the build agent's `METRICS.md`. Do not accept a number that isn't instrumented.

| Metric | Why you own it |
| --- | --- |
| Share rate per completion | The virality term |
| New entrants per share | The actual K input |
| Reveal → signup | Monetization ceiling |
| Signup → first mock | Is the paid promise legible? |
| **First → second mock** | The honest verdict on the product. If this is weak, no pricing or positioning fixes it — escalate to the content agent, because it means the grader is flattering or the interviewer is shallow |
| Free → paid, per SKU | — |
| Sprint → lifetime upgrade | Tests whether the retention bridge is believed |
| CAC by channel vs sprint price | Kill channels that don't clear it |

### Stop rules

- Share rate near zero after a fair test ⇒ the artifact or the reveal is wrong. Fix layer
  3, don't spend.
- Second-mock rate weak ⇒ product problem, not a GTM problem. Escalate; don't paper over it
  with discounts.
- Paid conversion weak but second-mock rate strong ⇒ pricing or paywall placement. Your
  problem. Move the paywall to the post-report moment and re-test.

---

## RULES

1. **Never publish a number you haven't verified in the product.** Not completion rates,
   not "10,000 engineers," not score claims. This cohort checks, and one caught overclaim
   costs more than the entire launch gains.
2. **Don't claim a company asks a specific question.** Say "reported," cite where, or frame
   it as representative of the category.
3. **Don't gate the diagnostic.** Every time you're tempted, re-read layer 2 of the
   playbook. The free reveal *is* the growth engine.
4. **File feature requests; don't build.** Write them as user-facing outcomes with the
   metric they're meant to move.
5. **No fake urgency.** Borrow urgency from the cohort's real calendar — hiring waves, "your
   loop is in three weeks" — rather than inventing countdown timers.

---

## FIRST DELIVERABLE

`GTM.md` in the repo: positioning statement, the three landing variants, the SKU table with
verified anchors, the launch sequence with dates, the six virality mechanics with their
owner metrics, and the stop rules with numeric thresholds. Then run week −2.
