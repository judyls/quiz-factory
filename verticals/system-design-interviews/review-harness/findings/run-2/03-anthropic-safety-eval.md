# REVIEWER 3 — inline safety and evaluation infrastructure — RUN 2

**Persona:** `review-harness/personas/03-anthropic-safety-eval.md`.
**Owned:** `inline-safety-classifier-budget`, `eval-infra-per-commit-cost`,
`annotation-throughput-vs-agreement`, and the judge design in `prompts.md`.
**Badge is shorthand for the problem domain, not a claim about any employer's practice.
Nothing below describes any named company's actual interview process.**

## Contamination disclosure — read first

To create my own output directory I ran `mkdir -p` + `ls` on
`review-harness/findings/run-2/`. The listing returned one filename:
`00-ANSWER-KEY.md`. **I did not open it.** I ran that command *after* Part A was complete
and fixed in my own reasoning, so no cell is affected. I am disclosing the filename
sighting because the protocol asks for disclosure, not repair, and because the existence of
an answer key inside `findings/run-<N>/` — the directory every reviewer must `mkdir` into —
is itself a harness defect (see B5.4): the off-limits list names `findings/` wholesale, but
every reviewer is *required* to write into it, so every reviewer will see that filename.
Move the key out of the directory reviewers write to.

Files opened: the three required, then `rubric.md`, `questions.json`, `prompts.md`.
Not opened: `calibration-plants.json`, `dry-run-report.md`, `calibration-plan.md`,
anything under `findings/`.

---

# PART A — Blind scoring

Seven answers, two axes each. (The set says 7; `review-protocol.md` says 5 — see B5.4.)

---

### Answer `D4` — heterogeneous routing under a cost ceiling

**D4 / capacity_cost_estimation: 3**
  cell clause applied: "All of band 2, unprompted, **and the result changed the design**:
  the number ... revealed that the stated SLO is unachievable at the stated budget — and
  they said so."
  evidence: "the 5 percent on the 400B contributes 0.285 of baseline while the whole 70
  percent on the 8B contributes 0.07, so the big model's sliver costs four times what the
  small model saves. To get under the ceiling I need the 400B share below about 4 percent.
  That is the number I would hold the routing policy to."
  admits another reading: **yes — band 2.** Arithmetic verified: 0.7(0.1)+0.25+0.05(5.7) =
  0.605, ×$2.60 = $1.573, over the $1.50 ceiling; my own re-derivation of his threshold
  (holding the 8B at 70% and moving 400B traffic to the 70B) gives 0.37+4.7x ≤ 0.5769,
  x ≤ 4.4%, so "below about 4 percent" is correct and conservative. The 2-reading is
  available because what changed is a *policy threshold*, not an architecture: nothing in
  the answer is a component. A grader reading "changed the design" as "changed the box
  diagram" scores 2. I score 3 because the cell's own enumerated examples include "forced an
  admission-control policy", and a routing-share ceiling is that.

**D4 / high_level_design: 1**
  cell clause applied: "A box diagram that does not satisfy the requirements already stated
  — ... or ignores a constraint from the prompt."
  evidence: "At 70 percent on the 8B, 25 on the 70B and 5 on the 400B, the blend is 0.7
  times 0.1, plus 0.25, plus 0.05 times 5.7"
  admits another reading: **yes — band 0, and this is the most important flag in my Part A.**
  Band 0's first clause ("No end-to-end path") is *literally satisfied*: there is no router,
  no classifier, no confidence scorer, no fallback, no measurement component, and the
  prompt's second question — "what do you measure to know you have not quietly made the
  product worse?" — is never touched. Meanwhile **not one of band 1's clauses fits**: every
  band-1 clause presupposes a design exists ("a box diagram that...", "components named by
  brand", "added a cache ... by reflex"). I score 1 only because the scoring contract gates
  band 0 on "and nothing in the answer depended on it", and the entire answer depends on a
  three-tier routing structure. So the band table says 0 and the scoring contract says 1.
  The rubric's own hard-cap row — "Band 0 vs 1 must be distinguishable from the transcript |
  If the grader can't tell, the cell is badly written" — is the row this cell fails. See
  B5.2; I hit this same 0-vs-1 fork twice more below.

---

### Answer `F3` — 4PB corpus, dedup / shuffle / reproducibility

**F3 / high_level_design: 3**
  cell clause applied: "All of band 2, **and the design visibly follows from the numbers or
  the requirement cut** rather than from a template — the component boundary is where it is
  *because* of a quantity they computed."
  evidence: "A true global shuffle of 4 petabytes means writing 4 petabytes — at even 100
  gigabytes a second of sustained I/O that is on the order of 11 hours, so it is not
  something you do every epoch. I would shuffle once into shards at ingest and do cheap
  in-shard shuffling plus shard-order randomisation per epoch"
  admits another reading: **yes — band 2.** Arithmetic verified: 4e15 B / 1e11 B/s = 4e4 s =
  11.1 h. The boundary between one-time global shuffle and per-epoch cheap shuffle sits
  exactly where the 11-hour figure puts it, which is the required clause verbatim. The
  2-reading: the prompt states "2,000 GPUs will read it during training" and he never sizes
  the training read path at all — no read bandwidth, no shard-count-vs-reader-count, no
  prefetch. A grader who requires every stated requirement to have a component tied to it
  (band 2's "each component existing for a reason tied to a stated requirement") can hold
  this at 2 on a missing-requirement basis.

**F3 / deep_dive_failure_modes: 3**
  cell clause applied: "All of band 2, unprompted, **and a failure mode they found changed
  the design**."
  evidence: "which is where the trust problem probably comes from: nobody has measured the
  resulting distribution. I would add a verification job that samples it."
  admits another reading: **yes — band 2, and it exposes a wording gap.** Band 3's three
  enumerated examples are all failure modes of *the candidate's own* design ("admission
  control added because the queue is unbounded", "an idempotency key added because the retry
  path double-charges"). F3's failure modes are all diagnoses of the *existing* system —
  which is precisely what the prompt asked for ("what breaks first"). **The cell never says
  whose design.** On this item the prompt makes diagnosing the incumbent the band-2
  behaviour, so a strict reading leaves no route above 2. I score 3 because adding the
  verification sampler and content-addressing the shards are both design changes caused by
  found failure modes. What is genuinely missing and would have settled it: nothing about
  partial failure during the training read — a node dies mid-epoch and resumption must stay
  bit-exact, which is band 2's own indicator ("said what happens to in-flight work when a
  node dies") and is the hardest part of the stated reproducibility requirement.

---

### Answer `J2` — vector index at 10B (IVF-PQ)

**J2 / capacity_cost_estimation: 2**
  cell clause applied: "**Required:** named which constraint binds — memory capacity vs
  memory bandwidth vs compute vs network vs dollars — and supported it with a quantity they
  derived, arithmetic within ~2–3×."
  evidence: "10 billion vectors at 1,024 dimensions in float32 is 4 kilobytes each, so about
  40 terabytes raw, which makes memory the binding constraint here."
  admits another reading: **no.** Not 3, and the reason is the rubric's own anti-pattern,
  cleanly triggered: he states the decision *before* the number. "I'd go with IVF-PQ — it's
  what most billion-scale deployments run. On sizing: ..." The number could not have changed
  a decision already made. Arithmetic verified (1024×4 = 4096 B; ×1e10 = 41 TB; 200M/10B =
  2%). Not 1 either — band 1's targeted clause ("chose an index that needs all of it
  resident") does not fire, because PQ compression is the whole point of his choice. The real
  gap, which the cell does not reach: he never sizes the *compressed* index, so "memory is
  the binding constraint" is asserted and then never resolved numerically — at e.g. 128 B/
  vector PQ that is ~1.3 TB, and that number is the one his design actually rests on.

**J2 / tradeoff_articulation: 1**
  cell clause applied: "Or chose, but justified it with an unfalsifiable claim ('it's more
  scalable', 'it's industry standard', 'it's more flexible')."
  evidence: "I'd go with IVF-PQ — it's what most billion-scale deployments run."
  admits another reading: **no.** This is the cleanest cell in the set and the hard cap
  independently pins it: no trade-off axis is named anywhere. The prompt says "tell me what
  the choice costs you" and the entire answer on cost is "keep an eye on recall", which
  names no axis and quantifies nothing. Both routes to ≤1 agree.

---

### Answer `H4` — agent fan-out with side effects

**H4 / deep_dive_failure_modes: 2**
  cell clause applied: "**Required:** picked the genuinely hard component and named a
  concrete failure mode of *this* design — not of distributed systems in general — with its
  mitigation."
  evidence: "The actual bug is that retrying the whole turn re-executes side effects, so we
  are duplicating emails and double-charging. I would put an idempotency key on each logical
  operation, generated once per turn."
  admits another reading: **yes — band 3, and this is the hardest cell in the set (see the
  end of Part A).** His first turn is band-3 material almost verbatim against the cell's own
  example ("an idempotency key added because the retry path double-charges"), unprompted, and
  the 21% figure is correct (1 − 0.98¹² = 21.5%) and load-bearing — it establishes that this
  is the normal path. Then the interviewer pushes and he abandons it: "Yeah, you know what,
  that is probably fine actually. ... Let's go with that." Tool-layer retries without
  idempotency do not fix duplicate side effects, so **the transcript ends with the design not
  changed.** I score 2 because band 3's required clause is that a failure mode *changed the
  design*, and by the final turn it did not — he reverted to the broken shape. A grader who
  treats the retraction as purely a communication event, scoreable on the other axis of this
  item, scores 3. **No cell on any of the six axes says what to do when a band-3 behaviour is
  performed and then retracted under pushback.** That is the single most valuable thing I
  found in Part A, because this item exists to produce exactly that transcript and the rubric
  has no rule for it. Expect reviewer disagreement here to be 2-vs-3 and to be the rubric's
  fault, not the reviewers'.

**H4 / communication_collaboration: 1**
  cell clause applied: "Collapsed at the first push — abandoned a correct design because it
  was questioned, with no attempt to defend it."
  evidence: "Yeah, you know what, that is probably fine actually. If the retries live at the
  tool layer then each tool handles its own failure, which is cleaner separation anyway.
  Let's go with that."
  admits another reading: **yes — band 2, through a wording loophole that should be closed.**
  Band 2's required clause reads "...either conceding and saying what changes or holding the
  position with a reason rather than with volume." He *did* concede and he *did* say what
  changes. Read literally, the required clause for band 2 is satisfied by a total collapse,
  while band 1's clause describes the same utterance as below bar. I score 1 — the intent is
  unmistakable and `prompts.md` line 264 states it correctly ("Abandoning a correct position
  with no defence ... below bar") — but the rubric cell itself does not say that, and a
  grader reading only the cell can land on 2. Fix is one clause: band 2's concession route
  must require a reason *why the objection is right*, not merely a statement of what changes.

---

### Answer `P7` — 70B, 95/5 short/long context

**P7 / requirements_scoping: 3**
  cell clause applied: "All of band 2, **and cut scope in a way that visibly changed the
  design** ... and said what the cut bought ... Asked the one question whose answer would
  most change the architecture, rather than a list of safe clarifications."
  evidence: "What I'm protecting is the short traffic: say a 400 millisecond p99
  time-to-first-token for the 95 percent, and the long-context 5 percent held to its own,
  worse target rather than blended into one p99. ... Out of scope: tuning the eviction
  policy."
  admits another reading: **no, though one band-2 indicator is genuinely absent.** He does
  two band-3 things: de-blends the p99 (relaxing the long-context target so the short one
  closes — a requirement relaxation with its payoff stated) and rules eviction tuning out of
  scope with a numeric reason. "KV bytes per token" is exactly the one-question-that-most-
  changes-the-architecture clause. The absent indicator: "asked rather than assumed" — he
  asserts the 400 ms rather than eliciting it, and supplies 80 layers / 8 KV heads / head_dim
  128 himself without flagging them as assumptions. Indicators do not block a 3 under the
  rubric's own stated structure, so this stays a 3; I note it because a grader who treats the
  indicators as a conjunction would score 2, and that is the failure mode the rubric's
  band-2/band-3 "Required vs Indicators" split was introduced to prevent.

**P7 / capacity_cost_estimation: 3**
  cell clause applied: "All of band 2, unprompted, **and the result changed the design**: the
  number ruled out an architecture ... forced an admission-control policy."
  evidence: "that's about 320 kilobytes a token, so a 100,000-token request is around 32
  gigabytes — on cards that are mostly holding weights already. ... No policy frees 32
  gigabytes; this is about admitting long requests against a reserved share of memory."
  admits another reading: **no.** Arithmetic verified exactly against the KV formula:
  2 × 80 × 8 × 128 × 2 B = 327,680 B = 320 KiB/token; × 1e5 = 32.8 GB. The number rules out
  an architecture (eviction-policy tuning) *by name* and forces admission control, with the
  consequence stated in the same breath. Cleanest 3 in the set.

---

### Answer `N7` — vector index at 10B (HNSW)

**N7 / capacity_cost_estimation: 1**
  cell clause applied: "Derived the number that decides the question, then proposed a design
  it rules out (computed 40TB raw, then chose an index that needs all of it resident) — the
  number was produced but not understood."
  evidence: "10 billion vectors at 1,024 dimensions in float32 is 4 kilobytes per vector, so
  about 40 terabytes raw. ... Given the recall requirement I would use HNSW"
  admits another reading: **no.** Doubly supported, which is why I rate this the best-written
  cell in the rubric. The band-1 clause matches almost word for word; and band 2's required
  clause independently fails, because he never names a binding constraint at all — the cell
  says outright that "a correct number with no statement of what it binds is also band 1."
  For the record, HNSW here is worse than the cell implies: M=32 adds roughly 128–256 B/vector
  of graph links, so ~1.3–2.6 TB *on top of* the 40 TB that must stay resident.

**N7 / tradeoff_articulation: 2**
  cell clause applied: "**Required:** named the axis of the trade-off in units — latency vs
  throughput, cost vs tail latency, recall vs p99 ... — **and picked a side.**"
  evidence: "because it has the best recall-latency curve of the ANN families — typically
  0.95-plus recall at single-digit millisecond latency"
  admits another reading: **yes — band 1, and the reason is an asymmetry between two axes'
  band-2 cells that I would fix before shipping.** He names recall-vs-latency in units and
  picks HNSW, so the required clause is literally met and the hard cap does not fire. But
  recall-vs-latency is the axis HNSW *wins* on; the axes it loses on — memory
  (40 TB+ resident) and incremental-update cost (200M inserts/day into a proximity graph,
  which is the stated 2% churn and is brutal for HNSW) — are never named, and the prompt
  explicitly asked "what the choice costs you". **`capacity_cost_estimation` band 2 requires
  the constraint named to be the one that *binds*; `tradeoff_articulation` band 2 does not
  require the axis named to be the one that *decides*.** A grader who imports the stricter
  reading scores 1. I score 2 by the cell as written, per the protocol's instruction to apply
  the rubric as written. This is a 1-vs-2 disagreement I expect to see across reviewers.

---

### Answer `W7` — eval infra per commit

**W7 / requirements_scoping: 1**
  cell clause applied: "Listed eight requirements and prioritised none." (also: "recited a
  generic checklist unconnected to this scenario")
  evidence: "There is also cold start on the replicas which I have not accounted for, and
  sharding overhead. Storage for the results is negligible. Network egress depends on where
  the judge runs."
  admits another reading: **yes — band 0.** Band 0's distinguishing clause is "Treated an
  underspecified prompt as a specification", and that is precisely and completely what he
  did: he consumed 50,000 / 10 minutes / 40 commits as given, costed them, and never once
  asked whether any of them should hold. No requirement is prioritised, none is cut, none is
  challenged, and the prompt's explicit second half is dropped. I score 1 because the
  requirements behaviour did *appear* — he restated them numerically and enumerated what he
  had not accounted for, which is engagement, badly — and the scoring contract reserves 0 for
  "the behaviour never appeared". **This is my third 0-vs-1 fork in seven answers** (D4,
  F3-adjacent, W7). The 0/1 boundary, not the 2/3 boundary, is where this instrument is
  loosest. See B4.

**W7 / communication_collaboration: 1**
  cell clause applied: "Answered a different, easier question than the one asked and did not
  acknowledge the substitution."
  evidence: "Okay so 50,000 times 2,000 is 100 million tokens." (and the answer ends at
  "Network egress depends on where the judge runs" — no pushback anywhere)
  admits another reading: **yes — band 2, weakly.** The prompt is two-part: "Tell me what
  that costs, **and tell me what you would push back on.**" He answers part one competently
  and silently drops part two; he also ignores the named audience ("I am a research
  engineer") and never names the decision the gate is meant to make. A grader scoring
  structure and numeracy rather than completeness lands on 2. I score 1: half of a two-part
  question is not "answered the question that was actually asked". **Cell defect worth
  fixing:** band 2's required clause handles pushback flowing *interviewer → candidate*
  ("where the prompt contained pushback, engaged that specific objection"). This item, and
  `inline-safety-classifier-budget`, are *candidate → interviewer* pushback items — the
  prompt asks the candidate to push back. The cell has no clause for "the prompt asked for
  pushback and none came", so the item's primary discriminator is scoreable only by analogy.
  Arithmetic note: his chain is internally exact (166,667 tok/s; 27.8→28 replicas; 112 GPUs;
  18.67 GPU-h; $37.33; $1,493/day; ×365 = $544,580). It is exact and it is built on a
  throughput figure the pack's own Appendix B says is wrong — see B3.1.

---

## Hardest cell to apply, and why

**`H4` / `deep_dive_failure_modes`.** Not because the bands are vague — they are unusually
sharp here — but because the rubric is **silent on retraction**. The candidate performs the
band-3 behaviour, precisely, unprompted, with correct supporting arithmetic, and matching the
cell's own worked example. He then gives it away under a one-line push and ends the session
with the defective design. Band 3 requires that a failure mode "changed the design"; the
design finished unchanged. Band 2 requires that he "named a concrete failure mode of *this*
design with its mitigation"; he did, beautifully, and then withdrew the mitigation.

Both bands have a complete and honest claim on this transcript and the rubric gives no
ordering rule. Worse, the choice is not neutral: scoring 3 means the scorecard reports
above-bar depth for a candidate who surrendered the correct answer to the first objection —
the exact failure this item was built to detect. Scoring 2 means a grader can be accused of
double-counting one utterance across both axes of the item.

The fix I would make is a single global clause in the scoring contract, not six cell edits:
*a behaviour that the candidate retracts without a reason does not satisfy any band-3
required clause on any axis; it is capped at band 2 on the content axis and scored on its
merits on `communication_collaboration`.* That makes the item deterministic and keeps the
collapse scored once, in the axis built for it.

---

# PART B — Critique from inline safety and evaluation infrastructure

## B1. Axis legitimacy

**Yes, with one structural objection that is checkable rather than a matter of taste.**

The six axes do correspond to what this round attends to, in the sense that I cannot name a
seventh thing I listen for that is not distributed across these six, and I cannot name one of
the six that I would not listen for. The band definitions are observable, which is rarer than
it sounds — "names the axis of the trade-off in units and picks a side" is a thing you can
check from a transcript; most rubrics I have been handed say "demonstrates strong judgement".

**What my answer rests on:** I have interviewed in this category and I have built the eval
system on the other side of the glass, but **I have never owned a hiring rubric, and my
instinct for what a loop actually scores is materially weaker than my instinct for the
systems.** Weight this finding accordingly — it is the single place my persona brief tells me
I am likely wrong and I think the brief is right. **What would change my mind:** twenty real
scored sessions where two interviewers' free-text notes are coded against these six axes. If
the notes cluster into four, this is a six-mark scorecard pretending to be a measurement.

**The structural objection, which is not a matter of taste:**

**B1a — `capacity_cost_estimation` and `tradeoff_articulation` have the same band-3 event.**
Capacity band 3: "the result changed the design: the number ruled out an architecture...".
Tradeoff band 3: "the trade-off was resolved against a number they produced". *These are one
observable event described from two sides.* On any answer that reaches band 3, the two axes
are near-perfectly correlated by construction, so the composite double-weights numeracy and
the "profile shape" the level claim reads is one dimension short of what it appears to be.
`rubric.md` line 400 already flags "whether `capacity_cost_estimation` deserves axis status"
as the most likely error; I agree, and I can give the mechanism, which changes the fix. The
answer is **not** to delete the axis. It is to make capacity's band 3 about **sensitivity**
instead of about the decision changing: *stated which assumption the answer is most sensitive
to, and what that number would have to be for the decision to flip.* That is a genuinely
different behaviour, it is the one I actually interview for, it is already sitting in
capacity's band-3 indicator list, and `P7` and `D4` both demonstrate it, so the fix is
reachable. Note that it is also the band-2/3 discriminator on `rubric.md` line 490's own
story about the KV term.

**B1b — two axes are computed from 75% the same items.** From `_meta.axis_coverage`:
`requirements_scoping` = {kv-cache, inline-safety, eval-infra, annotation} and
`communication_collaboration` = {inline-safety, eval-infra, annotation, agent-retry}. **Three
of four items are shared.** The other two axis pairs share 2 of 4. Those two axis scores are
means over 75% identical transcripts, so they will correlate strongly for reasons of item
assignment rather than candidate behaviour — and the level mapping's "≥4 axes ≥ 1.75" and
"≥5 axes ≥ 1.75" rules read that correlated profile as if it were six independent reads. This
is arithmetic off the file, not judgement. The cause is visible and fixable: all three shared
items are the "talk to a human" items, and they were assigned both of the human-facing axes.
Re-assign so no pair shares more than 2 of 4, or state the correlation next to the level
table so nobody reads profile shape as six independent signals.

## B2. Scenario realism — my three

### `inline-safety-classifier-budget` — realistic-but-wrong-in-one-detail

First, the question I was told to answer hardest: **the tech lead's proposal is not a straw
man.** "Run it async alongside generation and kill the stream at the first unsafe token" is a
real proposal, made by competent people, and it has a real merit the item correctly credits in
`good` ("killing the stream is a genuine mitigation"). It also beats the alternative on one
axis nothing else in the item covers: output-side classification catches unsafe completions
from benign prompts, which prompt-side classification structurally cannot. This is the
best-constructed pushback item I have read in a prep pack, and the `at_bar_1` probe — "The
classifier is down. Do you serve or refuse, **and who decides?**" — is the right question
with the right second half. Someone who has done this work wrote it.

**The single thing most wrong: the prompt never says what the classifier classifies** — the
prompt, the output, or both — and the entire model answer turns on it being prompt-side. The
model answer's "third option" is "classifying the prompt during prefill ... so most of the 40
milliseconds overlaps and costs almost nothing". That is not a third option that dominates the
tech lead's proposal; it is a **coverage reduction** that drops exactly the case the tech
lead's design exists to handle, and the model answer presents it as a resolution. The item
knows this — `at_bar_2` asks "the output turns unsafe at token 500. What did your design
buy?" — but `model_answer` is what the grader generates `contrast` against
(`prompts.md` line 272), so the judge is taught that substituting prompt classification for
output classification is the at-bar move. Fix: state in the prompt that the classifier scores
prompt *and* streamed output, and make the model answer's third option explicitly a partial
mitigation with its gap named.

Two further things I would change, both from inside this problem:

- **The model answer commits, at the design step, the exact error it corrects at the
  arithmetic step.** Its first half is a correct and well-put refusal to reason about the tail
  from the median. Its second half then argues the overlap using **40 ms, the p50**. Argue it
  at the tail and it fails: by the pack's own Appendix B numbers (1.6 PFLOPS achieved), a
  2,000-token prefill is 2 × 70e9 × 2000 = 0.28 PFLOP ÷ 1.6 PFLOPS ≈ **175 ms** — so the
  classifier's own 180 ms p99 does not fit inside prefill, it consumes all of it. The overlap
  argument holds at p50 and collapses at p99, which is the item's whole lesson. This is the
  most teachable defect in the pack because the file contains the numbers that refute itself.
- **"Async as a mitigation" is only half-named, and the other half is where it bites.** Even
  for prompt-side classification, "overlaps and costs almost nothing" is a *utilisation*
  claim, not a latency claim. On a fleet at high utilisation the classifier competes for the
  same GPUs; overlapping does not make the work free, it makes it invisible in the latency
  budget while reducing serving throughput. The model answer never says where the classifier
  runs. I would add that to `good`: *said where the classifier executes and what it displaces*.
- **Secondary, and a missed branch:** a 4.5× p99/p50 spread (40 → 180 ms) on a small
  in-path classifier reads like **queueing behind the main model**, not classifier compute. If
  that is the shape, the fix is priority/admission, not overlap, and the "composition" framing
  is beside the point. A candidate who says this is doing the strongest thing available in the
  item and there is no `followups` branch for it.

**Scoring-coverage defect in this item, and it is serious:** its assigned axes are
`requirements_scoping` and `communication_collaboration`, but `bad` makes the central failure
an **arithmetic** one ("adding the two p99s to get 490 and presenting that as the combined
tail") and `good` makes handling that arithmetic a requirement. `capacity_cost_estimation` is
not scored on this item. So the pack's most carefully designed failure mode lands on no cell
that would catch it — no band-1 clause on either assigned axis describes a p99 composition
error. Either add `capacity_cost_estimation` to this item's axes or move the arithmetic trap
to an item that scores it.

Last, a direction the item does not cover and should: `good` says "Escalates the fail-open
versus fail-closed call rather than deciding it", and the fail-open/fail-closed question is
the **single most binding unstated requirement in this scenario**. It appears only in an
`at_bar_1` probe. As written, a candidate who never asks what happens when the classifier is
down can reach band 3 on `requirements_scoping` here. In my domain that is the requirement;
it should be in `good` as a named beat, not held behind a probe that only fires if the
candidate is already at bar.

### `eval-infra-per-commit-cost` — realistic

The requirement shape is exactly how this request arrives, down to the register: a research
engineer naming a number, a latency, and a gate, in one sentence, with the expensive clause
hidden in the middle. The flake-rate beat in `good` — "a flake-prone gate blocking 40 merges
a day is worse than no gate" — is the best line in the pack and is the thing I would most
want a candidate to say.

**The single thing most wrong: the headline cost assumes perfect elasticity and never says
so.** "Roughly 37 dollars a commit, so 1,500 dollars a day — about half a million a year"
prices 112 H100s for exactly ten minutes, i.e. acquiring and releasing 112 H100s forty times
a day in under a minute. That is not a procurement that exists. Duty cycle is 40 × 10 = 400
minutes of 1,440, so **28%**; a reserved fleet is 112 × 8,760 h × $2 = **$1.96M/yr**, which
is **3.6× the stated figure**. The honest answer is a range with the assumption named
($544k shared-and-elastic → $1.96M reserved), and which end you are at *is the design
question* — it is what decides between a dedicated gate fleet, borrowing idle training
capacity, and queueing. Appendix B's own rule ("Model answers that quote a cost figure state
the $/GPU-hour assumption out loud") is satisfied while the larger term goes unstated.

**Is the reference answer's pushback the pushback I would make? Mostly, and it is missing the
one I would make first.** Everything in `good` is right. But the item treats flake as a cost
and an annoyance, and at this scale it is a statement about the gate's **decision rule**: at
50,000 evaluations, the probability a commit trips at least one flaky eval is 1 − (1−ε)^50000,
which is ~39% at ε = 1e-5 and ~99.3% at ε = 1e-4. So "50,000 graded evals must pass" is not
expensive, it is **impossible** — the gate can only work if its verdict is an aggregate (a
score threshold, or a regression test against the previous commit's distribution) rather than
all-pass. Nothing in the prompt, `good`, or `model_answer` distinguishes "50,000 evaluations"
from "a merge decision computed from 50,000 evaluations", and that distinction is the whole
design. That is the third option this item should be reaching for and it is absent. I would
add it to `good` as a named beat and add a `followups` branch: *"Suppose 40 of the 50,000 are
flaky. Does the gate block? What is the rule?"*

Minor: the judge call is deferred as "plus the judge calls" and never costed, but it is ~100M
input tokens per commit of prefill. Prefill is cheap per token, so it is perhaps 10–20% more
GPUs — but it is the variable the researcher actually controls (judge model size), so leaving
it uncosted leaves the cheapest lever off the table. `terms` lists "merge queue" and nothing
in the item engages it, even though at 40 commits/day with a 10-minute gate the queue is the
binding constraint on wall-clock, not the GPUs.

### `annotation-throughput-vs-agreement` — realistic-but-wrong-in-one-detail

The framing is right and I would not change it: 30 seconds, a VP, not an ML person, and a
question with a correct premise. The item's refusal to let the candidate win by denying the
premise — `good`: "does NOT claim that agreement work beats volume on effective sample size
... a candidate who denies that is wrong" — is good rubric design and rare.

**The single thing most wrong: the `bad` field declares a defensible position wrong, and it is
the position I would take.** `bad` says the "substantive failure ... that sounds sophisticated"
is "arguing that raising agreement is worth MORE than doubling volume. It is not, on effective
sample size — lifting kappa from 0.62 to 0.80 buys about 1.3x while doubling the pool buys 2x.
A candidate who makes the stronger claim is both wrong and checkable."

The 1.3× is arithmetically fine and I verified it (B3.4). But it holds **only under an
independent-symmetric-noise model**, where disagreement is random and averages out, so
n_eff ∝ kappa. Preference-annotation disagreement is substantially **systematic** — annotators
differ in how they read the guideline, not coin-flip-wise — and systematic disagreement does
not average out with volume; it biases the reward signal, and doubling the pool buys 2× of a
biased signal plus 120 new readings of the same ambiguous guideline. Under that model, raising
agreement genuinely can be worth more than doubling volume, and at kappa 0.62 on a preference
task systematic disagreement is the more likely story. **So the pack marks a candidate wrong
for making the argument that is correct under the more realistic noise model — and does it in
the one place it is willing to say flatly that the candidate is wrong and checkable.** That
asymmetry is what makes this a defect rather than a quibble. Fix: keep the premise-conceding
beat (it is right, and the sequencing argument in `model_answer` is excellent and survives
intact), but rewrite `bad` so the failure is *asserting the stronger claim without naming the
noise model it depends on*, not holding the position. A candidate who says "if the
disagreement is systematic rather than random, volume does not fix it, and at kappa 0.62 I
would bet it is systematic — here is how I would check" is above bar, and today's `bad` marks
them down.

Second item-level defect: **the prompt says "about 30 seconds" while `_meta.answer_budget_
seconds` is 60**, and its own `model_answer` is 161 words ≈ 64–74 s spoken. The model answer
is 2–2.5× the time the prompt allots. See B3.5 — this is systematic across all twelve.

Throughput sanity check, which is fine: 200,000 ÷ 120 annotators ÷ ~21 working days ≈ 79
comparisons/annotator/day ≈ 6 min each. Plausible; not a defect.

### The judge design in `prompts.md` — what I was asked to assess

**`contrast provenance` via trigram overlap: security theatre, and the pack already knows it.**
`prompts.md` §"Two things the first version of this table could not do", item 2, independently
reaches my conclusion and gives the right three reasons (structurally rigged to pass because
the contrast is generated *from* `model_answer`; blind to conclusion-copying; false-fires on
strong candidates). I confirm all three. So the answer to my brief's question is: yes it was
theatre, and it has already been removed. **The replacement is better and still does not test
the thing that paragraph says it was supposed to protect.** Two holes:

1. **It is still a wording check.** The replacement row rejects "a verbatim span of 8+ words
   from the candidate's transcript". The diagnosis one page later says the failure that
   matters is "copying the candidate's *conclusions* rather than their wording". An LLM
   generating the contrast paraphrases by default, so an 8-word span check is trivially
   cleared by a contrast that is wholly derived from the candidate's conclusions. The check
   and its own stated purpose are in direct contradiction.
2. **The other half of the row cannot be code.** "reject if `contrast.at_bar_answer` does not
   cover at least one beat from `<reference>.good` that the candidate missed" requires
   semantic coverage judgement, and **`good` is free prose** — there is no enumerated beat
   list anywhere in `questions.json`. `prompts.md` line 44 references `scenario.required_beats`,
   but that field belongs to the 40-scenario bank, which §"Three defects" item 1 says does not
   exist. So on Layer 1, the only layer that currently runs, this row is either unimplementable
   or implemented by a second model call — which puts a model back inside the mechanism whose
   entire justification is "**Code-enforced validation — NOT prompt instructions**" and "A cap
   that lives only in the prompt is not a cap". Also "at least **one** beat" is a very low bar
   against `good` fields carrying five to seven beats.

**The fix I would make, and it is cheaper than the check:** get provenance **by construction**
instead of by post-hoc string matching. Generate `contrast` in a **separate call that is given
`model_answer` and the list of missed beats and never sees the transcript.** It then cannot
copy the candidate, no check is needed, and the failure mode is eliminated rather than
detected. With twelve items and a finite beat set, you can precompute every (item, missed-beat
subset) contrast offline and have the grader *select* one — removing generation from the hot
path entirely, which also removes it from the flake budget. This requires enumerating `good`
into a `required_beats` array per item, which the row needs anyway.

**Is the validation table sufficient? No — three defects, and the first is the one that will
actually take the gate down.**

1. **`Numeric truth` has no tolerance and an unbounded reject loop. This is the defect I would
   block on.** The row says code recomputes `derivation_steps` and rejects "if the stated
   result does not follow from the stated inputs". The schema's own example is
   `{"inputs": "140 GB weights, 13.4 TB/s aggregate", "op": "140/13400", "result_stated":
   "10ms"}` — and 140/13400 = 0.01045, which is 10.4 ms, so matching "10ms" already requires a
   unit conversion the schema has no field for and a ~4.5% tolerance the table never states.
   **The tolerance is the entire check.** Set it tight and you reject answers the rubric
   explicitly calls at-bar (band 2 accepts "arithmetic within ~2–3×"); set it at 2–3× and the
   check cannot catch a 2× error — which is the exact error class Appendix B just corrected
   four of. Worse, the row conflates two different things: *the grader fabricated a derivation*
   (a grader defect, reject and re-ask is right) and *the candidate's arithmetic does not
   recompute* (a **finding about the candidate**, which should produce a band-1 score). There
   is no field for the second, so a candidate with genuinely bad arithmetic makes the grader
   fail validation **deterministically and forever** — reject-and-re-ask with no retry bound
   on a deterministic failure. I have been on the other side of this: the team's response to a
   gate that hangs on a reproducible input is to turn the gate off, and then every downstream
   claim rests on a check nobody runs. Fix: add `derivation_recomputes: bool` that the grader
   asserts and code verifies; a mismatch **clamps the axis to ≤1 and is logged as a candidate
   finding**, it does not reject the row. Reserve reject-and-re-ask for malformed output, and
   bound it (3 attempts, then fail the row loudly into `METRICS.md`).
2. **Three of the four clamps have no over-firing fixture.** §"The 12 plants ... includes a
   **negative control** for the relevance gate — the others only test harshness, so without it
   a gate that clamps everything would pass the suite." That reasoning is exactly right and it
   was then applied to one clamp out of four. `derived_quantity`, `tradeoff_axis_named` and
   `first_raised_by` each clamp an axis to ≤1 and each can only fail *harsh* against the
   current suite. A `derived_quantity` extractor that returns null on a correct derivation
   silently caps every numerate candidate at band 1 and **passes all twelve plants**. Add a
   negative control per clamp. (I have not opened the plants file, so I am reasoning from the
   prose in `prompts.md`; if controls exist for the other three, this finding is void and the
   prose should say so.)
3. **`first_raised_by` is per-axis where it needs to be per-evidence.** In a 45-minute
   transcript an axis score draws on several behaviours with different origins. One enum per
   axis forces all-or-nothing: a single interviewer-prompted contribution clamps the whole axis
   to ≤1 even where the candidate produced three others unprompted. Attach it to each evidence
   quote and clamp only the contributions the interviewer raised. (Low urgency: it is near-dead
   code on the diagnostic, where one probe per item leaves little room to be prompted, and the
   mock it matters for does not exist yet.)

**One more, in Prompt 2, and it is a determinism bug in the component whose whole justification
is determinism** ("Free generation here would make every candidate's diagnostic different,
which destroys the percentile"):

- **Rules 3 and 6 contradict each other inside one prompt block.** Rule 3: 'say "Thanks — next
  one." and stop'. Rule 6: 'Output ONLY one of: a verbatim probe from the list, or the exact
  string NEXT.' Two different literals for the same action. Pick one.
- **`if` conditions overlap, and `_meta.design_rules` fixed only duplicate *labels*.** The
  design rule correctly says a tie "makes the diagnostic non-deterministic — which destroys
  the percentile", then guards only against two branches sharing an `if` *label*. The live
  problem is overlapping *populations*: in `inline-safety-classifier-budget`, "argues from
  policy only" and "no engagement with the numbers" describe nearly the same candidate, and in
  `eval-infra-per-commit-cost`, "no number produced" and "refuses on cost without a number"
  do the same. A candidate matching both gets a probe chosen by model whim. Declare an explicit
  priority order (`followups` as an ordered list, first match wins) and say so in rule 2. This
  is a one-line fix that makes the percentile defensible.

## B3. Arithmetic

Checkable findings, with my own calculation. I re-derived every figure in Appendix B; it is in
good shape apart from item 3.

**B3.1 — `eval-infra-per-commit-cost` `model_answer` uses the throughput figure Appendix B
says is wrong. Internal contradiction between two files in the pack.** The model answer: "A
four-H100 replica serving a 70B model does on the order of 6,000 tokens a second, so roughly
28 replicas, about 112 GPUs". Appendix B, line 486: at batch 64, 2k context, "The step floors
at (140 + 41.9)/13,400 ≈ **13.6ms**, giving **≈ 4,700 tok/s** aggregate, **not the ~6,000 the
weights-only figure implies**." I verified both: weights-only 140/13,400 = 10.45 ms → 64/0.01045
= 6,124 tok/s; KV-corrected 181.9/13,400 = 13.57 ms → 64/0.01357 = 4,716 tok/s. Correcting the
model answer: 166,667 / 4,700 = **35.5 → 36 replicas = 142 GPUs**, 142 × (1/6) h × $2 =
**$47.3/commit**, × 40 = **$1,893/day**, ≈ **$691k/yr**. The model answer understates fleet and
bill by **~27%**. This matters more than a 27% error normally would: `prompts.md` line 272
generates the judge's `contrast` against `model_answer`, so the wrong number is what the grader
is taught at-bar looks like — and Appendix B's own preamble says "If any of these is wrong, the
model answer teaching the judge is wrong, which is worse than a missing number."

**B3.2 — Appendix B's token-economics sentence is self-contradictory, and is the likely
mechanism of B3.1.** Line 522: "At ~6,000 output tok/s — **the KV-corrected figure, not the
weights-only 6,000** — that is ≈ $0.47 per million output tokens". The sentence calls 6,000
both the KV-corrected figure and the weights-only figure, and the KV-corrected figure stated
36 lines earlier is 4,700. The **number is right and the prose is wrong**: 4 GPUs × $2/h = $8/h
= $0.002222/s; ÷ 4,700 tok/s = $4.73e-7/token = **$0.473/M**, which is the stated $0.47. At
6,000 it would be $0.370/M. So this is a stale-text artifact of the correction pass, and it is
very likely where the eval-infra model answer picked up 6,000. Fix both together.

**B3.3 — Appendix B's prefill table claims a causal halving it does not apply. Live arithmetic
error in the section that was already corrected once.** The formula block, line 501:
`attention ≈ 2 × n² × d_model × layers` with the annotation "**(QK^T and AV, halved for the
causal mask)**". No number in the table is halved. At n = 10k: halved = 1e8 × 8192 × 80 =
6.55e13 = **0.066 PFLOP**; the table says **0.13 PFLOP**, which is exactly the un-halved
2 × 1e8 × 8192 × 80 = 1.31e14. Same at 100k: halved = 6.55 PFLOP, table says **13.1**,
un-halved = 1.31e16. ✓ So the table is consistently un-halved while the formula says halved.
Since the causal mask does roughly halve attention FLOPs, the table **overstates attention by
2×**, and two downstream claims move:
  - 100k prefill: 14 + 6.55 = 20.6 PFLOP ÷ 1.6 PFLOPS = **~12.9 s, not ~17 s**. (10k is
    unaffected to one decimal: 1.47 ÷ 1.6 = 0.92 s.)
  - The dense/attention crossover doubles. Un-halved, 2Pn = 2n²dL → n = P/(dL) = 70e9/(8192×80)
    = **106,800**, which is the figure stated. Halved, 2Pn = n²dL → n = 2P/(dL) = **213,600**.
    So "the dense-only formula is ... wrong by roughly 2× in exactly the long-context regime
    this pack is about" is a claim about a regime that starts at ~214k tokens, not ~107k — i.e.
    **above** the 100k context the pack's scenarios use, where attention is ~32% of prefill
    rather than the stated 48%.
  Either drop the parenthetical or halve the table, and re-derive the crossover either way.
  The qualitative point ("long-context prefill is why TTFT and ITL need separate budgets")
  survives both readings, which is why I rate this a correctness defect in a teaching file
  rather than a change to the design advice.

**B3.4 — `annotation-throughput-vs-agreement`: the 1.3× checks out, but the model it depends on
is never stated.** Reconstructing: for two independent annotators with symmetric error rate p
on a balanced binary task, observed agreement p_o = 1 − 2p + 2p², chance p_e = 0.5, so
kappa = (p_o − p_e)/(1 − p_e) = (1 − 2p)². Effective sample size under that noise model scales
as (1 − 2p)² = kappa, so n_eff ∝ kappa × n, and 0.80/0.62 = **1.29 ≈ 1.3×**. ✓ Also consistent
with `model_answer`'s "roughly a quarter to a third". **I verify the number and object to it
being load-bearing without its model stated** — a reviewer who does not reconstruct the two
steps above will call 1.3× invented, and the `bad` field uses it to declare a candidate "wrong
and checkable" (B2). State `kappa = (1−2p)²` and `n_eff ∝ kappa` in Appendix B next to the
figure, and note that it assumes independent symmetric noise.

**B3.5 — all twelve `model_answer`s overrun the stated answer budget.** `_meta.answer_budget_
seconds` is 60. Measured word counts run **148–178 words**, i.e. **59–71 s at 150 wpm** and
**68–82 s at a more realistic spoken-under-pressure 130 wpm**. Eleven of twelve overrun at 150
wpm; all twelve overrun at 130. Worst case: `annotation-throughput-vs-agreement`, whose prompt
text allots "**about 30 seconds**" against a 161-word model answer — a 2–2.5× overrun, and also
an inconsistency with the 60 s in `_meta`. This bears directly on `rubric.md` lines 48–58: the
band-3 conjunction was relaxed because the bands "demanded more clauses than fit in a 60-second
spoken answer". The band was fixed; **the model answers were not**, so the artifact the judge
grades `contrast` against still cannot be spoken in the time the instrument gives. Either
trim them to ~120 words or state that `model_answer` is a written reference, not a speakable
target — but the second option needs saying out loud, because `good` fields read as beat lists
a candidate is expected to hit inside the budget.

**B3.6 — figures I checked and found correct**, recorded so the next reviewer need not redo
them: KV/token 2 × 80 × 8 × 128 × 2 B = 327,680 B = 320 KiB ✓; 100k → 32.8 GB ✓; 32.77/640 =
5.12% ✓; 32.77/80 = 41% ✓; 8B-class 2 × 32 × 8 × 128 × 2 = 128 KB ✓; batch-1 2k floor
(140 + 0.655)/13,400 = 10.49 ms, 95.3 tok/s ✓ ("~96"); batch-64 KV 64 × 2000 × 327,680 =
41.9 GB ✓ and 30% of weight bytes ✓; 13.6 ms and 4,716 tok/s ✓; 10k prefill total 1.53 PFLOP →
0.96 s ✓; headroom 400 − 310 = 90 ms ✓; `D4`'s blend 0.605 → $1.573 ✓; `F3`'s 4 PB ÷ 100 GB/s
= 11.1 h ✓; `H4`'s 1 − 0.98¹² = 21.5% ✓; `W7`'s chain 166,667 / 27.8 / 112 / 18.67 / $37.33 /
$1,493 / $544,580 ✓ (internally exact, built on B3.1's wrong throughput); `J2`/`N7`'s 41 TB and
2% churn ✓. One soft note on $544,580: ×365 prices weekends at 40 commits/day; ×260 business
days gives ~$388k, so the annualisation is ~40% high even before B3.1 and the elasticity
problem in B2 pulls it the other way by 3.6×.

**B3.7 — one place the rubric's own teaching is too flat, in my domain.** `bad` and the
`followups` for `inline-safety-classifier-budget` say p99s "do not add". True, and well worth
teaching. The precise statement is that for **independent** stages the p99 of the sum is
*less* than the sum of the p99s, so 490 ms is an upper bound. Here the stages are **not**
independent — classifier latency and model latency both scale with prompt length, so positive
correlation pushes the composition *toward* the sum. The item's conclusion is unaffected (90 ms
of headroom cannot absorb a 180 ms p99 stage however you compose them, which `good` states
correctly). But as written the item rewards knowing one fact and does not test knowing which
direction it cuts: a candidate who says "they don't add, so we probably have more headroom
than 490" has made the mirror error, and there is no branch for it. Add one: *"If the
classifier's latency rises with prompt length, does your composition argument still hold?"*

## B4. The band 2/3 boundary

**It is in roughly the right place, it was applicable, and — on the evidence of my own Part A —
it is not the boundary that is breaking.** That is the useful finding here and it is not what I
expected to report.

In the seven answers I scored, a 3 was live in eight cells and the boundary resolved cleanly in
seven of them. The "Required vs Indicators" split (`rubric.md` lines 42–71) is doing real work:
it let me score `P7`/`requirements_scoping` a 3 despite a missing indicator ("asked rather than
assumed") and `F3`/`high_level_design` a 3 despite an untouched read path, without either
feeling like charity. The required clause — *the result of the behaviour changed a design
decision* — is observable from a transcript, which is the property that matters. On `P7`'s
"No policy frees 32 gigabytes; this is about admitting long requests against a reserved share
of memory" I did not hesitate for a second. I would not move this boundary.

**The three joints that did break, in the order they cost me time:**

1. **The 0/1 boundary, three times in seven answers** (`D4`/high_level_design,
   `W7`/requirements_scoping, and nearly `F3`). The pattern is consistent and diagnosable:
   **band 0 is written as an absolute ("No end-to-end path", "Treated an underspecified prompt
   as a specification") while every band-1 clause presupposes the behaviour appeared in a
   recognisable form.** A candidate who does the behaviour's *subject matter* with none of its
   *structure* satisfies a band-0 clause and no band-1 clause, while the scoring contract's
   band-0 gate ("nothing in the answer depended on it") says 1. The rubric's own hard-cap table
   demands this be distinguishable and it is not. **Fix:** give each band-1 cell a catch-all
   clause for "engaged the subject of this axis but produced none of its structure", and
   re-word band 0 to require that the subject itself be absent. This is six small edits and it
   is where I would spend the next hour.
2. **The 1/2 boundary on `tradeoff_articulation`** (`N7`). `capacity_cost_estimation` band 2
   requires the constraint named to be the one that *binds*; `tradeoff_articulation` band 2
   does not require the axis named to be the one that *decides*. So a candidate can name the
   axis their choice wins on, never name the axis it loses on, be asked point-blank "what does
   the choice cost you", not answer, and still clear band 2. **Fix:** import capacity's
   wording — "named the axis on which the choice is actually contested".
3. **Retraction is unhandled anywhere** (`H4`). Covered at the end of Part A; the fix is one
   global clause in the scoring contract, not six cell edits.

One interaction worth noting rather than fixing: in the 60-second diagnostic, band 3's
"unprompted" is nearly free — with at most one probe per item there is barely time to be
prompted — so on Layer 1 the 2/3 discriminator rests **entirely** on "changed a design
decision". `rubric.md` line 58 says exactly this and is consistent with itself. The consequence
to be aware of is that the `first_raised_by` clamp is close to dead code on the only layer that
currently runs, and the senior/staff discriminator the level mapping is built on ("unprompted")
is therefore not really being measured by the diagnostic at all. That is an argument for the
mock, not against the rubric.

## B5. Top 3 defects, ranked

### 1. `prompts.md` validation table — `Numeric truth` has no tolerance and an unbounded reject loop on a deterministic failure

**File:** `prompts.md`, validation table row "Numeric truth" (and the schema's
`derivation_steps`), with "Reject-and-re-ask, not repair" immediately below.

**What is wrong:** three things in one row. (a) Code must recompute `op` against
`result_stated` with **no stated tolerance and no units field** — the schema's own example
needs both (140/13400 = 0.01045 vs "10ms"). (b) The tolerance is unspecified *and*
unspecifiable without contradicting the rubric: band 2 accepts "arithmetic within ~2–3×", so a
tolerance tight enough to catch the 2× errors Appendix B just corrected four of will reject
answers the rubric calls at-bar. (c) The row conflates *the grader fabricated a derivation*
with *the candidate's arithmetic is wrong*. The second is a finding about the candidate and the
schema has no way to record it, so a candidate with genuinely bad arithmetic makes the grader
fail validation deterministically, forever, with no retry bound.

**Why it matters:** this row is the anti-flattery mechanism's teeth — the table's own preamble
says "A cap that lives only in the prompt is not a cap; this table is the actual anti-flattery
mechanism." A gate that hangs on a reproducible input gets switched off, and this is the
specific failure I have watched happen: the binding constraint on an eval gate is never
compute, it is flake rate, because **a gate people override is worse than no gate.** Every
downstream claim in this pack — the percentile, the level claim, the "distribution check
matters more than the agreement number" argument — rests on this row running in production.

**What I would do:** (i) state a tolerance explicitly and justify it against the band-2 "~2–3×"
language; add a `unit` field so code is not parsing "10ms". (ii) Add
`derivation_recomputes: bool`; on mismatch **clamp the axis to ≤1 and log a candidate finding**
rather than rejecting the row. (iii) Bound reject-and-re-ask at 3 attempts, then fail the row
loudly into `METRICS.md` with its reason. Reserve rejection for malformed output.

### 2. `questions.json` `eval-infra-per-commit-cost` — the model answer the judge is taught from is wrong twice

**File:** `questions.json`, `eval-infra-per-commit-cost.model_answer`; root cause in `rubric.md`
Appendix B line 522.

**What is wrong:** (a) it uses 6,000 tok/s per 4-H100 replica, which Appendix B line 486
explicitly identifies as the superseded weights-only figure against a KV-corrected 4,700 —
understating the fleet by 27% (112 → 142 GPUs) and the bill by 27% ($544k → $691k/yr). The
likely vector is Appendix B's own self-contradictory sentence at line 522, which calls 6,000
"the KV-corrected figure, not the weights-only 6,000" while the $0.47/M it states is computed
from 4,700. (b) Separately and larger: the headline cost **assumes perfect elasticity and never
says so** — it prices 112 H100s for ten minutes, forty times a day. Duty cycle is 28%; a
reserved fleet is $1.96M/yr, **3.6×** the stated figure. Both derivations are in B3.1 and B2.

**Why it matters:** `prompts.md` line 272 generates the judge's `contrast` against
`model_answer`, so this is not a typo in a teaching aid — it is what the grader is taught at-bar
looks like, on the item whose whole subject is costing infrastructure honestly. Appendix B's own
preamble: "If any of these is wrong, the model answer teaching the judge is wrong, which is
worse than a missing number." A candidate who states the elasticity assumption and gives a
range — the behaviour `capacity_cost_estimation` band 3 describes ("Stated assumptions as
assumptions and flagged which one the answer is most sensitive to") — would be graded against a
reference that does neither.

**What I would do:** re-derive at 4,700 tok/s; fix Appendix B line 522's prose (the $0.47 is
right, the "~6,000" is stale); replace the single annual figure with a range and name the
elasticity assumption as the thing that decides between a dedicated gate fleet, borrowed
training capacity, and queueing. While in the file, add the aggregate-gate beat from B2 — at
50,000 evals, "all must pass" is impossible at any realistic flake rate, which is the pushback I
would actually make first and is absent.

### 3. `rubric.md` — the 0/1 boundary is not distinguishable from a transcript, against the rubric's own hard-cap rule

**File:** `rubric.md`, band 0 and band 1 rows of all six axes; the rule it violates is in the
hard-caps table ("Band 0 vs 1 must be distinguishable from the transcript | If the grader can't
tell, the cell is badly written").

**What is wrong:** band 0 is written as an absolute about the behaviour's *subject* ("No
end-to-end path"; "Treated an underspecified prompt as a specification"), while every band-1
clause presupposes the behaviour appeared with recognisable *structure* ("A box diagram that
does not satisfy...", "Listed eight requirements and prioritised none"). An answer that engages
the subject with none of the structure satisfies a band-0 clause and **no** band-1 clause, while
the scoring contract's band-0 gate ("nothing in the answer depended on it") points the other
way. **I hit this fork three times in seven answers** — `D4`/`high_level_design`,
`W7`/`requirements_scoping`, and nearly `F3` — and in each the band table said 0 and the scoring
contract said 1.

**Why it matters:** this is not a cosmetic tail-of-the-scale problem, because of the level
mapping. "Below the senior bar | **any axis < 1.00**" means a single 0-vs-1 coin flip on one of
four items moves an axis mean by 0.25 and can decide the public level claim outright. The
pack has invested heavily in the 2/3 boundary — correctly, and it held up in my Part A — while
the boundary that actually swings the headline verdict is the one with no agreed reading. Note
also that `rubric.md` line 209 shows the authors already found and patched *one* instance of
this exact contradiction on `capacity_cost_estimation` ("A reviewer found band 0 and the cap
contradicting each other here") without generalising the fix to the other five axes.

**What I would do:** add one catch-all clause to each band-1 cell — "engaged the subject of this
axis but produced none of its structure (named the behaviour's territory with no component, no
prioritisation, no mechanism)" — and re-word each band 0 to require the subject itself to be
absent. Six edits, and they should be made before any hand-scoring run, because they change
which side of the senior bar some sessions land on.

### Also, below the top three but worth fixing cheaply

**5.4 — harness defects that affect this measurement, not the pack.** (a) `blind-scoring-set.md`
contains **7 answers**; `review-protocol.md` says "For each of the **5** answers" twice. I scored
all 7. (b) The set says "nothing in the set tells you which answers share an item, or whether any
share one at all. **Do not try to infer either**" — but `J2` and `N7` carry **byte-identical item
prompts**, and so the instruction is self-defeating: the pairing is not inferred, it is stated. It
also matters. Knowing two answers share an item invites comparative scoring ("this one is the
better HNSW/IVF-PQ answer") instead of independent application of the cell, which inflates
inter-rater agreement for the wrong reason. I scored them in isolation and in the order given,
but I cannot claim the pairing did not inform me; it told me immediately that the
`capacity_cost_estimation` band-1 clause about "an index that needs all of it resident" was
authored with these two in mind. (c) `00-ANSWER-KEY.md` lives in the directory every reviewer is
required to `mkdir` and write into — see my disclosure at the top. Move it up a level.

**5.5 — `inline-safety-classifier-budget`'s axes do not cover its own discriminator.** Its
assigned axes are `requirements_scoping` and `communication_collaboration`, while `good` and
`bad` make the central failure a p99-composition error and the central requirement
fail-open/fail-closed. Neither assigned axis has a clause that catches either. Add
`capacity_cost_estimation` to the item, or move the arithmetic trap to an item that scores it,
and promote fail-open/fail-closed from an `at_bar_1` probe into a named beat in `good`. Details
in B2.

**5.6 — `annotation-throughput-vs-agreement`'s `bad` field marks a defensible position wrong.**
It declares "raising agreement is worth MORE than doubling volume" to be "wrong and checkable".
That holds under independent symmetric noise (where n_eff ∝ kappa, and the 1.3× is correct —
B3.4) and fails under systematic disagreement, which is the more likely story for preference
annotation at kappa 0.62. Rewrite so the failure is *asserting the stronger claim without naming
the noise model*, not holding the position. Details in B2.

**5.7 — Prompt 2 determinism:** rules 3 and 6 specify two different literals for the same action,
and `if` conditions overlap within items with no priority order. One-line fixes; they matter
because the percentile is the product. Details in B2.

**5.8 — contrast provenance:** generate `contrast` in a call that never sees the transcript, and
the check becomes unnecessary. Details in B2.

## B6. Sign-off

**Would I put my name on this rubric as legitimate? Yes.** With the caveat that I am signing the
*axes and the band definitions*, which I believe are sound and unusually observable, and that my
competence to sign is uneven: I can defend the systems content and the judge architecture; my
read on what a hiring loop actually scores is the weakest thing in this report (B7).

What I would refuse to let ship as-is:

1. **The level claim.** `rubric.md` lines 142–148 already carry the warning and record 0 of 5
   reviewers signing off last round. **Make it 0 of 6.** Six invented thresholds consuming six
   axis means, two of which are computed from 75% the same items (B1b) and two of which share a
   band-3 event (B1a), determine a public status claim. Do not display it before hand-scoring,
   and when you do, publish the inter-rater agreement on the **0/1** boundary specifically, since
   that is the one "any axis < 1.00" reads.
2. **`eval-infra-per-commit-cost`'s `model_answer`** — defect 2. A wrong reference answer teaches
   the judge, and this one is wrong on both the throughput figure and the elasticity assumption,
   on the item about costing infrastructure honestly.
3. **The `Numeric truth` row as written** — defect 1. Ship it with a stated tolerance, a units
   field, a non-rejecting path for candidate arithmetic errors, and a bounded retry, or do not
   ship the row and say in `METRICS.md` that numeric truth is unenforced. A row that hangs is
   worse than an absent row, because it will be switched off and the table will still claim it.
4. **`annotation-throughput-vs-agreement`'s `bad` field** — 5.6. It is the one place the pack
   calls a candidate "wrong and checkable", and it is the place the underlying model is most
   contestable.
5. **`inline-safety-classifier-budget`'s model answer second half** — B2. Arguing the overlap from
   the p50 after correctly refusing to reason about the tail from the median, in the item whose
   lesson is exactly that, and using a figure (175 ms for a 2k prefill) that the pack's own
   Appendix B supplies against it.
6. **The harness items in 5.4**, before the next run: the 5-vs-7 count, the de-blinded `J2`/`N7`
   pairing, and the answer key sitting in the directory reviewers write into. These cost
   measurement, not product.

Not blocking, and worth saying because the pack invites disagreement: `inline-safety-classifier-
budget` is the best pushback item I have read in a prep pack, the flake-rate beat in
`eval-infra-per-commit-cost` is the single most valuable sentence in it, and the decision to put
"who decides" into the fail-open probe is the mark of someone who has had that argument. The
judge architecture — separate calls, interviewer never scores, caps in code rather than in the
prompt, reject rather than repair, aggregation outside the model — is right, and it is right for
the reasons it states. My defects are mostly about tolerances, test coverage of the clamps, and
one stale number, not about the design.

## B7. Epistemic status — required

**Checkable facts** (anyone can verify from the files in under ten minutes; I show my working in
B3):
- B3.1 — `eval-infra` `model_answer` uses 6,000 tok/s against Appendix B's own 4,700. Two files
  in the pack contradict each other. **Fact.**
- B3.2 — Appendix B line 522 calls 6,000 both the KV-corrected and the weights-only figure in one
  sentence; the $0.47/M it states recomputes only from 4,700. **Fact.**
- B3.3 — Appendix B's prefill formula says "halved for the causal mask" and no table value is
  halved; the 100k figure is ~12.9 s under the stated formula, not 17 s, and the crossover is
  ~214k tokens, not ~106,800. One of the two is wrong. **Fact**, though *which* to change is a
  judgement (I would halve, since the mask does).
- B3.5 — all twelve model answers are 148–178 words (59–71 s at 150 wpm) against a 60 s budget,
  and `annotation`'s prompt allots 30 s. **Fact**, measured.
- B1b — `requirements_scoping` and `communication_collaboration` share 3 of 4 items in
  `_meta.axis_coverage`. **Fact**, read off the file.
- B2 (eval-infra) — the $544k figure prices 112 H100s for 10 minutes × 40/day; reserved is
  $1.96M. The arithmetic is fact; that reserved is the right comparison is domain judgement.
- 5.7 — Prompt 2 rules 3 and 6 give two different literals for one action; `if` conditions overlap
  within items. **Fact**, internal contradiction.
- 5.4 — the 5-vs-7 answer count, and `J2`/`N7` sharing a byte-identical prompt. **Fact.**
- B3.4 — the 1.3× recomputes under kappa = (1−2p)², n_eff ∝ kappa. **Fact** that it recomputes;
  that the model is the right one is judgement.

**Domain judgement a practitioner in my area would mostly share** (I would defend these in a
design review and expect agreement from people who build inline classifiers or eval gates; they
are not facts):
- Defect 1 in full — an unbounded reject-and-re-ask on a deterministic failure gets the check
  disabled, and the binding constraint on an eval gate is flake rate rather than compute. This is
  the thing I am most confident about in this report and it is still judgement.
- Three of four clamps lacking an over-firing fixture (5.4 / B2). The reasoning is the pack's own,
  applied to the clamps it was not applied to. **Caveat: I did not open `calibration-plants.json`,
  so I am reasoning from the prose in `prompts.md`. If controls for the other three exist, this
  finding is void** — and the prose should then say so, because as written it implies only one.
- The contrast-provenance replacement still being a wording check while its own stated purpose is
  conclusion-copying; and that generating the contrast without the transcript removes the problem
  rather than detecting it.
- "Async as a mitigation" critique of the inline-safety model answer: that overlap is a
  utilisation claim not a latency claim, that it must be argued at the tail, and that the 175 ms
  2k-prefill figure kills the p50 version of the argument. The arithmetic is fact; that this is
  the item's most important defect is judgement.
- The systematic-vs-independent disagreement objection to `annotation`'s `bad` field. Strongly
  held, genuinely contested in the literature, and the furthest from my daily work of anything in
  this section — a preference-data lead might tell me the independent model is the right default
  and that I am over-thinking it.
- The aggregate-gate point (at 50,000 evals, all-pass is impossible at any realistic flake rate).
  Arithmetic is fact; that the item should require it is judgement.
- B1a, that capacity's and tradeoff's band-3 cells describe one event. The textual overlap is
  checkable; that the fix is sensitivity rather than deletion is judgement.

**Guesses about interview practice that need a human to confirm** (a practitioner who has owned a
rubric should overrule me without hesitation):
- **B1 in its entirety.** Whether these six axes are what a loop scores. I have interviewed; I
  have never owned a rubric. My persona brief predicted this would be my weakest area and it is.
- **B4's claim that the 2/3 boundary is in the right place.** I found it applicable on seven of
  eight live cells, which is evidence about *one reviewer's* ability to apply it, and tells you
  nothing about agreement between two humans — which is the actual requirement
  (`rubric.md` line 398).
- Whether the 0/1 fix I propose is the right one, or whether real interviewers simply never score
  0 and the band is vestigial. If 0 is never used in practice, defect 3 shrinks considerably and
  the level mapping's "any axis < 1.00" clause is doing something different from what it looks
  like.
- Whether retraction-under-pushback should cap the content axis (my proposed global clause) or be
  confined to `communication_collaboration`. I have a view; I have no basis for it beyond
  reasoning about what the scorecard would then claim.
- Whether `communication_collaboration` is scorable from 60 seconds at all
  (`rubric.md` line 403's own open question). `H4` and `W7` both felt scorable to me on *band 1*,
  which is the easy direction. I have no read on band 3 from a short answer.
- **Over-indexing on safety-path rigour, as my brief warned.** The fail-open/fail-closed finding
  (B2) and the inline-safety critique are the things I care most about professionally, and this
  pack is aimed at general infra candidates. It is entirely possible that "who decides when the
  classifier is down" is a specialist's question that does not belong in a general instrument, and
  that I have graded its absence too harshly. **Someone who hires generalists should check this
  specific finding before acting on it.** Flagging per my brief.

**What I had to assume because the pack did not say:**
- That the inline-safety classifier is **output-side**, since the prompt does not say, and that
  the tech lead's "kill the stream at the first unsafe token" implies it. Nearly all of my B2
  critique of that item turns on this; if the prompt means prompt-side only, the model answer's
  third option is coherent and my strongest finding there weakens to "the prompt should say so".
- A **150 wpm** spoken rate for B3.5. At 180 wpm (fast, fluent) several model answers fit inside
  60 s and the finding narrows to the `annotation` item's 30 s.
- That `questions.json` `prompt` text is what reaches the grader as `<prompt_as_given>`, per
  `prompts.md` line 189, and therefore that the prompt's own numbers are what the
  derived-quantity cap excludes. This drove my reading of the cap in Part A (`P7`'s 320 KB/token
  counts as derived; `J2`'s and `N7`'s 40 TB also counts, since 4 KB/vector is computed from
  1024 × 4 rather than quoted).
- That **`good` fields are not an enumerated beat structure anywhere** — I checked all ten keys of
  every item and there is no `required_beats` on the diagnostic items. The "Contrast coverage"
  row's implementability rests on this; if beats exist elsewhere, that finding is void.
- A **$2/GPU-hour** market rate throughout, taken from Appendix B's own stated assumption, which
  that file correctly flags as needing re-verification. Every dollar figure in B3.1 and B2 scales
  linearly with it, so the *ratios* (27%, 3.6×) are the robust claims and the absolute figures
  are not.
- That **`derivation_steps` tolerance is genuinely unspecified** rather than specified in code I
  cannot see. There is no code in this pack to check, so defect 1(a) is a finding about the spec.
  If the implementation has a tolerance, the spec still needs to state it, since the table is
  explicitly the contract for that code.
