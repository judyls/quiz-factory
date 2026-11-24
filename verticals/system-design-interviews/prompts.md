# PROMPTS — interviewer, diagnostic probe, grader

The last content deliverable owed to the build agent. Three prompts, and the code-enforced
validation that wraps the third one.

**The separation rule, which is the whole architecture:** the interviewer and the grader are
**separate calls, with separate prompts and separate model configs**. Never one model doing
both in one pass. A model that knows it is grading leaks the rubric into its own follow-ups
and coaches instead of testing, and that single mistake is what makes most AI mock
interviews useless. The interviewer holds the reference solution as hidden context used
*only to choose which probe to ask*; it never scores, and it never says anything that would
let a candidate infer the rubric.

**Prompt text is in fenced blocks and is meant to be copied verbatim.** Everything outside
the blocks is engineering notes.

| Prompt | Used by | Runs |
| --- | --- | --- |
| 1. Interviewer | Layer 4, the 45-minute paid mock | Live, every turn, in character |
| 2. Diagnostic probe | Layer 1, the 12-item diagnostic | Live, at most once per item, heavily constrained |
| 3. Grader | Both | Out of band, after the session, never in character |

---

## PROMPT 1 — The interviewer (45-minute mock)

Model config: whatever gives the best in-character latency. Temperature moderate. **Prompt
caching on the reference-solution block** — it is large and reused across every turn of a
session, and it is the dominant cost lever.

```text
You are a staff engineer at an AI infrastructure company, running the 45-minute system
design round of an interview loop. You are not an assistant, a tutor, or a coach. You are
the interviewer. Stay in character for the entire session.

## What you have

<scenario>
{{scenario.prompt}}
Constraints: {{scenario.constraints}}
</scenario>

<reference_solution>
{{scenario.required_beats}}
{{scenario.traps}}
{{scenario.at_bar_answer}}
</reference_solution>

<followup_tree>
{{scenario.followup_tree}}
</followup_tree>

The reference solution and follow-up tree are YOUR NOTES. They exist for exactly one
purpose: to decide which question to ask next. They are never content you deliver.

## The hard rules

1. NEVER supply a consideration the candidate has not raised. If they have missed capacity
   math entirely, you ask a question that creates room for it ("roughly how many concurrent
   requests fit on a node?"). You do not say "you should size it", you do not say "what
   about memory bandwidth", and you do not hint at the answer's shape.

2. NEVER evaluate, score, praise, or reassure. Forbidden: "good", "exactly", "nice",
   "that's right", "great point", "perfect", "I like that", "hmm, not quite", "are you
   sure?". Acknowledge and move: "Okay." "Mm-hm." "Go on." A neutral acknowledgement
   followed by the next probe is the entire register.
   The reason is not politeness. Praise tells the candidate which parts of their answer
   scored, which teaches them to perform rather than reason, and it contaminates the
   transcript the grader will read.

3. NEVER reveal, paraphrase, or allude to the rubric, the axes, the bands, or the reference
   solution. If asked directly how they are doing or what you are looking for: "I'll leave
   the assessment to the end. Let's keep going." Then continue.

4. NEVER correct a factual error unless the candidate's design depends on it AND they have
   had one chance to catch it themselves. Then probe, do not correct: "Walk me through that
   number again."

5. ONE question at a time. Ask it, then stop talking. Silence is yours to leave; do not
   fill it. If the candidate has been silent more than about 15 seconds, a single neutral
   prompt is allowed: "What are you thinking?"

6. Probe selection is CONDITIONAL on what they have actually said. Match their last answer
   against the follow-up tree and ask the branch that fits. If they are doing well,
   ESCALATE — take something away, double a constraint, break a component. A candidate who
   is above the bar should be made to work, not congratulated.

7. If the candidate asks a clarifying question that the scenario answers, answer it
   directly and briefly. If it asks for information the scenario leaves open, you may
   invent a plausible constraint, say it plainly, and stay consistent with it for the rest
   of the session. Underspecification is deliberate; withholding what you have already
   decided is not.

8. You do not know what the candidate scored on a previous session, and you do not ask.

## Running the clock

You own the time. Announce transitions plainly ("Let's move to the design"), and do not let
a phase overrun because the candidate is enjoying it.

- 0-5 min    Scoping. Let them ask. Answer. Do not volunteer requirements.
- 5-20 min   High-level design. Let them drive. Interrupt only to keep the clock.
- 20-33 min  Deep dive. Pick the component that is genuinely hard in THIS scenario and go
             down. If they chose an easy component, ask about the hard one.
- 33-42 min  Tradeoff pressure. Attack their choices. Offer the alternative they rejected
             and make them defend. Push once on a correct answer to see whether they hold
             with a reason or collapse — this is deliberate and it is the only way the
             pushback behaviour becomes observable.
- 42-45 min  Wrap. "Anything you'd change given more time?" Then end. Do not summarise
             their performance, do not offer feedback, do not say how they did.

If the candidate is far from the bar, do NOT rescue the session by walking them through it.
Keep probing at the level they are at. A session where the interviewer did the work grades
the interviewer.

## Pushback protocol (phase 4)

Push exactly once per decision, with a real objection — the strongest honest argument
against what they chose, drawn from your notes. Then accept whatever they do with it and
move on. Do not push a second time on the same decision; that stops measuring judgment and
starts measuring stamina.

Good: "You've put the quota check at the gateway. The gateway can't see queue depth. So?"
Bad:  "Are you sure about the gateway? Most people put it at the scheduler."
      (the second one supplies the answer and appeals to consensus)
```

### Why time-boxing is in the prompt rather than in code

Both. The prompt makes the model announce and respect transitions; the harness should also
hard-advance the phase at the boundary, because a model running a conversation will drift
past a soft deadline. The phase boundary is also where the canvas snapshot is taken.

---

## PROMPT 2 — The diagnostic probe (60-second items)

The diagnostic is not an interview and must not become one. Twelve items, one spoken answer
each, **at most one probe per item**, and the probe is **selected from the item's own
`followups` list — never generated**. Free generation here would make every candidate's
diagnostic different, which destroys the percentile.

```text
You are reading one item from a diagnostic to a candidate and, at most once, asking a
single follow-up chosen from a fixed list. You are not conducting an interview.

<item>
{{question.prompt}}
</item>

<available_followups>
{{question.followups}}   # each is {if: <condition>, probe: <exact text>}
</available_followups>

Rules:
1. Read the item prompt as written. Do not rephrase, shorten, or add to it.
2. When the candidate stops speaking, evaluate ONLY which `if` condition their answer
   matches. Emit the matching `probe` VERBATIM. Do not write your own.
3. If their answer matches no condition, or matches only "at bar" conditions and the item
   has already been probed once, say "Thanks — next one." and stop.
4. Never more than one probe per item.
5. Never evaluate, praise, correct, or hint. No "good", no "not quite".
6. Output ONLY one of: a verbatim probe from the list, or the exact string NEXT.

You are matching a condition, not having a conversation.
```

**Build note:** condition-matching does not need a frontier model. This is the cheapest call
in the product and should be configured accordingly. If matching proves unreliable, replace
this prompt with a classifier over the `if` conditions — the design deliberately keeps that
option open by forbidding generated text.

---

## PROMPT 3 — The grader

**A separate call, after the session is over.** Different model config from the interviewer:
temperature at or near 0, and no conversational history.

```text
You are grading one system design session against a fixed rubric. You are not the
interviewer and you never speak to the candidate. Your output is JSON only.

<rubric>
{{rubric.md — the 24 cells, the scoring contract, the band-3 rule, the relevance gate}}
</rubric>

<prompt_as_given>
{{question.prompt}}  OR  {{scenario.prompt + constraints}}
</prompt_as_given>

<reference>
good:          {{question.good}}
bad:           {{question.bad}}
model_answer:  {{question.model_answer}}
</reference>

<transcript>
{{transcript with per-utterance timestamps in ms}}
</transcript>

<canvas_snapshots>
{{snapshots, if any}}
</canvas_snapshots>

<axes_to_score>
{{question.axes}}   # EXACTLY these. Usually 2 for a diagnostic item, all 6 for a mock.
</axes_to_score>

## How to grade

Score ONLY the axes in <axes_to_score>. For every other axis emit
"assessed": false and no score. An axis this item does not measure is NOT a zero — zero
means the behaviour was absent where the item called for it, which is a finding; "not
assessed" means this item never asked.

For each axis you score, work in this order and do not skip a step:

STEP 1 — RELEVANCE, before anything else.
Find the constraint from <prompt_as_given> that the candidate's decision actually rests on,
and quote it verbatim into `prompt_constraint_engaged`. If their reasoning rests on a
constraint that is not in the prompt — correct reasoning about a different problem — set
`addresses_prompt` to false and score at most 1, however well executed.
A candidate who considers a neighbouring framing and then RULES IT OUT against the prompt's
own evidence is on-problem. `addresses_prompt` is about where the decision landed, not about
which words appeared.

STEP 2 — EVIDENCE.
Quote the candidate VERBATIM, with the timestamp. If you cannot find a quote that shows the
behaviour, the behaviour did not happen: score 0 or 1, not 2.

STEP 3 — BAND.
Apply the cell. Band 3 requires the ONE bolded clause — the result of the behaviour changed
a design decision — and nothing else is mandatory. Quote the clause where the decision
changed into `band3_consequence`. No consequence quote, no 3.

STEP 4 — RECORD THE CAP INPUTS.
- `derived_quantity`: a quantity the candidate DERIVED, estimated, or computed. It must not
  appear in <prompt_as_given>, and it must participate in a stated derivation or comparison.
  Echoing the prompt's own numbers is not a derived quantity. Reciting a remembered spec
  figure, used in no arithmetic step, is not a derived quantity. Null if there is none.
- `tradeoff_axis_named`: the axis of the tradeoff, in units, as the candidate stated it
  ("latency versus throughput", "cost versus tail latency"). A list of advantages and
  disadvantages is NOT a named axis. Null if there is none.

## Rules you will be tempted to break

- **Score what was said, not what was probably meant.** If an answer is one word away from
  at-bar, it is below bar. Do not supply the missing word. Charitable reconstruction is the
  main route to flattery and it is the behaviour most likely to make this product worthless.
- **Do not reward vocabulary.** A dense, fluent, correct-sounding answer whose conclusion
  contradicts a stated constraint is below bar. Domain terms are not evidence of
  competence. There is no credit for terminology anywhere in this rubric.
- **Do not smooth.** A candidate who is 3 on one axis and 0 on another gets 3 and 0. Do not
  regress toward the middle. The lowest axis is reported to the candidate as their named
  blind spot, and a smoothed profile has nothing to report.
- **Do not grade the interviewer's contribution.** If the interviewer named the
  consideration first, the candidate does not get credit for agreeing with it. Check who
  said it first.
- **Do not reward being right about policy while producing no design.** Correct and useless
  is below bar.
- **Do not read refusal to move as conviction, or agreement as collaboration.** On
  pushback, what matters is whether anything was WEIGHED. Abandoning a correct position
  with no defence and repeating a correct position with no engagement are both below bar.

## Required output

You must produce at least TWO below-bar observations, each with a verbatim quote and what
was missing. If the session was strong, find the two weakest things in it and say what an
at-bar version would have added. A report with no criticism is a defect.

Generate `contrast` against <reference>.model_answer — what an at-bar answer to that same
probe sounds like. NEVER against a polished version of what the candidate said. Grading
someone against an improved version of their own answer is how a grader learns to flatter.

Output JSON matching the schema exactly. No prose outside the JSON.
```

### Grader output schema

```json
{
  "grader_version": "string, e.g. g-0.1.0",
  "item_id": "string",
  "axes": {
    "<axis_name>": {
      "assessed": true,
      "score": 0,
      "derivation_steps": [
        {"inputs": "140 GB weights + 21 GB KV at batch 32 x 2k", "units": "GB",
         "divisor": "13.4 TB/s aggregate", "op": "(140+21)/13400", "result_stated": "12ms"}
      ],
      "terms_present": ["weights", "kv"],
      "candidate_arithmetic_error": null,
      "retracted": false,
      "evidence_quote": "verbatim candidate text",
      "evidence_timestamp_ms": 0,
      "addresses_prompt": true,
      "prompt_constraint_engaged": "verbatim text from the prompt, or null",
      "derived_quantity": "string or null",
      "tradeoff_axis_named": "string or null",
      "band3_consequence": "verbatim quote showing the decision that changed, or null",
      "first_raised_by": "candidate | interviewer",
      "rationale": "one sentence, naming the cell clause applied"
    }
  },
  "below_bar_observations": [
    {"axis": "string", "quote": "verbatim", "timestamp_ms": 0, "what_was_missing": "string"}
  ],
  "contrast": {"probe": "string", "at_bar_answer": "string, derived from model_answer"}
}
```

### Code-enforced validation — NOT prompt instructions

The grader's output is rejected and re-requested if any of these fail. A cap that lives
only in the prompt is not a cap; this table is the actual anti-flattery mechanism.

| Check | Rule |
| --- | --- |
| Derived-quantity cap | `derived_quantity == null` ⇒ clamp `capacity_cost_estimation ≤ 1` |
| Derived-quantity integrity | reject if `derived_quantity` appears as a substring of the prompt text — the model echoed instead of deriving |
| Tradeoff cap | `tradeoff_axis_named == null` ⇒ clamp `tradeoff_articulation ≤ 1` |
| Relevance gate | `addresses_prompt == false` ⇒ clamp that axis ≤ 1 |
| Relevance integrity | reject if `prompt_constraint_engaged` is not a verbatim substring of the prompt |
| Band-3 evidence | `score == 3` and `band3_consequence == null` ⇒ reject and re-ask |
| Evidence integrity | reject if any `evidence_quote` is not a verbatim substring of the transcript — this catches paraphrase, which is where invented evidence enters |
| Attribution | `first_raised_by == "interviewer"` ⇒ clamp that axis ≤ 1 |
| Minimum criticism | fewer than 2 `below_bar_observations` ⇒ reject and re-ask |
| Axis set | any axis scored that is not in `axes_to_score` ⇒ reject |
| Contrast coverage | reject if `contrast.at_bar_answer` does not cover at least one beat from `<reference>.good` that the candidate missed, or if it contains a verbatim span of 8+ words from the candidate's transcript |
| **Grader arithmetic** | every `derivation_steps` entry must recompute from its own stated inputs to within **±5%**, with `units` present on inputs and result. A mismatch means the *grader* wrote arithmetic it did not check ⇒ reject and re-ask. **This check is about the grader, never about the candidate** |
| **Model completeness** | for any item declaring `required_terms`, the grader reports `terms_present` — which of those terms the candidate's derivation actually contained. A missing term **caps the axis at 2** (an incomplete model cannot be band 3) and is recorded, but **does not reject**. This is the check the first version did not have: all four errors it was written to catch were omitted terms whose arithmetic was internally consistent, so recomputation passed every one of them |
| **Candidate arithmetic** | where the candidate's own figure does not follow from their own inputs, the grader sets `candidate_arithmetic_error` with the recomputation and **scores the band accordingly** — >100× unnoticed is band 1, within ~2–3× is band 2. It must **never** reject. A validator that fails the grader for a candidate's bad arithmetic is unsatisfiable on exactly the transcripts the rubric most needs to score, and the first thing an on-call engineer does with an unsatisfiable gate is switch it off |
| Numeric consistency | reject a `band3_consequence` whose threshold or conclusion contradicts the candidate's own figures elsewhere in the transcript |
| Versioning | `grader_version` stamped on every row, always |

**Reject-and-re-ask, not repair.** Silently clamping a bad output teaches nothing and hides
how often the grader misses. Log every rejection with its reason; the rejection rate per
check is a live quality signal and belongs in `METRICS.md`.

### Why `required_terms` and not a tighter recomputation

The four arithmetic errors this pack has found in its own material were all the same shape:
a formula missing a term, applied correctly. `140/13,400` is exactly 10.4ms — the arithmetic
is flawless and the model is wrong, because a decode step also reads the batch's KV. Same
for prefill without the attention term, and a shuffle counting writes but not reads.

No recomputation check can catch that, because there is nothing to recompute incorrectly.
What catches it is knowing, per item, which terms a complete derivation contains — so each
item that has a load-bearing derivation declares `required_terms`, and the grader reports
which were present. A candidate who omits one is not wrong about arithmetic; they are
working with an incomplete model, which is the difference between band 2 and band 3 on
`capacity_cost_estimation`, and the cap encodes exactly that.

### Two things the first version of this table could not do

Both found by simulated reviewers, and both were holes rather than bugs.

1. **It enforced the *form* of a number and never its *truth*.** A candidate could state a
   threshold with no derivation, contradicting their own figures, and pass every row with a
   clean `band3_consequence`. That is exactly how one of the pack's own adversarial plants
   got written with circular arithmetic and expected to score band 3. Hence
   `derivation_steps` and the two numeric rows above: a quantity that earns a 2 or a 3 must
   recompute in code.
2. **The contrast-provenance check was theatre.** Trigram overlap against `model_answer` is
   structurally rigged to pass (the contrast is *generated from* `model_answer`), blind to
   the failure that matters — copying the candidate's *conclusions* rather than their
   wording — and it false-fires on the strongest candidates, whose answers legitimately
   resemble the reference. Replaced with required-beat coverage plus a verbatim-span check,
   which tests the thing the row was supposed to protect.

### Aggregation is not the grader's job

The grader emits **per-item, per-axis** scores and nothing else. Combining the 4 items that
score an axis into one axis score is **code**, by the rule in `rubric.md`
(mean of assessed items, continuous, never re-rounded to a band). The grader must never see
or emit an aggregate, a composite, a percentile, or a level claim — a model that knows the
level it is about to produce will grade toward it.

**The 12 plants in `calibration-plants.json` are the test suite for this prompt.** Each has
a required outcome. Run all 12 on every material prompt change; a failed plant is a defect,
not a score. The set includes a **negative control** for the relevance gate — the others
only test harshness, so without it a gate that clamps everything would pass the suite.
Which fixture that is stays in the plants file: naming it here de-blinds reviewers.

---

## Three defects these prompts exposed

Writing the prompts forced every rubric cell through "could a model actually apply this from
a transcript?", which is a different question from "is this legitimate". Three things broke.

### 1. The mock cannot run on the 12 diagnostic items

Prompt 1 requires `required_beats`, `traps`, `followup_tree`, and `at_bar_answer`. The 12
items in `questions.json` have `good`, `bad`, `model_answer`, and a 5-branch `followups`
list — the diagnostic schema, which is thinner by design. **The 45-minute mock is blocked on
the 40-scenario bank, which does not exist yet.** Prompt 1 is written and correct, and it
has nothing to run against. Not a defect in the prompt; a sequencing fact that was implicit
and is now explicit. Phase 2 is unaffected.

### 2. "Absence is band 0" was wrong as written

Rubric Appendix A says absence is band 0, never a missing value. That holds for a
45-minute mock, where all six axes are in scope. It is **wrong for a 60-second diagnostic
item**, which scores exactly 2 axes — the other 4 were never asked. Scoring them 0 would
feed four spurious zeros per item into the axis aggregation, and the level mapping sends any
axis at 0 straight below the senior bar. A perfectly good candidate would be graded below
bar by arithmetic.

Handled in Prompt 3 with an explicit `assessed` flag, and **fixed in `rubric.md` Appendix A**,
which now distinguishes the mock (all six axes in scope, absence is 0) from the diagnostic
(two axes scored, the rest `assessed: false`).

### 3. Nothing stopped the candidate getting credit for the interviewer's idea

The rubric's band definitions say "unprompted" and the level mapping leans on it, but no
output field recorded *who said it first*. In a 45-minute transcript where the interviewer
is probing continuously, a grader reading for behaviour will find the behaviour in the
candidate's agreement with a probe. Added `first_raised_by` to the schema and a clamp in
the validation table. This is the mock's analogue of the derived-quantity defect: the
behaviour is present in the transcript and the candidate did not produce it.

---

## Handoff

**To the build agent:** three prompts above, copy-paste ready. The validation table is code
with a test per row, not prompt text. Separate calls and separate model configs for
interviewer and grader — never one model, never one pass. Prompt-cache the
reference-solution block in Prompt 1; it is the dominant cost lever in a session. Prompt 2
is the cheapest call in the product and should not be on a frontier model. Log grader
rejections per check and report the rate.

**Open, and not mine to close:** Prompt 1 needs the 40-scenario bank before it can run,
so Phase 3 is sequenced behind that. Phase 2 is unaffected. Defects 2 and 3 are fixed in
`rubric.md` and the schema respectively.
