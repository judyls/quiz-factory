# REVIEWER 5 — hiring rubric operator

Read: `review-harness/personas/05-meta-rubric-operator.md`, `review-harness/review-protocol.md`,
`review-harness/blind-scoring-set.md`, `rubric.md`, `questions.json`, `prompts.md`,
`calibration-plan.md`.

**Not read, as instructed:** `calibration-plants.json`, `dry-run-report.md`, anything in
`review-harness/findings/`. I saw no expected-score content. I did read `prompts.md:332`,
which says the plants are the grader prompt's test suite and that plant 08b is the
over-fire control — that is a reference to the plants, not their contents, and it is also
stated in `rubric.md:78`.

Part A was completed before any of `questions.json`, `prompts.md` or `calibration-plan.md`
was opened.

---

# PART A — BLIND SCORING

## Answer 1 — `A01` (batch window vs TTFT budget)

```
Answer 1 / capacity_cost_estimation: 1
  cell clause applied: "Gave a number with no derivation"
  evidence: "Given our 400 millisecond target I would bias toward latency."
  admits another reading: yes — band 0. Band 0 reads "No quantity of any kind, in a
  scenario whose constraints were stated numerically" (rubric.md:151). Literally, no
  quantity of the candidate's own appears anywhere; the only number is the prompt's own
  400ms, and the hard-cap gloss at rubric.md:163-164 says in terms that echoing the
  prompt "puts a number in the transcript while deriving nothing". A grader who takes that
  gloss seriously scores 0. The cap says "≤ 1", which sets a ceiling and not a floor, so
  the cell and its own cap point in different directions.
```

```
Answer 1 / tradeoff_articulation: 2
  cell clause applied: "Named the axis of the trade-off in units ... stated which side of
  it this system should sit on and why, given the stated requirement, and acknowledged
  specifically what the choice gives up. Picked."
  evidence: "The trade-off is latency against throughput: a wider batch window buys you
  utilisation and spends time-to-first-token. Given our 400 millisecond target I would bias
  toward latency."
  admits another reading: yes — band 1, if "in units" is enforced. He names two
  dimensions, not units; no ms and no tok/s appear on either side. Under a strict reading
  the hard cap at rubric.md:242 ("if no trade-off axis was named explicitly ⇒ ≤ 1") fires.
  The cell's own example list makes the strict reading untenable, because it offers
  "latency vs throughput" as an instance of an axis named *in units*. The cell contradicts
  its own examples, so the cap will be applied loosely in practice.
  Not 3: band 3 requires the trade-off "resolved against a number they produced". He
  resolves it against the prompt's number and then defers the one number that would decide
  it — "I would tune the window empirically".
```

## Answer 2 — `A03` (vector index, HNSW)

```
Answer 2 / capacity_cost_estimation: 1
  cell clause applied: "Derived the number that decides the question, then proposed a
  design it rules out (computed 40TB raw, then chose an index that needs all of it
  resident) — the number was produced but not understood."
  evidence: "so about 40 terabytes raw ... Given the recall requirement I would use HNSW"
  admits another reading: yes — band 2. The arithmetic is derived and correct
  (1,024 × 4 B = 4 KB; × 10e9 = 40 TB; 200M/10B = 2%), and "We would shard across machines"
  is a real answer to 40TB, so a grader who credits sharding reaches band 2. I hold at 1
  because band 2's bolded clause — "Named which constraint binds ... and showed why the
  others have slack" — never happens: he restates the latency budget and the recall floor
  without saying which of them binds.
  Instrument note: this band-1 clause names "40TB" and an all-resident index explicitly.
  It is written around an answer of this exact shape. Scoring it correctly is therefore no
  evidence the cell generalises — see B5.1.
```

```
Answer 2 / tradeoff_articulation: 1
  cell clause applied: "Or chose, but justified it with an unfalsifiable claim"
  evidence: "because it has the best recall-latency curve of the ANN families — typically
  0.95-plus recall at single-digit millisecond latency"
  admits another reading: yes — band 0. "No alternative considered. Presented one design as
  the design" fits: no competing index is ever named. He uses comparative language about
  families in the abstract but compares nothing. The prompt asked "tell me what the choice
  costs you" and no cost is stated, so the trade-off is not merely under-defended, it is
  absent. The 0/1 boundary on this axis is the second ambiguous crack I hit in five answers.
```

## Answer 3 — `A03` (vector index, IVF-PQ)

```
Answer 3 / capacity_cost_estimation: 2
  cell clause applied: "Named which constraint binds — memory capacity vs memory bandwidth
  vs compute vs network vs dollars — and showed why the others have slack."
  evidence: "which makes memory the binding constraint here. Latency has slack — 50
  milliseconds is generous for an approximate lookup — and 200 million changes a day is
  about 2 percent, which is an ingest-volume question rather than a throughput one."
  admits another reading: yes — band 3, and this is the sharpest 2/3 case in the set. A
  grader who reads 40TB → memory binds → choose a compressing index as one causal chain
  scores 3 on "the number ruled out an architecture". I hold at 2 on two grounds the cell
  supports: he announced the choice *before* the arithmetic and justified it with "it's
  what most billion-scale deployments run", which is the rubric's own band-3 counter-case
  at rubric.md:31-33 ("sizes the system correctly and then proposes the architecture they
  were always going to propose"); and he never states a compressed footprint, so no number
  of his connects 40TB to PQ. Two competent graders will split here.
```

```
Answer 3 / tradeoff_articulation: 1
  cell clause applied: "Or chose, but justified it with an unfalsifiable claim ('it's more
  scalable', 'it's industry standard', 'it's more flexible')"
  evidence: "I'd go with IVF-PQ — it's what most billion-scale deployments run."
  admits another reading: yes — band 0, same crack as Answer 2. Independently, the hard cap
  fires: no trade-off axis is named, so ≤ 1 regardless. Here the cap is doing exactly the
  work it was built for — the prompt asked what the choice costs and PQ's recall cost is
  never mentioned.
```

## Answer 4 — `A08` (long-context cache eviction)

```
Answer 4 / requirements_scoping: 0
  cell clause applied: "Began designing from the prompt as given. Never asked what the
  system must do ... never bounded the problem. Treated an underspecified prompt as a
  specification."
  evidence: "The problem is that a fixed batch size makes time-to-first-token depend on
  batch fill rather than on compute." — the A08 prompt never mentions a fixed batch size.
  The prompt asked two direct questions ("what exactly are you protecting, and what is the
  first number you would want?") and neither is answered.
  admits another reading: yes — band 1, via "recited a generic checklist unconnected to
  this scenario", and via the relevance gate's phrasing at rubric.md:62 ("scores at most
  band 1"), which reads as naming where a wrong-problem answer *lands*. I changed my mind
  twice on this cell. It is the hardest in the set (see end of Part A) and the two readings
  produce different public level claims from the same transcript, because "any axis at 0"
  sends the scorecard below the senior bar on its own.
```

```
Answer 4 / capacity_cost_estimation: 1
  cell clause applied: relevance gate, rubric.md:62 — "A behaviour performed on the wrong
  problem scores at most band 1 on every axis, however well executed." Corroborated by band
  1's "Used a number that contradicts a constraint stated in the prompt."
  evidence: "across four H100s at 3.35 terabytes per second that is roughly 13 terabytes per
  second aggregate" — the prompt states eight nodes of eight H100s.
  admits another reading: yes — band 3, and this is the most dangerous cell in the set.
  Every clause of bands 2 and 3 is literally satisfied: the quantity is derived, the
  arithmetic is right (140/13,400 s ≈ 10.4 ms), bandwidth is named as binding, and the
  number visibly moves the design ("size the admission window at 20 to 25 milliseconds").
  Only the gate holds it at 1. The gate's integrity check accepts any verbatim prompt
  substring, and A01 and A08 share the phrases "p99 time-to-first-token" and
  "70-billion-parameter model" — so a judge that quotes "p99 time-to-first-token" passes
  the check and this answer scores 3. See B5.3.
```

## Answer 5 — `A09` (heterogeneous fleet routing)

```
Answer 5 / capacity_cost_estimation: 2
  cell clause applied: "Derived the binding quantity from assumptions stated out loud ...
  Arithmetic within ~2–3×."
  evidence: "blended cost is 0.7 times a tenth plus 0.3 times one, which is 0.37 — so about
  37 percent of what all-70B serving costs."
  admits another reading: yes — band 1, via "Gave a number with no derivation", which
  applies to two of his three figures. (a) "somewhere near 55 cents" rests on an all-70B
  baseline he never states; it implies ~$1.49/M, which happens to be the ceiling. (b) "the
  ceiling only starts to bind if the 8B share drops below roughly 20 percent" does not
  follow from his own numbers: at a 0% 8B share his model gives 1.0 × baseline ≈ $1.49,
  still inside $1.50, so on his figures the ceiling never binds at any share. (c) The blend
  omits the 400B entirely in a three-model scenario; at 70/25/5 it is 0.07 + 0.25 + 0.285 =
  0.605, i.e. 1.6× his figure. The ratios he does derive are accurate (70/8 ≈ 8.75;
  400/70 ≈ 5.7), which is why I land on 2.
  Gap: no cell on this axis covers "arithmetic correct, model structurally incomplete".
  The 2–3× tolerance absorbs the omission of a whole model.
```

```
Answer 5 / high_level_design: 0
  cell clause applied: "No end-to-end path ... Could not say what happens to a single
  request from arrival to response."
  evidence: the nearest thing to a design in the whole answer is "If 70 percent goes to the
  8B". There is no router, no classifier, no confidence threshold, no escalation or fallback
  path, and no answer at all to the prompt's second question, "what do you measure to know
  you have not quietly made the product worse".
  admits another reading: yes — band 1, for a grader who infers a router from "if 70 percent
  goes to the 8B". Band 1's clauses do not fit, though: there is no box diagram to be wrong,
  and no component named by brand. 0 is the better reading.
  Instrument note: this answer reproduces `questions.json`'s own `model_answer` cost
  reasoning almost phrase for phrase and omits only its design half. One 0 here sends the
  entire scorecard to "Below the senior bar". That is a lot of weight on one cell.
```

## Hardest cell to apply

**`requirements_scoping` band 0 vs band 1, on Answer 4.** Not because the answer is
ambiguous — it is plainly a wrong-problem answer — but because the rubric gives two
incompatible instruments for the same situation and no tie-break. The cell's band-0 row
matches three of its four clauses verbatim. The relevance gate says "at most band 1", which
reads like a landing point. The scoring contract says 0 means "the behaviour never appeared,
and nothing in the answer depended on it", and requirement-shaped material *did* appear —
for a different scenario. I scored 0 and I would not bet much on it.

This matters more than a one-band disagreement normally would, because of the asymmetry in
the level mapping: a 1 on every axis is "At the senior bar" territory, while a single 0
anywhere is "Below the senior bar" (rubric.md:88-89). The 0/1 boundary is the only boundary
in the instrument with a cliff behind it, and it is the boundary the rubric spends the least
text on. Four of the six band-0 cells admit two readings (B-table below).

Runner-up for hardest, and the cleanest contradiction in the file:
`capacity_cost_estimation` band 0 on Answer 1, where the cell ("no quantity of any kind")
and its own hard cap ("no quantity of their own ⇒ ≤ 1") disagree about whether a
prompt-echoed number is a quantity.

---

# PART B — CRITIQUE

## B1. Axis legitimacy

**Yes, with one real objection: `capacity_cost_estimation` and `tradeoff_articulation` are
substantially the same measurement, and the rubric's own band-3 definitions say so.**

The six axes correspond to what this category of round scores. Nothing here is invented and
nothing important is missing — scoping, design, depth, trade-offs and communication are the
spine of every structured design rubric I have operated. The AI framing is a vocabulary
layer over classic material, and `rubric.md:12-17` is right to say so out loud.

The objection is about axis independence, not legitimacy. Compare:

- `capacity_cost_estimation` band 3: "**the result changed the design**" (rubric.md:154)
- `tradeoff_articulation` band 3: "**the trade-off was resolved against a number they
  produced**" (rubric.md:240)

Those are one event described twice. A candidate who derives a number and lets it decide a
contested choice scores 3 on both; one who does neither scores low on both. Two of six axes
firing on the same observation inflates the scorecard's apparent dimensionality — and
`rubric.md:318-323` already admits six axes exist partly because "a six-mark scorecard is
readable as a share artifact". The risk is that the share artifact shows six marks of which
four are independent.

**What my answer rests on.** Operating rubrics and running calibration sessions in this
category, where the recurring empirical finding is that estimation rarely produces an
independent signal — it shows up as the evidence inside a scoping call or a trade-off.
Nothing here rests on knowledge of any named employer's process, and I make no claim about
one.

**What would change my mind, and some evidence against me already.** My own Part A diverges
between these two axes more than my concern predicts: Answer 1 scored 1/2, Answer 3 scored
2/1, Answer 2 scored 1/1. Three of five answers split by a band in opposite directions.
That is weak evidence — n=5, one rater, items selected to stress the rubric — but it is
evidence against me and I would rather report it than suppress it. The decisive test is
cheap: compute inter-axis correlation across the ten double-scored sets
`calibration-plan.md:38` already plans. If capacity and trade-offs correlate above ~0.8,
collapse them or rename one to measure something else. `calibration-plan.md:154` tracks item
discrimination but nothing tracks axis independence; add it.

**A sourcing circularity worth naming.** Band 3's spine across all six axes is "unprompted",
justified at `rubric.md:103-104` as "the senior/staff discriminator", from [HI-L]. The
band-3 rule itself ("performing the behaviour is band 2; letting it alter the design is band
3") rests on one sentence of [HI-D]. So the entire top band of a 24-cell instrument rests on
two sentences from two prep sites — and `rubric.md:464` records that [HI-L]'s level-breakdown
image could not be read, i.e. the primary artifact for the level discriminator was partially
unavailable. The pack is honest about this. It is still a single point of failure dressed as
grounding, and it is the thing a practitioner should be asked about first.

## B2. Scenario realism — instrument-adjacent items only

Technical realism belongs to the domain reviewers; my AI-infra depth is real but dated. I
took the four items I scored plus the four `communication_collaboration` items, and I judged
each as an *item* — does the constraint arrive the way such a constraint arrives, and does
the stated binding constraint actually bind.

| Item | Verdict | The single thing most wrong |
| --- | --- | --- |
| `batch-window-vs-ttft-budget` (A01) | Realistic | Nothing I can act on. Two bad numbers that co-occur only under one diagnosis is good item design. |
| `vector-index-at-10b` (A03) | Realistic, wrong in one detail | "200 million vectors **change** every day" never says whether that is in-place update or append. It is the load-bearing word in the item and it selects a different index: HNSW handles deletes badly, IVF-PQ handles append badly and partition-rebuild well. Two candidates answer two questions. Fix: "200 million are updated in place" or "added". |
| `kv-cache-admission-control` (A08) | Realistic | The prompt asserts the mechanism ("push the short ones out of cache"), which partly answers its own question "what exactly are you protecting". Minor; the capacity math underneath is sound against Appendix B. |
| `heterogeneous-fleet-routing` (A09) | Realistic, wrong in one detail | **The $1.50/M ceiling does not bind at the stated numbers.** Appendix B derives $0.37/M raw for a 70B on 4×H100, so all-70B serving already clears $1.50 by ~4× with no routing at all. The item's premise is that finance has imposed a real constraint; a candidate reasoning from the pack's own economics correctly concludes it is slack and will be marked down for it. Fix: state the loaded multiplier over raw compute, or drop the ceiling to ~$0.50. Secondary: "a mixed fleet of A100s and H100s" is stated and then plays no role in `good` or `model_answer`, even though a 400B in bf16 is ~800GB and does not fit on an A100 node without a lot of them — the most interesting constraint in the item is unused. |
| `inline-safety-classifier-budget` | Realistic — best-built item in the set | The arithmetic it rewards is invalid. See B3.3. |
| `eval-infra-per-commit-cost` | Realistic | 50,000 evaluations per commit at 40 commits/day is a caricature-scale ask, but the caricature is load-bearing for the pushback test, so leave it. The real problem is in the model answer's cost (B3.5). |
| `annotation-throughput-vs-agreement` | Realistic, wrong in one detail | "You have about 30 seconds" inside an instrument whose `_meta.answer_budget_seconds` is 60. The item halves its own budget, so `communication_collaboration` on this item is scored against a stricter clock than any other item — and against a clock that penalises slower speech. Pick one number. |
| `agent-retry-side-effects` | Realistic | Nothing. Arithmetic correct, the bug is correctly located in side-effect re-execution rather than in retry placement, and the `bad` field names the genuinely tempting wrong answer. |

## B3. Arithmetic

Checked every derivation in `rubric.md` Appendix B and every number in the eight items
above. Most of it is right. Six findings, ordered by how much they matter.

**1. "A fifth of a node's HBM" is wrong by 2–4×.** `rubric.md:404-406` derives 320 KB/token
correctly (2 × 80 × 8 × 128 × 2 B = 327,680 B ✓) and 100k tokens ≈ 32 GB ✓. Then: "comparable
to a fifth of a node's HBM". A fifth needs a 160 GB node. The pack uses two node
definitions: TP=4 (`rubric.md:410`) = 320 GB → 32/320 = **10%**; and eight H100s (the A08
prompt) = 640 GB → **5%**. Neither is a fifth. The sentence is load-bearing — it is the
justification for "why long-context admission control is a capacity problem and not a tuning
problem" — and it is still true at 5–10%, so fix the fraction, not the claim.

**2. The decode floor omits tensor-parallel collectives, and is then used as a throughput
estimate.** `rubric.md:409-413`: 140 GB / 13.4 TB/s ≈ 10 ms ✓ as a *bandwidth floor*, and
the word "floors" is honest. But two lines later "Batch 64 therefore yields ~6,000 tok/s" and
then the whole token-economics paragraph treat the floor as achievable. TP=4 needs two
all-reduces per layer × 80 layers = 160 collectives per token; at a latency-dominated
10–20 µs each that is 1.6–3.2 ms, so ~12–14 ms per step and ~20–30% less throughput, which
propagates straight into the $0.37/M figure. **This is the one number I most want a current
practitioner to check** — my collective-latency figures are from dated experience, and the
protocol's own example at `review-protocol.md:83-86` is this exact critique, so I may be
reproducing a prompt rather than a measurement. The structural point stands regardless: a
figure labelled a floor is consumed downstream as an estimate.

**3. The safety-classifier item rewards adding percentiles.** `inline-safety-classifier-budget`
`good` and `model_answer` both do 310 + 180 = 490 > 400 and call it "the arithmetic that
makes the disagreement concrete". p99 of a sum is not the sum of p99s. For independent
components, P(sum > q₁+q₂) ≤ 0.02, so the sum of two p99s bounds roughly the p98 of the
total, not the p99. The direction is conservative so the conclusion ("does not fit") probably
survives — but the rubric is teaching the judge that an invalid composition is the at-bar
behaviour, and a candidate who says "you can't just add p99s, I need the distributions"
is making a better observation than the model answer and will be scored against it. Fix:
have the model answer say "490 as an upper bound, and I'd want the joint distribution".

**4. Appendix B contains a 4× internal tension it does not reconcile.** It derives
$0.37/M output tokens for a 70B (`rubric.md:427-430`: $2/GPU-hr × 4 = $8/hr = $0.00222/s ÷
6,000 tok/s ✓) and then cites [H100] at roughly $0.09/M for a *120B* model
(`rubric.md:430-432`). A 1.7× larger model at 4× lower cost means the two rest on very
different concurrency or price assumptions. Both appear in the same appendix without
comment, and the looser of them is what makes A09's ceiling non-binding (B2). Reconcile or
drop one.

**5. The eval-infra model answer conflates marginal cost with fleet cost.** The chain is
arithmetically right: 50,000 × 2,000 = 100M tokens / 600 s = 166,667 tok/s ✓ ("about
170,000"); /6,000 = 28 replicas ✓; × 4 = 112 GPUs ✓; 112 × $2 × (10/60) = $37.33 ✓; × 40 =
$1,493/day ✓; × 365 ≈ $545k ✓. Every step checks. But $37/commit is a *marginal* cost that
assumes perfectly elastic capacity. 40 commits × 10 min = 6.7 hours of 112-GPU occupancy a
day; a reserved fleet is 112 × 24 × $2 = $5,376/day ≈ $1.96M/year, **3.6× the stated
figure**, and bunched commits need more than 112. This matters beyond the number:
`capacity_cost_estimation` band 3 lists "resized a fleet" as a qualifying consequence, so
the model answer teaching the judge conflates the two cost models the band distinguishes.

**6. Answer 5's threshold does not follow from Answer 5's figures** — detailed in Part A.
Flagged here because it is checkable, not a judgement: at a 0% 8B share his own model gives
1.0 × baseline ≈ $1.49 < $1.50, so the ceiling never binds at any share, and "below roughly
20 percent" is not derivable from anything he said.

Verified correct and worth saying so: the 8B KV figure (2 × 32 × 8 × 128 × 2 = 131,072 B =
128 KB ✓), prefill (1.4 PFLOP / 1.584 PFLOPS = 0.88 s ✓, 100k → ~9 s ✓), the agent fan-out
(1 − 0.98¹² = 21.5% ✓), and the 90 ms headroom in the safety item (400 − 310 ✓). The
sparsity caveat at `rubric.md:396-400` is exactly the right call and most packs get it wrong.
I could not verify the H100 NVL figures or the April 2026 third-party benchmark.

## B4. The band 2/3 boundary

**The 2/3 boundary is in roughly the right place and is roughly applicable. It is not the
boundary this instrument should be worried about.** Having applied all 24 cells, the
problems are at 0/1 and inside band 2 itself.

What I found applying it:

- **Band 3's required clause is genuinely operable.** "The result changed the design", with a
  consequence quote, is the most reliably testable thing in the file. On all ten cells I knew
  within seconds whether it was satisfied. One real 2/3 dispute in ten (Answer 3 /
  capacity), which is a good rate.
- **The boundary is in the right place substantively.** Answer 3 is the test: correct
  arithmetic, correct binding constraint, choice announced before the arithmetic and
  justified by appeal to practice. Scoring that 2 and not 3 is the behaviour I would want
  from a calibrated interviewer, and `rubric.md:31-33` anticipates the case precisely.
- **It is slightly too generous in one direction.** Band 3's indicators ("stated assumptions
  as assumptions", "rounded conservatively on purpose") are now non-blocking, so a candidate
  can reach 3 on one causal sentence. In a 60-second item that is the right call. In the
  45-minute mock, `rubric.md:56-58` says to treat indicator absence as the discriminator —
  which means the same cell has two bars depending on format, and nothing in the grader
  prompt tells the judge which format it is grading. `prompts.md` passes `axes_to_score` but
  no mode flag. Add one; it is a one-field fix with a one-band effect.

**And the answer to the question I was actually asked: the band-3 change made band 3
operable and made band 2 the new failure point. It moved the conjunction down a band rather
than removing it.** Every band 3 opens "All of band 2", and every band 2 is an unmarked
conjunction of three to five clauses with no required clause. So band 3 now needs one clause
and band 2 needs five — the instrument's bars are inverted, with the loosest requirement at
the top.

This is not hypothetical. It creates a **band-3-without-band-2** case the rubric cannot
score. Answer 4 is nearly it: a derived number that visibly moves the design (band 3's
required clause, satisfied) without ever showing the other constraints have slack (band 2,
failed). The rubric says band 3 is unreachable; it does not say what to award. A grader will
pick 2 or 1 by temperament. The author's fix was right and is incompletely applied.

The concrete repair, which costs one editing pass:

1. Give each band 2 **one bolded required clause**, the rest as indicators, exactly as band 3
   now does. The bolded clauses mostly exist already — "Named which constraint binds" and
   "Named the axis of the trade-off in units" are the right ones. `requirements_scoping`,
   `high_level_design`, `deep_dive_failure_modes` and `communication_collaboration` need one
   chosen.
2. Replace "All of band 2" with "band 2's required clause, **and** band 3's required clause".
   That removes the inversion and kills the band-3-without-band-2 hole.

## B5. Top 3 defects, ranked

### 1. Band 2 is the softest band in the file, and the level mapping rests entirely on it

**File:** `rubric.md:125, 153, 193, 218, 239, 268` (the six band-2 cells); the fix note at
`rubric.md:42-58`; the level mapping at `rubric.md:86-90`.

**What is wrong.** All six band-2 cells are unmarked conjunctions of 3–5 observations. Band 1
is the best-written band in the file — five of its six cells are clean disjunctive lists of
specific anchored failures, and the author's stated worry at `rubric.md:38` ("Band 1 is the
dangerous band to write loosely") is the one worry that has been fully discharged. Band 3 was
just hardened. Band 2 was left as the soft one. My 24-cell audit (below) puts **six of six
band-2 cells** in the two-readings column against **one of six band-1 cells**.

**Why it matters.** Every row of the level mapping is a statement about band 2: "≥4 axes ≥ 2",
"≥5 axes ≥ 2", "`tradeoff_articulation` ≥ 2" at every level. The public status claim is a
function of the 2 boundary almost exclusively, and the 2 boundary is where two graders will
least agree. A conjunctive band is applied as requiring whichever clause the reader noticed —
and in a 60-second answer, `high_level_design` band 2 ("traceable end to end", every
component justified, hard part in the design, read/write paths separated, where state lives)
cannot be satisfied in full by anyone, so in practice it will be scored on whichever one or
two clauses a given grader weights.

**What I would do.** The two-step repair in B4. Then double-score ten sets and report
agreement **at the 1/2 and 2/3 boundaries separately** — `calibration-plan.md:63-64` already
insists on per-axis reporting, which is right; add per-boundary.

### 2. The level claim is not computable from the document

**File:** `rubric.md:80-90` against `rubric.md:376-383`; `questions.json` `_meta.axis_coverage`.

**What is wrong.** The diagnostic is 12 items × 2 axes, with each axis covered by exactly 4
items (`axis_coverage`). The level mapping consumes **one score per axis**. Nothing anywhere
in the pack says how four per-item scores on an axis become that one score.
`rubric.md:83`'s `mean(axis_scores)` is the percentile's rule, and is itself ambiguous about
whether it averages 6 axis scores or 24 cells.

**Why it matters.** The rule is not a detail — it inverts the instrument's character:

- **Under mean:** "any axis at 0 ⇒ Below the senior bar" requires all four items on an axis
  to score 0. The harshest rule in the pack is effectively dead, and the mapping drifts
  generous — the exact failure `rubric.md:295-297` says matters most.
- **Under min:** one weak answer out of twelve sends every candidate below the senior bar.
  The mapping is unusably harsh and the top two rows almost never fire.

Both are defensible readings of a document that picks neither, and this produces the public
status claim that `rubric.md:349-351` already names as the highest-stakes unvalidated
numbers in the pack. Compounding it: four of six band-0 cells admit two readings, so the
rule with the cliff behind it sits on the boundary with the least agreement. And there is no
"no level claim" row — no output for insufficient evidence, even though
`calibration-plan.md:167` gates percentiles at n ≥ 200 and gates nothing on the level claim,
which is the louder of the two assertions.

**Direct answer to whether the thresholds are safe to ship: no.** Not because the numbers are
wrong — uncalibrated-but-defensible is a reasonable place to start, and the pack is honest
about it — but because the *function* is undefined, so "wrong" is not yet a thing the
thresholds can be. Ship the band plus the named blind spot, which
`calibration-plan.md:167-169` already proposes as the pre-n=200 reveal and which is the
honest claim the evidence supports. Hold the "At the staff bar" / "At the senior bar"
language until (a) the aggregation rule is written down, (b) the 0/1 boundary is double-scored
on ten sets, and (c) someone checks what fraction of real sessions the "any axis at 0" rule
actually catches. That third number will be the surprise.

### 3. The relevance gate and the derived-quantity cap can both be passed by a wrong-problem answer

**File:** `prompts.md:315, 318` (integrity checks); `rubric.md:73-78` (the gate); the probe
lists in `questions.json`.

**What is wrong.** Two holes, both the same shape as a defect the author already found and
fixed in the adjacent case.

**(a) The gate validates form, not correspondence.** `prompts.md:318` rejects only if
`prompt_constraint_engaged` is not a verbatim substring of the prompt. Adjacent items in this
bank share constraint phrasing by design — A01 and A08 both contain "p99 time-to-first-token"
and "70-billion-parameter model". Answer 4 in the blind set is this case: a judge that quotes
"p99 time-to-first-token" passes integrity, `addresses_prompt` stays true, and an answer to a
different item scores 3 on `capacity_cost_estimation` with every clause literally satisfied.
That is precisely the failure documented at `rubric.md:66-71` as the reason the gate exists.
The gate catches it only if the judge independently notices "four H100s" contradicts "eight
nodes of eight" — i.e. the mechanism adds no enforcement over the judge's own care, which is
the thing `prompts.md:281` ("A cap that lives only in the prompt is not a cap") says not to
rely on.

**(b) The derived-quantity cap is defeated by probe-echo.** `prompts.md:315` rejects
`derived_quantity` only if it appears in the **prompt** text. It does not check the
interviewer's utterances. Several probes state the answer: "One in five turns hits this. Is
it still an edge case?"; "Does 180 milliseconds fit in the budget or not? Show me."; "How
often does at least one of the 12 time out? Work it through." A candidate who repeats "one in
five" now has a `derived_quantity` absent from the prompt, participating in a comparison, and
the cap passes. `first_raised_by` is the intended backstop, but it is a per-axis judgement
with no integrity check of its own, so the clamp it feeds is as reliable as the judge. This is
the same defeat as prompt-echo (`rubric.md:159-166`), one source away.

**Why it matters.** These two caps plus the trade-off cap are the only anti-flattery
mechanisms that survive prompt drift — `prompts.md:281-282` is right that this table, not the
prose, is the product. A cap with a substring check that the failure mode routes around is
worse than no cap, because it is counted as coverage.

**What I would do.** Add a per-item `binding_constraint` field to `questions.json` and check
`prompt_constraint_engaged` against *that*, not against the whole prompt — it makes the gate
mechanical and costs twelve short strings. Extend the `derived_quantity` substring check to
the concatenation of prompt plus every interviewer utterance. Rewrite the four probes that
state their own answer ("Work it through" is fine; "One in five turns hits this" is not —
Prompt 1's rule 1 forbids exactly this and Prompt 2 permits it).

**Two smaller things found on the way, not in the top three:**

- `prompts.md:134` says the probe is "selected from the item's own `followups` list" and
  `prompts.md:141` says free generation "destroys the percentile". But every one of the four
  `communication_collaboration` items has **two conditions both labelled `if: at bar`**, with
  no tie-break rule. An at-bar candidate's probe is therefore nondeterministic, and the two
  probes are not equivalent — `inline-safety`'s are "the classifier is down, do you serve or
  refuse" versus "the output turns unsafe at token 500". Different candidates get different
  items, by the pack's own standard for what destroys a percentile. Fix: order the branches
  and take the first match, or label them `at_bar_1` / `at_bar_2` with a stated rule.
- `rubric.md:56-58` sets different band-3 bars for the mock and the diagnostic, and Prompt 3
  receives no mode flag. Add one field.

## B6. Sign-off

**Would I put my name on this rubric as legitimate? Yes for the axes and for band 1. No for
the instrument as a whole, as currently written.**

What I would refuse to let ship as-is:

1. **The level claim on the public share artifact** — "At the staff bar" / "At the senior
   bar" / "Below the senior bar". Not computable from the document (B5.2), resting on the
   softest band (B5.1) and on the 0/1 boundary with the least agreement. Ship the band and
   the named blind spot instead; that claim the evidence supports.
2. **`communication_collaboration` band 0's "near-silence" clause**, in the diagnostic. It
   is scoreable from the per-utterance timestamps the grader receives, it has no instruction
   excluding pre-speech thinking time, and the behaviour it penalises is deliberation (B-d
   below). Delete it from the diagnostic or re-specify it as a measured response latency.
3. **`inline-safety-classifier-budget`'s `good` and `model_answer` as written.** They teach
   the judge that adding two p99s is the at-bar move (B3.3). Cheap fix, and it is the item I
   otherwise rate highest.

What I would ship, with the fixes above: the six axes, all six band-1 cells (genuinely good
work, and the hardest band to write), the hard-cap mechanism as a *mechanism*, the
separation of interviewer and grader, the `assessed: false` flag, and the honesty of
`rubric.md:336-357` and `prompts.md:338-372`. A pack that documents its own three defects
before review is a pack I would work with.

The caveat on my yes: I am signing off on an instrument I have applied to five answers, not
to fifty sessions. Ten cells is enough to find ambiguity and nowhere near enough to find
drift.

### On the hard caps as a mechanism, and the floor effect

Asked directly: **the caps are the right mechanism, and they will produce a floor effect.**
Both are true and the second is fixable.

Right mechanism, because a prompt-level instruction to be harsh does drift generous within a
few revisions, and `prompts.md:281` names this correctly. Nothing else in the design survives
model substitution.

But four separate rules clamp to the **same** value: derived-quantity ≤ 1, relevance ≤ 1,
trade-off-axis ≤ 1, attribution ≤ 1. A wrong-problem answer, a numerate answer with no
derivation of its own, a decisive answer that never named the axis, and a good answer the
interviewer prompted all land on 1. My own Part A: **six of ten cells scored 1 or 0**, and
three of those were clamped there rather than reasoned there. `calibration-plan.md:207`
already predicts mid-level candidates near composite 1.3–1.7, i.e. the author expects the
pile. That is where most paying users will sit, and a percentile is worthless in a region
where the instrument cannot distinguish.

The fix is to let the clamps differ. The relevance gate at ≤ 1 is right — a correct answer to
the wrong question is not partial credit. Attribution at ≤ 1 is too harsh: doing the thing
well after one probe is genuinely better than not doing it, it is exactly what [HI-L]'s
mid-level expectation describes, and clamping it to the same value as answering a different
question destroys the distinction the axis exists to draw. Clamp attribution to ≤ 2 and the
pile at 1 thins where it should.

## B7. Epistemic status

### Checkable facts — verify these in minutes, no practitioner needed

- "A fifth of a node's HBM" (B3.1). Arithmetic; wrong under both node definitions the pack
  uses.
- p99s do not add (B3.3). A mathematical fact about percentiles.
- Answer 5's 20% threshold does not follow from Answer 5's own figures (B3.6, Part A).
- The $0.37/M vs $0.09/M tension inside Appendix B (B3.4); and A09's ceiling not binding
  against Appendix B's own $0.37/M (B2).
- The eval-infra marginal-vs-provisioned conflation (B3.5). Arithmetic correct, cost model
  mismatched to the conclusion drawn.
- **No aggregation rule exists** mapping 4 per-item axis scores to the 1 axis score the level
  mapping consumes (B5.2). I grepped every file in the pack for it. This is an absence, and
  absences are the one kind of finding I could have got wrong by searching badly — the grep
  covered `rubric.md`, `prompts.md`, `calibration-plan.md`, `CONFIG.md`, `01-BUILD-AGENT.md`,
  `03-GTM-AGENT.md`.
- The gate's substring-only integrity check, and the derived-quantity check not covering
  interviewer utterances (B5.3). Read directly off `prompts.md:315, 318`.
- Two identically-labelled `if: at bar` branches on all four comm items, with no tie-break.
- `annotation-throughput-vs-agreement` says 30 seconds; `_meta.answer_budget_seconds` is 60.
- Six of six band-2 cells are unmarked multi-clause conjunctions; five of six band-1 cells
  are anchored disjunctive lists. Structural, countable.
- Already self-flagged by the pack, so not my finding: Prompt 1 templates five variables
  (`constraints`, `required_beats`, `traps`, `at_bar_answer`, `followup_tree`) that
  `questions.json` does not have. `prompts.md:343-351` states it. Noting it only so a reader
  does not think I missed it.

### Domain judgement — a practitioner operating rubrics would mostly share

- Conjunctive bands get applied as whichever clause the reader noticed. This is the single
  most reliable thing I know about rubrics and it is why B5.1 is ranked first. It is
  experience, not a measurement.
- Band 2 carrying the level mapping makes the softest band the highest-stakes one.
- Four clamps to the same value pile the distribution at 1 and make the percentile
  uninformative where most users sit.
- "Unprompted" is a real discriminator, but it is partly an artifact of who gets interrupted —
  worth a human's attention, not something I can prove here.
- Register-matching and "loses the room" are bias vectors. Widely held among calibration
  facilitators; contested by people who think communication *is* the job.

### Guesses about interview practice — need a human to confirm

- **Whether `capacity_cost_estimation` deserves axis status** (B1). My own Part A data partly
  contradicts my concern. `rubric.md:342-344` already names this as the most likely place the
  rubric is wrong, and I cannot settle it. The correlation test can.
- **Whether a 60-second monologue yields any `communication_collaboration` signal at all.**
  `rubric.md:345-348` raises this and I cannot answer it. I believe bands 0–1 are worse than
  unscorable — they are actively misleading, because what they key on in a monologue is
  fluency and speech rate. That belief is a guess about what the transcripts will look like.
- **Whether register-matching is scored in real loops** or whether I am importing my own
  calibration culture's preoccupation with it. I would not act on my own answer here.
- Whether the band-1 cells read as diagnostic or as insulting. Not my competence;
  `rubric.md:352-354` asks the right two readers.

### What I had to assume because the pack does not say

- That all 12 items are administered to every candidate. If the diagnostic is shorter, some
  axes get no observation and the level mapping consumes axes that were never assessed —
  which would make B5.2 worse, not better.
- That the four per-item scores on an axis combine *somehow*. I reported the consequences of
  both mean and min because the document picks neither.
- That "a node" means 8 GPUs in A08 and 4 elsewhere. The pack uses both without defining
  either; B3.1 reports the error under both.
- That the diagnostic has no interviewer beyond the one scripted probe, so comm band 3's
  pushback requirement is reachable only when the matched probe is pushback-shaped — which,
  on 3 of 4 comm items, the at-bar branches are not.
- That my TP collective-latency figures (10–20 µs) are current. They may not be. B3.2 flags
  this as the number I most want checked.

### My own blind spots, as my persona requires

- **Bias toward structure for its own sake.** My central prescription — one required clause
  per band, indicators demoted — would make the instrument more mechanical. A rubric can be
  too mechanical to measure judgment, and a fully operable rubric may be measuring compliance
  with a format. I am the wrong reviewer to notice when that line is crossed. If a domain
  reviewer says band 2 needs to stay holistic because judgment does not decompose, weigh that
  against B5.1 rather than treating my version as the default.
- **Dated AI-infra depth.** I judged the instrument. B3.2 is the one place I reasoned from
  hardware intuition and it is the one place I would most expect to be wrong. B2's realism
  verdicts should be read as item-construction judgements, not technical ones; defer to the
  domain reviewers on whether any scenario is physically realistic.
- **n=5, one rater.** Everything in Part A is one person's reading of ten cells. The
  two-readings count below is the output I would stand behind; the specific scores are the
  input to a disagreement measurement, not findings in themselves.

---

# APPENDIX — all 24 cells, two-readings audit

Every cell, not a sample. "Two readings" means a competent grader applying the rubric as
written could defensibly land on an adjacent band; it does not mean the cell is unusable.

**16 of 24 cells admit two readings.**

| Cell | Two readings? | Why |
| --- | --- | --- |
| `requirements_scoping` 0 | **Yes** | Four unmarked clauses. "Never asked what the system must do" is unsatisfiable-as-signal in a 60-second monologue where asking is impossible, so every diagnostic answer matches a band-0 clause. |
| `requirements_scoping` 1 | No | Five anchored disjunctive clauses, mostly observable. Two are dead in the diagnostic ("only after being asked twice" — at most one probe exists), but the live ones are clear. |
| `requirements_scoping` 2 | **Yes** | Conjunction of three, including "Stated at least one thing explicitly out of scope", a hard gate that 60 seconds rarely affords. No required clause. |
| `requirements_scoping` 3 | **Yes** | Required clause is clear; inherits band 2's conjunction via "All of band 2". |
| `capacity_cost_estimation` 0 | **Yes** | "No quantity of any kind" contradicts its own cap's "no quantity of their own". Answer 1 is the live case, and 0 vs 1 here changes the public level claim. |
| `capacity_cost_estimation` 1 | No | Six well-anchored disjunctive clauses — the best-written cell in the file. Caveat: one clause names "40TB" and an all-resident index, i.e. it is written around a specific answer shape and does not evidence generality. |
| `capacity_cost_estimation` 2 | **Yes** | Conjunction of derive + ~2–3× + "Named which constraint binds". The bolded clause helps; Answers 2 and 3 split cleanly on it for me, and a grader reading the other clauses first scores Answer 2 a 2. |
| `capacity_cost_estimation` 3 | No | Required clause plus five alternative consequences, all observable. |
| `high_level_design` 0 | **Yes** | "No end-to-end path ... what happens to a single request" is a 45-minute test applied to items whose own design rule (`_meta.design_rules[0]`) asks for "exactly ONE decision plus its reason". Band 0's clause fires on almost any compliant 60-second answer, so 0 vs 1 is format-driven, not performance-driven. With "any axis at 0 ⇒ Below the senior bar", this is where the floor effect bites hardest. |
| `high_level_design` 1 | No | Clean and well anchored (brand names, reflex cache, [IIO-1] grounding). |
| `high_level_design` 2 | **Yes** | Five clauses: traceable end-to-end, each component justified, hard part in the design, read/write paths separated, where state lives. Unsatisfiable in full in 60 seconds, so scored on whichever clauses a grader weights. The most ambiguous cell in the file. |
| `high_level_design` 3 | **Yes** | Required clause clear; inherits band 2. |
| `deep_dive_failure_modes` 0 | No | Observable and unambiguous. |
| `deep_dive_failure_modes` 1 | No | The best-anchored band 1 in the file: retries with no budget, deep on the easy component, autoscaling without time-to-capacity. All real failures, all observable. |
| `deep_dive_failure_modes` 2 | **Yes** | Turns on "Picked the genuinely hard component" — and no item declares which component is hard. Prompt 1 tells the interviewer to "pick the component that is genuinely hard in THIS scenario" but no field names it, so this is author knowledge the grader does not have. Fixable: add a `hard_component` field. |
| `deep_dive_failure_modes` 3 | **Yes** | Required clause clear; inherits band 2's undeclared "hard component". |
| `tradeoff_articulation` 0 | **Yes** | "No comparative language anywhere" vs band 1's "chose but justified it unfalsifiably". Answers 2 and 3 both sit in this crack: comparative language present, no alternative ever named. Two of five blind answers landed here. |
| `tradeoff_articulation` 1 | No | Four anchored clauses, including the clearest-written clause in the file ("Listed pros and cons of two options and did not choose"). |
| `tradeoff_articulation` 2 | **Yes** | "Named the axis of the trade-off in units" is bolded and right, but the cell's own examples ("latency vs throughput") are not in units. The cell contradicts its examples, so the hard cap it feeds will be applied loosely. |
| `tradeoff_articulation` 3 | No | Strictest and clearest band 3 in the file. Note it is unreachable on items where 60 seconds affords no derivation, and this axis is gated at every level of the mapping. |
| `communication_collaboration` 0 | **Yes** | "Near-silence requiring the interviewer to extract every step" — no interviewer exists in the diagnostic, and the clause is nonetheless scoreable from the timestamps the grader gets. Penalises deliberation. |
| `communication_collaboration` 1 | **Yes** | Mixed register. "Talked continuously without signposting" is observable. "Repeated the original answer louder" is an audio property the grader never receives — it gets text plus timestamps. "Did not adjust when it clearly failed to land" is a listener-reaction inference, and the diagnostic's scripted probe never signals failure to land. |
| `communication_collaboration` 2 | **Yes** | Conjunction of five, one of which ("Matched register to the audience named in the prompt") is the bias vector. |
| `communication_collaboration` 3 | **Yes** | Requires pushback to have changed something. On 3 of 4 comm items the at-bar probes introduce a new constraint rather than pushing back on the candidate's position, so band 3 is partly unreachable — while "At the staff bar" requires ≥2 axes at 3. |

**The pattern matters more than the count.** Band 1: 1 of 6 ambiguous. Band 2: **6 of 6**.
Band 3: 4 of 6, all four by inheriting band 2. Band 0: 4 of 6. The author's stated worry
(`rubric.md:38`: "Band 1 is the dangerous band to write loosely") is the one worry fully
discharged. Band 2 — the band every row of the level mapping depends on — is where the
looseness went.

---

# ANSWERS TO THE FOUR QUESTIONS I WAS ASKED DIRECTLY

**(a) Which cells admit two readings.** 16 of 24, all enumerated above, concentrated in band
2 (6/6) and band 0 (4/6). Band 1 is near-clean.

**(b) Did the band-3 change make it operable or mushy?** Operable — and it moved the problem
rather than solving it. Band 3's required clause is now the most testable thing in the file
and I applied it to ten cells with one dispute. But every band 3 still opens "All of band 2",
so the conjunction the fix removed from band 3 now sits one row down, unmarked, in the band
the level mapping actually consumes. The bars are inverted: one clause at the top, five in
the middle. It creates a band-3-without-band-2 case (Answer 4 is nearly one) that the rubric
cannot score. The author diagnosed the right disease and treated one symptom; the same edit
applied to band 2, plus dropping "All of band 2", finishes it. I would not revert the change.

**(c) Are the level-mapping thresholds safe to ship?** No — and not primarily because they
are uncalibrated. The function is undefined (no aggregation rule from 4 per-item scores to
the 1 axis score the mapping reads), so under one reading its harshest rule never fires and
under another it always does. It also leans entirely on band 2, the softest band, and its one
cliff sits on the 0/1 boundary, where 4 of 6 cells admit two readings. Ship the band plus the
named blind spot — the claim `calibration-plan.md:167-169` already proposes for the pre-n=200
reveal and the one the evidence supports. Hold the staff/senior language until the
aggregation rule is written and the 0/1 boundary has been double-scored.

**(d) Does `communication_collaboration` score observable behaviour or polish, and would it
penalise a strong non-native speaker or someone who thinks before speaking?** It scores both,
and the balance tips to polish on 3 of its 4 items. **Yes to both groups, through four
identifiable mechanisms:**

1. **"Matched register to the audience named in the prompt"** (band 2) is a sociolinguistic
   skill strongly correlated with native fluency and familiarity with American corporate
   idiom. `annotation-throughput-vs-agreement` is close to a pure test of it — "they are not
   an ML person", "in the VP's units", 30 seconds.
2. **"Did not adjust when it clearly failed to land"** (band 1) and the `good` field's "loses
   the room" are inferences about listener reaction, not behaviours. They are also the two
   phrases a grader will reach for when an answer is correct but reads as foreign.
3. **"Near-silence"** (band 0) is scoreable from the per-utterance timestamps Prompt 3
   receives, with no instruction excluding pre-speech thinking time. A candidate who thinks
   for twelve seconds and then delivers forty seconds of dense, well-structured answer has
   been silent for a fifth of the window. The rubric cites [IIO-1] that long silences count
   against senior candidates — but that is about a 45-minute interactive session, where
   silence is a failure to collaborate. In a 60-second monologue, silence is thinking, and
   there is nothing to collaborate with. `calibration-plan.md:157`'s words-spoken metric
   compounds it, since L2 speech is slower and the budget is fixed.
4. **Construct narrowness.** Three of four comm items are "disagree with a more senior
   person" scenarios. That conflates assertiveness in a particular corporate register with
   communication skill, and it is the sub-skill most culturally variable.

The axis is salvageable, and `rubric.md:271-275` is right that it is the most valuable thing
here. Four fixes, cheapest first:

- **State in Prompt 3** — not only in the rubric — that grammatical error, accent-driven
  transcription artefacts, disfluency, filler and speech rate are **not** scored on any axis.
  This is currently nowhere, and it is one sentence.
- **Delete "near-silence" from the diagnostic**, or re-specify it as response latency
  measured from the end of the probe with an explicit thinking-time allowance.
- **Replace "clearly failed to land"** with something observable: "did not restate the point
  in different terms after the listener's reply showed the first framing had not been taken
  up". That is in the transcript. "Loses the room" is not.
- **Replace "matched register"** with a content test a non-native speaker can satisfy:
  "stated the consequence at least once in the listener's decision terms — money, time, or
  risk — rather than only in system terms". That is the real skill the annotation item is
  reaching for, and it survives an accent.

Then add one comm item that is pure structure — explain your own design to a peer, no social
conflict — so the axis is not measured entirely through disagreement scenarios.
