# CONTENT AGENT BRIEF — the rubric, the question bank, the grader calibration

> Paste as the opening message of a dedicated session.
> **This is the moat.** The web app is a weekend; a calibrated rubric and 40 genuinely
> discriminating scenarios are not, and they are the only thing a competitor can't clone
> from a screenshot.

---

## What you own

1. The **6-axis rubric** with observable behaviors at each of 4 levels.
2. **40 scenarios**, AI-infra flavored, each with a reference solution tree.
3. The **12 diagnostic items** (open spoken response, graded by the judge) derived from
   the scenarios.
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

#### Coverage gap found in review, to close in the bank

A simulated reviewer whose domain is training infrastructure **declined to sign the claim
that the 12-item pack covers AI infrastructure**, and the count supports it: 2 of 12 items
touch training at all, only 1 is a training-infra design problem, and nothing covers
distributed training, collective communication, or checkpoint/restart. The 12 seeds lean
heavily on inference serving and the request path, which is where the cheapest realistic
scenarios are, not where the field's weight sits.

This is a real limitation of what shipped, not a note for later: the public pages must not
claim coverage the bank does not have. Either the bank fixes the balance, or the framing
narrows honestly to inference and serving — which is a defensible product and arguably a
sharper one.

To fix the balance, the **Training & data** family needs the problems that family is
actually about, not just its data pipeline:

- a collective-communication problem — all-reduce cost against batch size, where the
  bandwidth arithmetic decides tensor-vs-data parallelism
- checkpoint/restart under failure — checkpoint size against write bandwidth and MTBF,
  where the interval is a derived number and not a config value
- a straggler or elasticity problem — what a slow or lost node does to a synchronous step
- gradient accumulation vs microbatching against a memory ceiling

Each is a capacity problem with a binding constraint and a number that moves the design,
which is what this rubric scores. The absence is a sampling artifact of writing 12 items
quickly, and it is visible to anyone from that domain.

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

**Open spoken response, not multiple choice.** The engine already captures voice,
transcribes it, and runs a judge against vetted per-item rubrics — so the diagnostic uses
the instrument the engine has, and the same rubric grades both the diagnostic and the paid
mock. Shipped form: `questions.json` in this folder.

**Why not multiple choice**, since the playbook's generic Layer 1 prescribes it and it is
the cheaper instrument:

- `communication_collaboration` is **structurally unmeasurable** by multiple choice. It is
  one of the six axes, the playbook names a communication axis as mandatory, and it is the
  most shareable finding on the scorecard because nobody has ever scored it for this
  cohort. An instrument that cannot produce it cannot produce the artifact.
- Recognising the right answer among four and *generating* it under time pressure are
  different skills, and the loop tests the second one. A multiple-choice diagnostic would
  systematically over-score the cohort, and the reveal has to be credible enough to share.
- One rubric across both instruments is what lets the diagnostic be the baseline the paid
  product shows movement against. Two instruments means two calibrations and a progress
  claim that does not hold.

Rules, which keep the parts of the playbook's guidance that survive the format change:

- Scenario-based forced tradeoff under constraints. Never trivia — trivia is googleable and
  measures recall, not the thing the loop tests. **Unchanged, and it is the important one.**
- **Hard numeric constraints stated in the prompt**, and the prompt asks for exactly ONE
  load-bearing decision plus its reason. A 45-minute design cannot be answered in 60
  seconds; a single judgement call can.
- **Answerable out loud in under 60 seconds.** Reference answers run ~150–175 words. An
  item whose answers systematically run long is over-scoped — see the item analysis in
  `calibration-plan.md`.
- **Every `model_answer` contains at least one concrete number**, with its derivation or its
  assumption stated out loud. No exceptions. A model answer without a number teaches the
  judge that vagueness scores at the bar.
- **The `traps` become the `bad` field, not distractors.** Same discipline, better use: each
  `bad` is a real failure mode a competent senior engineer actually makes, and the write-up
  says *why* it is real. Several are failure modes the published interview guides name
  directly. An invented failure mode teaches the judge to penalise something nobody does.
- `terms` is diagnostic vocabulary, **not a keyword scorer**. Presence of a term is not
  credit. Absence of all of them alongside a correct decision is a communication finding,
  not a knowledge finding. The judge must be told this explicitly or it degrades into bingo.
- Each item maps to 1–2 axes. Twelve items × 2 axes = 24 slots over 6 axes, so aim for
  **4 items per axis** rather than the ≥2 minimum — per-axis reliability is what makes the
  named blind spot defensible, and a 2-item axis cannot support it.
- **Difficulty targets do not carry over.** "A strong candidate gets ~8/12" is a
  right/wrong-scored target. For an ordinal 0–3 instrument the equivalent checks are mean
  band per item, item–total correlation, floor/ceiling share, and per-axis Cronbach's α —
  all specified with thresholds in `calibration-plan.md`. Expect to cut items, so author
  4–6 spares from the same families.

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
schema above, 12 open-response diagnostic items with axis mappings, grader + interviewer
prompts, calibration report.

**Delivered so far:** [`rubric.md`](rubric.md), [`questions.json`](questions.json) (the 12
items), [`prompts.md`](prompts.md) (interviewer, diagnostic probe, grader, plus the
code-enforced validation table), [`calibration-plan.md`](calibration-plan.md),
[`calibration-plants.json`](calibration-plants.json) (12 grader fixtures) and
[`dry-run-report.md`](dry-run-report.md). **Still owed:** the 40-scenario bank — which
Prompt 1, the 45-minute mock interviewer, is blocked on — and the calibration numbers,
which need live sessions.

The diagnostic is **open spoken response**, which has two consequences the build agent owns:

1. **A mic-permission prompt before question 1 would violate the hardest non-negotiable in
   the playbook** — no interstitial before first paint. So question 1 renders with a text
   box and offers voice as an upgrade; the text path stays first-class, not a fallback,
   because it is also what every user on a shared desk or a commute uses. The judge grades
   the transcript either way and must not reward spoken answers over typed ones.
2. **The caps and gates are code with tests, not prompt text.** The authoritative list is
   the validation table in [`prompts.md`](prompts.md) — one test per row, reject-and-re-ask
   rather than silent repair, and log the rejection rate per check. The 12 adversarial
   plants in [`calibration-plants.json`](calibration-plants.json) belong in the test suite
   as fixtures: they are regression tests on grader harshness and the cheapest protection
   against drift toward flattery across prompt revisions. Plant 08b is the one that tests
   the relevance gate does not *over*-fire; the other eleven only test harshness.

To the **GTM agent**: the 40 scenario slugs and titles, the rubric axes in plain language
for public copy, and the calibration numbers — they are the strongest credibility claim the
product has, and the only honest basis for saying the scoring is real.
