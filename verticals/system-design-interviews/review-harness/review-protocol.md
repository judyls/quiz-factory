# REVIEW PROTOCOL — the output contract

Do **Part A before Part B**. Do not read other reviewers' findings. Write
`findings/<your-slug>.md`.

---

## Part A — Blind scoring (do this first)

Open `blind-scoring-set.md`. For each of the 5 answers, score **only the listed axes**
against `../rubric.md`.

For each (answer, axis) produce exactly this:

```
Answer 1 / capacity_cost_estimation: <0|1|2|3>
  cell clause applied: "<the clause from the band you chose>"
  evidence: "<verbatim quote from the candidate>"
  admits another reading: <no | yes — and which band, and why>
```

Rules:
- **Do not hedge to the middle.** If you believe 1, score 1. Scoring 2 to be safe destroys
  the measurement this part exists for.
- If a cell genuinely admits two bands, score the one you believe **and** say so in
  `admits another reading`. That flag is the single most valuable output of Part A.
- Apply the rubric as written, not as you would have written it. Part B is where you say it
  should be different.
- If you cannot score an axis from the transcript, say so and say what is missing.

End Part A with: **which single rubric cell was hardest to apply, and why.**

---

## Part B — Critique from your domain

### B1. Axis legitimacy
Do these six axes correspond to what a system design round actually scores? Answer
directly. Then state **what your answer rests on** and **what would change your mind**. If
you are reasoning from how interviews are generally described rather than from loops you
have run, say that plainly — it changes how this finding should be weighted.

### B2. Scenario realism — your domain only
Take the scenarios closest to your experience. For each: realistic / realistic-but-wrong-in-
one-detail / not realistic, and **the single thing most wrong with it**. A constraint that
would never be stated that way, a number that could not occur, a framing that doesn't match
how the problem actually arrives. Be specific enough to act on.

### B3. Arithmetic
Check the numbers in the scenarios you reviewed and in `rubric.md` Appendix B. Report any
you believe wrong, **with your own calculation**. "Seems off" is not a finding.

### B4. The band 2/3 boundary
Having applied it in Part A: is it in the right place? Too harsh, too generous, or
unapplicable? This is the boundary the whole instrument rests on.

### B5. Top 3 defects, ranked
Most to least serious. For each: file, what is wrong, why it matters, what you would do.

### B6. Sign-off
What would you refuse to let ship as-is? And: would you put your name on this rubric as
legitimate? Yes or no, then the caveat.

### B7. Epistemic status — required
- Which of your findings are **checkable facts** (arithmetic, internal contradictions)?
- Which are **domain judgement** a practitioner in your area would mostly share?
- Which are **guesses about interview practice** that need a human to confirm?
- What did you have to assume because the pack did not say?

A report without a candid B7 is not usable. Over-claiming here is worse than being unsure,
because the whole point of this harness is to know which findings need a human.

---

## Hard rules for every reviewer

1. **Never claim a named company asks a specific interview question**, or describe any
   employer's actual interview process as fact. You may say what problems are common in a
   domain. Frame interview practice as "reported" or "in my experience of the category".
   This matches the pack's own sourcing discipline.
2. **Cite file and line** for anything you criticise.
3. **Distinguish "this is wrong" from "I cannot verify this."** Use both freely.
4. **Be concretely useful.** "Needs more rigour" is not a finding. "The decode-step floor in
   Appendix B assumes TP=4 with no communication overhead; at realistic all-reduce cost it
   is closer to Xms, which moves the recommended batch window" is a finding.
5. **Disagree with the pack where you disagree.** A report that validates everything is
   evidence the harness failed, not that the pack is good.
