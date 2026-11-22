# CONTENT AGENT BRIEF — <<VERTICAL NAME>>

> Paste as the opening message of a dedicated session.
> **This is the moat.** The web app is a weekend. A calibrated rubric and 40 genuinely
> discriminating scenarios are not, and they are the only part a competitor can't clone
> from a screenshot.
>
> Worked example: `verticals/system-design-interviews/02-CONTENT-AGENT.md`.

---

## What you own

1. The **`<<N>>`-axis rubric** with observable behaviors at 4 levels.
2. **`<<N>>` scenarios** with reference solution trees.
3. The **`<<N>>` diagnostic items**.
4. The **grader calibration set** and the agreement measurement.
5. The **public scenario pages** — worked at-bar answers that double as acquisition.

You don't build UI. You don't write the launch plan.

---

## Part 1 — The rubric

`<<4-7 AXES. Use the industry's own vocabulary, not a taxonomy you invented — a
practitioner has to recognize it instantly. At least one axis must be
communication/stakeholder-facing: in almost every vertical that's the real ceiling on
advancement, it's the axis nobody has ever scored for them, and it's therefore the most
shareable finding.>>`

| Axis | What it measures |
| --- | --- |
| | |

### The 4-level scale

Write **observable behaviors, not adjectives**, in all `<<N×4>>` cells:

```
0  No signal   — never addressed
1  Below bar   — addressed but wrong, vague, or only when directly prompted
2  At bar      — does the thing competently when it matters
3  Above bar   — does it unprompted, with precision, and anticipates the consequence
```

**The pattern for every "above bar" cell:** the person doesn't just perform the behavior,
they *let the result of it change their decision*. That's the actual signal, in every
vertical. Write every level-3 cell that way.

### Grounding

Do not invent the rubric from imagination. Ground each axis in observable sources —
published guides, real rubrics, practitioner write-ups, the structure of respected existing
courses — and **cite them inline in the rubric file**. An invented rubric reads as
invented, and a professional cohort detects it fast.

---

## Part 2 — The scenarios

### Positioning constraint

`<<THE SURFACE FRAMING THAT IS THE WEDGE>>` is the surface. `<<THE TRANSFERABLE UNDERLYING
SKILL>>` is the substance. Keep the surface — it's the positioning, the SEO, and the reason
they pick you over a generic course. State the distinction explicitly on the public pages:
it's genuinely useful to the user and it inoculates you against the "this is hype"
reaction.

### Target: `<<N>>` scenarios across these families

`<<LIST FAMILIES, 4-6 OF THEM>>`

### Scenario schema

```yaml
slug:
title:
family:
axis_weights: {}
prompt: >            # one paragraph, realistic, hard constraints stated up front
constraints: []
required_beats: []   # what an at-bar person must reach
traps: []            # plausible wrong turns; the counterpart probes toward these,
                     # multiple-choice distractors, or the `bad` field, for free
followup_tree: []    # escalating probes, CONDITIONAL on what the person has said
at_bar_answer: >     # the worked answer. Grader contrast + published on /q/[slug]
sources: []
```

`followup_tree` is the most important field. It's what makes the counterpart feel like a
real human rather than a question-reader: the probe is conditional on what was already
said, and it escalates when they're doing well. **≥6 conditional branches per scenario.**

### The diagnostic items

- Scenario-based forced tradeoff under constraints. Never trivia — trivia is lookup-able
  and measures recall, not the thing the real event tests.
- **Pick the format first.** Multiple choice is the default; open response if any axis is
  about how the person communicates, because multiple choice cannot measure that. See the
  format note in `playbook/QUIZ-FACTORY.md`, Layer 1.
- If multiple choice: 4 options, **≥2 defensible-looking**.
- **Every distractor is a real mistake a competent person makes.** An obviously-wrong
  distractor wastes one of only `<<N>>` slots. Source from `traps`.
- ≥2 items requiring an actual number or order of magnitude.
- Each item maps to 1–2 axes; ≥2 items per axis.
- **Target difficulty: a strong candidate gets ~`<<N-4>>`/`<<N>>`.** If the median is near
  perfect the items don't discriminate and the percentiles become meaningless.

---

## Part 3 — Grader calibration

**This step determines whether the product retains.** A counterpart that flatters is
detected in one session and never reopened.

1. **Collect ≥20 transcripts.** Recruit from the cohort; pay for them if needed. Include
   deliberately weak and deliberately strong runs.
2. **Hand-score all of them**, with a second scorer on ≥10. Measure inter-human agreement
   *first* — if humans don't agree on an axis, the axis is badly defined and must be
   rewritten before you tune any model.
3. **Run the grader**, compare per-axis. Report confusion **per axis**, not one aggregate —
   graders fail on specific axes, and the judgment-on-form axes (communication, tradeoff
   articulation, and their equivalents) are the usual offenders.
4. **Tune the prompt, not the rubric**, unless step 2 showed the rubric is the problem.
5. **Check the distribution for flattery.** Plot the histogram. No real left tail means the
   grader is generous regardless of its agreement numbers. Enforce the hard caps from the
   build brief in code, not just in the prompt.
6. **Version it.** `grader_version` on every grade row.

Re-run calibration whenever the counterpart or grader prompt changes materially.

---

## Part 4 — The public scenario pages

Each scenario becomes `/q/[slug]`: the problem, constraints, the tradeoff space, the traps,
and the worked at-bar answer.

Write them to be **the best free answer on the internet to that specific question**. A page
that is obviously a teaser converts worse than a complete one, because the complete one
earns the link and the trust — and what you're selling, repeated scored practice, isn't
substitutable by reading the page anyway.

Don't fabricate claims about what a specific organization asks or does. Say "reported,"
cite where, or frame it as representative of the category.

---

## Handoff contract

To **build**: rubric as structured data (all `<<N×4>>` cells), `<<N>>` scenarios in the
schema, diagnostic items with axis mappings, counterpart + grader prompts, calibration
report.

To **GTM**: scenario slugs and titles, the rubric axes in plain language for public copy,
and the calibration numbers — they're the strongest credibility claim the product has and
the only honest basis for saying the scoring is real.
