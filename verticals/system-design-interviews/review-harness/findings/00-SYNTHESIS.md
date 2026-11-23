# SYNTHESIS — five simulated reviewers

Run 2026-11-23 against commit `908abee`. Five reviewers, each scoring a blind set before
critiquing. Full reports in this directory; this file is the roll-up and the defect queue.

**Headline:** the rubric's *reliability* held up far better than expected and its
*arithmetic* did not. 8 of 10 blind cells were unanimous. Appendix B teaches four wrong
numbers. The public level claim is not computable at all.

**What this run is:** a pre-screen. Five models, not five engineers. Every claim below is
either (a) arithmetic I re-derived myself, marked ✓, or (b) a judgement that still needs a
human. The reviewers were required to separate these in their own reports and all five did.

---

## 1. Inter-rater agreement — the measurement this run existed for

| Cell | R1 | R2 | R3 | R4 | R5 | spread | my expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A1 `capacity` | 1 | 1 | 1 | 1 | 1 | 0 | ≤1 ✓ |
| A1 `tradeoff` | 2 | 2 | 2 | 2 | 2 | 0 | may reach 2 ✓ |
| A2 (03a) `capacity` | 1 | 1 | 1 | 1 | 1 | 0 | ≤1 ✓ |
| A2 (03a) `tradeoff` | 1 | 1 | 1 | 1 | 1 | 0 | ≤1 ✓ |
| A3 (03b) `capacity` | 2 | 2* | 2 | 2 | 2 | 0 | ==2 ✓ |
| A3 (03b) `tradeoff` | 1 | 1 | 1 | 1 | 1 | 0 | ≤1 ✓ |
| A4 (08) `requirements` | 1 | 1 | 1 | 1 | **0** | 1 | ≤1 ✓ |
| A4 (08) `capacity` | 1 | 1 | 1 | 1 | 1 | 0 | ≤1 ✓ |
| **A5 (09) `capacity`** | **1** | **2** | **2** | **1** | **2** | 1 | **==3 ✗** |
| A5 (09) `HLD` | 0 | 0 | 0 | 0 | 0 | 0 | ≤1 ✓ |

\* R2 self-reported contamination on this cell (see §5) and asked for it to be excluded.
Excluding it does not change any conclusion.

- **Exact agreement across all five: 80%.** Adjacent: **100%**.
- `calibration-plan.md` floors are ≥50% exact and ≥90% adjacent. **Both cleared comfortably.**
- My expected outcome held on 9 of 10. It failed on one, and failed unanimously.

### The recorded prior was wrong, which is the most useful thing here

`calibration-plan.md` states in advance: *"`tradeoff_articulation` and
`communication_collaboration` will be the weakest, because both are judgements about the
form of an answer rather than its content."*

**All five reviewers independently nominated `capacity_cost_estimation` as the hardest axis
to apply**, by five different routes: band 2's undeclared conjunction (R1), the 1-vs-2 call
on A5 (R2), band 0 vs 1 colliding with the cap (R3), band 3's counterfactual being
unevidenceable from a transcript (R4), and band 2 being the softest band in the file (R5).
`tradeoff` was unanimous on every cell where it appeared. The prior was recorded so it could
be falsified, and it was.

### Plant 09 is broken, and five reviewers caught it

I asserted `capacity == 3`. Scores came back 1, 2, 2, 1, 2 — **nobody gave it a 3**. R2 and
R5 independently found why, and I re-derived it: ✓ the plant claims blended cost is 37% of
an all-70B baseline *and* lands near $0.55, which implies a baseline of $1.49 — i.e. the
ceiling itself. Circular. ✓ Its "reverses below a 20% small-model share" threshold is false
under its own numbers: at 20% the blended figure is $1.22, still inside the $1.50 ceiling.

Plant 09's entire job is to test that the grader does not smooth a 3/0 profile toward 2/2.
It cannot do that job while its own arithmetic is fabricated. **The plant needs rewriting,
not the rubric.** Note what this means: the band-3 cell correctly refused a plausible-sounding
answer with invented numbers. That is the rubric working.

---

## 2. Convergent defects — three or more reviewers, independently

| # | Defect | Found by | Status |
| --- | --- | --- | --- |
| C1 | Appendix B: "32GB is a fifth of a node's HBM" — it is **5.1%** of a 640GB node, off 3.9× | R1 R2 R4 R5 | ✓ re-derived |
| C2 | `followups` that hand over the reference answer's insight, breaking Prompt 1 rule 1 — and then `first_raised_by` clamps the candidate for using the leak | R2 R4 R5 (**three different probes**) | ✓ verified |
| C3 | `eval-infra-per-commit-cost` understates cost 3–6×: judge calls never costed, consumed GPU-minutes priced as provisioned fleet | R3 R4 R5 | agreed magnitude |
| C4 | **Per-axis aggregation is specified nowhere.** Nothing maps the 4 per-item scores to the 1 axis score the level mapping consumes. Under `mean`, "any axis at 0" can never fire; under `min` it almost always does | R3 R5 | ✓ verified — no such rule exists |
| C5 | Band 2 is a 3–5-clause undeclared conjunction in **6 of 6** cells, while band 3 now declares exactly one required clause. My band-3 fix pushed the problem down into band 2 — which is the band every row of the level mapping actually reads | R1 R4 R5 | ✓ verified |
| C6 | `annotation-throughput-vs-agreement`'s leverage claim is **backwards**: κ 0.62→0.80 buys ~1.29×, doubling the pool buys 2× | R3 R4 | ✓ re-derived |
| C7 | The contrast-provenance trigram check is theatre: structurally rigged to pass, blind to copied *conclusions*, and it false-fires on the strongest candidates | R2 R3 | accepted — delete it |

---

## 3. Arithmetic errors I re-derived myself

All in `rubric.md` Appendix B or the model answers it backs. Appendix B is what anchors the
judge, so these are the highest-severity findings in the run.

| Claim | Pack says | Correct | Why |
| --- | --- | --- | --- |
| 100k-token prefill, 70B | ~9s | **~17s** | Attention FLOPs omitted entirely. At 100k they are **48%** of the total. Crossover where attention equals the dense term is `N/(d·L)` = **106,811 tokens** — so the formula is fine at 10k and wrong exactly in the long-context regime the pack is about |
| Decode step floor, batch 64 @ 2k ctx | 10.4ms | **13.6ms** | KV reads omitted; at batch 64 they are 30% of bytes moved (41.9GB on top of 140GB of weights) |
| Aggregate throughput | ~6,000 tok/s | **~4,714 tok/s** | follows from the above |
| Cost per 1M output tokens | $0.37 | **$0.47** | follows |
| 100k KV vs node HBM | "a fifth" | **5.1%** | 32.8GB of 640GB |
| 4PB global shuffle | 11h | **22h** | A shuffle reads *and* writes 4PB. 8PB at 100 GB/s |

---

## 4. Where a reviewer was wrong, and why it still matters

R4 claimed 2,000 GPUs need 3.8–7.5 GB/s of read bandwidth. I get **~7.6 MB/s** of token
bytes at that training throughput — off by ~1000×, in the direction of R4's own conclusion.

But the discrepancy *is* the finding. Reading the whole 4PB corpus once per 30-day epoch is
1.5 GB/s; once per day is 46 GB/s; the token bytes the GPUs actually consume are MB/s. Three
framings, three orders of magnitude — because **the scenario conflates the 4PB corpus with
what the GPUs read**, which was R4's structural point. Their conclusion (bytes are not the
binding term; access pattern and IOPS are) stands on better evidence than their number.

Recorded because a harness that only reports reviewer agreement, and never where a reviewer
is wrong, is measuring the wrong thing.

---

## 5. Two defects in the harness itself

Both self-disclosed by reviewers, unprompted. Both mine.

1. **`calibration-plan.md` leaks expected scores** (lines 115–121 carry the full plant
   outcome table) and the protocol listed it as optional Part B reading. R2 disclosed it,
   named the affected cell, and asked for its exclusion. **Fix:** remove it from allowed
   reading, or strip the table into a separate file.
2. **The blind set was partially de-blinded.** ✓ Verified: my generator labelled answers
   `A01`, `A03`, `A03`, `A08`, `A09` — so the labels leak plant numbers, and answers 2 and 3
   visibly share an ID, revealing them as a matched pair. Worse, `rubric.md` and `prompts.md`
   both name "plant 08b is the control". R1 flagged its own A08 scores as "the least
   independent thing in the report". **Fix:** opaque IDs, never adjacent-place two answers to
   one prompt, move plant commentary out of the rubric.

---

## 6. Sign-off

| Reviewer | The six axes / 24 cells | The level claim | Appendix B / model answers |
| --- | --- | --- | --- |
| R1 on-device | **yes** | — | **no** — three wrong numbers |
| R2 hosted API | **yes** | **no** until calibrated | **no** on four items |
| R3 safety/eval | **yes** | **no** | **no** on three model answers |
| R4 training | **yes** | — | **no** on Appendix B, and band 3 as phrased |
| R5 rubric operator | **yes** on the axes and all six band-1 cells | **no** | **no** on the safety-classifier answer |

**5 of 5 sign off on the six axes as legitimate. 0 of 5 sign off on the level claim.**

R5's count: **16 of 24 cells admit two readings** — band 1: 1/6 (genuinely good), band 2:
6/6, band 3: 4/6 (all by inheriting "All of band 2"), band 0: 4/6. Note the agreement
measurement came back at 80% exact *despite* that, which suggests the ambiguity is mostly
latent on these five answers rather than absent.

---

## 7. Defect queue, ranked

**Blocking any public score or level claim:**

1. **C4 — specify per-axis aggregation.** The level mapping consumes a number the pack never
   defines. This gates the share artifact, which is the growth engine.
2. **Fix Appendix B's four numbers** (§3). It anchors the judge.
3. **C5 — give band 2 the same one-required-clause treatment band 3 got**, since band 2 is
   what the level mapping reads.
4. **Rewrite three model answers**: `heterogeneous-fleet-routing` (no derivable baseline),
   `annotation-throughput-vs-agreement` (C6, claim is backwards),
   `inline-safety-classifier-budget` (adds two p99s, and R3 judges the straw man soft in the
   half that matters — "retract after the fact" is incoherent on a streaming path).
5. **C2 — rewrite the leading `followups`**, and fix the duplicate `if: at bar` branches.
   ✓ Verified: **all 12 items** have two identically-labelled `at bar` branches with no
   tie-break, which by Prompt 2's own determinism rule is a defect. R5 reported this for the
   four comms items; it is universal.

**Also:**

6. Delete the contrast-provenance row (C7); replace with required-beat coverage.
7. Resolve capacity band 0 vs 1 against the derived-quantity cap — band 0 still says "no
   quantity of any kind" while the cap says "none of their own".
8. Rewrite plant 09 so its arithmetic is sound and it can do its job.
9. Fix both harness defects (§5) before any re-run.
10. `communication_collaboration` would penalise non-native speakers and deliberate
    thinkers through four named mechanisms (R5 gives four cheap fixes). **This one needs a
    human, not a model** — it is a bias question and these reviewers are the wrong
    instrument for it.

---

## 8. What a human practitioner is still needed for

Unchanged by this run, and sharpened by it:

- **Whether the six axes are what real loops score.** 5/5 said yes; all five also marked
  that answer as the least reliable thing in their report. It remains one practitioner's
  opinion ×5, from models that share a training distribution — the agreement is close to
  worthless as evidence here.
- **The level-mapping thresholds**, once C4 makes them computable at all.
- **Whether band 1 reads as diagnostic or insulting**, and the `communication` bias question
  in item 10 above.
- **Whether the scenarios feel like the real round.** The reviewers judged realism of the
  *systems*; nobody here has sat in the chair.

The run does make the cold-outreach ask much smaller: *"here are five reviews, here are the
nine defects I already found and fixed, I need twenty minutes on the two cells that are
still contested"* is a far better opening than *"please review my rubric."*
