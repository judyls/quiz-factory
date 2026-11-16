# BUILD AGENT BRIEF — <<VERTICAL NAME>>

> Paste as the opening message of a dedicated build session.
> Read `playbook/QUIZ-FACTORY.md` and `playbook/VIRALITY-TEARDOWN.md` first, then
> `verticals/<slug>/CONFIG.md`.
> You do **not** own go-to-market. A separate agent owns that, deliberately. Don't write a
> launch plan, and don't set prices.
>
> A worked example of this template, filled in, is
> `verticals/system-design-interviews/01-BUILD-AGENT.md`. Read it for the level of
> specificity expected.

---

## Inputs

- CONFIG: `verticals/<slug>/CONFIG.md` — gates must have passed before you start
- Rubric + scenarios: from the content agent. Use the seed list below to unblock yourself.
- Teardown: `TEARDOWN.md` if it exists

## Layer 1 — The Diagnostic (free, zero auth)

- `<<N>>` items, `<<N>>` minutes. **Question 1 renders on first paint at `/`.** No landing
  page, no start button, no email gate. Resume from `localStorage`.
- Every item: a realistic `<<DOMAIN>>` situation, **hard constraints stated**, 4 options
  with ≥2 defensible-looking. The discriminator is always whether the person reasons from
  the stated constraint. Never trivia.
- Every distractor is a real mistake a competent `<<COHORT>>` makes. Source them from the
  content agent's `traps` field.
- Include 1–2 items requiring an actual number or order of magnitude. Highest-signal items
  in the instrument.
- Instrument per-question drop-off from the first deploy.

**Seed scenarios** — `<<LIST 10-14. Keep the positioning framing; it IS the wedge>>`

## Layer 2 — The Reveal (free, still no auth)

Show immediately, no gate: composite score + **cohort percentile**; the **named blind
spot** (lowest axis, specific and a little blunt, with what it costs them in the real
event); the named strength; one concrete next action.

Gate behind signup only: full per-axis breakdown, drill plan, retake-and-track, first
session of the paid product.

## Layer 3 — The Artifact

- `/api/scorecard/[id]` → OG image. Renders as **a real professional instrument**
  (`<<WHAT KIND — rubric sheet / eval form / scorecard>>`), not a badge. Light + dark.
  Legible at 400px in a feed.
- One-tap share, pre-filled with text a person would actually write.
- **Challenge link** `/c/[token]` — same items, head-to-head on completion.
- `/leaderboard` — anonymous per-item percentiles.
- `/q/[slug]` — a public page per scenario. The compounding acquisition surface. Build the
  template early even if content lands later.

## Layer 4 — The Paid Product

A practice loop, never content. Architecture, which is the part to get right:

- **Counterpart model**: in character as `<<THE ADVERSARIAL HUMAN IN THE REAL SITUATION>>`.
  Holds the reference solution as hidden context used *only to choose follow-ups*. Never
  grades, never praises, never reveals the rubric, never supplies a missing consideration —
  only probes for it. Time-boxed phase control.
- **Grader model**: a **separate out-of-band call** after the session, over the full
  transcript + reference solution + rubric. Scores each axis 0–3 with **quoted evidence
  from what the user actually said**, timestamped.
- **Never one model for both roles in one pass.** A model that knows it is grading leaks
  the rubric into its questions and coaches instead of testing. This single mistake is what
  makes most AI practice products useless.
- **Anti-flattery caps, enforced in code and not only in the prompt:**
  - ≥2 below-bar observations with quoted evidence, every report
  - `<<AXIS>>` capped at 1 if `<<THE OBSERVABLE THING>>` never happened
  - any score of 3 requires a quoted justification, or reject and re-ask
- **Report**: per-axis score with evidence, two highest-leverage fixes, and the contrast —
  *"here is what an at-bar answer to that same follow-up sounds like."* **The contrast is
  the product.**

## Layer 5 — Retention

- **Micro-drills**: 60–120s single-axis reps. The surface that earns a daily open.
- Per-axis progress against the user's own first diagnostic as baseline.
- Weekly new scenario by email. Email is the only channel you own.
- The **retention bridge** from CONFIG, shipped before the first cohort's event passes.

## Tech

Boring and fast. Next.js App Router + TypeScript on Vercel · Postgres (Neon/Supabase) ·
magic-link + Google auth, no passwords · Claude API with **separate prompts and calls** for
counterpart and grader, prompt caching on the reference-solution context (the dominant cost
lever) · Stripe Checkout, both one-time and subscription paths wired, prices set by GTM ·
`ImageResponse`/satori for OG · PostHog.

`<<ADD: voice, canvas, or other modality needs>>`

### Data model sketch

```
users · diagnostic_attempts · diagnostic_answers · scenarios · reference_solutions
sessions · grades(…, grader_version) · drills · drill_attempts · shares · challenges
```

Version the grader. You will retune it, and you need to compare across versions without
silently invalidating users' progress history.

## Metrics — instrument before launch

`diagnostic_started` · `diagnostic_question_answered{n,ms}` · `diagnostic_completed` ·
`reveal_viewed` · `scorecard_generated` · `share_clicked{channel}` · `challenge_sent` ·
`challenge_accepted` · `signup_completed` · `session_started` · `session_completed` ·
`report_viewed` · `drill_completed{axis}` · `checkout_started{sku}` ·
`purchase_completed{sku}` · `outcome_reported{result}`

Report in `METRICS.md`, updated as you go. The two that matter most: **share / completion**
(the virality term) and **second session / first session** (the honest verdict on the
product).

## Build order

1. Scenarios + rubric + reference solutions in the DB. One real practitioner confirms the
   axes are legitimate before you build UI on them.
2. **Diagnostic + Reveal + Scorecard + Challenge, instrumented. Ship this alone and measure
   it.** If it doesn't spread, a better counterpart won't save it — and the counterpart is
   the expensive part.
3. Counterpart + grader. Calibrate against ≥20 hand-scored transcripts before exposing it.
4. Paywall, Stripe, drills, progress.
5. Retention bridge.

## Handoff contract

To **content**: scenario + reference-solution schema, rubric as structured data.
To **GTM**, the day step 2 is live: live URL, the share artifact, `METRICS.md` with real
numbers, scenario slugs, the unpriced Stripe SKUs, and an honest list of what is stubbed or
uncalibrated.

**Never hand GTM a number you haven't verified in the product.** They will put it in public
copy.
