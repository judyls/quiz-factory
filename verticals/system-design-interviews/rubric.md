# RUBRIC — AI-lab system design interviews

6 axes × 4 bands = 24 observable-behaviour cells. This file is the judge's spec and the
scorecard's source of truth. The build agent consumes it as structured data
(`scenarios.axis_weights`, `grades.axis`, `grades.score_0_3`).

**Grounded, not invented.** Every axis cites published interview guidance below. Citation
keys resolve in [Sources](#sources). Where the sources disagree with each other or with
this rubric, the disagreement is stated rather than smoothed over — see
[Where this rubric departs from its sources](#where-this-rubric-departs-from-its-sources).

**The surface is AI infra; the substance is classic distributed systems.** Every axis here
is a general system-design axis. The AI framing — batch windows, KV cache, token quotas,
GPU credits — is the vocabulary the cohort is interviewed in, but what gets scored is
capacity math, queueing, backpressure, multi-tenancy, and consistency. This is stated
plainly on the public pages on purpose: it is true, it is useful to the candidate, and it
is the honest answer to "isn't this just AI hype?"

---

## The scoring contract

```
0  No signal   — the behaviour never appeared, and nothing in the answer depended on it
1  Below bar   — appeared, but wrong, unquantified, generic, or only after direct prompting
2  At bar      — done competently, on the thing that mattered, without being walked to it
3  Above bar   — done unprompted and precisely, AND the result changed a design decision
```

**The band-3 rule, in every cell: performing the behaviour is band 2. Letting the result
of the behaviour alter the design is band 3.** A candidate who sizes the system correctly
and then proposes the architecture they were always going to propose has demonstrated
arithmetic, not judgment. This is not a stylistic preference — Hello Interview's delivery
guidance tells candidates to do capacity calculations only where they will directly
influence the design, and to skip them otherwise [HI-D]. The rubric scores the influence,
not the calculation.

Band 1 is the dangerous band to write loosely. "Vague" is not observable. Each cell below
states what band 1 *looks like*, usually as a specific thing the candidate said or failed
to say.

### Band 3 has ONE required clause. The rest are indicators.

Each band-3 cell lists several behaviours. **Only the bolded clause — the result of the
behaviour changing a design decision — is required.** The others are indicators: any one of
them corroborates a 3, and their absence does not block one.

This is not a softening, it is a correction found by dry-running the reference answers
against this rubric (see `dry-run-report.md`). Read as a conjunction, band 3 on
`tradeoff_articulation` and `high_level_design` demanded more clauses than fit in a
60-second spoken answer — **5 of the 24 reference answers in `questions.json` failed to
reach the band they exist to teach**, concentrated in exactly those two axes. A band that
the gold-standard answer cannot reach is a broken band, and every grade anchored on those
answers would have been pulled low.

In the 45-minute mock, where there is room, expect the indicators to appear and treat their
absence as the 2/3 discriminator. In the 60-second diagnostic, the required clause is the
whole test.

### Relevance gates every content axis

**A behaviour performed on the wrong problem scores at most band 1 on every axis, however
well executed.** Correct arithmetic about a constraint this scenario does not have is band
1, not band 2 — and never band 3, no matter how cleanly the number drove a decision.

Added because a plant exposed this: a strong, numerate, genuinely at-bar answer to a
*neighbouring* item in the bank scored band 3 on `capacity_cost_estimation` when graded
against this rubric, because every clause in the cell was literally satisfied. Only
`communication_collaboration` mentioned answering a different question, and most items do
not score that axis. The judge must check the answer against the prompt's stated
constraints before scoring any axis.

**How it is enforced.** Per axis, the judge emits `addresses_prompt` (bool) and
`prompt_constraint_engaged` — a verbatim quote from the *prompt* naming the constraint the
answer's decision rests on. Code clamps the axis to ≤ 1 when `addresses_prompt` is false or
the quoted constraint is not in the prompt. The gate tests the answer's **binding constraint
and decision**, not its topic or vocabulary: a neighbouring scenario considered and rejected
on the way to the right problem does not trigger it (plant 08b is the control).

### Composite and level mapping

Axis scores are not averaged into a single number for the user-facing level claim. The
composite is `mean(axis_scores)` for the percentile, but the **level claim** uses the
profile shape, because that is how real loops read a scorecard:

| Level claim | Rule |
| --- | --- |
| Below the senior bar | any axis at 0, or ≥3 axes at 1 |
| At the senior bar | all axes ≥ 1, ≥4 axes ≥ 2, `tradeoff_articulation` ≥ 2 |
| At the staff bar | ≥5 axes ≥ 2, ≥2 axes at 3, `tradeoff_articulation` ≥ 2, no axis at 0 |

`tradeoff_articulation` is gated at every level deliberately. It is the axis the sources
converge on hardest: interviewing.io's guide says the interviewer cares less about which
decision you made than about whether you can discuss the trade-offs, and names failure to
decide at all as a common failure point [IIO-1]. Hello Interview's level guidance makes the
same move differently — breadth expectations *fall* with seniority while depth and
proactiveness rise [HI-L].

Expectation shifts by level come from Hello Interview's three named dimensions — Depth,
Breadth, Proactiveness [HI-L]: mid-level candidates can expect the interviewer to drive;
senior candidates are expected to go deep in roughly two places and to surface limitations
in their own design unprompted; staff+ candidates are expected to lead nearly the whole
session. That maps onto the 0–3 bands directly: **"unprompted" is the senior/staff
discriminator, and it is why it appears in the band-3 definition of all six axes.**

---

## Axis 1 — `requirements_scoping`

Elicits functional and non-functional requirements, quantifies the ones that bind, and
**explicitly cuts scope**.

*Grounding:* Hello Interview's delivery guidance tells candidates to keep requirements
targeted, to prioritise roughly the top three to five, and warns that a long requirements
list hurts more than it helps; it also says non-functional requirements should be
quantified where possible, and calls an unquantified "low latency" requirement not very
meaningful [HI-D]. interviewing.io frames the prompt as deliberately underspecified with
the interviewer withholding information, names diving straight into design as a mistake,
and warns against extrapolating a whole product from a two-word prompt [IIO-3].

| Band | Observable behaviour |
| --- | --- |
| **0** | Began designing from the prompt as given. Never asked what the system must do, never named a non-functional requirement, never bounded the problem. Treated an underspecified prompt as a specification. |
| **1** | Produced requirements, but they are unquantified ("needs to be fast", "should scale", "must be reliable"), or recited a generic checklist unconnected to this scenario, or only named requirements after being asked twice. Listed eight requirements and prioritised none. Named a nines target with no reasoning about what it costs — interviewing.io reports that unmotivated availability targets read as impostor signal and invite harsher follow-ups [IIO-3]. |
| **2** | Named the two or three requirements that actually bind for *this* scenario and attached a number or a unit to each (a latency target, a tenant count, a cost ceiling, a recall floor). Stated at least one thing explicitly out of scope. Distinguished what the system must do from how it will be built. |
| **3** | All of band 2, **and cut scope in a way that visibly changed the design** — dropped a requirement, relaxed a consistency guarantee, or deferred a feature, and said what the cut bought (a simpler component, a smaller fleet, a latency budget that now closes). Named the requirement they would relax *first* under pressure, before being pushed. Asked the one question whose answer would most change the architecture, rather than a list of safe clarifications. |

**Band-1 trap specific to this cohort:** reciting SLO vocabulary (p99, nines, SLI/SLO/SLA)
without binding any of it to this system's traffic. Fluency in the words is band 1.

---

## Axis 2 — `capacity_cost_estimation`

Produces numbers — QPS, bytes, GPU-hours, tokens/sec, $/1M tokens, memory footprint — to
the right order of magnitude, from stated assumptions, and identifies the binding
constraint.

*Grounding, and a real tension in it:* interviewing.io says back-of-envelope math is
optional and interviewer-dependent, tells candidates to ask whether the interviewer wants
it, says being wrong largely doesn't matter, and recommends rounding up for margin of
safety [IIO-3]. Hello Interview goes further and calls upfront estimation often
unnecessary, advising calculations only where they will directly influence the design
[HI-D]. **Both sources are telling candidates that unmotivated estimation is not the
signal.** This rubric therefore does not score "did they produce a number" in the
abstract. It scores whether, when a number was load-bearing, they produced one and let it
move the design. See [the departure note](#where-this-rubric-departs-from-its-sources).

| Band | Observable behaviour |
| --- | --- |
| **0** | No quantity of any kind, in a scenario whose constraints were stated numerically. Chose between two options whose only real difference is a number, without computing either. |
| **1** | Gave a number with no derivation, or off by >100× without noticing, or only after being asked twice. Computed something irrelevant (storage for a latency-bound problem). Recited a spec figure — 80GB of HBM, 3.35 TB/s [H100] — without using it in an arithmetic step. Used a number that contradicts a constraint stated in the prompt. Derived the number that decides the question, then proposed a design it rules out (computed 40TB raw, then chose an index that needs all of it resident) — the number was produced but not understood. |
| **2** | Derived the binding quantity from assumptions stated out loud: request volume × payload, tokens/sec per GPU, KV bytes per token × context length, cost per million tokens. Arithmetic within ~2–3×. **Named which constraint binds** — memory capacity vs memory bandwidth vs compute vs network vs dollars — and showed why the others have slack. |
| **3** | All of band 2, unprompted, **and the result changed the design**: the number ruled out an architecture, resized a fleet, moved a component, forced an admission-control policy, or revealed that the stated SLO is unachievable at the stated budget — and they said so. Stated assumptions as assumptions and flagged which one the answer is most sensitive to. Rounded in the conservative direction on purpose and said which direction that was. |

**Hard cap, enforced in code, not only in the prompt:** if the candidate produced no
quantity **of their own**, `capacity_cost_estimation ≤ 1`.

"Of their own" is load-bearing and was wrong in the first draft of this file. A cap written
as "no quantity in the transcript" is trivially defeated two ways, both of which a plant
caught:

- **Echoing the prompt.** Every item states its constraints numerically, so saying "given
  our 400 millisecond target" puts a number in the transcript while deriving nothing.
- **Reciting a remembered statistic.** "vLLM gets fragmentation waste under 4 percent" is a
  quantity about someone else's system, used in no arithmetic step.

So the cap tests for a quantity the candidate **derived, estimated, or computed** — one
that is not copied from the prompt and not a recalled spec figure. Implementation: a number
satisfies the cap only if it does not appear in the prompt text and participates in a
stated derivation or comparison. All 12 diagnostic scenarios state numeric constraints, so
the cap is fair by construction — but a future scenario with no numeric constraint must be
exempted rather than scored unfairly by it.

---

## Axis 3 — `high_level_design`

A coherent set of components and a data flow that actually satisfies the stated
requirements, at the stated scale.

*Grounding:* interviewing.io says the interviewer is looking for a holistic view of the
system and its users, and for fundamentals rather than domain expertise [IIO-1]. Hello
Interview's delivery guidance allocates the largest single block of the round to high-level
design (roughly 10–15 minutes of a 45–60 minute round, after ~5 minutes of requirements and
~5 on the interface) and names failing to deliver a working end-to-end system as the most
common reason mid-level candidates fail [HI-D].

| Band | Observable behaviour |
| --- | --- |
| **0** | No end-to-end path. Named technologies without connecting them. Could not say what happens to a single request from arrival to response. |
| **1** | A box diagram that does not satisfy the requirements already stated — serves a latency target the design cannot meet, or ignores a constraint from the prompt. Components named by brand rather than by role, with no reason for the choice; interviewing.io advises naming the generic component rather than the vendor, and warns the obvious follow-up is "why this one and not the other" [IIO-1]. Added a cache, a queue, or a load balancer by reflex with no stated pressure it relieves. |
| **2** | A design whose request path is traceable end to end and whose components each exist for a stated reason tied to a requirement. The hard part of *this* problem is in the design rather than abstracted away. Read/write paths separated where their shapes differ. Said where state lives and what is stateless. |
| **3** | All of band 2, **and the design visibly follows from the numbers or the requirement cut** rather than from a template — the component boundary is where it is *because* of a quantity they computed. Named the one component that is the bottleneck and said at what multiple of current load it becomes the bottleneck. Chose the simpler design and said what they gave up, instead of adding a component per concern. |

**Band-1 trap specific to this cohort:** reproducing a reference LLM-serving diagram
(gateway → router → vLLM → KV cache) accurately but without the prompt's binding constraint
appearing anywhere in it. Pattern recall is band 1.

---

## Axis 4 — `deep_dive_failure_modes`

Goes deep on the component that is actually hard, and names failure modes: partial failure,
backpressure, overload, retry amplification, idempotency, eviction, head-of-line blocking.

*Grounding:* Hello Interview's level guidance expects senior candidates to go deep in
around two places, expects depth in multiple areas at staff+, and expects senior candidates
to recognise limitations in their own design without being prompted [HI-L]; its delivery
guidance allocates roughly 10 minutes to deep dives and frames them partly as improving the
design under interviewer probing [HI-D]. interviewing.io's guide says the interviewer is
looking for well-reasoned, qualified decisions rather than certainty [IIO-1].

| Band | Observable behaviour |
| --- | --- |
| **0** | Stayed at the box-diagram layer for the whole answer. No failure case considered. Overload, eviction, and partial failure never came up even where the prompt made one of them the point. |
| **1** | Named a failure mode generically and moved on ("we'd add retries", "it'd be highly available", "we'd monitor it"). Proposed retries with no budget, no backoff, and no circuit breaker — a real and common way to convert a brownout into an outage. Went deep on the easy component (the stateless API layer) while leaving the hard one (the scheduler, the cache, the quota ledger) as a box. Treated autoscaling as the answer to an overload question without accounting for the time to add capacity. |
| **2** | Picked the genuinely hard component and went a level down: the actual eviction policy, the actual queue discipline, where backpressure is applied and what the caller sees when it is, what happens to in-flight work when a node dies. Named a concrete failure mode of *this* design, not of distributed systems in general, and stated the mitigation and its cost. |
| **3** | All of band 2, unprompted, **and a failure mode they found changed the design** — admission control added because the queue is unbounded, an idempotency key added because the retry path double-charges, a request class isolated because one shape starves another. Named their own design's weakest point before being asked, and said what signal would tell them it is failing in production. Distinguished the degraded mode from the failed mode and said which one they are designing for. |

---

## Axis 5 — `tradeoff_articulation`

**Names the axis, picks a side, defends it against the alternative.** The bar-setter.

*Grounding:* this axis is where the sources are most emphatic. interviewing.io's guide
reports that the interviewer cares less about which decision was made than about whether
the candidate can discuss the trade-offs, and names candidates not making decisions at all
as a common failure point; it gives the explicit form of a good answer as "given these
trade-offs, I will use X" [IIO-1]. Its framework page frames non-functional requirements as
a game of trade-offs in which you cannot optimise everything, and treats each requirement
as an opportunity to relax a different one [IIO-3].

| Band | Observable behaviour |
| --- | --- |
| **0** | No alternative considered. Presented one design as the design. No comparative language anywhere in the answer. |
| **1** | Listed pros and cons of two options and did not choose — the single most common failure on this axis, and the one the sources call out by name [IIO-1]. Or chose, but justified it with an unfalsifiable claim ("it's more scalable", "it's industry standard", "it's more flexible"). Or named a trade-off that isn't one in this scenario (consistency vs availability where there is one replica). Or chose and then quietly redesigned around the cost they had just acknowledged. |
| **2** | **Named the axis of the trade-off in units** — latency vs throughput, cost vs tail latency, recall vs p99, consistency vs availability, utilisation vs isolation — stated which side of it this system should sit on and why, given the stated requirement, and acknowledged specifically what the choice gives up. Picked. |
| **3** | All of band 2, **and the trade-off was resolved against a number they produced**, not against a preference — the batch window is 25ms because the TTFT budget is 400ms and prefill costs X; the index is IVF-PQ because exact search costs Y. Named the condition under which they would reverse the decision ("if long-context share goes above ~20%, this flips"). Volunteered the strongest argument *against* their own choice before the interviewer raised it. |

**Hard cap, enforced in code:** if no trade-off axis was named explicitly,
`tradeoff_articulation ≤ 1`. Listing advantages and disadvantages is not naming an axis.

---

## Axis 6 — `communication_collaboration`

Structures the answer, signposts, checks in, and handles pushback without either collapsing
or digging in.

*Grounding:* this is the axis most often left as adjectives, so it is grounded hardest.
interviewing.io's guide names pushing back against interviewer feedback as a red flag and
integrating that feedback into the design as a green flag; it says it is fine to change
your mind when challenged, while also noting there is an art to pushing back when the
situation warrants it. For senior-and-above roles it treats directing more of the interview
as a positive signal, and notes that a long silence is held against candidates above the
senior bar, while over-talking can count against a mid-level candidate [IIO-1]. Hello
Interview's delivery guidance warns against talking over the interviewer and says to leave
room for them to probe, and notes the round's own evaluation of communication and
collaboration is affected by how the candidate runs the time [HI-D]. Its level guidance
defines proactiveness as how far the candidate takes the lead in driving the session [HI-L].

| Band | Observable behaviour |
| --- | --- |
| **0** | Unstructured stream with no stated plan, or near-silence requiring the interviewer to extract every step. The listener cannot tell which phase of the answer they are in. |
| **1** | Talked continuously without signposting, or over the interviewer's attempt to redirect [HI-D]. Collapsed at the first push — abandoned a correct design because it was questioned, with no attempt to defend it. Or the opposite: repeated the original answer louder, treating the probe as a misunderstanding rather than information. Answered a different, easier question than the one asked and did not acknowledge the substitution. Used jargon with an audience for whom it is the wrong register (brand names, internal shorthand) and did not adjust when it clearly failed to land. |
| **2** | Stated the shape of the answer before giving it and kept to it. Signposted transitions. Answered the question that was actually asked, inside the time available. On pushback: engaged with the specific objection, either conceded the point and said what changes, or held the position with a reason — not with volume. Matched register to the audience named in the prompt. |
| **3** | All of band 2, **and the pushback changed something concrete and they said what** — "you're right that the ledger is the bottleneck, so I'm moving the quota check to the gateway and accepting ~1% overdraft." Ran the clock themselves, including saying what they are deliberately not covering and why, which is the proactiveness signal the senior/staff bar is defined by [HI-L]. Surfaced their own uncertainty with its boundary ("I'd want to measure X before committing to this") rather than bluffing fluency. Left the listener able to restate the design and the one decision it rests on. |

**Why this axis carries the product.** It is the axis nobody has ever scored for this
cohort, it is the one the playbook identifies as the real ceiling on advancement, and it is
therefore the most shareable finding on the scorecard. It is also the axis a voice-captured
diagnostic can measure that a multiple-choice instrument structurally cannot — which is a
reason to keep the diagnostic voice-first.

---

## Hard caps and anti-flattery rules

Enforced in code against the grader's output, not only requested in the prompt. A grader
asked nicely to be harsh drifts generous within a few prompt revisions.

| Rule | Why |
| --- | --- |
| No quantity **the candidate derived** ⇒ `capacity_cost_estimation ≤ 1` | The axis is unobservable otherwise. Not "no quantity in the transcript" — that is defeated by echoing the prompt's own numbers |
| Judge emits `addresses_prompt = false` (decision rests on a constraint not in the prompt) ⇒ code clamps that axis ≤ 1 | A correct answer to a different question is not partial credit |
| No trade-off axis named ⇒ `tradeoff_articulation ≤ 1` | Pros-and-cons lists are band 1 [IIO-1] |
| Any score of 3 requires a verbatim quote from the candidate | A 3 without evidence is the grader's opinion |
| Every report carries ≥2 below-bar observations with quotes | Reports with no criticism are detected in one session |
| A 3 on any axis requires the quote to contain the *consequence* | Band 3 is the decision changing, not the behaviour happening |
| Band 0 vs 1 must be distinguishable from the transcript | If the grader can't tell, the cell is badly written |
| `grader_version` stamped on every row | Retuning must not silently invalidate progress history |

The distribution check matters more than the agreement number: if the score histogram has
no real left tail, the grader is flattering regardless of how well it agrees with humans on
the cases it sees. See `calibration-plan.md`.

---

## Where this rubric departs from its sources

Stated explicitly so a practitioner reviewer can disagree with a decision rather than a
vibe.

1. **Estimation is scored, though both major sources call it optional.** interviewing.io
   tells candidates to ask whether the interviewer wants the math [IIO-3]; Hello Interview
   calls upfront estimation often unnecessary [HI-D]. This rubric keeps
   `capacity_cost_estimation` as a first-class axis because the AI-infra variant of the
   round is unusually numeric — reported prompts carry explicit capacity math, GPU
   throughput and memory-efficiency follow-ups [RN] — and because in this domain the
   binding constraint genuinely is a number (HBM capacity, memory bandwidth, dollars per
   million tokens). The reconciliation: the rubric never rewards unmotivated estimation.
   Band 3 requires the number to have changed a decision, which is exactly what Hello
   Interview's guidance asks for. **A candidate following Hello Interview's advice
   precisely should score 2–3 here, not 1.** If that is not true in practice, this rubric
   is wrong and the cell needs rewriting.
2. **Six axes, where the sources name three or four.** Hello Interview names Depth,
   Breadth, Proactiveness [HI-L]. These six axes are not an alternative taxonomy: breadth
   and depth are distributed across axes 3 and 4, and proactiveness is the "unprompted"
   clause inside every band 3. Six was chosen because a six-mark scorecard is readable as a
   share artifact and a three-mark one is not — a product constraint, honestly a product
   constraint, not a claim about how real loops score.
3. **No weighting by level in the axis definitions themselves.** Real loops weight
   differently by level [HI-L]; this rubric scores identically and shifts the *level claim*
   instead. One instrument, three verdicts.
4. **A widely-circulated four-category framing is deliberately not cited.** A search
   summary attributed a Problem Navigation / Solution Design / Technical Excellence /
   Communication framework to Hello Interview. Direct fetches of the two relevant pages did
   not contain it. It may exist elsewhere on their site, but it is unverified, so it is not
   used here. Flagged because it is the kind of thing that gets cited second-hand into a
   rubric and then into public copy.

---

## What needs a practitioner's review before this ships

Honest list. None of this is resolvable by more desk research.

1. **The band 2/3 boundary on all six axes.** This is the whole instrument. Two
   practitioners scoring the same transcript must land on the same side of it. Untested.
2. **Whether `capacity_cost_estimation` deserves axis status** given point 1 above, or
   whether a real frontier-lab interviewer would say it is subsumed by trade-offs. The
   single most likely place this rubric is wrong.
3. **Whether `communication_collaboration` is scorable from a 60-second voice answer** or
   only from a full 45-minute session. Bands 0–2 look scorable; band 3 may require a
   session, since it depends on pushback having happened. If so, the diagnostic should
   report it as provisional and the mock should own it.
4. **The level-mapping thresholds.** Invented to be defensible, not calibrated. They
   determine the status claim on the share artifact, which is the growth engine, so they
   are the highest-stakes unvalidated numbers in this pack.
5. **Whether band-1 cells read as insulting rather than diagnostic.** They are blunt on
   purpose, and the reveal is public-facing. One practitioner and one person who recently
   failed a loop should both read them.
6. **AI-infra specificity of the band-1 traps.** The pattern-recall traps (reference
   diagram, spec-sheet recitation) are inferred from how the category behaves, not observed
   in real transcripts. Verify against the first 20 real sessions.

---

## Appendix A — the judge's operating instructions

Constraints on the grader prompt that follow from this rubric. Prompt text is the build
agent's to write; these are the invariants it must satisfy.

- The judge sees: full transcript, canvas snapshots, the scenario's `good` / `bad` /
  `model_answer`, and this rubric. It never sees the user's prior scores — per-session
  grading only, or scores drift toward the user's history.
- The judge is a **separate out-of-band call** from the interviewer. An in-character model
  that knows it is grading leaks the rubric into its own follow-ups and coaches instead of
  testing.
- Per axis, the judge must emit: `score_0_3`, a verbatim `evidence_quote` with a timestamp,
  and for any 3, the clause showing the decision that changed.
- The judge scores what was said, not what was probably meant. Charitable reconstruction of
  a vague answer is the main route to flattery.
- **Absence is band 0 only on an axis the item actually asked about.** In the 45-minute
  mock all six axes are in scope, so `deep_dive_failure_modes = 0` on a scenario whose whole
  point is overload is a real, reportable finding. In the 60-second diagnostic each item
  scores exactly 2 axes and the other 4 were never asked: those are **not assessed**, and
  the judge must emit an `assessed: false` flag rather than a 0. Scoring them 0 would feed
  four spurious zeros per item into the axis aggregation, and the level mapping sends any
  axis at 0 straight below the senior bar — so a strong candidate would be graded below bar
  by arithmetic. Found while writing `prompts.md`; the mechanism is in Prompt 3.
- The report's contrast section — what an at-bar answer to that same follow-up sounds like
  — is generated against `model_answer`, never against the candidate's own answer. Grading
  someone against a polished version of what they said is how a grader learns to flatter.

## Appendix B — the arithmetic behind the model answers

The numbers in `questions.json` model answers are **derivations from stated assumptions**,
not cited facts, except where a source key appears. A practitioner reviewer should be able
to check each in under a minute. If any of these is wrong, the model answer teaching the
judge is wrong, which is worse than a missing number.

**Hardware anchors** (H100 SXM, vendor page [H100]): 80GB HBM3, 3.35 TB/s memory
bandwidth, 900GB/s NVLink GPU-to-GPU, up to 700W TDP. Tensor-core throughput on that page
is quoted **with sparsity** (BF16 1,979 TFLOPS; FP8 3,958 TFLOPS); dense BF16 is
conventionally about half the sparsity figure, ~990 TFLOPS, but the page states no dense
number, so model answers use bandwidth and capacity — which are unambiguous — wherever
possible. H100 NVL for contrast: 94GB, 3.9 TB/s.

**KV cache per token** = `2 (K,V) × layers × kv_heads × head_dim × bytes_per_element`.
For a 70B-class model with 80 layers, 8 KV heads under grouped-query attention, head_dim
128, in bf16: `2 × 80 × 8 × 128 × 2 B = 327,680 B ≈ 320 KB/token`. So 100k tokens of
context ≈ **32GB of KV for one request** — comparable to a fifth of a node's HBM, which is
why long-context admission control is a capacity problem and not a tuning problem. For an
8B-class model (32 layers, 8 KV heads, head_dim 128, bf16): 128 KB/token.

**Why decode is bandwidth-bound.** A decode step reads every weight once. 70B in bf16 =
140GB. Across TP=4 H100s, aggregate bandwidth ≈ 4 × 3.35 = 13.4 TB/s, so a step floors at
≈ 140/13,400 s ≈ **10ms**, i.e. ~100 tokens/sec for a single stream — and that same 10ms
serves the whole batch. Batch 64 therefore yields ~6,000 tok/s aggregate off the same
weight read. **That is the entire economic argument for continuous batching**, and it is
why the inter-token latency a user sees is nearly flat in batch size until compute
saturates. NVIDIA's benchmarking guidance describes the same shape from the measurement
side: system throughput rises with concurrency until the GPU saturates and can then
decrease [NIM].

**Why prefill is compute-bound.** Prefill ≈ `2 × params × prompt_tokens` FLOPs. A 10k-token
prompt on 70B = `2 × 70e9 × 1e4` = 1.4 PFLOP; at 4 GPUs × ~990 TFLOPS dense × ~40% achieved
utilisation ≈ 1.6 PFLOPS, that is **~0.9 seconds**, and a 100k-token prompt is ~9 seconds.
This is why a long-context request in the same queue as short ones destroys their
time-to-first-token, and why TTFT and inter-token latency need separate budgets. NVIDIA
defines TTFT as including queuing time, prefill, and network latency, and notes longer
prompts raise it [NIM].

**Token economics.** At an assumed $2/GPU-hour for H100 capacity (a market-rate assumption
that must be re-verified, not a cited figure), 4 GPUs = $8/hr = $0.0022/sec. At ~6,000
output tok/s that is ≈ **$0.37 per million output tokens** of raw compute, before
utilisation losses, redundancy, prefill, and margin. Useful independent reference point:
NVIDIA's H100 page cites roughly $0.09 per million tokens for a 120B open model at 66
tokens/sec/user under vLLM, attributed to a third-party benchmark dated April 2026 [H100].
Model answers that quote a cost figure state the $/GPU-hour assumption out loud, because
that is the behaviour the rubric is scoring.

**KV cache waste.** vLLM's launch post reports that pre-paging serving systems wasted
60–80% of KV memory to fragmentation and over-reservation, reduced to under 4% by
block-based allocation, with sharing cutting usage up to 55% and lifting throughput up to
2.2× in sampling workloads [VLLM]. **Dated June 2023** — directionally the key insight of
the field and safe to teach as such; the specific percentages should not be quoted as
current.

---

## Sources

Accessed 2026-11-22. All third-party prep material; none is an official company rubric. No
source here states what any named company asks, and neither does this rubric.

| Key | Source | Used for |
| --- | --- | --- |
| **[HI-D]** | Hello Interview — *System Design in a Hurry*, delivery framework. https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery | Scope cutting, quantified NFRs, phase time allocation, estimation-only-if-it-changes-the-design, talking over the interviewer |
| **[HI-L]** | Hello Interview — *The System Design Interview: What Is Expected at Each Level*, Evan King. https://www.hellointerview.com/blog/the-system-design-interview-what-is-expected-at-each-level | Depth / Breadth / Proactiveness; level expectations; "unprompted" as the senior discriminator |
| **[IIO-1]** | interviewing.io — *The Senior Engineer's Guide to the System Design Interview*. https://interviewing.io/guides/system-design-interview | Trade-offs over decisions; failure to decide; generic over brand names; pushback red/green flags; silence by level |
| **[IIO-3]** | interviewing.io — same guide, part three. https://interviewing.io/guides/system-design-interview/part-three | Underspecified prompts; estimation as optional; margin of safety; NFRs as a trade-off game; unmotivated nines as impostor signal |
| **[NIM]** | NVIDIA — LLM benchmarking metrics. https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html | TTFT (includes queuing + prefill + network), ITL/TPOT, throughput saturating then decreasing with concurrency |
| **[H100]** | NVIDIA — H100 product page. https://www.nvidia.com/en-us/data-center/h100/ | HBM capacity, memory bandwidth, NVLink, TDP; sparsity caveat on TFLOPS; third-party $/1M-token reference |
| **[VLLM]** | vLLM — *vLLM: Easy, Fast, and Cheap LLM Serving with PagedAttention*, 20 Jun 2023. https://vllm.ai/blog/2023-06-20-vllm | KV fragmentation 60–80% → under 4%; sharing and throughput gains. **Dated; teach the insight, not the percentages** |
| **[RN]** | `RESEARCH-NOTES.md` (this folder, gathered 2026-11-16) | Reported frontier-lab themes; the AI-framing-over-classic-core observation; competitive landscape |

**Verification notes.** The two Exponent rubric URLs cited in `RESEARCH-NOTES.md` now
301-redirect to `aced.io` and return an empty body to a non-browser fetch, so nothing from
Exponent is cited here and the research notes' Exponent links should be treated as stale.
Hello Interview's level page carries a level-breakdown image that could not be read, so
anything it contains is not reflected above. interviewing.io part three was only partially
retrievable verbatim; every [IIO-3] claim used here came from the verbatim portion.
