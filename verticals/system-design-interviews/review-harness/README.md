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

- **Part A — blind scoring.** Score the answers in `blind-scoring-set.md` against
  `../rubric.md`. Expected scores are stripped. This is the inter-rater measurement.
- **Part B — critique.** Review `../rubric.md`, `../questions.json`, `../prompts.md` from
  the reviewer's domain. Arithmetic, realism, defects, sign-off.

**Off limits to reviewers:** `keys/`, `../calibration-plants.json`, `../dry-run-report.md`,
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
| `blind-scoring-set.md` | The candidate answers, expected scores stripped. Generated, not hand-written |
| `generate-blind-set.py` | Generates the above from the fixtures, and asserts no expected score leaked |
| `personas/*.md` | The 5 reviewer briefs |
| `findings/run-<N>/` | One report per reviewer per run, plus that run's synthesis and answer key |

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

## Blinding defects fixed after run 2

Two self-disclosed by reviewers again, one caught by all five.

3. **The answer key was in the directory reviewers write into.** Listing `findings/run-2/`
   to create a report returned the key's filename. The reviewer did not open it and said so.
   Keys now live in `keys/`, which is off limits and which nobody needs to list.
4. **The set claimed the pairing was hidden when it was not.** Two answers quoted
   byte-identical prompts while the preamble forbade inferring which answers shared an item.
   Run 1's fix — separate the pair — does not help when the prompt text is the tell. The
   preamble now says a shared prompt is visible and carries no information about either
   score, which is true, instead of an instruction a reader can see is impossible.
5. **The protocol said "the 5 answers" when the set had 7.** A patch targeting a string
   that did not match the file, which failed silently. All five reviewers noticed.

**Lesson for re-runs:** anything a reviewer is told to read is part of the blind — and so is
anything they must *list* to do their job. Before each run, grep the allowed reading list for
expected scores and fixture names, and for counts that go stale. Every blinding defect across
both runs was in material written while thinking about blinding, so assert mechanically:
`generate-blind-set.py` aborts on a leak, and any patch to the prose must assert its target
exists before replacing it.

## Re-running

Re-run when `rubric.md` changes materially. `python3 generate-blind-set.py <run> >
blind-scoring-set.md` — never hand-edit the set, so it cannot drift from the fixtures. The
script re-randomises labels per run, refuses to reuse a label from any earlier run, and
aborts if an expected score, a fixture id or a required outcome survives into the output.

Then grep every file the reviewers are allowed to read for fixture descriptions, not just
fixture names: run 2 found `rubric.md` saying a negative-control fixture existed for the
relevance gate, which was enough to telegraph one cell of the set.

Findings go in `findings/run-<N>/`. Keep earlier runs: the only way to know whether a fix
worked is to compare agreement on the answers the two runs share.

### Runs

| Run | Answers | Axes covered | Against |
| --- | --- | --- | --- |
| 1 | 5 | 3 of 6 | `908abee` — the pack as first written |
| 2 | 7 | 6 of 6 | `d9de968` — after the 9 fixes from run 1's queue |
