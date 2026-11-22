# THE QUIZ FACTORY — generalized agent script

> Paste this whole file as the opening message of a new agent session, with the CONFIG
> block filled in. It is vertical-agnostic: the same script produced the system design
> product in `verticals/system-design-interviews/`, and will produce the next one. Blank
> scaffolds to fill are in `templates/`.

---

## Your role

You are building a **skill-diagnostic funnel**: a free assessment that is so specific it
gets shared, attached to a paid practice product that fixes what the assessment found.

You are not building a personality quiz. A personality quiz gets one burst of traffic and
dies, because it has no second use. You are building a *diagnostic with a treatment* —
the quiz is the top of a funnel, not the product. Every decision below serves that.

The product only works if all three of these are true at once. If you trade one away to
make another easier, you have built something that fails quietly:

1. **Useful** — the result tells someone something true and actionable they did not know
   about themselves, from a credible rubric. If it flatters, it dies on retention.
2. **Viral** — the result is a status-bearing artifact a person wants to put in public.
3. **Monetizable** — the gap the diagnostic exposes is painful, dated, and already has
   budget attached to it.

---

## STEP 0 — Qualify the vertical before you build anything

Score the vertical against these five gates. **Fewer than 4 of 5: stop and tell the user
the vertical is weak, and why.** Do not build a quiz for a cohort that fails this.

| Gate | Question | Why it matters |
| --- | --- | --- |
| **1. Dated pain** | Is there a specific, scheduled, high-stakes event? (an interview loop, a promo cycle, a board meeting, an exam) | A deadline converts. Open-ended self-improvement does not. |
| **2. Status at stake** | Does the result say something about the person's competence or identity that they'd want others to see? | This is the entire virality engine. No status, no shares. |
| **3. Credible rubric exists** | Can the skill be scored on observable axes a practitioner would recognize as legitimate? | Without this you get a BuzzFeed quiz: fun once, worthless twice. |
| **4. Proven spend** | Is this cohort *already* paying someone for this, at a price you can anchor against? | Never be the one teaching a cohort that the problem is worth money. |
| **5. Public watering hole** | Do they congregate somewhere observable? (a subreddit, a Slack/Discord, a hiring-season X cohort, a LinkedIn niche) | Distribution has to have a surface. |

Record the scores and the evidence. If gate 4 has no evidence, go find it — competitor
pricing pages, coaching rates, course prices — before writing a single question.

---

## CONFIG — fill this in

```yaml
vertical:            # e.g. "AI-lab system design interviews"
cohort:              # who precisely. Not "engineers" — "L5/L6 backend + infra engineers
                     # actively in or targeting frontier-lab loops"
dated_pain:          # the scheduled event that makes this urgent
status_currency:     # what the result confers. e.g. "scored at the Staff bar on tradeoffs"
scored_axes:         # 4-7 axes. Must be nameable by a practitioner. See rubric rules below.
share_artifact:      # the exact thing that gets posted. Describe the image.
price_anchor:        # what they pay today, with a source
paid_product:        # what the quiz graduates into. MUST be a practice loop, not content.
retention_bridge:    # what keeps them after the dated event passes. Critical — see below.
kill_metric:         # the number that, if unmet by week 4, means stop
```

### Rules for `scored_axes`

- 4 to 7 axes. Fewer feels crude, more makes the scorecard unreadable.
- Each must be **observable**, not dispositional. "Capacity estimation" yes.
  "Analytical mindset" no.
- At least one axis must be **communication or stakeholder-facing**. In almost every
  professional vertical this is the real ceiling on advancement, it is the axis people
  have never had scored, and it is therefore the most shareable finding.
- Each axis gets a 4-level scale with observable behaviors at each level:
  `0 no signal / 1 below bar / 2 at bar / 3 above bar`. Write the behaviors, not adjectives.

### Rules for `retention_bridge`

Diagnostic products built on a dated event have structural churn: the user succeeds and
leaves. You must name, up front, the second use of the same engine for the same person
after the event passes. Usually it is the *on-the-job* version of the same skill.
If you cannot name it, the business is a one-shot and should be priced as one.

---

## THE INVARIANT ARCHITECTURE

Five layers. Build in this order. Do not skip layer 3.

### Layer 1 — The Hook (free, zero auth)

- **Question 1 renders on first paint.** No landing page before it, no "start" button, no
  email gate, no account. Every interstitial costs you a large share of entrants.
- 10–14 questions, 5–8 minutes. Show a progress indicator with a *shrinking* count.
- Questions are **scenario-based forced tradeoffs under constraints**, never trivia.
  Trivia measures recall and is googleable; tradeoffs measure judgment and are the thing
  the cohort is actually scored on. Format: a realistic situation, hard constraints,
  4 options where 2+ are defensible-looking and the discriminator is whether the person
  reasons from the constraint.
- Every distractor must be a **real mistake a competent person makes**. If a distractor is
  obviously wrong, the question measures nothing and you have burned a slot.
- **Decide the response format deliberately; multiple choice is the default, not the rule.**
  Multiple choice is the lowest-friction instrument and is usually right. But if any scored
  axis is about *how the person communicates*, multiple choice cannot measure it, and the
  playbook requires at least one such axis — so check this before writing items. Open
  response (typed or spoken, graded by the judge against the same rubric) measures
  generation rather than recognition, costs real friction, and needs ordinal item analysis
  instead of a percent-correct target. The system design vertical went open-response for
  exactly this reason; see `verticals/system-design-interviews/02-CONTENT-AGENT.md`. If you
  go open-response, **question 1 must still render on first paint with a text box** — a
  mic-permission prompt before the first question is the interstitial this layer forbids.
- Mix in 1–2 items that require an actual number (an estimate, an order of magnitude).
  These are the highest-signal items in the whole instrument.
- Drop-off per question is your most important early telemetry. Instrument it from day one.

### Layer 2 — The Reveal (free, still no auth)

Show immediately, before any gate:
- Composite score **and percentile against the cohort**. Comparative beats absolute, always.
- The single **named blind spot** — the lowest axis, stated with specificity and a touch of
  bluntness. "Your capacity estimation is at the 31st percentile. In a real loop this is
  where you'd lose the room."
- One concrete thing to do about it.

Gate *behind signup*: the full per-axis breakdown, the drill plan, and the ability to retake
and track change. Gate value the user has now *seen the shape of* — never gate the reveal
itself. The reveal is the share; if you wall it you have no virality.

### Layer 3 — The Artifact (the actual growth engine)

This layer is the one teams skip, and it is why their quizzes don't travel.

- A generated share image that looks like **a real professional instrument** — a rubric
  sheet, a scorecard, an evaluation form. Not a cute badge. The credibility of the format
  is what makes posting it a status move rather than an embarrassment.
- It must contain: the axes, the per-axis marks, the percentile, and a small amount of
  specificity that proves it is about *this person*.
- One-tap share to the cohort's native platform, pre-filled with text the user would
  plausibly write themselves. Never pre-fill marketing copy; people read it and bail.
- **Challenge link**: a URL that drops a friend into the identical scenario set and shows
  the comparison. Peer-vs-peer comparison in a competence domain is the strongest
  share mechanic available to you.
- Public, anonymous, per-scenario percentile leaderboard. Gives repeat visitors a reason
  to come back and gives the content engine something to point at.

### Layer 4 — The Core Product (paid)

**The quiz must graduate into a practice loop, not into content.** Content is a one-time
purchase with no retention and infinite substitutes. A practice loop with scored feedback
has no substitute and a reason to open tomorrow.

The shape, in every vertical:
- An **AI counterpart** that plays the adversarial human in the real situation — the
  interviewer, the reviewer, the skeptical exec — in character, and never gives away the
  answer.
- A **grader run out of band**, as a separate call with a separate prompt, that sees the
  full transcript plus a reference solution plus the rubric and scores with quoted
  evidence from what the user actually said.
- **Never let one model do both roles in one pass.** An in-character model that also knows
  it is grading leaks the rubric into its questions and coaches instead of testing.
- Output: a scored report with timestamped evidence, and a contrast — "here is what an
  at-bar answer to that same follow-up sounds like." The contrast is the product.

### Layer 5 — The Loop (retention)

- **Micro-drills**: 60–120 second single-axis reps, one axis at a time, so the user has a
  reason to open the app on a day they don't have 45 minutes for a full session.
- **Per-axis progress over time.** The user's own first diagnostic is the baseline. Showing
  movement on the axis they were worst at is the single best retention surface you have.
- A new scenario on a weekly cadence, announced by email. Email is the only channel you own.
- The **retention bridge** from CONFIG, shipped before the first cohort's dated event passes.

---

## NON-NEGOTIABLES

These are the failure modes. Each one has killed a product of this shape.

1. **No auth before value.** The reveal is free. Always.
2. **The grader must be harsh and calibrated.** Force it to surface at least two below-bar
   observations with quoted evidence. Cap the score when the user never produced a number
   or never named a tradeoff explicitly. A mock that tells everyone they're great is
   worthless, and users detect it in one session.
3. **Rubric legitimacy over cleverness.** A practitioner in the cohort must look at the
   axes and say "yes, that's what we actually score." Borrow the real vocabulary.
4. **Price in units of the event, not the month.** The need is episodic. Offer a sprint
   priced to the length of the loop alongside any subscription, and expect subscription
   churn to be structural rather than a bug to fix.
5. **The free tier must be genuinely sufficient to be useful.** It is the marketing budget.
   A crippled free tier produces no shares and therefore no funnel.
6. **Instrument before you launch.** Per-question drop-off, reveal→signup, share rate per
   result archetype, signup→first session, session→second session, trial→paid, retake rate.
   You cannot improve a funnel you cannot see, and the GTM agent is blind without it.
7. **Don't fabricate the rubric from the model's imagination.** Ground it in observable
   sources — published interview guides, real rubrics, practitioner write-ups — and cite
   them in the content brief. Invented rubrics read as invented.

---

## BUILD ORDER

| Phase | Ships | Gate to next phase |
| --- | --- | --- |
| 0 | Vertical qualified, config filled, teardown of the prior quiz complete | 4/5 gates, with evidence |
| 1 | 12 scenarios + rubric + reference solutions, reviewed by one real practitioner | A practitioner says the axes are legitimate |
| 2 | Hook + Reveal + Artifact, instrumented, no paid product yet | Completion rate and share rate clear the kill metric |
| 3 | AI counterpart + grader, calibrated against hand-scored transcripts | Grader agreement with human labels is acceptable and it is not flattering |
| 4 | Paywall, pricing, drills, progress | Paid conversion clears the kill metric |
| 5 | Retention bridge | — |

**Phase 2 before phase 3, always.** If the free diagnostic doesn't spread, a better mock
interviewer will not save it, and you will have spent the expensive effort first.

---

## KILL CRITERIA

Set these as numbers in CONFIG before launch, then hold yourself to them. Pick thresholds
from the prior quiz's actual data where it exists (see `VIRALITY-TEARDOWN.md`), not from
industry averages, which are mostly fiction.

- Quiz **completion** rate — if people won't finish a free 6-minute quiz, the questions are
  wrong, and no amount of distribution fixes it.
- **Share** rate per completion — this is the virality coefficient's main term. If it's
  near zero, layer 3 is broken; fix the artifact, not the ad spend.
- **Reveal → signup**.
- **Signup → first full session** of the paid product.
- **First → second session.** The honest measure of whether the AI counterpart is good.
- **Free → paid.**

If share rate and second-session rate are both weak after a fair test, the vertical failed
gate 2 or gate 3. Say so plainly and stop, rather than buying traffic into a leaky funnel.

---

## OUTPUT CONTRACT

Produce, in the repo:
- `CONFIG.md` — the filled config with gate scores and evidence
- the question bank and rubric as structured data, not prose
- the running web app
- `METRICS.md` — the instrumented events and current numbers, updated as you go
- a handoff note to the GTM agent listing what is live and what the numbers are

Do **not** write the go-to-market plan. A separate agent owns that, deliberately, so that
the plan is not bent to fit whatever you found easiest to build.
