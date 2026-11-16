# CONTENT AGENT BRIEF — the rubric, the question bank, the grader calibration

> Paste as the opening message of a dedicated session.
> **This is the moat.** The web app is a weekend; a calibrated rubric and 40 genuinely
> discriminating scenarios are not, and they are the only thing a competitor can't clone
> from a screenshot.

---

## What you own

1. The **6-axis rubric** with observable behaviors at each of 4 levels.
2. **40 scenarios**, AI-infra flavored, each with a reference solution tree.
3. The **12 diagnostic items** (multiple choice) derived from the scenarios.
4. The **grader calibration set** and the agreement measurement.
5. The **public scenario pages** — the worked at-bar answers that double as the
   acquisition engine.

You do not build UI. You do not write the launch plan.

---

## PART 1 — The rubric

Six axes. These mirror how real system design rounds are actually scored; use the
industry's own vocabulary rather than inventing a taxonomy, because a practitioner has to
look at this and recognize it instantly.

| Axis | What it measures |
| --- | --- |
| `requirements_scoping` | Elicits functional + non-functional requirements, states SLOs, and **explicitly cuts scope** |
| `capacity_cost_estimation` | Produces numbers. QPS, bytes, GPU-hours, $/1M tokens, memory. Orders of magnitude, stated assumptions |
| `high_level_design` | Coherent components and data flow that actually satisfies the stated requirements |
| `deep_dive_failure_modes` | Goes deep on the hard component; names failure modes, backpressure, partial failure, idempotency |
| `tradeoff_articulation` | **Names the axis**, picks a side, defends it against the alternative. The bar-setter |
| `communication_collaboration` | Structures time, signposts, checks in, handles pushback without collapsing or digging in |

### The 4-level scale

For every axis, write observable behaviors — not adjectives — at each level:

```
0  No signal      — never addressed; did not come up
1  Below bar      — addressed but wrong, vague, or unprompted-only
2  At bar         — does the thing competently when it matters
3  Above bar      — does it unprompted, with precision, and anticipates the consequence
```

Worked example, `capacity_cost_estimation`:

- **0** — never produced a quantity.
- **1** — gave a number with no derivation, or was off by >100x without noticing, or only
  estimated after being directly asked twice.
- **2** — derived request volume, payload size, and storage/GPU need from stated
  assumptions; arithmetic roughly right; identified the binding constraint.
- **3** — sized it unprompted, stated assumptions explicitly, did the GPU/token cost math,
  and **used the result to change a design decision** — which is the actual signal.

That last clause is the pattern for every "above bar" definition: the candidate doesn't
just perform the behavior, they *let the result of it alter the design*. Write all 24 cells
this way.

### Where to ground it

Do not invent the rubric from imagination. Ground each axis in observable sources —
published interview guides, company engineering-blog descriptions of their loops,
practitioner write-ups, the structure of existing well-regarded system design courses —
and **cite the sources inline in the rubric file**. An invented rubric reads as invented,
and this cohort is unusually good at detecting that.

---

## PART 2 — The scenarios

### Positioning constraint

Keep the **AI-infra framing**, always. This is the entire wedge. But understand what's
underneath: reported frontier-lab questions use AI framing over classic distributed-systems
cores — you'll hear "GPU cluster," "inference batch," "model binary," and the actual skills
tested are capacity math, queueing, backpressure, multi-tenancy, and consistency. So:

- The *surface* is AI infra. That's the positioning, the SEO, and the reason this cohort
  picks you over a generic course.
- The *substance* is classic infra judgment. That's why the training transfers, and it's
  what keeps the product honest.

Say this explicitly on the public pages. It's a genuinely useful insight for the candidate
and it inoculates you against "this is just AI hype."

### Target: 40 scenarios

Expand from the 12 seeds in `01-BUILD-AGENT.md`. Spread across these families:

- **Inference serving** — continuous batching, KV cache pressure, speculative decoding
  rollout, heterogeneous fleet routing, cold-start on large weights
- **Multi-tenancy & quota** — token rate limiting, fair-share scheduling, GPU credits,
  noisy-neighbor isolation, overdraft semantics
- **Request path** — streaming delivery, safety classifiers inline, caching semantically
  similar prompts, retry/idempotency with side-effecting tools
- **Training & data** — PB-scale data pipelines, dedup, shuffle, reproducibility,
  checkpoint storage, annotation/RLHF throughput
- **Eval & observability** — 50k evals per commit, flake detection, cost attribution per
  tenant/model, token-level telemetry
- **Retrieval & agents** — 10B-embedding vector search, index refresh, agent orchestration
  fan-out, partial failure

### Scenario schema

```yaml
slug: continuous-batching-latency-budget
title: Design the request batcher for a hosted LLM API
family: inference_serving
axis_weights: {capacity_cost_estimation: 0.3, deep_dive_failure_modes: 0.3, ...}
prompt: >
  One paragraph. Realistic. Hard numeric constraints stated up front.
constraints:
  - p99 time-to-first-token < 400ms
  - 8x H100 per node, 40 nodes
  - traffic is 70% short prompts, 30% 100k-token context
required_beats:            # what an at-bar candidate must reach
  - sizes the batch window against the TTFT budget
  - separates prefill from decode scheduling
  - names the latency/throughput tradeoff explicitly and picks a side
  - handles the long-context minority without starving short requests
traps:                     # plausible wrong turns; the interviewer probes toward these
  - static batch size chosen with no reference to the latency budget
  - one queue for all request shapes
  - assumes GPU memory is the only binding constraint
followup_tree:             # escalating probes, keyed to what the candidate has said
  - if_missing: capacity math      -> "Roughly how many concurrent requests fit?"
  - if_asserted: "we'll just autoscale" -> "Weights take 90s to load. Now what?"
  - if_at_bar: everything          -> "Halve the GPU budget. What breaks first?"
at_bar_answer: >
  The worked answer. Used by the grader for contrast, and published on /q/[slug].
sources: [...]
```

`followup_tree` is the most important field. It is what makes the AI interviewer feel like
a real interviewer rather than a question-reader: the probe is **conditional on what the
candidate has already said**, and it escalates when they're doing well. Write at least 6
conditional branches per scenario.

### The 12 diagnostic items

Derive multiple choice items from the scenarios. Rules:

- Scenario-based forced tradeoff under constraints. Never trivia — trivia is googleable and
  measures recall, not the thing the loop tests.
- 4 options, **at least 2 defensible-looking**. The discriminator is always whether the
  reader reasons from the stated constraint.
- **Every distractor is a real mistake a competent senior engineer makes.** If a distractor
  is obviously wrong, you have wasted one of only 12 slots. Source distractors from the
  `traps` field — those are real by construction.
- Include 2 items requiring an actual number or order of magnitude. Highest-signal items in
  the instrument.
- Each item maps to 1–2 axes, so 12 items produce a 6-axis profile with ≥2 items per axis.
- Target difficulty: a strong candidate gets ~8/12. If the median is 10+, the items don't
  discriminate and the percentiles become meaningless.

---

## PART 3 — Grader calibration

**This is the step that determines whether the product retains.** A mock interviewer that
flatters is detected in one session and never opened again.

1. **Collect 20+ transcripts.** Run real sessions — recruit from the cohort, pay for
   transcripts if needed, include deliberately weak and deliberately strong runs.
2. **Hand-score every one** against the rubric, with a second scorer on at least 10.
   Measure inter-human agreement first; if humans don't agree on an axis, the axis is
   badly defined and must be rewritten before you tune the model.
3. **Run the grader** and compare per-axis against the human labels. Report the confusion
   per axis, not a single aggregate score — graders usually fail on one or two specific axes
   (`communication_collaboration` and `tradeoff_articulation` are the usual offenders,
   because both are judgment calls on form rather than content).
4. **Tune the prompt, not the rubric**, unless step 2 showed the rubric is the problem.
5. **Check the distribution for flattery.** Plot the score histogram. If there is no real
   left tail, the grader is being generous regardless of its agreement numbers. Enforce the
   hard caps from `01-BUILD-AGENT.md` in code, not just in the prompt:
   - no number stated ⇒ `capacity_cost_estimation` ≤ 1
   - no tradeoff axis named ⇒ `tradeoff_articulation` ≤ 1
   - any score of 3 requires a quoted justification, or it's rejected and re-asked
   - every report carries ≥2 below-bar observations with quoted evidence
6. **Version it.** `grader_version` on every grade row, so retuning doesn't silently
   invalidate users' progress history.

Re-run calibration whenever the interviewer or grader prompt changes materially.

---

## PART 4 — The public scenario pages

Each scenario becomes `/q/[slug]`: the problem, the constraints, the tradeoff space, the
traps, and the worked at-bar answer. ~40 of these.

This is the compounding acquisition surface — it's the mechanism behind the incumbents'
moats in this exact category, it gets cited by assistants when someone asks how to prepare
for these loops, and it keeps working while paid acquisition stops the day you stop paying.

Write them to be **the best free answer on the internet to that specific question**. A
page that is obviously a teaser converts worse than one that is genuinely complete, because
the complete one earns the link and the trust, and the thing being sold — repeated scored
practice — isn't substitutable by reading the page anyway.

Do not fabricate claims about what any specific company asks. Describe questions as
*reported* and cite where, or frame them as representative of the category. Overclaiming
here is both wrong and, for this cohort, instantly noticed.

---

## HANDOFF CONTRACT

To the **build agent**: rubric as structured data (24 behavior cells), 40 scenarios in the
schema above, 12 diagnostic items with axis mappings, grader + interviewer prompts,
calibration report.

To the **GTM agent**: the 40 scenario slugs and titles, the rubric axes in plain language
for public copy, and the calibration numbers — they are the strongest credibility claim the
product has, and the only honest basis for saying the scoring is real.
