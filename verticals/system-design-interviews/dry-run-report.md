# DRY-RUN REPORT — the pack graded against itself

**Date:** 2026-11-22. **Grader:** none. Every score below is **hand-assigned by the author
of the rubric**, which is the weakest possible form of validation and is the reason this
exercise finds defects rather than certifying quality.

**What this was for:** find the defects a paid practitioner should not have to spend their
first hour discovering. Two tests were run:

1. The **10 adversarial plants** (`calibration-plants.json`) graded against `rubric.md`.
2. **Plant 10 generalised**: all 24 reference-answer cells in `questions.json` checked
   against the band they exist to teach.

**What it cannot tell you:** whether the rubric is *legitimate*. Grading my own rubric with
my own answers measures internal consistency and nothing else. Two scorers can agree
perfectly on a rubric no real interviewer would recognise — agreement and validity are
different properties, and only a practitioner supplies the second.

---

## Result: 9 of 10 plants pass. 3 defects found, all 3 fixed.

| Plant | Target axis outcomes | Verdict |
| --- | --- | --- |
| 01 confident and empty | capacity **1** (cap fires), tradeoff **2** | **PASS** — and exposed defect A |
| 02 pros and cons, no decision | tradeoff **1**, deep dive **1** | **PASS** |
| 03 number salad | capacity **2**, tradeoff **1** | **PASS** — the hardest call in the set |
| 04 correct but mute | requirements **1**, communication **1** | **PASS** |
| 05 jargon-dense and wrong | requirements **1**, capacity **1** | **PASS** — confirmed defect A a second time |
| 06 collapses under pushback | deep dive **2**, communication **1** | **PASS** |
| 07 digs in under pushback | requirements **1**, communication **1** | **PASS** |
| 08 right answer, wrong scenario | requirements **1**, capacity **3** | **FAIL** — defect B |
| 09 spiky | capacity **3**, high-level design **0** | **PASS** |
| 10 verbatim reference answer | HLD **3**, deep dive **3** | **PASS** |

---

## Defect A — the capacity cap was trivially defeatable

**Found by:** plants 01 and 05, independently.

The cap read: *if the transcript contains no quantity, `capacity_cost_estimation ≤ 1`.*
Every item states its constraints numerically, so a candidate who derives nothing still
puts numbers in the transcript two ways:

- **Echoing the prompt** — plant 01 says "given our 400 millisecond target" and computes
  nothing.
- **Reciting a remembered statistic** — plant 05 says "vLLM gets fragmentation waste under
  4 percent", a figure about someone else's system used in no arithmetic step.

A literal implementation of the old wording lets both through, and both are answers the cap
exists to catch. This is the single most likely way the shipped grader would have been
generous, because it is the cap the whole axis depends on.

**Fixed:** the cap now requires a quantity the candidate **derived, estimated, or
computed** — not present in the prompt text, and participating in a stated derivation or
comparison. Both the axis text and the hard-caps table in `rubric.md` are updated, with the
implementation rule spelled out for the build agent.

---

## Defect B — the content axes had no relevance gate

**Found by:** plant 08. The only failing plant.

Plant 08 is a strong, numerate, genuinely at-bar answer about continuous batching, graded
against the KV-cache admission item. Against the old `capacity_cost_estimation` cell it
scored **band 3**, and correctly so by the letter of the rubric: it derived the quantity
from stated assumptions, named a binding constraint, and let the number change the design.
Every clause was satisfied. It just answered a different question.

Only `communication_collaboration` band 1 mentioned answering a different question than the
one asked, and 8 of the 12 items do not score that axis. So a fluent answer to the wrong
problem could score at or above bar on content.

**Why this matters more than it looks:** this is the failure mode of a candidate who has
memorised four reference designs and pattern-matches the prompt to the nearest one. That is
a large fraction of the people a prep product attracts, and the rubric would have told them
they were above bar.

**Fixed:** a relevance gate added to the scoring contract — *a behaviour performed on the
wrong problem scores at most band 1 on every axis, however well executed* — plus a row in
the hard-caps table. The judge must check the answer against the prompt's stated
constraints before scoring any axis.

---

## Defect C — band 3 was unreachable in 60 seconds on two axes

**Found by:** generalising plant 10 from one reference answer to all 24 cells. The most
consequential finding, and invisible without the generalisation.

Plant 10 passed: the `training-data-dedup-and-shuffle` reference answer reaches band 3 on
both its axes. So I checked the other 11. Read as a **conjunction** of every clause listed,
band 3 was unreachable in a 60-second spoken answer on two axes:

| Axis | Reference answers reaching band 3 | Failing |
| --- | --- | --- |
| `requirements_scoping` | 4 / 4 | — |
| `capacity_cost_estimation` | 4 / 4 | — |
| `high_level_design` | 2 / 4 | `multi-tenant-token-limiter-placement`, `heterogeneous-fleet-routing` |
| `deep_dive_failure_modes` | 3 / 4 | `gpu-credit-ledger-consistency` |
| `tradeoff_articulation` | 2 / 4 | `batch-window-vs-ttft-budget`, `multi-tenant-token-limiter-placement` |
| `communication_collaboration` | 4 / 4 | — |
| **Total** | **19 / 24** | **5** |

**5 of 24 reference answers failed to reach the band they exist to teach**, concentrated in
`tradeoff_articulation` and `high_level_design`. The cause is specific: band 3 on tradeoff
required naming the reversal condition *and* volunteering the counter-argument; band 3 on
high-level design required naming the bottleneck *and* the load multiple at which it binds.
Those clauses are right for a 45-minute round and do not fit alongside the primary answer
in 175 words.

**A band the gold-standard answer cannot reach is a broken band.** The grader anchors
contrast generation on `model_answer`; every grade on those two axes would have been pulled
systematically low, and the product would have under-scored the cohort on the axis the
whole level claim is gated on.

**Fixed, two ways:**

1. **`rubric.md`** — band 3 now has **one required clause** (the bolded one: the result of
   the behaviour changed a design decision). The remaining clauses are **indicators**: any
   one corroborates a 3, absence does not block one. In the 45-minute mock, where there is
   room, their absence is the intended 2/3 discriminator; in the 60-second diagnostic the
   required clause is the whole test.
2. **`questions.json`** — the two weakest reference answers rewritten.
   `batch-window-vs-ttft-budget` now names the reversal condition ("that flips if the budget
   is relaxed past about a second, or if long prompts grow past a fifth of traffic").
   `multi-tenant-token-limiter-placement`, which failed on *both* its axes and was the
   weakest answer in the bank, now derives the design from the 1,670 tokens/second figure,
   names the reversal condition (paid overage), and names the ledger as what breaks first.

**Residual, not fixed:** the rewritten `multi-tenant` answer is 178 words, the longest in
the bank and at the ceiling of the 60-second budget. That length is itself evidence for
defect C — reaching band 3 on two axes at once genuinely crowds the time budget. If item
analysis later shows real candidates cannot reach band 3 on two axes in one 60-second
answer, the honest fix is to cap the diagnostic at band 2 and report band 3 as
mock-only, rather than to keep shortening the gold answers.

---

## What the plants confirmed was already right

Worth recording, so these are not re-litigated:

- **The 06/07 pair works.** Collapsing under pushback and digging in under pushback both
  land at band 1. Writing both directions into the cell was deliberate and it held — a
  grader that only punishes caving would have scored plant 07 at bar for conviction.
- **Axis independence holds.** Plant 01 scores 1 and 2 on its two axes; plant 09 scores 3
  and 0. Nothing in the rubric pushes a weak axis up or a strong axis down.
- **The tradeoff cap is not the only defence.** Plant 02 *does* name its tradeoff axis
  explicitly, so the cap does not fire — and the band 2 cell still catches it, because band
  2 requires picking a side. The cell and the cap are independent, which is correct.
- **Plant 03 sits exactly on the 2/3 line and the cell resolves it.** Correct arithmetic
  (40TB), followed by an index choice the arithmetic rules out. Band 2, because the number
  changed nothing. This is the boundary the whole instrument rests on and the cell as
  written does discriminate — by my reading, which is the caveat on this entire document.

---

## What still needs a practitioner, unchanged by this exercise

The dry run fixed three mechanical defects. It cannot touch any of these:

1. **Whether the six axes are what real loops score.** Unchanged. The gate on everything.
2. **Whether the band 2/3 line is in the right place.** I moved it in defect C, by my own
   judgement, which makes a second opinion *more* necessary rather than less.
3. **Whether `capacity_cost_estimation` deserves axis status** given that both published
   sources call estimation optional. Still the most likely place the rubric is wrong.
4. **Whether band 1 reads as diagnostic rather than insulting.** Untested and
   public-facing.
5. **The level-mapping thresholds.** Still invented, still the highest-stakes unvalidated
   numbers in the pack.

**One thing this exercise did change about the practitioner brief:** send them plants 03
and 08 alongside the rubric. Plant 03 sits on the 2/3 boundary and plant 08 is the
pattern-matcher. Asking two practitioners to score those two independently is a ten-minute
task that tests the most load-bearing and most contestable judgements in the pack, and it
can be done before anyone records a real session.

---

## Honest caveats on this document

- **Self-grading.** Author of the rubric scored answers written by the author of the rubric
  against plants written by the author of the rubric. Every "PASS" means internally
  consistent, never correct.
- **No grader exists.** These are hand-assigned scores, not model output. The plants' real
  purpose is as fixtures for the grader once it is built; defects A and B are precisely the
  kind that a hand-grader forgives and a literal implementation does not.
- **n = 10.** Ten plants probe ten failure modes. There are more.
- **Defect C's fix is a judgement call, not a measurement.** Softening band 3 to one
  required clause makes band 3 easier to reach. If that turns out to be too easy — more
  than about 15% of axis scores landing at 3, per the distribution check in
  `calibration-plan.md` — the fix was wrong and the right answer was mock-only band 3.
