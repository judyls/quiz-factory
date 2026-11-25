# REVIEWER 3 — inline safety and evaluation infrastructure

Persona: `review-harness/personas/03-anthropic-safety-eval.md`. Protocol:
`review-harness/review-protocol.md`. Part A completed before opening `questions.json`,
`prompts.md`, or `calibration-plan.md`.

**Exclusions honoured.** I did not open `calibration-plants.json`, `dry-run-report.md`, or
anything in `review-harness/findings/`. I saw no expected-score content. `rubric.md` refers
to the plants and to `dry-run-report.md` in prose (lines 50, 65–71, 240); I read those
references, which describe *that* plants exist and what they caught, not any expected score.
I do not know any item's expected band.

---

# PART A — BLIND SCORING

Scored against `rubric.md` as written. Five answers, eleven (answer, axis) cells.

---

## Answer 1 — `A01` (batch window vs TTFT budget)

```
Answer 1 / capacity_cost_estimation: 1
  cell clause applied: "Gave a number with no derivation" — and the hard cap:
    "if the candidate produced no quantity of their own, capacity_cost_estimation ≤ 1"
  evidence: "Given our 400 millisecond target I would bias toward latency."
  admits another reading: YES — band 0, and this is the closest call in the set.
    Band 0's clause "Chose between two options whose only real difference is a number,
    without computing either" is an exact fit: the batch window IS the choice, and he
    defers it entirely ("I would tune the window empirically ... and iterate"). I scored 1
    because the scoring contract defines band 0 as a conjunction — "the behaviour never
    appeared, AND nothing in the answer depended on it" — and something did depend on a
    quantity: he bound the latency/throughput decision to the stated 400ms target. Also,
    the cap is written "≤ 1", which implies the drafters expected echo-only answers to
    land at 1. See the hardest-cell note at the end of Part A.
```

```
Answer 1 / tradeoff_articulation: 2
  cell clause applied: "Named the axis of the trade-off in units — latency vs throughput
    ... stated which side of it this system should sit on and why, given the stated
    requirement, and acknowledged specifically what the choice gives up. Picked."
  evidence: "The trade-off is latency against throughput: a wider batch window buys you
    utilisation and spends time-to-first-token. Given our 400 millisecond target I would
    bias toward latency."
  admits another reading: YES, weakly — band 1 via "Listed pros and cons of two options
    and did not choose". The *direction* is chosen but the actual decision (the window
    value) is handed to empiricism: "tune the window empirically ... until both numbers
    look healthy". A harsh reader can call that a non-decision dressed as a decision. I
    scored 2 because the cell requires a side and a reason, not a parameter value. Band 3
    is clearly out: nothing is resolved "against a number they produced", there is no
    reversal condition, and no counter-argument is volunteered.
```

Note for Part B: this answer is the cleanest demonstration that `capacity_cost_estimation`
and `tradeoff_articulation` diverge here only because of the hard caps, not because of the
band language.

---

## Answer 2 — `A03` (vector index at 10B), HNSW

```
Answer 2 / capacity_cost_estimation: 1
  cell clause applied: "Derived the number that decides the question, then proposed a
    design it rules out (computed 40TB raw, then chose an index that needs all of it
    resident) — the number was produced but not understood."
  evidence: "10 billion vectors at 1,024 dimensions in float32 is 4 kilobytes per vector,
    so about 40 terabytes raw. ... Given the recall requirement I would use HNSW"
  admits another reading: NO — but with a caveat I owe you. The band-1 clause above is
    written so tightly around this exact answer shape (same index family, same 40TB
    figure) that applying it feels less like judgement than like pattern-matching a
    key. The derivation itself (4KB/vector, 40TB, 2% churn) satisfies band 2's first
    sentence completely, and band 2 fails only on its second requirement — "Named which
    constraint binds ... and showed why the others have slack", which this answer never
    does. So the 1 is correct on the cell as written, and a grader who weighted the
    derivation over the consequence would land on 2. Band 3 is unreachable.
```

```
Answer 2 / tradeoff_articulation: 1
  cell clause applied: "Or chose, but justified it with an unfalsifiable claim ('it's
    more scalable', 'it's industry standard', 'it's more flexible')."
  evidence: "I would use HNSW, because it has the best recall-latency curve of the ANN
    families — typically 0.95-plus recall at single-digit millisecond latency."
  admits another reading: YES — band 2, if a grader counts "recall-latency curve" as
    "named the axis of the trade-off in units". I scored 1 because the cell's band 2
    additionally requires that the candidate "acknowledged specifically what the choice
    gives up", and this answer acknowledges no cost at all — on an item whose prompt
    literally asks "tell me what the choice costs you". Naming a curve you claim to be
    on the good end of is the opposite of naming a trade-off: it asserts there isn't one.
    Band 0 is out: there is comparative language ("best ... of the ANN families").
```

---

## Answer 3 — `A03` (vector index at 10B), IVF-PQ

```
Answer 3 / capacity_cost_estimation: 2
  cell clause applied: "Named which constraint binds — memory capacity vs memory
    bandwidth vs compute vs network vs dollars — and showed why the others have slack."
  evidence: "about 40 terabytes raw, which makes memory the binding constraint here.
    Latency has slack — 50 milliseconds is generous for an approximate lookup — and 200
    million changes a day is about 2 percent, which is an ingest-volume question rather
    than a throughput one."
  admits another reading: YES — band 3, and this is the most consequential ambiguity in
    Part A. A charitable grader reads "40TB ⇒ memory binds ⇒ I pick the index that
    compresses memory" as the number ruling out an architecture, which is band 3's
    required clause. I scored 2 for two reasons, both from the transcript's own ordering
    and wording: (i) the decision is stated BEFORE the arithmetic and is justified by
    popularity — "I'd go with IVF-PQ — it's what most billion-scale deployments run" —
    so the stated cause of the choice is consensus, not the number; (ii) he never closes
    the loop, i.e. never says what PQ's compression ratio buys against the 40TB, which is
    the one step that would make the number load-bearing. Per the band-3 rule
    ("performing the behaviour is band 2; letting the result alter the design is band 3")
    I cannot show the result altering anything. Flagged hard: this cell cannot
    distinguish causation from post-hoc narration. See B4.
```

```
Answer 3 / tradeoff_articulation: 1
  cell clause applied: "Or chose, but justified it with an unfalsifiable claim ... 'it's
    industry standard'" — plus the hard cap: "if no trade-off axis was named explicitly,
    tradeoff_articulation ≤ 1".
  evidence: "I'd go with IVF-PQ — it's what most billion-scale deployments run."
  admits another reading: YES — band 0, via "No alternative considered. Presented one
    design as the design." No competing index is ever named, and the cost of PQ — recall
    loss from quantisation, which is THE cost and is what the prompt asks for — appears
    nowhere; "keep an eye on recall" is the whole of it. I scored 1 rather than 0 because
    band 0 also requires "No comparative language anywhere in the answer", and there is
    some ("rather than a throughput one"), and because band 1's "industry standard" clause
    is an exact lexical match to what he said.
```

---

## Answer 4 — `A08` (long-context contention), answering A01

```
Answer 4 / requirements_scoping: 1
  cell clause applied: the relevance gate first — "A behaviour performed on the wrong
    problem scores at most band 1 on every axis, however well executed" — then band 1's
    "appeared, but wrong".
  evidence: "I would track p99 time-to-first-token and inter-token latency as separate
    series." (The requirements-shaped behaviour in the answer. It is competent, and it is
    about the wrong scenario.)
  admits another reading: YES — band 0, via "Began designing from the prompt as given.
    ... never bounded the problem." The prompt asks two direct questions — "what exactly
    are you protecting, and what is the first number you would want?" — and the answer
    addresses neither: it never says the thing being protected is short-request TTFT, and
    the number it offers (a decode-step floor) is not a number for this problem. I scored
    1 because separating TTFT from ITL budgets IS naming quantified non-functional
    requirements, which band 0 requires to be absent. NOTE: the relevance clamp is ≤ 1,
    so the clamp cannot arbitrate 0 vs 1 — and the rubric gives no guidance for a clamped
    axis. Reported in B5.
```

```
Answer 4 / capacity_cost_estimation: 1
  cell clause applied: "Used a number that contradicts a constraint stated in the prompt."
    (Also clamped by the relevance gate.)
  evidence: "across four H100s at 3.35 terabytes per second that is roughly 13 terabytes
    per second aggregate"
  admits another reading: NO. The prompt states "eight nodes of eight H100s"; the answer
    sizes on four. The arithmetic itself is right (140GB / 13.4 TB/s ≈ 10.4ms — I checked),
    which makes this the cleanest case in the set of the rubric working as intended:
    well-executed arithmetic on a hardware assumption the prompt contradicts is band 1,
    not band 2. Without the relevance gate this answer would otherwise satisfy band 2
    and arguably band 3 ("so I would ... size the admission window at 20 to 25
    milliseconds against the budget"), on a budget this prompt never states.
```

---

## Answer 5 — `A09` (heterogeneous fleet routing)

```
Answer 5 / capacity_cost_estimation: 2
  cell clause applied: "Derived the binding quantity from assumptions stated out loud ...
    Arithmetic within ~2–3×."
  evidence: "blended cost is 0.7 times a tenth plus 0.3 times one, which is 0.37 — so
    about 37 percent of what all-70B serving costs."
  admits another reading: YES — and in BOTH directions, which is why I am flagging it as
    the single most dangerous cell in the set.
    Toward 1: the number he nominates as the decision-driving one is derivationless and
    contradicts his own figures. "The ceiling only starts to bind if the 8B share drops
    below roughly 20 percent" — in his own units, cost = 1 − 0.9s of all-70B baseline, so
    at s = 0 cost equals baseline, which he put at ~$1.49 ("near 55 cents" at ratio 0.37
    implies baseline $1.486). Under his own assumptions the ceiling NEVER binds at any
    8B share, and at s = 0.20 the cost is 0.82 × 1.486 = $1.22, comfortably inside.
    The 20% figure is simply unsupported. Band 1's "Gave a number with no derivation"
    applies to it directly.
    Toward 3: that same unsupported sentence is a textbook band-3 quote — a number, a
    consequence, a monitoring decision, "so that is the number I would watch". It would
    satisfy `band3_consequence` and every row of the prompts.md validation table.
    I scored 2 because the derivation chain he DOES show is sound (0.7×0.1 + 0.3×1 = 0.37
    ✓; 0.5×0.1 + 0.5×1 = 0.55 ✓), and band 1's triggers are "no derivation" or ">100×
    off", neither of which describes the answer as a whole. He also drops the 400B from
    a blended cost on a three-model prompt, which blocks 3.
```

```
Answer 5 / high_level_design: 0
  cell clause applied: "No end-to-end path. ... Could not say what happens to a single
    request from arrival to response."
  evidence: the entire transcript. There is no component, no router, no classifier, no
    confidence threshold, no escalation or fallback path, and no answer at all to the
    prompt's second question ("what do you measure to know you have not quietly made the
    product worse") beyond a cost figure. The nearest thing to a design is "If 70 percent
    goes to the 8B", which is an assumption, not a mechanism.
  admits another reading: YES, weakly — band 1, if a grader treats the implied 70/30 split
    as a skeletal cascade and applies "A box diagram that does not satisfy the
    requirements already stated". I scored 0 because there is no box and no diagram: the
    answer is a cost model with a routing outcome assumed. This is the one score in Part A
    I would defend hardest.
```

---

## Hardest rubric cell to apply

**`capacity_cost_estimation`, band 0 vs band 1, on Answer 1.**

Not the 2/3 boundary (though Answer 3 was close behind) — the 0/1 floor, because here the
rubric contradicts itself and the contradiction is load-bearing:

- The hard cap says no quantity of the candidate's own ⇒ `≤ 1`. A cap of "≤ 1" presupposes
  that 1 is the right score for an answer with no derived quantity.
- Band 0 says "No quantity of any kind, in a scenario whose constraints were stated
  numerically" — and adds a second clause, "Chose between two options whose only real
  difference is a number, without computing either", which fits Answer 1 exactly.
- The scoring contract makes band 0 a conjunction ("never appeared, AND nothing in the
  answer depended on it"), which pushes toward 1.
- And `rubric.md` line 237 promises, as an enforced anti-flattery rule, "Band 0 vs 1 must
  be distinguishable from the transcript | If the grader can't tell, the cell is badly
  written." By the rubric's own test, this cell is badly written.

This matters more than a one-band disagreement looks, because the level mapping sends **any
axis at 0** straight below the senior bar. The difference between my 1 and a co-reviewer's
0 on this cell is the difference between two level claims on the share artifact.

Concrete fix: make the floor mechanical and stop using band 0 for it. Band 0 =
`derived_quantity == null` **and** no prompt quantity used in any decision. Band 1 =
`derived_quantity == null` but a prompt quantity was bound to a decision. That is
computable from fields the grader schema already emits.

---
---

# PART B — CRITIQUE

---

## B1. Axis legitimacy

**Five of the six are legitimate. `capacity_cost_estimation` is not a separate axis from
`tradeoff_articulation` — it is the same axis measured twice, and that inflates the
scorecard's apparent dimensionality.**

The rubric itself flags this as its "single most likely place this rubric is wrong"
(`rubric.md` line 334), so I am agreeing with its own doubt, but I can say something more
specific than it does. Compare the two band-3 cells:

- `capacity_cost_estimation` 3: "**the result changed the design**: the number ruled out an
  architecture, resized a fleet, moved a component" (line 161)
- `tradeoff_articulation` 3: "**the trade-off was resolved against a number they produced**
  ... the batch window is 25ms because the TTFT budget is 400ms" (line 220)

These are one behaviour. The band-2 cells are nearly as close: "Named which constraint
binds" versus "Named the axis of the trade-off in units" are the same sentence about the
same utterance in most answers. In Part A the two axes diverged on only two of five
answers (A1: 1/2; A3: 2/1), and **both divergences were produced by the hard caps, not by
the band language** — the derived-quantity cap on A1, the named-axis cap on A3. Strip the
caps and you have one axis with two names.

Testable prediction, stated so it can be falsified: on the golden set, the Pearson
correlation between these two axes will exceed 0.8, and higher than any other axis pair.
`calibration-plan.md` line 154 measures Cronbach's α **within** each axis (4 items per
axis) but nothing measures correlation **between** axes, so this would never be detected.
Add a 6×6 inter-axis correlation matrix to the Phase 2 table; any off-diagonal above ~0.8
means two axes should be merged or one rewritten.

Why I would still keep six: the honest reason is already in the file — "a six-mark
scorecard is readable as a share artifact and a three-mark one is not ... honestly a
product constraint" (line 318). I respect that it is labelled as a product constraint
rather than a measurement claim. But then do not also claim the six are independent
diagnostic axes, and do not let the "named blind spot" (the lowest axis, per
`calibration-plan.md` line 173) be chosen between two axes that are the same thing — a
candidate told their blind spot is "capacity estimation" when it is really trade-off
resolution gets sent to practise the wrong skill.

**What this rests on:** the cell text, and the eleven cells I applied in Part A. That part
is solid. **What it does not rest on:** any loop I have owned. I have interviewed on both
sides of the table and I have never owned a rubric or normed one against a cohort, so my
claim that six axes over-count is an argument about the instrument, not a report about what
hiring committees do. **What would change my mind:** an inter-axis correlation below ~0.6
on 50+ real sessions, or a practitioner who has read scorecards at volume telling me that
loops do in fact score "could they do the math" and "could they use the math" as separate
lines — which is plausible and I would believe it.

---

## B2. Scenario realism — my three items

### `inline-safety-classifier-budget` (`questions.json` line 301) — **realistic in its first half, straw man in the half the item rests on**

This is the question I was asked to own, so here is the direct answer.

**"Just run it asynchronously" is absolutely something a competent tech lead says.** I have
been on the other end of that sentence more than once. It is the standard move when a check
does not fit a budget, it is usually said by someone who is right that the budget is the
real problem, and the item is right to put it in a tech lead's mouth.

**"...and retract anything bad after the fact" is not.** On a token-streaming product,
retraction is not a weak mitigation, it is a category error: the tokens are on the user's
screen. Anyone who has looked at the delivery path knows this. A lead who proposes it is
not making a defensible trade-off, they are confused about the product.

Why that is a measurement problem rather than a nitpick: the item's `good` field and
`model_answer` both make "retraction is not a mitigation, it is a different policy" **the
discriminating insight**. But that insight is available to anyone who knows the product
streams. It is a fact about the UI, not a judgement about the safety/latency tension. So
the pack's only explicitly pushback-shaped item hands its candidate a free win, and a
candidate who cannot produce it has failed a product-comprehension check, not a design one.
The item as written measures less than it costs.

**The fix, concretely.** Give the lead the strong version: *"Just run it async and kill the
stream at the first unsafe token."* That is realistic, it is defensible, and it forces the
candidate onto the actual ground — the exposure window is bounded but nonzero. Using the
pack's own anchors (~100 tok/s per stream, `rubric.md` line 411; classifier p99 180ms), the
window is roughly 18 generated tokens, a handful of which the user has actually seen. Now
the candidate has to argue about whether a bounded exposure window is acceptable, who owns
that decision, what the fail-open/fail-closed policy is when the classifier is down, and
what happens at token 500 when the output turns unsafe (the item already has that
follow-up, and it is currently better than the item). Keep "retract after the fact" as a
`bad`-field branch a weak candidate proposes — it belongs there, not in the lead's mouth.

**Second thing wrong, same item: the prompt tells the candidate their conclusion.** "You
disagree. Say what you would say to them." The `bad` field names "agreeing too fast and
taking the async path" as one of its two real failure modes, and the `followups` list has a
branch for `"if": "accepts async immediately"` — a branch the prompt's own wording makes
nearly unreachable. That is an internal contradiction between three fields of the same
item, and it is checkable. Drop "You disagree."

### `eval-infra-per-commit-cost` (line 395) — **realistic**

The ask is exactly right in shape: a research engineer who wants a gate, states a volume, a
latency, and a trigger, and whose requirement is expensive in a clause they have not
noticed. "50,000 graded evaluations on every commit, results in under 10 minutes, gating
merges" is the most realistic thing in the pack from my side of the house. Numbers are
plausible: 40 commits/day is a real team; 2,000-token generations are a real eval shape.

**Is the reference answer's pushback the pushback I would make? Partly — and it pushes on
the wrong clause.** The model answer says explicitly: "What I would push back on is not the
50,000, it is the 'every commit, in 10 minutes, gating merges' clause". I would push on the
50,000, first, and here is why that is not a preference:

1. **The sample size is unmotivated and nobody costed the question it answers.** The gate
   makes one binary decision: did this commit regress. The required n follows from the
   effect size you need to detect and the judge's own noise floor, not from a round number.
   50,000 samples give a standard error of ~0.2% on a binary metric — far finer than an
   LLM judge's self-disagreement rate. You are paying for three digits of precision on a
   measurement whose instrument has one. That is the requirement conversation, and it is
   the one the model answer declines to have.
2. **The flake-rate question is in the model answer and is the best thing in it** — "At
   50,000 runs a slightly nondeterministic gate will block you constantly and you will
   start overriding it." Correct, and it is the thing I care most about. But it is
   downstream of (1): flake rate × n is what determines whether the gate is informative, so
   the two must be argued together.
3. **Caching is under-weighted to the point of being the missed answer.** "cache by content
   hash" is the third item in a list. It should be the design. Most commits touch neither
   the model weights nor the eval harness, so a correctly-keyed cache makes the marginal
   cost of a gated commit *near zero* and dissolves the conflict entirely. That is the
   third option this item is shaped to reward and the model answer walks past it.
4. **`good` and `model_answer` disagree.** The `good` field requires "asks what decision
   the gate is meant to make, because a flake-prone gate blocking 40 merges a day is worse
   than no gate." That sentence has **no counterpart in `model_answer`**. Since
   `prompts.md` generates the candidate-facing `contrast` from `model_answer` and not from
   `good` (line ~250), the best beat in the item never reaches the candidate.

Arithmetic faults are in B3; they are substantial.

### `annotation-throughput-vs-agreement` (line 442) — **realistic**

200,000 comparisons/month with 120 annotators is ~83/annotator/working-day, about 6 minutes
per comparison — plausible for preference comparisons over model outputs. κ = 0.62 is a
realistic, uncomfortable, non-cartoonish number (substantial on the conventional scale, bad
enough to matter). The VP framing and the "they are not an ML person" register constraint
are the most convincing audience-modelling in the pack, and the `bad` field ("Explains
Cohen's kappa to the VP") is the single most accurate failure-mode description in
`questions.json`.

**The one thing most wrong is in the `model_answer`, not the scenario: it teaches a
statistical fallacy.** See B3. The scenario is fine; the gold answer is not.

---

## B3. Arithmetic

Checked: my three items, `heterogeneous-fleet-routing` (because Answer 5 scores against it),
and `rubric.md` Appendix B. Appendix B's own chain is **correct** — I verified 320KB/token
KV (2 × 80 × 8 × 128 × 2 = 327,680 B ✓), 32GB for 100k context ✓, the 10ms decode floor
(140GB / 13.4 TB/s = 10.4ms ✓), ~6,000 tok/s at batch 64 ✓, 1.4 PFLOP for a 10k prefill ✓
and ~0.9s at 1.6 PFLOPS ✓, and $0.37/M output tokens at $2/GPU-hr ✓. The sparsity caveat on
BF16 TFLOPS is handled honestly. Appendix B is the strongest file in the pack.

The errors are in the model answers, which is worse, because the model answers are what the
judge is anchored on.

### B3.1 — `inline-safety`: p99s are added, not composed (**error**)

`model_answer`: "We are at 310 at p99 with 90 milliseconds of headroom and the classifier
wants 180, so it does not fit on the critical path as things stand". 400 − 310 = 90 ✓, and
the item's `followups` reinforce it: "Does 180 milliseconds fit in the budget or not? Show
me."

p99(T + C) ≠ p99(T) + p99(C). For independent T and C, the sum's 99th percentile is far
below 490ms, because it would require both variables to be in their top percentile
simultaneously (p ≈ 10⁻⁴). A usable approximation for independent, right-skewed latencies
is p99(T) + p50(C) ≈ 310 + 40 = **350ms, which fits**. The honest statement of this item's
arithmetic is "it fits at p50 and breaches in the tail; what fraction of requests breach
depends on the correlation between classifier cost and prompt length."

And the correlation is the interesting part: a safety classifier's cost scales with prompt
length, and so does prefill, which dominates TTFT. So they **are** positively correlated,
near-additive is the right conservative assumption, and the model answer's *conclusion* is
probably right — for a reason it never states and does not teach.

Why this is a defect rather than pedantry: a candidate who says "you can't add p99s, I'd
want the distribution of the composed path" is doing the strictly better engineering and
will be graded **down** against this reference, because the reference's load-bearing step is
the sum. The grader is instructed to "Score what was said, not what was probably meant" and
to compare against `model_answer`; a correct objection to the reference looks like a failure
to produce the reference's number.

Fix: change `model_answer` to "310 plus a 40ms median puts us at 350 with 50ms of margin,
and the tail is where this breaks — and because the classifier's cost tracks prompt length
the same way prefill does, I'd assume near-additive until I've measured the composed p99."
Add the composition point to `good`. Add a follow-up: "Is 310 plus 180 the right sum?"

### B3.2 — `inline-safety`: "overlap with prefill" contradicts Appendix B (**error**)

`model_answer`: "classify the prompt during prefill, which for a 2,000-token prompt is
already hundreds of milliseconds of work we are paying for, so most of the 40 milliseconds
overlaps and costs us almost nothing in wall clock."

Two problems.

(i) **The magnitude.** Using Appendix B's own method: 2 × 70e9 × 2,000 = 2.8e14 FLOP; at
4 GPUs × ~990 TFLOPS dense × 40% achieved = 1.58 PFLOPS → **177ms**, consistent with
Appendix B's 0.9s for 10k tokens. "Hundreds of milliseconds" is one hundred and seventy
seven. Minor on its own.

(ii) **The mechanism is wrong, and this one is not minor.** Appendix B states plainly that
"prefill is compute-bound". You cannot overlap new compute with a compute-saturated phase
for free. Whether the overlap is free depends entirely on **where the classifier runs**,
which the model answer never says:

- *Separate accelerator pool*: overlap is genuinely ~free in wall clock — but you have
  added hardware nobody costed and a new cross-service dependency, which is exactly where
  the fail-open/fail-closed question becomes load-bearing.
- *Same serving GPUs*: the cost is additive, not overlapped. And the 40ms p50 figure
  *implies* a classifier large enough for this to matter — 40ms against a 177ms/2k-token
  prefill on the same hardware back-solves to ~6.4e13 FLOP, roughly a 16B-parameter model
  at that context. Running it inside prefill adds ~23% to prefill, i.e. ~+40ms. No free
  lunch at all; you have simply renamed the serialized cost.

So the pack's own "third option" — the thing the model answer offers as the mark of an
at-bar engineer — is unsound as stated and contradicts Appendix B two files over. This is
the sibling of the fallacy my persona exists to catch: "async as a mitigation" has a cousin,
**"overlap as a mitigation"**, and the gold answer commits it.

Fix: require the model answer to name where the classifier runs and to state the
consequence of each branch. That is a better item than the one that exists, and it is one
sentence longer.

### B3.3 — `eval-infra`: the stated chain is right; two large omissions make it ~5× light

The chain as written checks out exactly:
- 50,000 × 2,000 = 100M tokens; /600s = 166,667 tok/s → "about 170,000" ✓
- 166,667 / 6,000 = 27.8 → 28 replicas → 112 GPUs ✓
- 112 × $2 × (600/3600) = $37.33 → "roughly 37 dollars a commit" ✓
- × 40 = $1,493/day → "1,500 dollars a day" ✓; × 365 = $545k → "about half a million" ✓

**Omission 1: the judge calls are named and never costed.** The prompt says "one 2,000-token
generation **plus a judge call**"; the model answer says "plus the judge calls" and stops. A
judge pass over a 2,000-token generation is dominated by prefill, which is compute-bound:
2 × 70e9 × 2,000 = 2.8e14 FLOP per eval × 50,000 = 1.4e19 FLOP in 600s = **23.3 PFLOPS**.
At 990 TFLOPS × 40% = 0.396 PFLOPS/GPU that is **~59 GPUs**, plus ~11 more if the judge
emits ~200 tokens of verdict. So ~112 GPUs is really **~180**, $37/commit is ~$60, and
$545k/yr is ~$900k/yr. For a model answer whose entire teaching point is "cost it before you
argue with it", dropping ~40% of the fleet is the wrong lesson. It also fails the axis's own
band-3 indicator — "Stated assumptions as assumptions and flagged which one the answer is
most sensitive to": the judge's model size is unstated and is the single most sensitive
assumption in the estimate.

**Omission 2, and the bigger one: GPU-minutes consumed is not GPUs provisioned.** $37/commit
prices 112 GPUs for exactly 600 seconds, as if capacity were elastic per-second. For a
*merge gate* it is not, because the gate cannot queue — queuing is the thing it exists to
avoid. Two ways to see the gap:

- *Provisioned floor, one lane*: 112 GPUs reserved × 24h × $2 = **$5,376/day ≈ $1.96M/yr**,
  versus the stated $545k. A **3.6× understatement** before concurrency.
- *Concurrency, from queueing*: 40 commits over an 8-hour workday is one every 12 minutes
  against a 10-minute deterministic service time, so ρ ≈ 0.83 on a single lane. M/D/1 mean
  wait = ρS/(2(1−ρ)) = (0.83 × 10)/(2 × 0.17) ≈ **25 minutes**. The 10-minute gate becomes
  a ~35-minute gate on one lane. Holding the 10-minute promise needs ~3 lanes, i.e.
  ~340 GPUs provisioned (with the judge, ~540), which is **$6M+/yr**.

Stack the two and the real figure is roughly **5–10× the model answer's**. This is my
domain's characteristic failure — eval infrastructure costed by compute alone — and the
pack's gold answer commits it in a scenario explicitly about costing eval infrastructure.

The fix also makes the item much better: the honest answer is that the 10-minute *gating*
requirement is what forces provisioned-for-peak capacity, so the cost is driven by the
concurrency the SLO implies, not by the token count. That is a far sharper version of the
pushback the item already wants to teach.

### B3.4 — `annotation`: the model answer's core argument is statistically false (**error**)

`model_answer`: "Doubling the team doubles both the signal and the noise, so the model sees
maybe 200,000 comparisons' worth of usable preference even though we paid for 400,000".

**Doubling n at a fixed noise rate doubles effective sample size.** Label noise reduces the
constant factor; it does not cancel the benefit of more data. The sentence as written is a
fallacy, and it is the sentence the argument rests on.

My calculation. Binary comparisons with balanced marginals ⇒ p_e = 0.5, so κ = 0.62 ⇒
p_o = 0.81. Under a mixture model (fraction λ decidable and always agreed, 1 − λ coin flips
agreeing half the time): p_o = 0.5(1 + λ) ⇒ **λ = 0.62**, so ~38% of comparisons are
effectively coin flips and the per-label error rate is e ≈ 0.19. Effective sample size under
symmetric label noise scales as n(1 − 2e)² = n(0.62)² ≈ **0.38n**.

- Today: 200,000 nominal → **~77,000 effective**.
- Doubled: 400,000 nominal → **~154,000 effective** — which is 2× today, not "the same as
  200,000." The model answer's figure is both wrongly derived and, read literally,
  optimistic about the doubled case.
- Lift κ to 0.80: p_o = 0.90 ⇒ λ = 0.80 ⇒ e = 0.10 ⇒ (1 − 0.2)² = 0.64, so **~1.67×**
  effective data — on every comparison already collected and all future ones, for ~6 weeks
  of guideline work, against 2× for permanently doubled headcount.
- And they compose: fix agreement *then* double = 2 × 0.64 = 1.28n effective, versus
  2 × 0.38 = 0.77n for doubling first. **That** is the leverage argument.

Note that the item's `good` field asks for exactly this — "Makes the leverage argument
quantitatively: raising agreement is worth more than raising volume, because effective
sample size depends on both" — and is **correct**. The `model_answer` teaches a different,
wrong argument. Same `good`/`model_answer` split as `eval-infra`, and it matters more here
because the judge and the candidate-facing contrast are both anchored on `model_answer`
(see B5.2). The onboarding-dilution point in the model answer's fourth sentence is the only
part of its reasoning that is actually valid, and it is the part presented as a secondary
aside.

### B3.5 — `heterogeneous-fleet-routing`: a blended cost that omits the most expensive model

Both the `model_answer` and `good` compute "0.7 times a tenth plus 0.3 times one" and
assign the entire non-8B remainder to the 70B. The prompt states **three** models and asks
for a **blended** ceiling. If even 5% of traffic lands on the 400B at the model answer's own
stated ratio ("several times worse again"; 400/70 = 5.7×):

0.70 × 0.1 + 0.25 × 1.0 + 0.05 × 5.7 = 0.07 + 0.25 + **0.285** = 0.605

That is 60% of baseline against the stated 37%, and the 400B contributes **47% of the bill
off 5% of traffic**. That is the insight the item exists to teach — in a three-tier fleet
the top tier's share is the cost control variable, not the bottom tier's — and neither
`good` nor `model_answer` contains it. Answer 5's identical omission in Part A is inherited
from the reference, not invented by the candidate.

Also unengaged: "a mixed fleet of A100s and H100s" is a stated constraint, and per-token
cost differs ~1.7× by memory bandwidth (2.0 vs 3.35 TB/s) at a different $/hr. Neither
reference field mentions it. Under the relevance gate the judge must quote
`prompt_constraint_engaged` verbatim from the prompt — so a candidate who does the harder,
more correct analysis on the mixed fleet has no anchor in the reference at all.

### B3.6 — Every model answer over-runs the pack's own time budget (**checkable, systemic**)

`questions.json._meta.answer_budget_seconds: 60`. `calibration-plan.md` line 158 sets a
health threshold: "Answer length | words spoken | median under 170 | Items whose answers
systematically run long are over-scoped for 60 seconds."

Measured word counts of all 12 `model_answer` fields: median **172**, mean **168**, range
148–178. At a normal spoken 150 wpm (2.5 words/s) that is 59–71 seconds; **11 of 12 exceed
60 seconds**. The pack's gold answers fail the pack's own item-difficulty check, and the
check's prescribed action is to re-scope the item.

Worst case: `annotation-throughput-vs-agreement`'s prompt says "You have about 30 seconds"
and its model answer is 166 words ≈ **66 seconds — 2.2× its own stated budget.**

`rubric.md` lines 43–57 already noticed this squeeze from the other end and responded by
relaxing band 3 to one required clause. That was a fix to the rubric for a problem in the
items. Fix the items too, or state 90 seconds as the real budget.

---

## B4. The band 2/3 boundary

**The boundary is in the right conceptual place and the wrong operational one. As
implemented it measures narration of causality, not causality — and it is defeatable with
one sentence of coaching, which for a paid prep product is self-defeating.**

What applying it in Part A taught me, concretely. Answer 3 computes 40TB, names memory as
the binding constraint, and picks the memory-compressing index. Answer 3 is, on the
substance, a candidate whose number and whose design agree. I scored 2 — on the grounds
that he stated the decision *before* the arithmetic and justified it by consensus. But that
is an argument about **utterance order and phrasing**, not about whether the number drove
the choice. A transcript cannot show causation. It shows sequence and assertion.

Which means the operative test is: did the candidate say a sentence of the form "X,
therefore Y". And `prompts.md`'s validation table enforces exactly that sentence —
`band3_consequence` must be a verbatim quote showing the decision that changed, "No
consequence quote, no 3." So:

- A candidate coached to append "...and that number is why I chose Z" to any answer earns
  3s. The product that teaches this rubric is the product that defeats it.
- Answer 5 is the proof case, and it is worse than gameable. "The ceiling only starts to
  bind if the 8B share drops below roughly 20 percent, so that is the number I would watch"
  is a perfect band-3 quote attached to a number that **contradicts his own figures** (B3
  and Part A). Every row of the validation table passes.

**Net direction: too generous**, via narration. And simultaneously too harsh in one place:
line 59 says "In the 45-minute mock, where there is room, expect the indicators to appear
and treat their absence as the 2/3 discriminator." That quietly reinstates the conjunction
the file had just removed, for the mock only, without saying how many indicators are
needed. The "ONE required clause" fix is announced as universal (line 41) and retracted
three paragraphs later. Pick one.

**The fix I would actually make: promote the reversal condition to the required clause.**
Band 3 already lists it as an indicator — "Named the condition under which they would
reverse the decision ('if long-context share goes above ~20%, this flips')." Make that
mandatory and demote "the result changed the design" to an indicator, because:

1. A reversal condition **cannot be faked without understanding the number.** It requires
   inverting your own arithmetic and is falsifiable against it — had Answer 5's "below 20
   percent" been required to be checkable, it would have failed, where today it scores.
2. It is a counterfactual, so it does not depend on utterance order. It would have resolved
   Answer 3 cleanly: he never says what would make him choose differently, so 2, and I
   would not have needed to reason about whether popularity or arithmetic came first.
3. It is codeable. `band3_reversal_condition` plus a recomputation check (B5.1) is a real
   gate where `band3_consequence` is a rhetorical one.

**My persona's caveat, stated here rather than only in B7:** requiring a reversal condition
inside 60 seconds may be too demanding, and it is plausible that human interviewers *do*
reward narration — "I chose X because the number said Y" may be the actual signal a loop
scores, in which case the rubric is right and I am over-engineering. This needs a
practitioner, and it is the single highest-value thing in my report for a human to settle.

---

## B5. Top 3 defects, ranked

### B5.1 — The validation table enforces the *form* of band 3 and never the *truth* of a number

**File:** `prompts.md`, validation table (rows "Derived-quantity cap",
"Derived-quantity integrity", "Band-3 evidence"); `rubric.md` lines 161, 166–183.

**What is wrong.** `derived_quantity` is checked for *provenance* ("reject if it appears as
a substring of the prompt text") and never for *correctness*. Nothing in the table, the
schema, or the grader prompt recomputes anything. In a rubric whose highest-weight
behaviours are arithmetic, the entire anti-flattery layer verifies that a number was
*produced and not copied*, and is indifferent to whether it is *right*.

**Why it matters.** Answer 5 in the blind set passes every single row while resting its
band-3 claim on a number that contradicts its own arithmetic: the "20 percent" threshold is
derivationless and, under the answer's own assumptions, false at every traffic split. It is
not in the prompt, it participates in a comparison, it has a clean consequence quote. The
table's own stated purpose — "this table is the actual anti-flattery mechanism" — is
unmet for the dominant flattery vector in a numeric domain, which is **confident wrong
arithmetic**. This is also the vector a fluent model answerer produces most often, and the
one that most damages a candidate: being taught that a wrong number scored 3 is worse than
being taught nothing.

Note a second, smaller hole in the same rows: the integrity check is a *string* operation on
a *semantic* property. "400 milliseconds" in the prompt is not a substring match for "0.4
seconds" or "400ms", so a pure echo passes; and a genuinely derived "400" would false-reject
against a prompt containing "4,000". Likewise "Relevance integrity" verifies that
`prompt_constraint_engaged` is a verbatim substring of the prompt — which catches a
fabricated quote but not a mis-attributed one, i.e. it does not test that the decision
actually rests on the quoted constraint, which is the whole claim.

**What I would do.** Add a `derivation_steps` array to the schema — ordered
`{inputs, operation, result, units}` — and a code check that recomputes it and rejects when
the stated steps do not reproduce the stated result within, say, 1.5×. The arithmetic in
these items is all multiply/divide/sum over quantities with units; this is unit-aware
evaluation, not a research problem. Then: parse quantities to value+unit rather than
substring-matching numerals, and require ≥1 arithmetic operation for the cap to clear.
Pair with the B4 change (`band3_reversal_condition`, recomputed the same way).

### B5.2 — Two of the three model answers I checked teach something false, and the contrast-provenance check locks it in

**File:** `questions.json` line 442 (`annotation`, `model_answer`) and line 301
(`inline-safety`, `model_answer`); `prompts.md` validation table, "Contrast provenance".

**What is wrong.** `annotation`'s model answer argues that doubling the annotator pool buys
nothing because "doubling the team doubles both the signal and the noise" — statistically
false (B3.4), and contradicted by its own `good` field, which states the correct leverage
argument. `inline-safety`'s model answer adds two p99s and calls the result the budget
(B3.1), and offers a prefill-overlap third option whose mechanism contradicts Appendix B
(B3.2). These are not rough edges in an explanatory aside; in both items the false step is
the load-bearing one.

**Why it matters, and why it is coupled to the contrast check.** `prompts.md` instructs:
"Generate `contrast` against `<reference>.model_answer` ... NEVER against a polished version
of what the candidate said" — and the validation table *enforces lexical proximity* to
`model_answer`. So `model_answer` is simultaneously (i) the judge's anchor for what at-bar
sounds like and (ii) the text the candidate is shown as the model of a good answer, with a
code-level check pushing the shown text toward it. A falsehood in `model_answer` is
therefore taught twice: the grader marks down a candidate who gets it right, and the
candidate is shown the wrong version as the target. A paying candidate who repeats "doubling
doubles the noise so you gain nothing" or "310 plus 180 is 490 so it doesn't fit" to a real
interviewer who knows better is harmed by this product.

**What I would do.** Three things, in order. (1) Fix the two model answers per B3.1/B3.2/
B3.4. (2) Add a review gate to the authoring process: every `model_answer` numeric claim
must be reproducible from Appendix B's anchors or carry its own stated assumption —
Appendix B already holds this standard for itself and the model answers do not inherit it.
(3) Reconcile `good` against `model_answer` item by item; I found two items where `good`
contains the best beat and `model_answer` omits it, which means the contrast pipeline
systematically ships the weaker of two texts the pack already wrote.

### B5.3 — `inline-safety-classifier-budget`, the pack's only pushback item, has three independent faults

**File:** `questions.json` lines 301–347.

**What is wrong.** (a) The tech lead's proposal is a straw man in the half the item rests on
— "retract anything bad after the fact" is incoherent on a streaming path, so the item's
discriminating insight is a product-comprehension check, not a design judgement (B2).
(b) The prompt tells the candidate "You disagree", which forecloses the `bad` field's own
second failure mode and orphans the `accepts async immediately` follow-up branch — an
internal contradiction across three fields of one item. (c) The arithmetic adds p99s and the
proposed third option contradicts Appendix B on prefill (B3.1, B3.2).

**Why it matters.** This is the only item in the bank explicitly shaped around pushback, and
`communication_collaboration` is the axis the rubric itself calls the one that "carries the
product" (line 230). Of the four items carrying that axis, this is the one where pushback is
the entire content. If it measures a UI fact rather than a judgement, the product's
headline differentiator rests on its weakest item. It is also the item whose domain is
closest to mine, and it is the one I would be most embarrassed to see in front of a
practitioner.

**What I would do.** Replace the lead's line with "just run it async and kill the stream at
the first unsafe token", delete "You disagree", fix the two arithmetic faults, and add to
`good` the two beats the strong version demands: bound the exposure window in tokens, and
name where the classifier runs (shared GPUs ⇒ additive; separate pool ⇒ overlapped but
uncosted and newly dependency-coupled). The item then measures what it was built to measure.

### Also, below the top three but worth a line each

- **The per-axis aggregation function across items is nowhere specified.** `rubric.md`
  line 83 gives `mean(axis_scores)` for the *composite percentile*, and the level mapping
  consumes per-axis values ("any axis at 0", "≥4 axes ≥ 2"). But each axis is assessed on
  exactly 4 of the 12 items (`_meta.axis_coverage`), and nothing says how 4 item-level
  bands become the one axis value the level claim reads. Mean? Min? Modal? If min, one bad
  item sends every candidate below the senior bar; if mean, "any axis at 0" is nearly
  unreachable and that level rule is dead code. I grepped `rubric.md`, `prompts.md` and
  `calibration-plan.md`: the function is not stated anywhere. This is the input to the
  user-facing status claim and the share artifact. Specify it before any level is shown.
- **The relevance clamp cannot arbitrate 0 vs 1,** and Answer 4 is the case: both its axes
  clamp to ≤ 1, two readings (0 and 1) survive the clamp, and the rubric gives no rule. The
  level mapping treats 0 very differently from 1. Add one line: a clamped axis floors at 1
  when the behaviour was present-but-misdirected, 0 when it was absent.
- **No grader test-retest anywhere.** `calibration-plan.md` specifies quadratic-weighted κ,
  exact/adjacent agreement and mean signed difference against humans — genuinely good, and
  the sample-size honesty section (lines 72–83) is the most intellectually honest page in
  the pack. But nothing measures the grader against **itself**: re-grade the same transcript
  N times and report per-axis score variance. Temperature near 0 is asserted in prose and
  verified nowhere. In my experience this is the cheapest and earliest signal you can get,
  it needs no human labels, and a cell whose score moves across reruns is a badly written
  cell — which is the plan's own diagnosis criterion (line 44). Add it to the Phase 3 gate.
- **`first_raised_by` is one enum for a whole axis.** If a candidate raised the capacity
  math unprompted but only named the binding constraint after a probe, the field can hold
  one value and a grader will choose "candidate", clamping nothing. Attach it to
  `evidence_quote` and to `band3_consequence` separately; the clamp should key on who first
  raised the **consequence**, since that is what band 3 scores.
- **Minimum criticism (≥2 below-bar observations) is a floor on count, not substance.** Two
  trivially-true observations satisfy it forever, and for a genuinely excellent session it
  forces manufactured criticism — the mirror of flattery, degrading the top of the scale.
  Require each observation to name the cell clause and the axis it would have moved, and
  permit a logged single-observation output when both assessed axes scored 3.

---

## B5-bis. The judge design, and the contrast-provenance check specifically

Asked of me directly, answered directly.

**Is the validation table sufficient? No.** It is unusually good for a first draft — the
separation of interviewer and grader, `assessed: false` instead of spurious zeros,
`first_raised_by`, evidence-as-verbatim-substring, reject-and-re-ask rather than silent
repair, and logging rejection rate per check as a live signal are all things I would have
had to argue for. The evidence-integrity row in particular ("reject if any `evidence_quote`
is not a verbatim substring of the transcript — this catches paraphrase, which is where
invented evidence enters") is exactly right and is the row I would keep above all others.

What it does not cover: arithmetic truth (B5.1), semantic rather than substring quantity
matching (B5.1), per-clause attribution (B5), score determinism (B5), and completeness of
the `assessed: false` set — the "Axis set" row rejects scoring an axis *not* in
`axes_to_score`, but nothing rejects *omitting* one that is, or an axis absent rather than
explicitly `assessed: false`. Given that the file's own defect #2 is about spurious zeros
tanking the level claim, the schema should be defended in the direction the file already
knows it is fragile.

**Is contrast provenance via trigram overlap a real check or security theatre? Theatre —
and mildly harmful theatre. I would delete it, not tune it.** Four reasons:

1. **The comparison is rigged to pass.** The grader is *instructed* to derive
   `at_bar_answer` from `model_answer`, so lexical overlap with `model_answer` is
   structurally high; overlap with a 60-second spoken transcript — full of filler, hedges
   and false starts, where word trigrams almost never match written prose — is structurally
   low. The check passes near-unconditionally whether or not the grader flattered. A check
   that cannot fail is not a check; it is a line in a table that makes the anti-flattery
   layer look longer than it is.
2. **It is pointed at the wrong failure, and arguably inverted.** Flattery does not enter as
   *copying the candidate's words*. It enters as *copying the candidate's conclusions*: the
   grader writes a contrast in `model_answer`'s own vocabulary while silently selecting the
   subset of `model_answer` the candidate happened to hit, and omitting the beats they
   missed. In that case overlap with `model_answer` is **maximal** and the check is maximally
   satisfied. It scores the exact artefact the real failure produces.
3. **It is underspecified to the point of being unimplementable as written** — word trigrams
   or character trigrams? Jaccard, containment, or asymmetric coverage? What threshold, and
   normalised how? Character trigrams over same-domain English are near-saturated on both
   sides; word trigrams are near-zero on both. Whoever implements this picks one and the
   check then means whatever that choice made it mean.
4. **It false-fires precisely where the grader is working.** If the candidate genuinely was
   at bar, their transcript and `model_answer` have high mutual overlap, and which side the
   contrast lands closer to is noise. So the rejection rate rises on the strongest sessions
   — a flake source inside the validation layer. My formative lesson in this area is that a
   gate people override is worse than no gate, and the first thing an engineer does with a
   row that rejects valid output on good inputs is widen it until it never fires. At which
   point you are shipping row 11 of a 12-row table as decoration.

**What to replace it with — structural, deterministic, and it checks the property you
actually want.** The property is "the contrast tells the candidate something they did not
do." So verify coverage, not lexis:

- Enumerate the item's `required_beats` (Prompt 1 already requires this field for the mock;
  the 12 diagnostic items lack it, so this closes a known schema gap rather than opening a
  new one).
- Have the grader emit, per beat, `{beat_id, present_in_candidate: bool, evidence or null}`
  — reusing the evidence-integrity check already in the table.
- Reject when `contrast.at_bar_answer` covers no beat marked `present_in_candidate: false`.

That fails loudly, fails for the right reason, is cheap, needs no threshold, and gives you a
per-beat miss distribution across the cohort for free — which is better item analysis than
`calibration-plan.md` Phase 2 currently plans. It also lets you *drop* the flattery-shaped
risk entirely: a contrast built from beats the candidate missed cannot be a polished echo of
what they said, by construction.

One more, since I own the judge design: **the interviewer prompt is better than the grader
prompt.** Prompt 1's rules 1, 2, 4 and 6 and the pushback protocol ("Push exactly once per
decision ... Do not push a second time on the same decision; that stops measuring judgment
and starts measuring stamina") are the best-reasoned text in the pack, and the Good/Bad
pushback example is genuinely instructive. My only substantive note on it: rule 7 permits
the interviewer to "invent a plausible constraint" and stay consistent with it, but the
grader's relevance gate requires `prompt_constraint_engaged` to be a **verbatim substring of
the prompt**. A candidate who correctly reasons from an interviewer-invented constraint
cannot have that quoted, so the grader must either emit `addresses_prompt: false` and clamp
a good answer to ≤ 1, or fabricate. Fix: carry invented constraints into the grader's
`<prompt_as_given>` block as an appended, timestamped addendum, and let the integrity check
match against prompt + addenda.

---

## B6. Sign-off

**What I would refuse to let ship as-is:**

1. **The three `model_answer` fields I checked**, until the arithmetic is fixed — `inline-safety`
   (adds p99s; prefill-overlap mechanism contradicts Appendix B), `annotation` (teaches a
   statistical fallacy), `heterogeneous-fleet-routing` (a blended cost that omits the most
   expensive of three models). Model answers anchor the judge *and* generate the
   candidate-facing contrast, so a false one is taught twice. Blocking.
2. **Any percentile or level claim**, until the per-axis aggregation function across items is
   written down. Today the share artifact's status claim is computed by an unspecified
   function. Blocking, and cheap to fix.
3. **The contrast-provenance row.** Not "fix it" — remove it. Shipping a check that passes
   unconditionally manufactures false confidence in the layer the file calls "the actual
   anti-flattery mechanism", and it will be cited internally as covering a risk it does not
   cover. Replace with the beat-coverage check above, or ship with the row absent and the
   gap named.
4. **`inline-safety` in its current form**, as the pack's only pushback item. Not because
   the topic is wrong — because the straw man means it measures something other than what
   the scorecard will say it measured.

Everything else I would ship with findings attached, including the rubric itself.

**Would I put my name on this rubric as legitimate? Yes — with one caveat that matters.**

Yes, because it does the things most internal rubrics do not: it states where it departs
from its sources and why (lines 299–325); it lists its own unvalidated numbers as
unvalidated (lines 328–348); its band-1 cells describe observable behaviour rather than
adjectives; the relevance gate is a real idea and plant 08b as a negative control for it is
the single most sophisticated thing in the pack; Appendix B's arithmetic is correct and
honest about its sparsity caveat; and `calibration-plan.md`'s refusal to hand a κ computed
from n < 50 to the GTM agent is the kind of discipline that is usually absent. I have
reviewed worse rubrics that were in production.

The caveat, stated precisely because it is the thing my signature would be read as covering:
**I would sign this as a legitimate teaching artifact and a legitimate scoring framework. I
would not sign the level claim derived from it.** The 2/3 boundary measures narration rather
than causality (B4), the aggregation into a per-axis value is unspecified (B5), two of the
six axes are probably one axis (B1), and nothing yet measures whether the grader agrees with
itself across reruns. Those four together mean the band-level evidence on a report is
defensible today and the words "at the staff bar" on a share artifact are not.

---

## B7. Epistemic status

Required to be candid, so: roughly a third of what is above is checkable, a third is domain
judgement I would defend to a peer, and a third needs a human who has read scorecards at
volume. Sorted honestly.

### Checkable facts — verify these without me

- **`annotation` effective-sample-size math** (B3.4). κ = 0.62 ⇒ p_o = 0.81 ⇒ λ = 0.62 ⇒
  e ≈ 0.19 ⇒ n_eff ≈ 0.38n. Arithmetic shown; the conclusion that "doubling n at fixed
  noise doubles n_eff" is not a judgement call.
- **`eval-infra` judge-call omission** (B3.3): ~23.3 PFLOPS of judge prefill ⇒ ~59 GPUs
  unaccounted, on a stated 112.
- **`eval-infra` provisioned-vs-consumed and the M/D/1 queue result** (B3.3): ρ ≈ 0.83,
  W_q ≈ 25 min, so a 10-minute gate is a ~35-minute gate at one lane.
- **`heterogeneous-fleet-routing` omits the 400B from a blended cost** (B3.5): 5% at 5.7×
  contributes ~47% of the bill. Arithmetic shown.
- **Prefill of 2,000 tokens ≈ 177ms** by Appendix B's own method, where the model answer
  says "hundreds of milliseconds" (B3.2).
- **p99(T+C) ≠ p99(T) + p99(C)** (B3.1). The *mathematical* claim is a fact; which
  approximation is right for *this* system is judgement — see below.
- **Model-answer word counts**: median 172, mean 168, 11 of 12 over 60 seconds at 150 wpm,
  against the pack's own "median under 170" threshold; `annotation` at 166 words against its
  own stated 30 seconds (B3.6). I counted all twelve.
- **Internal contradictions**, each a file-and-line read: "You disagree" vs the
  `accepts async immediately` follow-up and vs the `bad` field; `good` containing beats
  absent from `model_answer` in two items; `rubric.md` line 41 ("ONE required clause")
  vs line 59 (indicators as the mock's 2/3 discriminator); Prompt 1 rule 7 (invented
  constraints) vs the grader's verbatim-substring relevance integrity check; "prefill is
  compute-bound" in Appendix B vs "costs us almost nothing in wall clock" in the
  `inline-safety` model answer.
- **Absences**, by grep across `rubric.md`, `prompts.md`, `calibration-plan.md**: no
  per-axis aggregation function across items; no grader test-retest / score-variance
  measurement; no inter-axis correlation check.
- **Answer 5's "20 percent" is internally inconsistent** with its own 55-cent figure
  (Part A, B3). Arithmetic shown.

### Domain judgement a practitioner in my area would mostly share

- **You cannot add p99s and call it a budget**, and the right conservative assumption here
  is near-additive *because* classifier cost and prefill both scale with prompt length. The
  correlation argument is mine; I am confident in it and it is not a proof.
- **"Overlap with prefill" is not free without saying where the classifier runs**, and the
  stated 40ms p50 back-solves to a classifier large enough for this to matter. The
  back-solve assumes the classifier runs on comparable hardware (see assumptions).
- **Async-plus-retraction is not what a competent lead proposes on a streaming path**, and
  async-plus-stream-termination is. This is the core of my straw-man verdict. It is the most
  confident domain judgement in this report — I have had this exact argument — and it is
  still a judgement about what a hypothetical competent person would say.
- **Trigram overlap is the wrong instrument for contrast provenance**, and the beat-coverage
  replacement is better. I have built and been burned by lexical proxies for semantic
  properties in eval infrastructure; this is the pattern.
- **Grade determinism belongs in the gate before human agreement does**, because it is free,
  needs no labels, and a cell that disagrees with itself cannot agree with a human. This is
  the single strongest conviction I hold from building eval systems and I would argue it
  against resistance.
- **A ≥2-criticism floor manufactures criticism at the top of the scale.** Widely observed;
  mechanism is obvious; I have not seen it measured.

### Guesses about interview practice — these need a human, and I am the wrong person

My persona's stated weakness is real and I am not going to hedge around it: **I have
interviewed, I have never owned a rubric or normed one against a cohort.** Everything in this
block is weaker than it reads.

- **Whether `capacity_cost_estimation` deserves axis status** (B1). My argument that it
  duplicates `tradeoff_articulation` is an argument about *this cell text*. Whether real
  loops score "did the math" and "used the math" as separate lines, I do not know. The
  rubric names this its most likely error and I have added specificity, not resolution.
- **Whether the 2/3 boundary should require a reversal condition** (B4). This is my most
  consequential recommendation and the one I am least sure of. If human interviewers in fact
  reward *narration* of causality — "I chose X because the number said Y" — then the rubric
  is right, my criticism is wrong, and my fix makes band 3 unreachable in 60 seconds. Settle
  this before acting on B4.
- **Whether six axes match what a system design round scores at all.** I can say the six are
  coherent and partially redundant. I cannot say they are the right six.
- **Whether `communication_collaboration` is scorable from 60 seconds** — the rubric's own
  open question 3. I did not score that axis in Part A (it was not listed on any of the five
  answers), so I have no evidence either way and deliberately did not opine.
- **Whether band-1 language reads as insulting** (open question 5). I found it diagnostic
  and useful. I am not the reader at risk, and my reaction is close to worthless here.
- **The level-mapping thresholds** (open question 4). I flagged that the aggregation function
  is missing, which is structural. Whether the thresholds themselves are right is a
  calibration question against a cohort that does not exist yet.
- **Whether fail-open/fail-closed ownership is a fair expectation for this audience.** My
  persona's second stated blind spot, and I think it bit: I have pressed hard on who owns
  the fail-open decision, and for a general infra candidate that may be a frontier-lab
  concern they would never be asked. Discount my `inline-safety` recommendations by
  whatever you know about the actual audience, and treat the straw-man finding (which does
  not depend on this) as more robust than the fix I proposed for it.

### What I had to assume because the pack does not say

Each of these flips a finding, so they are listed as risks, not footnotes.

1. **`inline-safety`: that the classifier shares the serving GPUs.** Unstated, and B3.2's
   conclusion inverts on it — separate pool means overlap really is nearly free in wall
   clock, and my criticism reduces to "say so, and cost the pool."
2. **`eval-infra`: that the judge is also a 70B model.** Unstated, and the fleet estimate
   roughly doubles or halves on it. My ~180-GPU figure is "same model as the generator".
3. **`eval-infra`: that commits arrive over an 8-hour workday.** If they arrive uniformly
   over 24h, ρ drops to ~0.28, queueing largely disappears, and the concurrency half of
   B3.3 weakens considerably. The provisioned-vs-consumed half survives either way.
4. **`annotation`: binary comparisons with balanced marginals**, giving p_e = 0.5. With
   three-way judgements or ties, κ → p_o differs and my 0.38n becomes something else. The
   direction of the finding (doubling n doubles n_eff) does not depend on this; the specific
   numbers do.
5. **"Trigram" means word trigrams.** If character trigrams were intended, my reason 3 gets
   stronger and reason 1 gets weaker — the check still does not do what it claims.
6. **That per-item axis scores aggregate by mean** across the 4 items per axis. I had to
   assume something to reason about the level mapping; this is exactly the unspecified
   function I flagged, so treat my level-mapping comments as conditional on it.
7. **That 150 wpm is the right spoken rate** for the word-count finding. At 180 wpm the
   median model answer is 57 seconds and B3.6 softens to "half the items are marginal".
   `calibration-plan.md` sets its threshold in words, not seconds, and the median exceeds
   that threshold regardless of rate.
8. **That `calibration-plants.json` does not already fix some of this.** I was instructed
   not to read it, and `rubric.md` says several cells were rewritten in response to plants.
   It is entirely possible a plant already covers B5.1 or the 0/1 floor. If so, say which,
   and discount accordingly — my report is written from the files I was permitted to see.
