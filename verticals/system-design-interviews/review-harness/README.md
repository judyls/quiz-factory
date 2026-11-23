# REVIEW HARNESS — simulated practitioner review

Five reviewer agents, each with a different domain background, review the content pack and
independently score a blind set of candidate answers. Built as a **pre-screen before real
practitioner review**, not a replacement for it.

Run from the repo root. Outputs land in `findings/`.

---

## What this can and cannot tell you

Read this before acting on anything in `findings/`.

**It can find:**
- Arithmetic that is wrong. Numbers are checkable and a competent reviewer checks them.
- Rubric cells that admit two readings — measured directly by whether five independent
  readers land on the same band for the same answer.
- Scenarios that are unrealistic in a way a domain practitioner would notice: a constraint
  that would never be stated, a framing that doesn't match how the problem actually arrives.
- At-bar reference answers that are not actually at bar.
- Internal contradictions between `rubric.md`, `questions.json` and `prompts.md`.

**It cannot tell you:**
- **Whether real interview loops score these six axes.** That is institutional knowledge
  held by people who have sat on hiring committees. A model has the internet's impression
  of that job, not the job. A persona prompt will nonetheless assert an answer confidently,
  which makes this the most dangerous output in the set.
- Whether the level-mapping thresholds match any real level.
- Whether band 1 reads as insulting to someone who just failed a loop.
- Anything requiring a named company's actual practice.

**Therefore:** treat the agreement measurement and the technical defects as real findings.
Treat every claim about what interviews are like as a hypothesis to put to a human. The
`epistemic_status` section in each report exists to keep that line visible, and reviewers
are required to fill it.

## Why the personas are not employer badges

Each reviewer is described by **domain and role experience** — someone who has run
inference serving at scale, someone who has operated a hiring rubric at volume — with a
company named only as shorthand for the kind of problem they have lived with. Differentiating
by badge alone produces stylistic variation, not different judgment, and it invites the
model to fabricate claims about what that employer asks. Every persona carries a hard rule
against doing so, which matches the pack's own sourcing discipline: never claim a named
company asks a specific question.

## Protocol

Each reviewer does Part A **before** Part B, and does not read the other reviewers.

- **Part A — blind scoring.** Score 5 answers in `blind-scoring-set.md` against
  `../rubric.md`. Expected scores are stripped. This is the inter-rater measurement.
- **Part B — critique.** Review `../rubric.md`, `../questions.json`, `../prompts.md` from
  the reviewer's domain. Arithmetic, realism, defects, sign-off.

Ordering matters: scoring blind first means Part B's critique is informed by having
actually tried to apply the rubric, rather than by reading it as prose.

## Files

| Path | What |
| --- | --- |
| `review-protocol.md` | What every reviewer must produce. The output contract |
| `blind-scoring-set.md` | 5 candidate answers, expected scores stripped |
| `personas/*.md` | The 5 reviewer briefs |
| `findings/` | One report per reviewer, plus the synthesis |

## Re-running

Re-run when `rubric.md` changes materially. The blind scoring set is regenerated from
`calibration-plants.json` by the snippet in this repo's history — regenerate it rather than
editing it by hand, so it cannot drift from the fixtures.
