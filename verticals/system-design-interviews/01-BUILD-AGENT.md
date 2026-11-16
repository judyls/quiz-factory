# BUILD AGENT BRIEF — Frontier Infra Interview Diagnostic + AI Mock Interviewer

> Paste as the opening message of a dedicated build session.
> Read `playbook/QUIZ-FACTORY.md` and `playbook/VIRALITY-TEARDOWN.md` first.
> You do **not** own go-to-market. A separate agent owns that. Don't write a launch plan.

---

## CONFIG (filled)

```yaml
vertical:          AI-lab system design interviews (Anthropic / OpenAI / frontier-lab tier)
cohort:            Mid-to-senior backend, infra, and ML-platform engineers (L4–L6) who are
                   in, or within 3 months of, a frontier-lab or AI-heavy loop. Secondary:
                   senior engineers blocked on promotion by design-communication signal.
dated_pain:        A scheduled onsite loop, 1–6 weeks out, with a 45–60 min system design
                   round that decides level and therefore several hundred thousand dollars
                   of compensation.
status_currency:   "Scored at the Staff bar on tradeoff articulation" — a credible,
                   rubric-shaped claim about engineering judgment.
scored_axes:       requirements_scoping, capacity_cost_estimation, high_level_design,
                   deep_dive_failure_modes, tradeoff_articulation, communication_collaboration
share_artifact:    An interview scorecard image: 6 axes, 4-level marks, cohort percentile,
                   one named blind spot, one named strength. Looks like a real eval form.
price_anchor:      Hello Interview Premium ~$47/month or ~$279 lifetime; human mock
                   sessions ~$90–120 each; AI interview tools $8–60/mo but almost none
                   cover system design. See RESEARCH-NOTES.md (same folder). Re-verify.
paid_product:      Unlimited AI mock system design interviews, in character, scored against
                   the 6-axis rubric with quoted evidence and at-bar answer contrasts.
retention_bridge:  "Design Review Mode" — the same engine pointed at on-the-job artifacts:
                   defend your RFC against a skeptical staff engineer, run a design review,
                   present a migration to a VP. Solves post-offer churn and is the
                   promotion-signal product the user explicitly wants.
kill_metric:       See METRICS section. Set thresholds from the CEO quiz teardown data.
```

### Gate scores (Step 0)

| Gate | Score | Evidence |
| --- | --- | --- |
| Dated pain | **Strong** | Scheduled onsite loops; comp delta between levels is large |
| Status at stake | **Strong** | Level and competence; engineers post interview outcomes publicly |
| Credible rubric | **Strong** | System design rounds are already scored on recognizable axes industry-wide; borrow the real vocabulary |
| Proven spend | **Strong** | $47–$279 course pricing, $90–120/session human mocks, already-paying cohort |
| Public watering hole | **Strong** | r/ExperiencedDevs, Blind, hiring-season X/LinkedIn, ML-infra Discords, Hacker News |

5/5. Build.

### Why this wedge is real

Two established facts, from `RESEARCH-NOTES.md`, that do not currently overlap:

1. AI mock-interview tools are cheap and plentiful — and overwhelmingly behavioral. System
   design is largely absent from them.
2. The credible system design players sell **courses plus human mocks**. Human mocks don't
   scale, cost $90–120, and can't be taken at 11pm the night before a loop.

The gap is **scaled, scored, adversarial system design practice**, and the sharpest version
of it is the AI-infra flavor — inference batching, GPU scheduling, token economics,
multi-tenant serving — where the question bank is small, expanding, and nobody owns the
prep narrative. Note that prep aggregators are already indexing company-specific ML system
design questions; speed and depth of the rubric are the defense, not secrecy.

---

## THE FUNNEL TO BUILD

### Layer 1 — The Diagnostic (free, zero auth)

**12 scenarios, ~7 minutes.** Question 1 renders on first paint at `/`. No landing page,
no start button, no email gate. A returning user resumes from `localStorage`.

Format of every item: a realistic frontier-lab infra situation, **hard numeric
constraints**, and 4 options of which at least 2 look defensible. The discriminator is
always whether the candidate reasons *from the stated constraint*. Every distractor is a
mistake a competent senior engineer actually makes.

Seed scenarios — hand to the content agent for expansion to 40, keep the AI-infra framing
over classic CRUD, because that framing is the whole positioning:

1. **Continuous batching** — p99 token-latency budget vs GPU utilization; batch window sizing.
2. **KV cache pressure** — long-context requests evicting short ones; admission control.
3. **Multi-tenant token rate limiting** — fair-share across tenants with wildly uneven
   request shapes; where the limiter lives.
4. **GPU credit / quota system** — metering, overdraft, and the consistency tradeoff.
5. **Streaming token delivery** — SSE vs WebSocket vs long-poll at scale; reconnection and
   partial-response semantics.
6. **Safety classifier in the request path** — adding 40ms of mandatory inference to every
   request without breaking the latency SLO.
7. **Heterogeneous model fleet scheduling** — routing across model sizes and GPU types
   under a cost ceiling.
8. **Eval infrastructure** — running 50k graded evals per commit; sharding, flakiness,
   caching, and cost.
9. **RLHF / annotation pipeline** — human labeling throughput, inter-annotator agreement,
   and the feedback loop into training.
10. **Training data pipeline at PB scale** — dedup, shuffle, and reproducibility.
11. **Vector retrieval at 10B embeddings** — recall vs p99 vs cost, index choice and refresh.
12. **Agent/tool-calling orchestration** — fan-out, timeouts, partial failure, idempotency
    on retried side-effecting tool calls.

Instrument per-question drop-off from the first deploy.

### Layer 2 — The Reveal (free, still no auth)

Immediately on completion, no gate:
- Composite score + **cohort percentile**.
- The **named blind spot**: lowest axis, specific and a little blunt, with what it costs in
  a real loop. "Capacity estimation: 31st percentile. You picked the right architecture
  twice without ever sizing it. In a 45-minute round this is where the interviewer stops
  believing you've run this in production."
- The named strength, so it isn't purely demoralizing.
- One concrete next action.

Gate behind signup: full 6-axis breakdown, the drill plan, retake-and-track, and the first
mock interview.

### Layer 3 — The Artifact

- `/api/scorecard/[id]` → OG image via Next.js `ImageResponse`. Renders as an **interview
  evaluation form**: 6 axes, 4-level marks, percentile, blind spot, strength. Dark and
  light variants. Legible as a thumbnail — assume it's seen at 400px wide in a feed.
- One-tap share to X and LinkedIn, pre-filled with text a person would actually write.
- **Challenge link** `/c/[token]`: same 12 scenarios, head-to-head comparison on completion.
- `/leaderboard`: anonymous per-scenario percentile distribution.
- `/q/[slug]`: a **public page per scenario** — the problem, the tradeoff space, a worked
  at-bar answer, and a CTA into the mock. This is the compounding acquisition surface;
  build the template early even if content lands later.

### Layer 4 — The AI Mock Interview (the paid product)

A 45-minute session. Voice preferred, text fallback, with a diagram canvas
(embed `tldraw` or `excalidraw` — do not build a canvas).

**Architecture — this is the part to get right:**

- **Interviewer model**: in character as a frontier-lab engineer running the round. Holds
  the scenario's reference solution tree *as hidden context used only to choose follow-ups*.
  It must never grade, never praise, never reveal the rubric, and never supply a missing
  consideration — only probe for it. Time-boxed phase control: scoping → HLD → deep dive →
  tradeoff pressure → wrap.
- **Grader model**: a **separate out-of-band call** after the session, over the full
  transcript + canvas snapshots + reference solution + rubric. Scores each axis 0–3 with
  **quoted evidence from what the candidate actually said**, timestamped.
- **Never one model for both roles in one pass.** A model that knows it is grading leaks
  the rubric into its questions and coaches instead of testing. This single mistake is
  what makes most AI mock interviews useless.
- **Anti-flattery constraints on the grader**, enforced in the prompt and validated in code:
  - must return ≥2 below-bar observations with quoted evidence
  - `capacity_cost_estimation` is capped at 1 if the candidate never stated a number
  - `tradeoff_articulation` is capped at 1 if no tradeoff axis was named explicitly
  - a 3 on any axis requires a quoted justification; reject and re-ask if absent
- **Report**: per-axis score with evidence, the two highest-leverage fixes, and — the thing
  people will pay for — **"what an at-bar answer to that follow-up sounds like,"** a short
  contrast generated against the reference solution. The contrast is the product.

### Layer 5 — Retention

- **Drills**: 90-second single-axis reps. Capacity math drills ("300k rps, 2KB payloads,
  what's your network bill?"), tradeoff drills, "name the failure mode" drills. This is the
  surface that earns a daily open.
- **Progress per axis** against the user's own first diagnostic as baseline.
- Weekly new scenario by email.
- **Design Review Mode** (the retention bridge) — ship before the first cohort's loops pass.

---

## TECH

Boring and fast. Do not spend the week on infrastructure.

- **Next.js** App Router + TypeScript, deployed on Vercel.
- **Postgres** (Neon or Supabase). Supabase also gives you auth cheaply.
- **Auth**: email magic link + Google. No password flows.
- **Claude API** for interviewer and grader. Separate prompts, separate calls, separate
  model configs. Use prompt caching on the reference-solution context — it is large and
  reused across every turn of a session, and this is the dominant cost lever.
- **Voice**: streaming STT + TTS. Keep a text-only path working at all times; it's the
  fallback when audio fails mid-session and it's what most users start on.
- **Canvas**: `tldraw` or `excalidraw`, snapshot to the transcript at each phase boundary.
- **Payments**: Stripe Checkout. One-time sprint SKUs *and* subscription — the GTM agent
  sets prices; you build both paths.
- **OG images**: `ImageResponse` / satori.
- **Analytics**: PostHog. Events listed below, named exactly.

### Data model sketch

```
users(id, email, created_at, cohort_tag, referred_by)
diagnostic_attempts(id, user_id?, anon_id, started_at, completed_at, scores_jsonb, percentile)
diagnostic_answers(attempt_id, question_id, choice, ms_to_answer)
scenarios(id, slug, title, axis_weights, constraints_jsonb, published)
reference_solutions(scenario_id, required_beats_jsonb, traps_jsonb, followup_tree_jsonb)
sessions(id, user_id, scenario_id, mode, started_at, ended_at, transcript_jsonb, canvas_snapshots)
grades(session_id, axis, score_0_3, evidence_quote, timestamp_ms, grader_version)
drills(id, axis, prompt, answer_spec)
drill_attempts(user_id, drill_id, score, created_at)
shares(id, attempt_id, channel, created_at)
challenges(token, from_attempt_id, to_attempt_id?)
```

Version the grader (`grader_version`). You will retune it, and you need to compare scores
across versions without silently invalidating users' progress history.

---

## METRICS — instrument before launch

Event names, exactly:

`diagnostic_started` · `diagnostic_question_answered{n,ms}` · `diagnostic_completed` ·
`reveal_viewed` · `scorecard_generated` · `share_clicked{channel}` · `challenge_sent` ·
`challenge_accepted` · `signup_completed` · `mock_started{mode}` · `mock_completed{duration}` ·
`report_viewed` · `drill_completed{axis}` · `checkout_started{sku}` · `purchase_completed{sku}` ·
`outcome_reported{result}`

Report these in `METRICS.md`, updated as you go:

| Funnel step | Why it's the one that matters |
| --- | --- |
| Q1 answered / landed | Hook friction |
| Per-question drop-off | Outlier drop = broken question, not a hard one |
| Completed / started | If people won't finish a free 7-min quiz, the questions are wrong |
| Share / completed | **The virality term.** Weak here ⇒ fix the artifact, not the ad spend |
| New entrants / share | The actual K input |
| Signup / reveal | Monetization ceiling |
| First mock / signup | Is the paid promise legible? |
| **Second mock / first mock** | **The honest verdict on the AI interviewer.** Watch this above all |
| Paid / signup | — |

---

## BUILD ORDER

1. **Phase 1** — 12 scenarios + rubric + reference solutions in the DB (content agent
   supplies; use the seed list to unblock). One real practitioner confirms the axes are
   legitimate before you build UI on top of them.
2. **Phase 2** — Diagnostic + Reveal + Scorecard + Challenge, instrumented. **Ship this
   alone and measure it.** If it doesn't spread, a better mock interviewer won't save it,
   and the mock interviewer is the expensive part.
3. **Phase 3** — AI interviewer + grader. Calibrate against ≥20 hand-scored transcripts
   before exposing it. Measure grader-vs-human agreement and, separately, check it is not
   flattering: score distribution must have a real left tail.
4. **Phase 4** — Paywall, Stripe, drills, progress.
5. **Phase 5** — Design Review Mode.

---

## HANDOFF CONTRACT

To the **content agent**: scenario + reference-solution schema, and the rubric as
structured data.

To the **GTM agent**, the day Phase 2 is live:
- the live URL and the share-artifact image
- `METRICS.md` with real numbers
- the scenario slug list for the content/SEO engine
- the Stripe SKUs you wired, unpriced
- an honest list of what is fake, stubbed, or not yet calibrated

Never hand the GTM agent a number you haven't verified in the product. They will put it in
public copy.
