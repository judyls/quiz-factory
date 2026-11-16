# Quiz Factory

A reusable system for shipping skill-diagnostic quizzes that spread on their own and
graduate into a paid AI practice product.

**One vertical is live in here:** AI-lab system design interview prep. The playbook and
templates are vertical-agnostic — point them at a new cohort and they produce the next one.

---

## Structure

```
playbook/      doctrine. vertical-agnostic. read first.
templates/     blank briefs to copy per vertical.
verticals/     one folder per instantiation.
```

| Path | What it is |
| --- | --- |
| **`playbook/QUIZ-FACTORY.md`** | **The core script.** Qualification gates, the 5-layer funnel architecture, non-negotiables, build order, kill criteria. Vertical-agnostic. |
| `playbook/VIRALITY-TEARDOWN.md` | Protocol for reverse-engineering a prior quiz's funnel data, plus the mechanics library to port |
| `templates/CONFIG.template.md` | Gate scoring + config. The first artifact of any new vertical |
| `templates/BUILD-AGENT.template.md` | Build brief scaffold |
| `templates/CONTENT-AGENT.template.md` | Rubric + question bank + grader calibration scaffold |
| `templates/GTM-AGENT.template.md` | Positioning, pricing, launch, virality scaffold |
| `verticals/system-design-interviews/` | Fully worked example: CONFIG, three filled briefs, research notes |
| `verticals/_archive-ceo-founders/` | The original vertical, and why it was replaced |

---

## To add a new vertical

1. **Copy `templates/CONFIG.template.md`** → `verticals/<slug>/CONFIG.md`. Fill it.
   Score the 5 gates honestly. **Fewer than 4 strong: stop.** Don't build a quiz for a
   cohort that fails this — that's the lesson from `_archive-ceo-founders/`.
2. **Run `playbook/VIRALITY-TEARDOWN.md`** against whatever quiz came before, so the kill
   thresholds are real numbers instead of industry averages.
3. **Copy the three agent templates** into the same folder and fill the `<<PLACEHOLDERS>>`.
   Read the system-design versions alongside them for the level of specificity expected.
4. **Run three separate sessions** — content, build, GTM, in that priority order.

## To run a vertical

Three agents, three sessions. **Do not merge them.** A single agent holding both build and
GTM will quietly reshape the go-to-market to fit whatever it already built, and will invent
features to justify a launch plan.

1. **Content** — paste `02-CONTENT-AGENT.md`. The critical path: without real questions and
   a calibrated grader you have a toy that flatters people, and flattery kills retention in
   prep products.
2. **Build** — paste `01-BUILD-AGENT.md`. Can run in parallel with content against the seed
   scenarios.
3. **GTM** — paste `03-GTM-AGENT.md`. Starts the day the free diagnostic is live, not after
   launch.

Each brief ends with a handoff contract naming what it owes the other two.

---

## The five things that make or break any vertical here

1. **Qualify before you build.** Dated pain, status at stake, a credible rubric, proven
   spend, a public watering hole. Four of five or stop.
2. **No auth before value.** The diagnosis is free, always. The free reveal *is* the
   growth engine, not a lead magnet for it.
3. **Separate the counterpart model from the grader model.** One model doing both leaks the
   rubric into its own questions and coaches instead of testing. This single mistake is why
   most AI practice products are useless.
4. **Ship the free diagnostic alone and measure share rate first.** If it doesn't spread,
   a better AI counterpart won't rescue it — and the counterpart is the expensive part.
5. **Price in units of the event, not the month.** The need is episodic. Name the retention
   bridge up front or accept that it's a one-shot business.
