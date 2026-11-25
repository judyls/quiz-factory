# SYNTHESIS — run 2

Run 2026-11-23 against commit `d9de968`, i.e. the pack **after** the nine fixes from run 1's
queue. Five reviewers, seven answers, fourteen cells, all six axes. Full reports in this
directory.

**Headline:** the two things this run existed to test both came back clean — the rewritten
plant 09 scored unanimously at its expected band, and the new relevance-gate negative control
did not over-fire. One of my run-1 fixes caused a regression, which the only cell comparable
across runs caught. And run 1's four corrected numbers never propagated out of Appendix B
into the files that actually anchor grading.

**What this run is:** still a pre-screen. Five models, not five engineers. Everything below
is either (a) arithmetic I re-derived myself, marked ✓, or (b) a judgement that needs a human.

---

## 1. Inter-rater agreement

| Cell | R1 | R2 | R3 | R4 | R5 | spread | expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **D4 (09) `capacity`** | **3** | **3** | **3** | **3** | **3** | 0 | **==3 ✓** |
| D4 (09) `HLD` | 0 | 0 | 1 | 1 | 0 | 1 | ≤1 ✓ |
| F3 (10) `HLD` | 3 | 3 | 3 | 3 | 3 | 0 | — |
| F3 (10) `deep_dive` | 2 | 2 | 3 | 2 | 2 | 1 | — |
| J2 (03b) `capacity` | 2 | 2 | 2 | 2 | 2 | 0 | ==2 ✓ |
| J2 (03b) `tradeoff` | 1 | 1 | 1 | 1 | 1 | 0 | ≤1 ✓ |
| H4 (06) `deep_dive` | 2 | 2 | 2 | 2 | 3 | 1 | — |
| H4 (06) `communication` | 1 | 1 | 1 | 1 | 1 | 0 | — |
| **P7 (08b) `requirements`** | **3** | **3** | **3** | **3** | **3** | 0 | **≥2 ✓ gate did not fire** |
| **P7 (08b) `capacity`** | **3** | **3** | **3** | **3** | **3** | 0 | **≥2 ✓** |
| N7 (03a) `capacity` | 1 | 1 | 1 | 1 | 1 | 0 | ≤1 ✓ |
| **N7 (03a) `tradeoff`** | 1 | **2** | **2** | **2** | 1 | 1 | **≤1 ✗ regression** |
| W7 (04) `requirements` | 1 | 1 | 1 | 0 | 1 | 1 | — |
| W7 (04) `communication` | 1 | 1 | 1 | 1 | 1 | 0 | — |

- **Exact agreement (all five identical): 9 of 14 = 64%.** Adjacent: **14 of 14 = 100%.**
- Plan floors are ≥50% exact, ≥90% adjacent. Both still cleared.

**64% is not a drop from run 1's 80%, and must not be reported as one.** Run 1 scored 10
cells across 3 axes; this set was deliberately built to be harder and to reach the three
axes run 1 never touched. The comparable measurement is the two answers present in both
runs: **4 of 4 unanimous in run 1, 3 of 4 in run 2.** One cell moved, and it moved because
of something I changed.

### The regression: my band-2 fix loosened `tradeoff_articulation`

`N7` / `tradeoff` was unanimous at 1 in run 1 and split 1/2/2/2/1 now. Nothing about the
answer changed — it still justifies its pick by convention ("what most deployments run"),
names no axis and concedes nothing.

What changed is my run-1 fix. Giving band 2 **one** required clause meant demoting the
others to indicators, and on this axis the clause I demoted was *"acknowledged what the
choice gives up"*. So an answer that concedes nothing can now satisfy band 2. R5 traced the
enforced code path and got 2; R1 flagged it as its loudest `admits another reading`; R2
independently proposed the fix (require **the binding** trade-off, not any trade-off).

This is the defect class the band-3 fix had in run 1, pushed down one band and into a
different axis. Run 1's queue note said the band-3 fix "moved the defect instead of removing
it" — that was true a second time and I did not catch it.

### Both recorded priors were wrong, in the same way

| Prior | Prediction | Result |
| --- | --- | --- |
| Original | `tradeoff` and `communication` weakest | ✗ `communication` unanimous on both cells |
| Revised, after run 1 | contested boundary is 0-v-1 and 1-v-2 on **`capacity`** | ✗ `capacity` unanimous on **all four** cells — now the most reliable axis in the file |

Two priors, two misses, and both guessed an **axis**. The five contested cells in this run
span four axes and cluster on **boundaries**:

| Boundary | Contested cells |
| --- | --- |
| 0-vs-1 | `D4 HLD`, `W7 requirements` |
| 2-vs-3 | `F3 deep_dive`, `H4 deep_dive` |
| 1-vs-2 | `N7 tradeoff` |

The invariant across both runs is that disagreement lives at a band boundary and migrates to
whichever boundary was least recently rewritten. Capacity is unanimous now **because** it is
the axis I rewrote twice. That is worth recording as the third prior: fixing a band moves the
disagreement, it does not reduce it, until every band in the cell declares its required
clause.

### The second prediction was right

`calibration-plan.md` records: reliability lowest on `high_level_design` and
`deep_dive_failure_modes`, with the data-pipeline item weakest.

| Axis | Unanimous cells |
| --- | --- |
| `deep_dive_failure_modes` | **0 / 2** |
| `high_level_design` | 1 / 2 |
| `tradeoff_articulation` | 1 / 2 |
| `requirements_scoping` | 1 / 2 |
| `capacity_cost_estimation` | 4 / 4 |
| `communication_collaboration` | 2 / 2 |

**Confirmed**, and `deep_dive_failure_modes` is the weakest at 0/2. Caveat that matters more
than the result: **two cells per axis cannot support a reliability claim.** This is a hint
that the prediction was in the right place, not a measurement. Cronbach's α across four items
per axis, on real candidates, is still the only thing that settles it.

### The unanimous hardest cell: there is no retraction rule

All five named `H4` / `deep_dive_failure_modes`, and four gave the same reason. The candidate
derives the correct insight — 12 tools at 2% each means ~21% of turns time out, so retrying
the whole turn double-charges — proposes idempotency keys, and then abandons it under one
mild push.

Nothing in `rubric.md` says whether an axis is scored on the answer's **best** state or its
**final** state. R1 found 1, 2 and 3 all defensible from the text; R4 noted the two readings
are two bands apart. The fixture's ending is close to verbatim the item's own `bad`, and the
rubric as written still admits a 3.

This is the cleanest finding of the run: five independent readers, one cell, one named cause,
and a one-sentence fix.

---

## 2. Convergent defects

| # | Defect | Found by | Status |
| --- | --- | --- | --- |
| D1 | **Appendix B's corrections never propagated.** `batch-window` still uses the weights-only ~10ms decode floor; `eval-infra` still uses 6,000 tok/s; `kv-cache-admission` still says 32GB sits "against 80GB per card, most of which is already holding weights"; `prompts.md` ships a stale derivation as the grader's worked example | R1 R3 R4 | ✓ confirmed by grep + re-derivation |
| D2 | **Bands 0 and 1 are still undeclared conjunctions** with no precedence rule — the band-3→band-2 fix stopped one band short. The 0/1 line is not distinguishable from a transcript, and `any axis < 1.00` makes it decide the public level claim | R1 R3 R4 R5 | ✓ verified structurally |
| D3 | **No retraction rule** (§1 above) | R1 R2 R3 R4 R5 | ✓ verified — no such rule exists |
| D4 | **The Numeric-truth check catches none of the four error classes it was written for.** It recomputes arithmetic; all four Appendix B errors were *omitted terms* with internally consistent arithmetic. R3 adds: no tolerance, no units field, and it conflates grader fabrication with candidate bad arithmetic, so a candidate's own wrong number fails validation with no retry bound — "the gate will get switched off" | R3 R4 R5 | ✓ verified — accepted |
| D5 | **Level mapping still not shippable.** R2: "At the staff bar" is unreachable because a staff profile matches the senior row first under top-down evaluation, and the rows are not exhaustive — counterexample `1.75,1.75,1.75,1.60,1.40,1.40`. R5: the mock path self-contradicts (insufficient-signal rule vs "thresholds apply unchanged"), and a floor effect puts the modal competent candidate below the senior bar | R2 R5 | ✓ counterexample verified |
| D6 | `rubric.md:523` **announces the throughput correction and then states the stale figure as the corrected one**: "~6,000 tok/s — the KV-corrected figure, not the weights-only 6,000", with a $0.47/M that only follows from 4,714 | R1 R2 R4 R5 | ✓ confirmed |
| D7 | The **shuffle correction Appendix B promises is absent.** The block quote at `:456` says the shuffle figure "counted writes but not reads. Corrected below" — there is no shuffle derivation anywhere in the appendix | R1 R5 | ✓ confirmed by grep |
| D8 | `eval-infra-per-commit-cost` **understates by 27%** on throughput alone, before the elasticity question: 141 GPUs and ~$688k/yr, not 112 and ~$500k. R3 adds that 112 H100s for a 10-minute burst states no elasticity assumption; reserved it is ~3.6× | R1 R3 R4 | ✓ re-derived |

### D9 — plant 10 no longer copies what it claims to copy

Found by R4 in the blind set and confirmed directly. The fixture is named
`plant-10-verbatim-model-answer` and its whole mechanism is being **verbatim the model
answer**, so a judge that rewards recitation can be caught. I corrected the model answer's
shuffle figure to 22 hours in run 1's queue and left the fixture at 11.

So the fixture now (a) does not match what it claims to copy, breaking its mechanism, and
(b) teaches the judge the number I had just established was wrong.

This is the same drift the new `generate-blind-set.py` exists to prevent, one level up, where
I did not think to look. Any fixture whose premise is "identical to X" needs a generated
assertion, not a copy.

### Scenario-validity findings worth a practitioner's eye

Not convergent, but specific and from the reviewer closest to the domain:

- **R4: the pack's AI-infra coverage is thin.** 2 of 12 items touch training, only 1 is a
  training-infra design problem, and nothing covers distributed training, collectives, or
  checkpoint/restart. It declined to sign the claim that the pack covers AI infrastructure.
  This bears directly on the 40-scenario bank.
- **R4: `training-data-dedup-and-shuffle` attaches a raw-crawl 4PB to the training read
  path.** A tokenised corpus is 40–80TB, where a per-epoch shuffle is ~27 minutes — which
  **inverts the item's teaching point**. Its axis pair also excludes `capacity`, so the I/O
  arithmetic the item is built around is unscoreable.
- **R1: `batch-window-vs-ttft-budget`'s three numbers may not co-occur** — batch 32 at 45%
  utilisation implies a fill time far longer than the stated 1.2s p99. Needs its own
  derivation from stated assumptions before it is accepted or rejected; the prompt does not
  pin down enough to settle it either way.
- **R2: the `gpu-credit-ledger` item** bounds $11 at admission-time leases, not accrual
  during a ledger outage (~$667 for 10 minutes on a 2,000-GPU fleet), and the prompt
  pre-states the insight that `good` then credits.
- **R2: the 21% compound-timeout figure** is sound as an upper bound but indefensible as a
  point estimate — a shared turn-level deadline collapses it toward 2% — and no `good` beat
  or probe rewards a candidate for flagging the independence assumption.

---

## 3. Harness defects found this run

Three, all mine, and the first two were self-disclosed by reviewers again.

1. **The answer key sat in the directory every reviewer must write into.** R3's `ls` of
   `findings/run-2/` returned the filename `00-ANSWER-KEY.md`. It did not open it and
   confirmed no cell was affected. Fixed: the key moves out of `findings/` entirely.
2. **`J2` and `N7` carry byte-identical prompts**, while the set's preamble tells reviewers
   not to infer which answers share an item. R2 and R3 both pointed out that the instruction
   is unsatisfiable. Run 1's fix — make the pair non-adjacent — does not help when the prompt
   text is the tell. The honest fix is to stop claiming the pairing is hidden.
3. **`review-protocol.md` still said "the 5 answers"** when the set had 7. My patch targeted
   a string that did not match the file and silently did nothing. All five reviewers noticed
   and scored all seven anyway. The patch script asserted nothing — the same failure mode as
   the run-1 script that aborted mid-way.

Pattern worth naming: all five blinding defects across two runs were in material I wrote
*while thinking about blinding*. The generator now asserts; the prose does not.

---

## 4. Sign-off

| | R1 | R2 | R3 | R4 | R5 |
| --- | --- | --- | --- | --- | --- |
| Six axes legitimate | yes | yes | yes | yes | yes |
| Band 2/3 boundary | ok | ok | **"fine, not what is breaking"** | ok | ok |
| Level mapping | no | no | no | no | no |

- **10 of 10 across two runs sign the six axes.**
- **0 of 10 across two runs sign the level mapping.** That is no longer a defect to fix; it
  is a feature to cut or hide until real data exists.
- R3 states plainly that the 2/3 boundary — which `calibration-plan.md` calls "the whole
  instrument" — is not the problem. Two runs now agree. The plan's framing should change.

Caveats attached to otherwise-yes sign-offs: R1 would not ship `tradeoff` band 2 as written
(the regression above); R2 would not ship the ledger item or any `communication` 2/3 from a
60-second diagnostic that never pushes back on a correct answer; R4 would not ship the 4PB
framing or the eval throughput figure, or the AI-infra coverage claim.

---

## 5. Queue

| # | Item | Severity | Mine to fix? |
| --- | --- | --- | --- |
| 1 | D1 — propagate Appendix B's four corrections into `questions.json` and `prompts.md` | **blocking** | yes |
| 2 | D9 — plant 10 vs its model answer, plus an assertion so it cannot drift again | **blocking** | yes |
| 3 | D6, D7 — the self-contradicting throughput sentence and the missing shuffle derivation | **blocking** | yes |
| 4 | The `tradeoff` band-2 regression — require *the binding* trade-off | high | yes |
| 5 | D3 — add a retraction rule (best state vs final state) | high | yes |
| 6 | D2 — declare required clauses for bands 0 and 1, with a precedence rule | high | yes |
| 7 | D4 — the Numeric-truth check needs to test the model, not the arithmetic; and must not fail the grader for a candidate's own bad number | high | yes |
| 8 | D5 — cut or hide the level claim | high | yes, by removal |
| 9 | D8 — re-cost `eval-infra`, and state the elasticity assumption | medium | yes |
| 10 | R4's coverage finding — the bank is thin on training infra | medium | yes, in the 40-item bank |
| 11 | Scenario-validity items: 4PB framing, batch-window's three numbers, the ledger $11 bound, the 21% independence assumption | medium | yes, except where a practitioner is the right judge |
| 12 | `communication_collaboration` bias — **still open from run 1** | — | **no — needs a human** |

Item 12 is unchanged and deliberately so. Both cells of that axis came back unanimous this
run, which says the cell is *clear*, not that it is *fair*. Five models sharing a training
distribution cannot answer the fairness question, and a unanimous score is exactly what
shared blind spots look like.

---

## 6. Queue worked — status

Eleven of twelve closed. Item 12 remains open on purpose.

| # | Item | Status |
| --- | --- | --- |
| 1 | Propagate Appendix B's corrections | **fixed** — and the sweep found 4 places no reviewer named, including two fixtures and the grader's own schema example |
| 2 | Plant 10 vs its model answer | **fixed** — now generated from the model answer, and `validate.py` fails if it ever diverges again |
| 3 | The self-contradicting throughput sentence; the missing shuffle derivation | **fixed** — Appendix B now carries a shuffle block with both corpus scales |
| 4 | `tradeoff` band-2 regression | **fixed** — band 2 now requires *the binding* trade-off, a side, **and** what that side gives up |
| 5 | No retraction rule | **fixed** — content axes score the final state, with revision (reason supplied) distinguished from retraction (none supplied) |
| 6 | Bands 0 and 1 undeclared | **fixed differently than queued** — see below |
| 7 | The Numeric-truth check | **fixed** — split into three checks; the new one tests the *model*, via per-item `required_terms` |
| 8 | The level claim | **cut** |
| 9 | Re-cost `eval-infra` | **fixed** — ~$690k on-demand, ~$2.5M reserved, elasticity stated |
| 10 | Training-infra coverage | **recorded** in `02-CONTENT-AGENT.md` as a limitation of what shipped, with four replacement scenarios named |
| 11 | Scenario-validity items | **fixed** — ledger, dedup, agent-retry, batch-window |
| 12 | `communication_collaboration` bias | **open — for a human** |

### Item 6 was not fixed the way it was queued

The queue said "declare required clauses for bands 0 and 1", by analogy with the band-3 and
band-2 fixes. Writing it that way made the error visible: **band 1 is not a set of
conditions.** It is what is left when band 2's required clause is unmet. Giving it required
clauses would have created a third conjunction — the same defect a third time, which is the
pattern run 2 recorded as the third prior.

So the fix is a precedence rule instead. Band 0 is one declared test per axis, about absence
only. Bands 3 and 2 are decided by their required clause. **Band 1 is the residual, and its
listed behaviours are explicitly marked as worked examples that must never be checked to
decide a score.** `validate.py` now asserts exactly six of each marker, and asserts that
band 1 has *not* acquired conditions.

That also predicts where run 3's disagreement should go. If the third prior is right, the
contested cells should move to the 2/3 boundary — the one both earlier priors expected and
neither found.

### Two scenarios got better rather than merely correct

- **`batch-window-vs-ttft-budget`** was not wrong, it was **underspecified**: it never said
  how a batch departs. Adding a one-second fill timeout makes its three stated numbers
  reconcile to within 2% (1s wait + a 178ms prefill = 1,178ms against the stated 1.2s p99,
  with half-full departures explaining 45% utilisation) — and it sharpens the item, because
  the discriminating insight becomes "the batch is departing on the timeout, so you pay the
  whole wait and get none of the throughput". The model answer now also budgets against
  prefill rather than the decode floor, which is a ~15× larger term at 2k context.
- **`gpu-credit-ledger-consistency`** now answers the exposure question properly. The $11
  lease bound holds only while the ledger is reachable; fail open through a ten-minute
  outage on a 2,000-GPU fleet and it is ~$670 and accruing. Two orders of magnitude, and the
  prompt no longer pre-states that 150ms is affordable.

### What this run cost, and what it bought

Four of the nine convergent defects were introduced or left behind by run 1's own fixes.
That is the honest summary of iterating on a rubric with a harness: each pass finds real
defects and plants a smaller number of new ones, and the only reason this is visible is that
the fixtures and the agreement measurement are kept across runs. The ratio is improving —
run 1 found 9 against a pack with no self-tests, run 2 found 9 against a pack with two
layers of them — but it is not zero and should not be reported as converged.

### Plant 10 caught a second thing, which is what it is for

Its scores came back `high_level_design` **3** (unanimous) and `deep_dive_failure_modes`
**2** (four of five), against an expected 3 and 3. Its own `known_defect_probed` says what a
2 means: *"the model answers are not written to the band they are supposed to teach, and
every grade anchored on them will be pulled low."*

Checking it against the cell, the reviewers were right. Band 3 requires a failure mode the
candidate found **that changed the design**, and the old answer had none — its design moves
were driven by a requirement (reproducibility) and a cost (the shuffle), both legitimate and
neither a failure mode. The answer was a band-2 answer sitting in the slot that teaches
band 3.

Fixed by adding the failure mode that lives in the design the answer itself proposes: shards
built in crawl order make in-shard shuffling return the same neighbourhoods every epoch, so
batches stay correlated while the loss curve looks healthy. That changes the design
(randomise shard assignment at ingest, not only within shards) and names the signal that
would reveal it.

This is the fixture doing exactly its job, on the second run, against a model answer that
had already been corrected once. It is also the reason `plant-10` is worth the awkwardness
of being generated rather than written.

---

## 7. Addendum — one live human test, three more defects

Run 2026-11-24, after the queue above was closed. Not part of the harness: one person, one
item drawn at random, answered out loud against a 60-second timer with nothing to look up.
It took about twenty seconds and produced a band-1 answer. It also found three item defects
the five reviewers did not.

**The answer, in full:** *"Okay, we want to have the input as a variable, and the output is
2,000 tokens. We have a judge call that we don't know how big that is, but it's 50,000 calls
of this. Each one is like 2 LLM calls to 100,000. That we need to do in 10 minutes, which
means 10,000 per minute. That's a lot of phone calls."*

Scored against the rubric as written: `requirements_scoping` **1**,
`capacity_cost_estimation` **1**. One real derivation (100,000 calls → 10,000/min, correct),
no binding constraint named, no cost produced, pushback never reached.

**But it stopped because the item ran out of information, not because the speaker did.** The
two things flagged in the first eight words — input length, judge size — are both genuinely
absent from `eval-infra-per-commit-cost`, and the judge call is 36–52% of the work. My model
answer waved at it with the words "plus judge calls" and costed neither. Run 1 had flagged
exactly this as defect C3 with three reviewers; I fixed the other half of C3 (fleet pricing)
and left the judge calls untouched through two queues.

Corrected: the item now states a 500-token prompt and a judge that reads 2,500 and writes
200. The honest cost is **243 GPUs, ~$81 a commit, ~$1.18M a year** — the previous figure was
**1.7–2.4× low**, because it counted generation output only. Prefill is a third of the work,
which stings given Appendix B had just been rewritten about prefill being the term everyone
drops.

### The audit this triggered, and what it found

Four other items leaned on six or more figures absent from their prompts. The crude count
over-flags, because most such figures are *derivations* (140GB from "70 billion parameters in
bfloat16") and deriving them is the skill being measured. The test that matters is narrower:
**is there a value the candidate cannot obtain, and would a different plausible value change
the conclusion?**

| Item | Unstated | Material? |
| --- | --- | --- |
| `eval-infra-per-commit-cost` | judge size, input length | **yes** — 1.7–2.4× on the cost |
| `batch-window-vs-ttft-budget` | context length | **yes** — at 20k tokens prefill is 2.1s and the 400ms target is *impossible*, so the premise inverts |
| `gpu-credit-ledger-consistency` | fleet size | **yes** — the outage exposure is entirely a function of it ($670 at 2,000 GPUs, $6,670 at 20,000). **I introduced this one in the commit immediately before the test** |
| `kv-cache-admission-control` | tensor-parallel degree | minor — the per-card figure implied TP=4 and the prompt gave 8-card nodes |
| `heterogeneous-fleet-routing` | — | clean. Every figure derives from the prompt's parameter counts |

All four fixed by stating the value in the prompt. I had guessed "one or two of the four are
real"; it was three, plus one minor. Recording the wrong guess because the pattern across
this session is that my estimates of how much is broken run low.

### Why the harness could not find this

A reviewer given an underspecified item **completes it from its own priors and does not
notice.** Five reviewers each silently picked a plausible judge size and scored on; two of
the three broken items were scored *unanimously*, which is the part worth sitting with —
unanimity measured agreement about a question nobody could actually answer.

A human with a mouth, a timer and nothing to look up cannot do that. The gap is the first
thing they hit.

This is a structural limit of model review, not a flaw in the personas, and it is now
recorded in the harness README. It also sets the cheapest next test: **the other eleven items
need a human to attempt them out loud, one pass each.** That is well under an hour and, on
today's evidence, worth more per minute than a third harness run.

### One open design question this raises

`requirements_scoping` band 3 rewards *"asked the one question whose answer would most change
the architecture"* — a behaviour the 60-second diagnostic structurally cannot permit, because
there is nobody to ask. The axis may be only partly measurable in the diagnostic and need its
real measurement in the 45-minute mock. Flagged, not acted on: it needs more than one item's
evidence, and it is a decision about the instrument rather than a defect in a file.
