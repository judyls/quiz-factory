# CONFIG — AI-lab system design interviews

Status: **qualified 5/5, not yet built.** Research grounded 2026-11-16, see
`RESEARCH-NOTES.md`.

## Step 0 — Qualification gates

| Gate | Score | Evidence |
| --- | --- | --- |
| **1. Dated pain** | **Strong** | A scheduled onsite loop with a 45–60 min system design round that sets level, and therefore a six-figure comp band |
| **2. Status at stake** | **Strong** | Level and engineering competence; this cohort already posts interview outcomes publicly |
| **3. Credible rubric** | **Strong** | System design rounds are already scored on recognizable axes industry-wide. Borrow the real vocabulary rather than inventing one |
| **4. Proven spend** | **Strong** | Hello Interview Premium ~$47/mo, ~$279 lifetime; human mock sessions ~$90–120; generic AI interview tools $8–60/mo |
| **5. Public watering hole** | **Strong** | r/ExperiencedDevs, Blind, ML-infra Discords, Hacker News, hiring-season X/LinkedIn |

**Verdict: 5/5 → build.**

## Config

```yaml
vertical:          AI-lab system design interviews (Anthropic / OpenAI / frontier-lab tier)
cohort:            Mid-to-senior backend, infra, and ML-platform engineers (L4-L6) in, or
                   within 3 months of, a frontier-lab or AI-heavy loop. Secondary: senior
                   engineers blocked on promotion by design-communication signal.
dated_pain:        A scheduled onsite loop 1-6 weeks out, whose system design round decides
                   level and therefore several hundred thousand dollars of compensation.
status_currency:   "Scored at the Staff bar on tradeoff articulation" — a credible,
                   rubric-shaped claim about engineering judgment.
scored_axes:       requirements_scoping, capacity_cost_estimation, high_level_design,
                   deep_dive_failure_modes, tradeoff_articulation, communication_collaboration
share_artifact:    An interview scorecard image: 6 axes, 4-level marks, cohort percentile,
                   one named blind spot, one named strength. Looks like a real eval form.
price_anchor:      $47-279 course pricing; $90-120 per human mock session. See
                   RESEARCH-NOTES.md, gathered 2026-11-16. Re-verify before use.
paid_product:      Unlimited AI mock system design interviews, in character, scored against
                   the 6-axis rubric with quoted evidence and at-bar answer contrasts.
retention_bridge:  "Design Review Mode" — the same engine on on-the-job artifacts: defend
                   your RFC against a skeptical staff engineer, run a design review, present
                   a migration to a VP. Solves post-offer churn and is the promotion-signal
                   product.
kill_metric:       See table below.
```

## Competitive gap

Two established facts that do not currently overlap. AI mock-interview tools are cheap
($8–60/mo) and **overwhelmingly behavioral** — one roundup notes a tool's scenario list
excludes coding and system design entirely. Meanwhile the credible system design players
sell **courses plus human mocks**: human mocks don't scale, cost $90–120, and can't be
taken at 11pm the night before an onsite. Nothing occupies *scaled, scored, adversarial
system design practice*, and the AI-infra flavor of it is emptier still.

## The honest differentiator

**The questions are AI-framed but the core is classic distributed systems.** Reported
frontier-lab prompts use "GPU cluster," "inference batch," "model binary," while the skills
actually tested are capacity math, queueing, backpressure, multi-tenancy, and consistency.
Teach the framing, drill the judgment. Saying this plainly is useful to the candidate and
inoculates the product against the "AI prep grift" reaction the category earns.

Second honest note: frontier-lab question banks are reported as **small but expanding**,
which means 40 deep scenarios can credibly cover the space — not true for a FAANG-wide
product.

## Known competitive risk

`prachub.com` already indexes company-specific ML system design questions at the
individual-question level. **The question list is not defensible.** The rubric, the
calibrated grader, and the worked at-bar answers are.

## Kill thresholds

Set actual numbers once the CEO-quiz teardown data is available
(`playbook/VIRALITY-TEARDOWN.md`). Use that data, not industry averages.

| Metric | Threshold | By when |
| --- | --- | --- |
| Quiz completion / started | TBD from teardown | Week 2 |
| **Share / completion** | TBD from teardown | Week 2 |
| Reveal → signup | TBD | Week 2 |
| **Second mock / first mock** | TBD | Week 4 |
| Free → paid | TBD | Week 4 |

Share rate and second-session rate are the two that decide whether this continues.
