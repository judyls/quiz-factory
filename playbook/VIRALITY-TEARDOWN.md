# VIRALITY TEARDOWN — reverse-engineering what actually worked

> Run this **before** building. Phase 0 of the factory script.

## Honest starting position

The `ceo-quizz` repository contains one commit and an 11-byte README. **There is no CEO
quiz source, copy, or analytics data here**, so nothing in this file is a finding about it.
What follows is (a) the protocol to extract the real learnings once you have access, and
(b) the mechanics library to port in the meantime.

Treat every item in part B as a **hypothesis to confirm against the CEO quiz's actual
numbers**, not as established fact. An agent that presents the mechanics library as
"the learnings from the CEO quiz" is fabricating, and will optimize the new product toward
things that may never have worked.

---

# PART A — The forensics protocol

## A1. Get the inputs

Ask the user for whichever of these exist, in priority order:

1. **The live URL** — then walk the funnel yourself as a cold user and record every screen.
2. **Analytics export** — funnel steps, per-question drop-off, traffic sources, share
   events. Plausible/PostHog/GA, whatever is attached.
3. **The question set and the result archetypes** — the actual copy.
4. **Share data** — which result archetype got posted most, and where it landed.
5. **Email list size and open rates**, if there was a capture step.
6. **Any revenue** — conversion rate and price point.
7. **The posts that drove traffic** — the original launch post, and any that outperformed.

If only the URL exists, A2 still produces most of the value. If nothing exists, say so to
the user and proceed on the mechanics library, clearly labelled as untested.

## A2. Walk the funnel cold

Open it as a new user with analytics blocked. Record, screen by screen:

- Time to first question. Count every click and every interstitial before it.
- Question count, question *type* (trivia vs scenario vs self-report), and whether any
  question required a number or a judgment call.
- Where the auth/email gate sits relative to the reveal.
- What the reveal shows: absolute score, percentile, archetype, named weakness?
- What the share artifact is: image or text link? Does it contain the person's result
  legibly? Would you post it?
- What happens after the reveal. Is there *anything* to do next? Is there a paid product?
- Whether a retake gives different questions, or the same ones.

Write this up as a screen-by-screen table in `TEARDOWN.md`. This document is the baseline
for every A/B decision later.

## A3. Extract the numbers that matter

Pull these six, and nothing else to start:

| Metric | Why | What to do with it |
| --- | --- | --- |
| Entrants → Q1 answered | Measures hook friction | Sets the floor for the new build |
| Per-question drop-off | Finds the bad questions | Any question with an outlier drop is wrong, not hard |
| Completion → reveal | Should be ~100%; if not, there's a bug or a gate | — |
| Reveal → share | **The virality term.** | Becomes the kill metric |
| Share → new entrant | The actual K factor input | If < 0.15 the artifact is the problem |
| Reveal → email/signup | Monetization ceiling | — |

Then the one qualitative question that matters most: **which result archetype was shared
disproportionately?** People share results that flatter or that are interestingly
unflattering. Which of the two it was in practice tells you how to write the new reveal,
and it is the single highest-value thing in this whole protocol.

## A4. Diagnose why it did or didn't retain

The CEO quiz is for founders — a cohort with no *dated* event and no rubric anyone
recognizes. Check whether that showed up in the data:

- Was there a second visit for anyone? Any retakes?
- Was there a paid product at all, or did the funnel end at the reveal?
- Did traffic decay to near-zero within days of the launch post?

If the pattern is "one traffic spike, no second visits, no paid product," then the lesson
being ported forward is **not** the quiz mechanics — it's that the vertical failed factory
gates 1, 3, and 4 (dated pain, credible rubric, proven spend). Say this to the user
directly. It is the most valuable finding available, and it is precisely why the system
design vertical is a better bet: that cohort has a scheduled interview, a rubric the
industry agrees on, and documented spend of $47–$279 on courses and $90–$120 per human
mock session.

## A5. Port, don't copy

For each mechanic that measurably worked, write one line: `mechanic → new-vertical
equivalent → how we'll measure it`. For each that didn't, write why, so it isn't rebuilt
from habit. Put the table in `TEARDOWN.md` and hand it to the build and GTM agents.

---

# PART B — The mechanics library

Hypotheses, ordered by expected effect. Confirm each against A3 where you can.

## B1. Comparative beats absolute
A bare score is inert. A score *against a cohort* creates a stake. "You scored 71" invites
nothing; "you're at the 34th percentile among engineers targeting frontier labs" produces
either relief or alarm, and both are motivating. Percentiles need volume, so seed them from
the question bank's expected distribution and switch to real data as it accumulates.

## B2. The specific, slightly unflattering diagnosis travels furthest
Pure flattery gets screenshot-shared less than people expect, because posting it is a
boast with no information in it. The high-share result is **specific, credible, and a
little bit of a problem** — it makes the poster look self-aware and the post look useful.
It also makes the paid product obviously relevant. Write the reveal to name one real
weakness precisely, with warmth, next to a genuine strength.

## B3. The artifact must look like a real instrument
A rubric sheet, an eval form, a scorecard with axes and marks. Credibility of *format* is
what converts a result into something a professional will attach their name to. Cute badges
read as entertainment and get shared inside friend groups rather than professional networks
— which is the wrong graph for a product sold to professionals.

## B4. Peer challenge is the strongest single loop
A link that drops a peer into the identical scenario and shows a head-to-head is more
powerful than any broadcast share, because it is a direct, personal, competitive
invitation in a competence domain. Build it in layer 3, not "later."

## B5. The question set is the distribution channel
Each scenario becomes a public page with the problem, the tradeoff space, and a worked
at-bar answer — indexed by search engines and, increasingly, cited by assistants when
someone asks how to prepare. This is the mechanism behind the incumbents' content moats in
this exact category, and it compounds while paid acquisition does not. Budget for ~40
scenario pages, not 8.

## B6. Specificity of cohort beats breadth of topic
"System design interview prep" competes with well-funded incumbents. "The system design
round at Anthropic and OpenAI — inference batching, GPU scheduling, multi-tenant token
limits" is a claim nobody owns, is searched by exactly the people who will pay, and is
narrow enough that a single credible artifact can make you the default answer. Niche down
until the claim is ownable, then widen after.

## B7. Urgency is borrowed from the calendar, not manufactured
Don't invent scarcity. Attach to the cohort's real calendar: hiring waves, performance
cycles, the week someone gets a recruiter email. Email sequences keyed to "your loop is in
three weeks" outperform discount timers in this category by a wide margin.

## B8. Free must be sufficient
The free diagnostic is the entire marketing budget. If it is crippled to protect the paid
tier, nobody shares it, and there is no funnel to protect. Give away the diagnosis
completely. Charge for the repeated practice that fixes it.

## B9. The outcome loop closes the flywheel
"I got the offer" is the most valuable content the product will ever have, and it is free.
Build the capture for it on day one — a prompt in the post-offer email, a one-tap way to
report the outcome — so that by month three the landing page is social proof rather than
claims.

---

## OUTPUT

Write `TEARDOWN.md` at the repo root containing: the screen-by-screen walk (A2), the six
metrics (A3), the retention diagnosis (A4), the port table (A5), and an explicit list of
which B-items the CEO quiz data confirmed, contradicted, or left untested. Hand it to both
the build agent and the GTM agent before either starts.
