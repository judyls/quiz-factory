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

**Off limits to reviewers:** `../calibration-plants.json`, `../dry-run-report.md`,
`../calibration-plan.md`, and anything in `findings/`. The first two obviously carry
expected scores. **`calibration-plan.md` was missed in run 1** — it carries the full
per-plant outcome table, and a reviewer self-disclosed reading it and asked for the
affected cell to be excluded.

Ordering matters: scoring blind first means Part B's critique is informed by having
actually tried to apply the rubric, rather than by reading it as prose.

## Files

| Path | What |
| --- | --- |
| `review-protocol.md` | What every reviewer must produce. The output contract |
| `blind-scoring-set.md` | 5 candidate answers, expected scores stripped |
| `personas/*.md` | The 5 reviewer briefs |
| `findings/` | One report per reviewer, plus the synthesis |

## Blinding defects fixed after run 1

Both self-disclosed by reviewers, unprompted. Both mine.

1. **`calibration-plan.md` carries the per-plant expected-outcome table** and the protocol
   listed it as optional reading. Now off limits. The durable fix is to split that table
   out of the plan; until then the exclusion stands.
2. **The blind set's labels leaked.** Generated IDs were `A01, A03, A03, A08, A09` — they
   encoded plant numbers, and two answers visibly shared a label, exposing them as a matched
   pair on one item. A reviewer flagged its own scores on the affected answer as "the least
   independent thing in the report". Labels are now opaque, the order is arbitrary, and the
   two answers sharing an item are no longer adjacent. Separately, `rubric.md` and
   `prompts.md` each named a fixture by number; both now describe it without naming it.

**Lesson for re-runs:** anything a reviewer is told to read is part of the blind. Before
each run, grep the allowed reading list for expected scores and fixture names.

## Re-running

Re-run when `rubric.md` changes materially. Regenerate `blind-scoring-set.md` from
`calibration-plants.json` rather than editing it by hand, so it cannot drift from the
fixtures — and re-randomise the opaque labels when you do.
