# CALIBRATION PLAN — golden set, agreement measurement, and the anti-flattery gate

How `rubric.md` and `questions.json` get turned from plausible into measured. Nothing in
this pack is calibrated yet; this file is the procedure and the thresholds, written before
the data exists so the thresholds cannot be chosen to fit the result.

**The thing being defended:** a mock interviewer that flatters is detected in one session
and never opened again. Second-session rate is the honest verdict on the product, and a
generous grader is the most likely cause of a bad one.

---

## There are two instruments, and they calibrate separately

| | **A. The diagnostic** | **B. The mock grader** |
| --- | --- | --- |
| What it is | 12 voice items, ~60s each, from `questions.json` | 45-minute session, judged over a full transcript |
| Ships in | Phase 2 (first) | Phase 3 |
| Output | composite + percentile + named blind spot → the share artifact | per-axis 0–3 with quoted evidence → the paid report |
| Calibrated against | item analysis + human band labels on the same 12 answers | 20+ hand-scored full transcripts |
| Fails by | items that don't discriminate; percentiles computed too early | flattery; disagreement concentrated in one or two axes |

They share `rubric.md`, which is why a rubric defect shows up in both. **Calibrate A
first** — it ships first, it is cheaper to label (12 short answers vs a 45-minute
transcript), and a rubric cell that two humans cannot agree on in A will not become
agreeable in B.

---

## PHASE 0 — Before any grader runs: can two humans agree?

Non-negotiable ordering. Measuring a model against labels that humans disagree on measures
nothing, and the failure presents as "the grader is bad on `communication_collaboration`"
when the truth is that the cell is badly written.

1. **Recruit 2 practitioner scorers** who have run real system design loops at an
   AI-heavy company. Not two members of the team. Pay them.
2. Both score the **same 10 diagnostic sets** (10 candidates × 12 items × 2 axes each =
   240 band judgements per scorer) independently, against `rubric.md` only, with no
   discussion first.
3. **Compute per-axis agreement** (statistics below). Then, and only then, discuss
   disagreements.
4. **Any axis below the floor gets its cells rewritten, not re-explained.** If a scorer
   needed a verbal gloss to apply a cell, the cell is wrong — the grader will never get
   the gloss.
5. Re-measure on 10 fresh sets after rewriting.

### The statistics, named exactly

Bands are **ordinal**, not nominal, so plain Cohen's κ is the wrong statistic — it treats
a 2-vs-3 disagreement as identical to a 0-vs-3 one. Report all four of these per axis:

| Statistic | Why | Proceed threshold | Rewrite the cell below |
| --- | --- | --- | --- |
| **Quadratic-weighted κ** | Correct for ordinal bands; penalises distant disagreement more | ≥ 0.60 | 0.40 |
| **Exact agreement %** | Interpretable; κ can look fine while raters rarely match | ≥ 50% | 35% |
| **Adjacent agreement %** (within 1 band) | Catches the catastrophic disagreements that matter | ≥ 90% | 80% |
| **Mean signed difference** (scorer A − B) | Detects a systematically harsher scorer, which κ hides entirely | within ±0.25 bands | — |

Use **Krippendorff's α (ordinal)** instead of weighted κ if a third scorer joins or labels
are missing.

**Report per axis. Never report one aggregate agreement number.** Graders and humans alike
fail on one or two specific axes, and an aggregate hides exactly the thing worth knowing.
Prior expectation, stated in advance so it can be wrong: `tradeoff_articulation` and
`communication_collaboration` will be the weakest, because both are judgements about the
form of an answer rather than its content.

### Sample-size honesty

With n = 10 candidates per axis, the standard error on weighted κ is roughly ±0.15. **A κ
of 0.60 at n = 10 is not distinguishable from 0.45.** So:

- n = 10 is a **screening** sample: it finds gross miscalibration and badly-written cells.
- n ≥ 50 per axis is needed before any agreement number is stable enough to defend.
- **Do not hand a κ computed from fewer than 50 labelled cases to the GTM agent.** It will
  end up in public copy, and "our grader agrees with human interviewers at κ = 0.71" is a
  falsifiable claim about a number with a ±0.15 error bar. This is the single most likely
  way this pack produces a dishonest marketing claim.

---

## PHASE 1 — Build the golden set

### Composition: 30 diagnostic sets, deliberately unbalanced

A random sample of volunteers will cluster in the middle and leave both tails untested,
and the tails are where graders fail.

| Count | Source | Purpose |
| --- | --- | --- |
| 12 | Real candidates recruited from the cohort (r/ExperiencedDevs, ML-infra Discords), paid, told they are helping calibrate | The actual distribution |
| 4 | Practitioners who pass these loops, answering normally | Establishes that band 3 is reachable |
| 4 | Practitioners asked to answer **at the mid-level bar on purpose** | The 1/2 boundary, which is where percentile claims live |
| 10 | **Adversarial plants, authored** (below) | Each targets one specific grader failure |

Real transcripts cannot be replaced by synthetic ones for the first 20. A grader tuned
only on model-written answers learns to grade model-written answers, which is a different
distribution from a nervous human speaking for 60 seconds.

### The 10 adversarial plants

Cheap to write, highest-yield test cases in the plan. Each has a **required** grader
outcome; failing one is a blocking defect, not a tuning note.

**Written: [`calibration-plants.json`](calibration-plants.json).** Hand-graded against the
rubric in [`dry-run-report.md`](dry-run-report.md) — 9 of 10 passed and the exercise found
three rubric defects, all since fixed. Note that the dry run was self-grading, so it
measured internal consistency only; the plants' real job starts when the grader exists.

| Plant | What it is | Required outcome |
| --- | --- | --- |
| 1. **Confident and empty** | Fluent, well-structured, correct-sounding, contains no quantity at all | `capacity_cost_estimation ≤ 1` via the hard cap. If it scores 2+, the cap is not enforced in code |
| 2. **Pros and cons, no decision** | Lists both sides of every trade-off articulately and never picks | `tradeoff_articulation ≤ 1`. The sources name this as a common real failure [IIO-1] |
| 3. **Number salad** | Many numbers, all decorative, none load-bearing, no decision changed | `capacity_cost_estimation ≤ 2`. Band 3 requires the number to have moved a decision |
| 4. **Correct but mute** | Right design, no structure, no signposting, answers a different question than asked | High on 3/4, low on `communication_collaboration`. Tests axis independence |
| 5. **Jargon-dense and wrong** | Dense correct vocabulary, conclusion contradicts a stated constraint | Must not score above band 1 on the content axes. Tests that `terms` has not become a keyword scorer |
| 6. **Collapses under pushback** | Correct answer, abandons it entirely at the first probe | `communication_collaboration ≤ 1` |
| 7. **Digs in under pushback** | Correct answer, repeats it louder, treats the probe as a misunderstanding | `communication_collaboration ≤ 1`. Both directions must fail, not just one |
| 8. **Right answer, wrong scenario** | A strong answer to a neighbouring question | Should score low. Tests the grader reads the prompt, not just the answer |
| 9. **Band 3 on one axis, 0 on another** | Deliberately spiky | Must produce a spiky scorecard. A grader that smooths toward the mean destroys the named-blind-spot reveal, which is the share mechanic |
| 10. **Verbatim `model_answer`** | The reference answer, read aloud | Should score near-ceiling. If it does not, the rubric and the model answers disagree with each other, and the rubric is probably right |

Plant 10 is a consistency check on this pack, not on the grader. Run it first.

### Labelling

- Both scorers label all 30. Disagreements adjudicated by discussion, with the **pre-
  adjudication** labels retained — agreement must be measured on independent labels, and
  overwriting them destroys the measurement.
- Labels stored per `(transcript_id, axis)` with the quote each scorer relied on. The quote
  is what makes a later disagreement diagnosable.
- Freeze the set. Re-tuning against a set the grader has already been fit to measures
  nothing; hold back 10 of the 30 as a **test set never used for tuning**.

---

## PHASE 2 — Item analysis on the 12 diagnostic items

The brief's original target — "a strong candidate gets ~8/12" — was written for multiple
choice. These items are open response graded 0–3, so the equivalent checks are:

| Check | Statistic | Healthy | Action if not |
| --- | --- | --- | --- |
| Item difficulty | mean band per item across candidates | 1.2 – 2.0 | <1.0: prompt is unclear or unfair, not hard. >2.2: not discriminating |
| Item discrimination | correlation of item band with the candidate's composite | ≥ 0.25 | <0.15: the item measures something unrelated. Replace it |
| Floor / ceiling | % of candidates at band 0, % at band 3 | neither >40% | A 60%-at-0 item usually means the prompt withholds something the answer needs |
| Axis reliability | Cronbach's α across the 4 items of each axis | ≥ 0.6 | <0.5: the four items are not measuring one axis. Likeliest culprit: `communication_collaboration`, where the four items differ in whether pushback occurs |
| Answer length | words spoken | median under 170 | Items whose answers systematically run long are over-scoped for 60 seconds |

**Expect to cut items.** 12 items that all survive first contact would be surprising; plan
to author 4–6 spares from the same families so the instrument stays at 12 after cuts.

### The percentile problem — a content decision, not a GTM one

The share artifact's credibility rests on the percentile, and the percentile cannot exist
before the cohort does.

- **Show no percentile until n ≥ 200 completions.** Until then the reveal shows the band,
  the named blind spot, and the named strength — which the playbook already says is the
  substantive part — and says plainly that percentiles unlock once the cohort is large
  enough. An honest absence is cheaper than a number that moves 20 points in week two.
- **Re-baseline at n = 200, 1,000, and 5,000**, and expect the distribution to shift:
  earliest traffic arrives through a sharer's own network and is not representative.
- Percentiles are computed **per axis as well as composite**, because the named blind spot
  is an axis-level claim.
- Store the norm version on every completed attempt, so a user's old scorecard can still
  be explained after re-baselining.

---

## PHASE 3 — Measure the grader against the humans

Only after Phase 0 clears. Same four statistics, per axis, grader vs the adjudicated human
label, on the **held-back 10** as well as the 20 used for tuning.

| Gate | Threshold | Meaning if missed |
| --- | --- | --- |
| Weighted κ per axis | ≥ 0.60 on at least 5 of 6 axes; no axis below 0.40 | Tune the prompt. If one axis stays low across prompt revisions, the rubric cell is the problem |
| Adjacent agreement per axis | ≥ 90% | The grader is making catastrophic misreads, not boundary calls |
| **Mean signed error (grader − human)** | within **±0.20 bands**, and **never above +0.20** | **This is the flattery number.** Positive bias means systematic generosity, and it can coexist with acceptable κ |
| All 10 plants | every required outcome met | Blocking. A failed plant is a defect, not a score |
| Hard caps | 100% enforced in code, verified by test | A cap that lives only in the prompt is not a cap |
| Evidence quotes | every score has a quote; every 3 has a quote containing the consequence | A 3 without a consequence quote is the grader's opinion |

### The distribution check, which matters more than κ

Agreement can be acceptable while the grader is still generous, because κ measures
correspondence on cases seen and says nothing about the shape of the output on live
traffic. After the first 100 real sessions, plot the composite histogram:

- **A real left tail must exist.** If no session in 100 scores below band 1 composite, the
  grader is not using bands 0 and 1 and the product is flattering.
- **Band 0 must appear.** Across 100 sessions, some axis should be 0 somewhere. A grader
  that never issues 0 has collapsed a 4-band scale into 3.
- **Band 3 must be rare.** If more than ~15% of axis scores are 3, the band-3 requirement
  (the result changed a decision) is not being checked.
- Prior expectation, recorded in advance: a self-selected prep-tool cohort should centre
  near composite **1.3–1.7**. A mean above 2.0 is a flattery signal regardless of κ.

### Tune the prompt, not the rubric

Unless Phase 0 showed the rubric is the problem. Changing the rubric to match the grader is
the failure mode that makes the whole pack circular: the rubric then measures what the
model happens to do, and the practitioner-legitimacy claim is gone.

Every change gets a `grader_version`. Re-run the full gate on the **held-back test set**
after any material prompt change, and log the result — the comparison across versions is
what tells you a change helped rather than overfit.

---

## Re-calibration triggers

Not a one-time step. Re-run the Phase 3 gate when any of these happen:

- The interviewer or grader prompt changes materially.
- The underlying model version changes. **This includes a silent provider-side update** —
  pin model versions explicitly, because an uncontrolled model change invalidates the
  calibration without any commit to point at.
- New scenarios are added to the bank (spot-check 5, not the full set).
- Any rubric cell is rewritten.
- Monthly on live traffic regardless, as a distribution check only — the full κ measurement
  needs fresh human labels and is quarterly at most.

Alert on **drift in the mean signed error on live sessions**, which is the earliest cheap
signal that the grader has started flattering, and needs no new human labels to compute
against a rolling baseline.

---

## Cost and schedule

Honest estimate so this can be approved or rejected rather than discovered mid-build.

| Step | Effort | Dependency |
| --- | --- | --- |
| Author the 10 adversarial plants | ~1 day, content side | Now. Nothing blocks this |
| Practitioner review of `rubric.md` + 12 items | ~4 hours × 2 practitioners, paid | Before any labelling. **This is the gate on everything** |
| Phase 0 inter-human agreement (10 sets) | ~6 hours × 2 scorers | Needs 10 real diagnostic sets |
| Recruit + record 20 real sets | 2–3 weeks elapsed, mostly waiting | Needs the diagnostic live (Phase 2 of the build) |
| Phase 2 item analysis | ~1 day analysis | Needs 30 labelled sets |
| Phase 3 grader measurement | ~2 days per tuning round, budget 3 rounds | Needs Phase 0 cleared and the grader built |
| Reach n = 50 per axis for a defensible κ | ongoing, weeks | Needs live traffic |

**Critical path is practitioner time, not model time.** The practitioner review of the
rubric is the gate on all of it, it costs about 8 paid hours, and it can start today
against this pack as written.

---

## What this plan cannot fix

1. **If the rubric is not legitimate, calibration will not reveal it.** Two scorers can
   agree perfectly on a rubric that no real interviewer would recognise. Agreement measures
   consistency, never validity. Validity comes only from practitioner review and,
   eventually, from `outcome_reported` — whether people who score well pass real loops.
2. **n = 20–30 is a screening sample.** It finds gross miscalibration, not subtle bias, and
   it cannot support a published agreement figure.
3. **Outcome validity is the real test and it takes months.** The strongest possible claim
   is that scores predict loop outcomes. That needs `outcome_reported{result}` at volume,
   it will be self-selected and noisy, and it is a year-one measurement, not a launch one.
   Do not imply it earlier.
4. **The percentile is a norm, not a standard.** It says where someone sits among
   self-selected prep-tool users, which is a harder reference group than the general
   applicant pool and should be described that way rather than as "the cohort".

---

## Handoff notes

**To the build agent:** the hard caps in `rubric.md` are code, not prompt text, and there
is a test per cap. `grader_version` and `norm_version` on every row. The 10 plants belong
in the test suite as fixtures — they are regression tests on grader harshness, and they are
the cheapest protection against the grader drifting generous across prompt revisions.
Percentile display is gated at n ≥ 200.

**To the GTM agent:** no calibration number exists yet. When one does, it will carry a
sample size and an error bar, and both belong in any public claim. The defensible claims
before calibration are about *method* — a separate out-of-band judge, caps that prevent a
score without a number, every score carrying quoted evidence, a rubric grounded in
published guidance with the departures stated — not about agreement. Also: the percentile
is against self-selected prep-tool users, not against all applicants, and saying so is
better positioning than the vaguer claim, because this cohort checks.

Cited keys resolve in [`rubric.md`](rubric.md#sources).
