# REVIEWER 5 — hiring rubric operator — RUN 2

Scope: `rubric.md` as an instrument, all 24 cells. Part A done before reading `rubric.md`'s
appendices in detail, `questions.json`, or `prompts.md`; Part A scores were fixed before any
model answer was read, and I say below where that ordering matters.

**Files not opened:** `calibration-plants.json`, `dry-run-report.md`, `calibration-plan.md`,
`review-harness/findings/**`. No contamination to disclose.

**Process note before anything else.** `review-protocol.md:19` says "For each of the 5
answers"; `blind-scoring-set.md` contains **7** (`D4 F3 J2 H4 P7 N7 W7`), and its own header
says 7. I scored all 7. One of the two files is stale, and since the protocol is the contract
every reviewer reads, a reviewer who trusts it may stop at 5 and silently drop two cells from
the agreement measurement. Fix the protocol to say "the answers in the set" rather than a count.

---

# PART A — BLIND SCORING

```
Answer D4 / capacity_cost_estimation: 3
  cell clause applied: "the result changed the design: ... revealed that the stated SLO is
    unachievable at the stated budget — and they said so"
  evidence: "about 0.6 of baseline, so near one fifty-seven. That is over the one-fifty
    ceiling. ... To get under the ceiling I need the 400B share below about 4 percent. That
    is the number I would hold the routing policy to."
  admits another reading: yes — 2. The band-2 required clause is "named which constraint
    binds — memory capacity vs memory bandwidth vs compute vs network vs dollars". That list
    reads as closed, and this candidate never utters a constraint-class statement; they name
    the binding *term inside* the cost (the 400B share). A literal reader scores 2 for a
    missing required clause. I score 3 because dollars-against-a-ceiling is the whole frame
    and the number forced an admission policy, which is the band-3 clause verbatim.
```

```
Answer D4 / high_level_design: 0
  cell clause applied: "No end-to-end path. ... Could not say what happens to a single
    request from arrival to response."
  evidence: (absence) the entire answer is "Cost per token tracks weight bytes read ... That
    is the number I would hold the routing policy to." No component, no path, and the
    prompt's second half — "what do you measure to know you have not quietly made the
    product worse" — is never touched.
  admits another reading: yes — 1, and I expect reviewers to split here. Band 1's three
    clauses all presuppose that something design-shaped was produced ("a box diagram that
    does not satisfy...", "components named by brand...", "added a cache ... by reflex"), so
    band 1 is unreachable for an answer with no design at all, which forces 0. But the
    scoring contract's band 0 says "nothing in the answer depended on it", and a routing
    policy does presuppose a router. A grader reluctant to put a 0 next to a 3 on the same
    answer will reach for 1 — and nothing in the rubric stops that halo. I score 0 because
    the cell is written to be scored on what appeared, and nothing appeared.
```

```
Answer F3 / high_level_design: 3
  cell clause applied: "the design visibly follows from the numbers or the requirement cut
    rather than from a template — the component boundary is where it is because of a
    quantity they computed"
  evidence: "at even 100 gigabytes a second of sustained I/O that is on the order of 11
    hours, so it is not something you do every epoch. I would shuffle once into shards at
    ingest and do cheap in-shard shuffling plus shard-order randomisation per epoch"
  admits another reading: no, on the cell as written. Flagging for the record that the
    driving number is 2x low (see B3) and that the 2,000-GPU read path never appears; both
    are indicators, not the required clause, and I noticed the 2x only after Part A closed.
```

```
Answer F3 / deep_dive_failure_modes: 2
  cell clause applied: "Required: picked the genuinely hard component and named a concrete
    failure mode of *this* design — not of distributed systems in general — with its
    mitigation."
  evidence: "which is where the trust problem probably comes from: nobody has measured the
    resulting distribution. I would add a verification job that samples it."
  admits another reading: yes — 3, and this is my second-least-confident cell. The
    verification job is a component added because of a weakness the candidate found
    unprompted, which maps onto band 3's "a failure mode they found changed the design". I
    score 2 because the axis header (`rubric.md:262-263`) enumerates what counts as a
    failure mode — "partial failure, backpressure, overload, retry amplification,
    idempotency, eviction, head-of-line blocking" — and **not one of them appears**. A
    missing measurement is a verification gap, not a failure mode. The deeper issue is that
    this axis is written for serving systems and transfers badly to a batch data-pipeline
    item; see B5.
```

```
Answer J2 / capacity_cost_estimation: 2
  cell clause applied: "Required: named which constraint binds ... and supported it with a
    quantity they derived" + indicator "showed why the other constraints have slack"
  evidence: "about 40 terabytes raw, which makes memory the binding constraint here.
    Latency has slack — 50 milliseconds is generous for an approximate lookup"
  admits another reading: yes — 3. IVF-PQ *is* the response to 40TB, so a grader who joins
    those two facts awards the band-3 clause. I score 2 because the candidate's stated reason
    is "it's what most billion-scale deployments run" — a popularity claim, not the number —
    and `prompts.md:245` forbids supplying the missing word. The 2-vs-3 here turns entirely
    on whether the grader obeys that instruction, which makes it a reliability hazard rather
    than a judgement call.
```

```
Answer J2 / tradeoff_articulation: 1
  cell clause applied: "chose, but justified it with an unfalsifiable claim ('it's more
    scalable', 'it's industry standard', 'it's more flexible')"
  evidence: "I'd go with IVF-PQ — it's what most billion-scale deployments run."
  admits another reading: yes — 0. Band 0's clauses are *also* all satisfied: no alternative
    considered, one design presented as the design, no comparative language anywhere. The
    prompt asked "tell me what the choice costs you" and the answer never says what it
    costs — PQ's cost is recall, against a stated 0.9 floor, and "keep an eye on recall" is
    not a cost. Bands 0 and 1 are simultaneously true and the rubric gives no precedence
    rule. I score 1 because the band-1 clause is the more specific match.
```

```
Answer H4 / deep_dive_failure_modes: 3
  cell clause applied: "a failure mode they found changed the design — ... an idempotency
    key added because the retry path double-charges"
  evidence: "The actual bug is that retrying the whole turn re-executes side effects, so we
    are duplicating emails and double-charging. I would put an idempotency key on each
    logical operation, generated once per turn."
  admits another reading: yes — 2, and possibly 1. The candidate then abandons it entirely
    ("that is probably fine actually ... Let's go with that"), so at the end of the
    transcript the design is tool-layer retries with no idempotency key and the failure mode
    changed *nothing*. No cell on this axis says whether a withdrawn insight still counts;
    `prompts.md:261-264` tells the grader that abandoning a correct position with no defence
    is below bar, but scopes that to pushback handling, which is the other axis. I score 3
    because the behaviour was performed unprompted and precisely and the collapse is exactly
    what `communication_collaboration` exists to catch; double-penalising it here is not
    authorised by any clause. This is my hardest cell — see the end of Part A.
```

```
Answer H4 / communication_collaboration: 1
  cell clause applied: "Collapsed at the first push — abandoned a correct design because it
    was questioned, with no attempt to defend it."
  evidence: "Yeah, you know what, that is probably fine actually. If the retries live at the
    tool layer then each tool handles its own failure, which is cleaner separation anyway.
    Let's go with that."
  admits another reading: yes — 2. Band 2's required clause is "engaged that specific
    objection, either conceding and saying what changes or holding the position with a
    reason". The candidate *did* concede and *did* say what changes (go with tool-layer
    retries). Read literally, a total collapse satisfies the required clause, and under the
    band-2 rewrite the indicators cannot block it. I score 1 because the concession does not
    engage the objection — tool-layer retries do not fix a non-idempotent side effect, which
    the candidate had just explained — but the overlap between this band-1 clause and that
    band-2 required clause is a defect, not a close call.
```

```
Answer P7 / requirements_scoping: 3
  cell clause applied: "cut scope in a way that visibly changed the design — dropped a
    requirement, relaxed a consistency guarantee, or deferred a feature, and said what the
    cut bought"
  evidence: "the long-context 5 percent held to its own, worse target rather than blended
    into one p99. ... Out of scope: tuning the eviction policy. No policy frees 32
    gigabytes; this is about admitting long requests against a reserved share of memory."
  admits another reading: no on the band, yes on whether the band is observable here. Band 3
    across all six axes rests on "unprompted" / "before being pushed", and this item's prompt
    says "Before you design anything: what exactly are you protecting, and what is the first
    number you would want?" — it asks for the band-3 behaviour. The candidate cannot
    volunteer what they were told to produce. I score 3 as written and flag in B4 that
    "unprompted" is unscorable on this item.
```

```
Answer P7 / capacity_cost_estimation: 3
  cell clause applied: "the result changed the design: the number ruled out an architecture
    ... forced an admission-control policy"
  evidence: "With 80 layers, 8 KV heads, head dimension 128 in bfloat16, that's about 320
    kilobytes a token, so a 100,000-token request is around 32 gigabytes ... No policy frees
    32 gigabytes; this is about admitting long requests against a reserved share of memory."
  admits another reading: no. Derived (not echoed, not a recited spec figure used in no
    arithmetic step), binding constraint named as memory capacity on cards "mostly holding
    weights already", and the number rules out an architecture. Cleanest 3 in the set.
```

```
Answer N7 / capacity_cost_estimation: 1
  cell clause applied: "Derived the number that decides the question, then proposed a design
    it rules out (computed 40TB raw, then chose an index that needs all of it resident) —
    the number was produced but not understood."
  evidence: "about 40 terabytes raw. ... Given the recall requirement I would use HNSW"
  admits another reading: barely — 2, if a grader treats "40 terabytes raw" plus the recall
    floor as naming a binding constraint. It does not: the candidate never says what binds,
    and the cell says "a correct number with no statement of what it binds is also band 1".
    Also uncaught by the cell: HNSW degrades under 200M daily mutations, the second number
    they computed and ignored. Confident 1.
```

```
Answer N7 / tradeoff_articulation: 1
  cell clause applied: "named a trade-off that isn't one in this scenario"
  evidence: "because it has the best recall-latency curve of the ANN families — typically
    0.95-plus recall at single-digit millisecond latency"
  admits another reading: yes — 2, and **the code path produces 2, not 1.** The band-2
    required clause is "named the axis of the trade-off in units ... and picked a side":
    recall-vs-latency is in units, is on the rubric's own enumerated list ("recall vs p99"),
    and HNSW is a side. The hard cap does not bite (`tradeoff_axis_named` is non-null) and
    the relevance gate does not fire (`prompt_constraint_engaged` = "recall at 10 must stay
    at or above 0.9" is a verbatim substring of the prompt, so `addresses_prompt` stays
    true). I score 1 because latency has 50ms of slack here, so recall-vs-latency is not a
    live trade-off, and the cost the prompt asked for — memory, and update churn — is never
    named. But nothing in the enforced rules reaches that judgement. See B5 defect 2.
```

```
Answer W7 / requirements_scoping: 1
  cell clause applied: band 1, "Listed eight requirements and prioritised none" (applied to
    the cost components) — and the answer is one clause short of band 0's "Treated an
    underspecified prompt as a specification."
  evidence: "The judge calls add more depending on which judge model. There is also cold
    start on the replicas which I have not accounted for, and sharding overhead. Storage for
    the results is negligible. Network egress depends on where the judge runs."
  admits another reading: yes — 0. "Never bounded the problem" and "treated an
    underspecified prompt as a specification" are both literally true: nothing is out of
    scope, nothing is cut, nothing is asked, and the prompt explicitly invited pushback
    ("tell me what you would push back on") and got none. I score 1 only because band 0 is
    an undeclared four-clause conjunction and one clause ("never named a non-functional
    requirement") is false — the candidate works the 10-minute budget throughout. That is a
    band placement decided by a conjunction the author never declared, which is precisely
    the defect the band-2 and band-3 rewrites were for.
```

```
Answer W7 / communication_collaboration: 1
  cell clause applied: "Answered a different, easier question than the one asked and did not
    acknowledge the substitution."
  evidence: "Okay so 50,000 times 2,000 is 100 million tokens." ... "Network egress depends
    on where the judge runs." (the answer ends there; the prompt's second ask is never
    addressed)
  admits another reading: yes — 2. The prompt asked two things and the candidate answered
    one well. Band 2's required clause is singular — "answered the question that was actually
    asked" — and the rubric never says what happens when an item asks two. A grader can
    honestly call the costing "the question". I score 1 because the dropped half was the
    judgement half and the substitution is unacknowledged. Note also the register failure:
    the audience is named in the prompt ("I am a research engineer") and the answer is an
    unsignposted wall of arithmetic ending in a $544,580 figure given to the dollar.
```

### Hardest cell to apply, and why

**`deep_dive_failure_modes`, band 2 vs 3, on `H4`.** The candidate performs the band-3
behaviour exactly as the cell describes it — the rubric's own worked example is "an
idempotency key added because the retry path double-charges" — and then retracts it under one
sentence of pushback, ending the turn endorsing the design that double-charges. Band 3 says "a
failure mode they found changed the design". At the moment it was said: yes. At the end of the
transcript: no. **Nothing in `rubric.md` says which of those two the axis scores**, and the
question generalises to every content axis: does a withdrawn correct answer score the content
axis, or only the communication axis? `prompts.md:261-264` has the only guidance and it is
scoped to pushback handling. I score 3 and expect other reviewers to score 2; whichever way
the pack rules, the rule has to be written into all five content cells, not just implied. The
sharpest version of the problem: H4's final position is verbatim the item's own `bad`
("Adds retries at the tool layer, which is the teammate's proposal"), and the rubric as
written awards it a 3.

---

# PART B — CRITIQUE

## B1. Axis legitimacy

**Yes, the six axes correspond to what a structured design round scores — but they are not
six independent axes, and the instrument treats them as if they are.**

Three of the six band-3 required clauses are **the same behaviour**: a quantity the candidate
produced moving a decision.

- `capacity_cost_estimation` band 3 (`rubric.md:212`): "the result changed the design"
- `high_level_design` band 3 (`:252`): "the design visibly follows from the numbers"
- `tradeoff_articulation` band 3 (`:298`): "the trade-off was resolved against a number they
  produced"

So one behaviour unlocks half the ceiling of a composite that `:129` uses for the percentile,
and a candidate who does not do arithmetic out loud is capped at 2 on three axes regardless of
their design judgement. That is a defensible choice for an AI-infra round — the rubric argues
for it at `:364-375` — but it is a **weighting** decision made implicitly inside three band-3
cells rather than stated in the composite, and `:382-384` claims "No weighting by level in the
axis definitions themselves". The honest version is to say on the public page that the
percentile is roughly half a numeracy score.

Second structural problem, visible only from `questions.json`: the axis **pairings** are fixed,
and `requirements_scoping` and `communication_collaboration` share **3 of their 4 items**
(`inline-safety-classifier-budget`, `eval-infra-per-commit-cost`,
`annotation-throughput-vs-agreement`). Those two axis scores are computed from 75% the same
evidence, so they will correlate for structural reasons and the "profile shape" the level claim
reads (`:130-131`) has fewer effective dimensions than six. `W7` is the live demonstration: one
omission — not pushing back — drove both of its scores to 1. Meanwhile `tradeoff_articulation`,
the axis gated at every level, never co-occurs with either of them, so the gating axis gets no
evidence from the three stakeholder-facing items.

On `communication_collaboration` specifically, which my brief singles out: **the band-2 rewrite
fixed this axis, and I did not expect to say that.** The required clause — "answered the
question that was actually asked ... engaged that specific objection" — is observable behaviour,
not polish, and the polish-shaped clauses ("stated the shape of the answer before giving it",
"signposted transitions", "matched register") are demoted to indicators that cannot block a 2.
A strong non-native speaker who answers the question and engages the objection gets a 2.

The bias did not disappear, it **moved to bands 0 and 1**, which were not rewritten. Band 0 is
"near-silence requiring the interviewer to extract every step"; band 1 is "Talked continuously
without signposting". Both are judgements about speech volume and fluency, both are undeclared
conjunctions, and both are where a non-native speaker or a candidate who thinks before speaking
will land. In a 60-second voice item, five seconds of thinking is 8% of the budget. The axis's
own cited support (`:315-316`, [IIO-1]) is that long silence is held against senior candidates —
that is guidance about a 45-minute session being imported into a 60-second one.

**What this rests on:** the text of the six cells, the axis-to-item mapping in
`questions.json`, and 14 applications of the cells in Part A. It does **not** rest on loops I
have run — I am a simulated reviewer and nothing in this report should be weighted as
observation of real interview practice. **What would change my mind:** the correlation matrix
from the first 50 graded sessions. If `requirements_scoping` and `communication_collaboration`
correlate above ~0.8 and `capacity_cost_estimation` correlates above ~0.7 with
`high_level_design` and `tradeoff_articulation`, the axes are not measuring six things and the
scorecard should show four. If they do not, I am wrong about the magnitude and the structural
argument stands only as a caution.

## B2. Scenario realism — the operator-adjacent items

I defer to the domain reviewers on technical realism and comment only where the item's shape
interacts with scoring.

**`eval-infra-per-commit-cost` (W7) — realistic-but-wrong-in-one-detail.** The ask is exactly
the right shape of unreasonable. The one thing wrong: the prompt says "Each evaluation is one
2,000-token generation **plus a judge call**" and then says "Tell me what that costs" — but
gives no judge model and no judge token count, so a material cost term is **uncostable by
construction**. The pack's own model answer punts on it ("plus the judge calls"), and `good`
does not list "flagged the judge call as the uncosted term" as a beat. On an item that scores
`requirements_scoping`, handing the candidate an uncostable term and then not rewarding them for
naming it is a trap on the item, not on the candidate. Fix: state the judge's token count, or
add that beat to `good`.

**`agent-retry-side-effects` (H4) — realistic.** Most wrong detail: "p99 tool latency is 8
seconds" is stated and then **used by nobody** — not by `model_answer`, not by `good`, not by
`bad`. The natural use is the one that makes whole-turn retry indefensible: 12 tools at p99 8s
is up to ~96 seconds of fan-out, so a retried turn is a two-minute turn. The item scores
`deep_dive_failure_modes` and `communication_collaboration`, so a candidate who does that
arithmetic earns nothing for it.

**`heterogeneous-fleet-routing` (D4) — realistic.** Most wrong detail: "a mixed fleet of A100s
and H100s" is in the premise and plays **no part in the answer**. The model answer's cost model
tracks parameters only. By my own calculation, decode cost tracks memory bandwidth, and A100
SXM 80GB (~2.0 TB/s, recalled not cited) against H100 SXM (3.35 TB/s, `rubric.md:459`) is a
~1.65x difference in $/token for the same model — **larger than the gap between the derived
$1.57 and the $1.50 ceiling**. So which fleet serves the 400B is decisive for the exact
question the item asks, the 4%-share threshold is not robust to it, and a candidate who raises
it finds no beat in `good` to land on. Either drop the heterogeneity from the premise or make
fleet placement a scored beat; as written it is a decorative constraint in an instrument whose
relevance gate is about engaging the prompt's stated constraints.

## B3. Arithmetic

Everything I could check in Appendix B recomputes, with two exceptions and one near-miss. My
own calculations:

**Wrong — `rubric.md:521-524`, token economics.** The text reads "At ~6,000 output tok/s — the
KV-corrected figure, not the weights-only 6,000 — that is ≈ **$0.47 per million** output
tokens". The sentence names the same number as both the corrected and the uncorrected figure,
and $0.47 does not follow from 6,000:

```
$2/GPU-hr x 4 GPUs = $8/hr
at 6,000 tok/s:  8 / (6000 x 3600) x 1e6 = $0.370 / M   <- weights-only
at 4,700 tok/s:  8 / (4700 x 3600) x 1e6 = $0.473 / M   <- KV-corrected, matches the $0.47
```

4,700 tok/s is the figure the appendix itself derives eight lines earlier (`:485`). The fix is
one word: "At ~4,700 output tok/s". This matters more than a typo because `model_answer`s are
written from this appendix and the judge is anchored on them (`:450-451`), and because it is a
fifth wrong number in the block whose own header announces that four were found and corrected.
Worth asking why the correction pass that produced 4,700 did not propagate 15 lines down.

**Missing — `rubric.md:456` promises a correction that is not in the appendix.** The preamble
lists four corrected numbers including "the shuffle figure counted writes but not reads.
Corrected below with the omitted term shown in each case." There is **no shuffle derivation
anywhere in Appendix B** (`grep -n -i shuffle rubric.md` returns only line 456). The corrected
number does exist — in `questions.json`, `training-data-dedup-and-shuffle.model_answer`: 4PB
read + 4PB written = 8PB moved, ~22 hours. So the spec-of-record is missing a number its own
model answer teaches. My calculation: 4e15 / 1e11 = 11.1h for writes alone; 8e15 / 1e11 = 22.2h
for the operation.

**This is the live cost of that gap.** Blind answer `F3` says "a true global shuffle of 4
petabytes means writing 4 petabytes — at even 100 gigabytes a second ... on the order of 11
hours". That is arithmetically correct for the claim as stated and **2x low for the operation**,
which is exactly the error the preamble says was found and fixed. It is unscoreable: that item
scores `high_level_design` and `deep_dive_failure_modes`, so no cell registers a 2x I/O error,
and `prompts.md`'s **Numeric truth** check (`:322`) recomputes stated inputs to stated
results — 4e15/1e11 does equal 11h, so the check **passes**. Which generalises to my second
defect in B5.

**Checked and correct** (my recomputation, Appendix B): KV/token 2x80x8x128x2 = 327,680 B;
100k ctx = 32.77 GB; 32.77/640 = 5.12%; 32.77/80 = 41.0%; 8B-class = 131,072 B; TP=4 aggregate
13.4 TB/s; batch-64 KV 41.94 GB = 30.0% of 140 GB; step 13.58 ms; 4,714 tok/s; weights-only
6,126 tok/s; prefill crossover 70e9/(8192x80) = 106,812 tokens; 10k = 1.53 PFLOP (attention
8.6%) ~0.96s; 100k = 27.1 PFLOP (attention 48.3%) ~16.9s; 1.584 PFLOPS at 4x990x40%.
Near-miss: the batch-1 decode floor is **10.50 ms** by my arithmetic, stated as 10.4 ms — 1%,
within rounding, but it is the one figure given to three significant figures.

**Blind-set answers, checked:** `D4` correct throughout (0.605 of baseline = $1.573; exact
break-even on the 400B share is 1.50/2.60 = 0.5769 = 0.37 + 4.7x, so **x = 4.40%** — the
candidate's "below about 4 percent" is conservative and right, as is the model answer's).
`H4` 1 - 0.98^12 = 21.5%. `P7` 320 KB/token and ~32 GB both exact. `W7` every figure correct
(100M tokens; 166,667 tok/s; 27.8 -> 28 replicas; 112 GPUs; 18.67 GPU-hr; $37.33; $1,493/day;
$544,580/yr from their own rounded $1,492). `J2`/`N7` 4 KB/vector, 40 TB, 2% churn all correct.

Note on `W7`: the arithmetic is *more* precise than the model answer's, and six significant
figures on an annualised number built from four unvalidated assumptions is a signal — of
false precision and unflagged assumption stacking. **No cell in the rubric penalises it.** The
closest is a band-3 *indicator* on `capacity_cost_estimation` ("Rounded in the conservative
direction on purpose and said which direction that was"), and that item does not score that
axis. A rubric this numeric should be able to mark down a candidate for spurious precision.

## B4. The band 2/3 boundary

**For the content axes it is in roughly the right place, it is slightly too generous in the
60-second diagnostic, and it is unapplicable in two specific situations that I hit in 3 of 14
cells.** But the more useful finding is that **my disagreements are not at 2/3 at all.**

Of my 14 cells, the band that admitted two readings was 2-vs-3 in 3 cells and **0-vs-1 or
1-vs-2 in 4** (`D4`/high_level 0v1, `J2`/tradeoff 1v0, `W7`/requirements 1v0,
`H4`/communication 1v2). The author found a conjunction defect in band 3, fixed it, found the
same defect in band 2, fixed it (`:60-71`) — and stopped. Bands 0 and 1 are still undeclared
conjunctions with no required clause and **no precedence rule against each other or against
band 2**. This is the thing my experience of calibration sessions says loudest: interviewers
disagree where the author is not looking. The author twice diagnosed this exact defect
correctly and twice stopped one band short of finishing it.

On the band-3 rewrite itself (one required clause, rest as indicators): **right call, and it
made the band operable rather than mushy** — but in the 60-second diagnostic the required clause
degenerates into an answer *shape*. "The result changed a design decision", with no room for
indicators (`:56-58` concedes this), is satisfied by any answer that ends in a threshold or a
policy — and in 60 seconds a threshold or a policy is the only thing a candidate has room to
state. 4 of my 5 threes (`D4` capacity, `F3` high_level, `P7` both) end in exactly that shape:
"...so I'd hold X below Y". That is a testable prediction: **count what fraction of band-3
awards in the first 50 sessions come from answers whose last sentence states a numeric
threshold.** If it is most of them, the clause is scoring a rhetorical template, and the fix is
to require the threshold to be *derived from the candidate's own earlier number*, which `N7`
shows is a different test.

The two situations where 2/3 is unapplicable:

1. **The item prompt asks for the band-3 behaviour.** `P7`: "Before you design anything: what
   exactly are you protecting, and what is the first number you would want?" Band 3 on all six
   axes rests on "unprompted", which `:162` calls the senior/staff discriminator. The grader
   schema's `first_raised_by` has only `candidate | interviewer` — **there is no value for "the
   prompt asked for it"**, so the attribution clamp (`prompts.md:324`) cannot fire and the item
   hands out 3s for compliance. Either add a `prompt` value and clamp it, or drop "unprompted"
   from band 3 on items whose prompt solicits the behaviour.
2. **The behaviour is performed and then withdrawn** (`H4`; see end of Part A).

## B5. Top 3 defects, ranked

### 1. The level mapping will put the modal competent candidate below the senior bar — and in the 45-minute mock it is not computable at all

`rubric.md:133-140`, with `:115-126`.

**What is wrong, part one (the mock — a flat internal contradiction).** `:115-117`: "If fewer
than 2 items assessed an axis ... the axis is reported as *insufficient signal* and is excluded
from the level claim rather than scored." `:121-122`: "In the **45-minute mock** there is one
scenario and all six axes are scored once ... The thresholds below apply unchanged." One is
fewer than two. By the rubric's own rules, **every axis in the 45-minute mock is insufficient
signal and excluded, leaving no axes to evaluate the level claim from.** The two rules are eight
lines apart and contradict directly. (Latent rather than live: `prompts.md:371-380` says the mock
is blocked on a 40-scenario bank that does not exist. It becomes a shipping bug the day that
bank lands, on the paid tier.)

Second, quieter mock problem: with one scenario, `axis_score` is an integer, so the thresholds
1.75 and 2.50 silently become **2 and 3**. The mock's staff bar needs two straight 3s where the
diagnostic's can be met by {3,3,2,2}. "The thresholds below apply unchanged" is true of the
numbers and false of the bar.

**What is wrong, part two (the diagnostic — a floor effect).** Each axis is a mean of 4 items
(`:124-126`), each item scores 2 axes, each answer is 60 seconds. A 60-second answer has room
for one axis's band-3 behaviour or two axes' band-2 behaviour, not both — `D4` is the clean
demonstration, scoring **3 on `capacity_cost_estimation` and 0 on `high_level_design` from the
same 90 words**, and it is the pack's own model answer with its second half removed. If a
competent candidate spends each item on one of its two axes, each axis sees roughly half its
items deep and half shallow:

```
axis mean ~ (2 x 2.5 + 2 x 0.5) / 4 = 1.50
```

which lands every axis **exactly on the "≥3 axes < 1.50" knife edge**, and any axis that draws
a 0 plus three 1s is 0.75, which trips "any axis < 1.00" and sends the whole scorecard below the
senior bar on its own. Supporting signal from Part A: of my 14 cells, **7 are 0 or 1** on
answers that are individually competent, and `prompts.md:247-250` instructs the grader never to
smooth that.

**Why it matters.** This is the public status claim and the growth engine. A floor effect makes
the percentile useless in the direction that matters — everyone clusters below the senior bar —
and the three-row table collapses into a one-clause test ("any axis < 1.00"), which destroys the
profile-shape reading the table exists to implement.

**What I would do.** (a) Fix the mock contradiction: exempt the single-scenario mock from the
insufficient-signal rule explicitly, and state the mock's effective thresholds as integers.
(b) Replace "any axis < 1.00" with "≥2 axes < 1.00", so one unlucky axis cannot decide the
claim. (c) Before any level claim ships, run the 12 items against ~20 hand-scored sessions and
**publish the axis-score histogram**; if the modal axis mean is 1.25-1.75 the thresholds are
miscalibrated downward and the fix is the thresholds, not the candidates. (d) Treat "which of
an item's two axes did the candidate spend the 60 seconds on" as a known confound and consider
scoring one axis per diagnostic item with 24 items, or stating a per-axis word budget.

### 2. Bands 0 and 1 are still undeclared conjunctions, with no precedence rule — which breaks the rubric's own hard cap

`rubric.md:181-182, 209-210, 249-250, 274-275, 295-296, 324-325`, against the hard cap at
`:350` ("Band 0 vs 1 must be distinguishable from the transcript | If the grader can't tell,
the cell is badly written").

**What is wrong.** The author declared Required/Indicators for all six band-2 cells and all six
band-3 cells and left bands 0 and 1 as 3-to-5-clause conjunctions. Three consequences, all of
which I hit:

- **0 vs 1 is undecidable for an answer with no design.** `D4`/`high_level_design`: all three
  band-1 clauses presuppose something design-shaped was produced, so they cannot match, which
  forces 0 — while the scoring contract's band 0 ("nothing in the answer depended on it")
  argues the other way.
- **0 and 1 are simultaneously satisfied with no precedence rule.** `J2`/`tradeoff`: band 0's
  "no alternative considered / one design as the design / no comparative language" and band 1's
  "chose, but justified it with an unfalsifiable claim" are both true.
- **A band placement turns on a conjunction clause the author never meant to be load-bearing.**
  `W7`/`requirements`: band 0 fits except for "never named a non-functional requirement", so the
  score is 1 instead of 0 because one clause of four is false.

And the bias consequence from B1: on `communication_collaboration`, bands 0 and 1 are the
fluency-and-volume bands, so the axis most likely to encode bias has its discipline exactly
where the bias is not and not where it is.

**Why it matters.** The level mapping reads band 2 (`:62`), but **the 0/1 line decides whether
the "any axis < 1.00" clause fires**, which per defect 1 is the clause that decides the public
claim. A 1-vs-0 disagreement on one item moves an axis mean by 0.25 and can move the level
claim. Inter-rater disagreement in Part A concentrated here, not at 2/3.

**What I would do.** Give bands 0 and 1 the same Required/Indicators treatment, and add one
precedence line to the scoring contract: *the lowest band whose required clause is satisfied
wins, and band 0 requires the behaviour to be wholly absent — any attempt at the behaviour,
however poor, is at least band 1.* That single sentence resolves all four of my 0/1 and 1/2
splits.

### 3. The one code check that was added to catch Appendix B's class of error cannot catch it — and nothing scores a withdrawn answer

`prompts.md:322` (Numeric truth), with `rubric.md:455-457`.

**What is wrong.** All four errors Appendix B announces as found and corrected are **omitted
terms in a formula**, not arithmetic slips: the KV-vs-node-HBM comparison (wrong denominator),
the decode floor (omitted KV reads), the prefill estimate (omitted attention FLOPs), the shuffle
figure (omitted reads). The Numeric truth check recomputes "if the stated result does not follow
from the stated inputs" — so **zero of the four would be caught by it**. `F3` proves it live:
"writing 4 petabytes ... on the order of 11 hours" recomputes perfectly and is 2x low for the
operation. The check validates arithmetic and is blind to the model, which is the error class
this pack has actually produced four times (five, with B3's $0.47 sentence).

Second, smaller item under the same head: **no cell says what happens to a content axis when a
correct, design-changing insight is withdrawn under pushback.** `H4` scores band 3 on
`deep_dive_failure_modes` while ending on the item's own `bad`.

**Why it matters.** The numeric checks are described as "the actual anti-flattery mechanism"
(`prompts.md:313-314`), and this one is load-bearing for every 2 and 3 awarded on a quantity.
An instrument that teaches candidates to be numerate must not award band 2 to an answer whose
formula is missing a term that doubles the answer.

**What I would do.** (a) Add the omitted shuffle derivation to Appendix B as promised at `:456`,
with the 8PB term shown, and fix the `$0.47`/6,000 sentence. (b) Extend `derivation_steps` with a
`terms_included` list, and for the four or five recurring derivations (KV bytes, decode floor,
prefill, I/O for a shuffle, $/M tokens) assert in code that the required terms are present —
checking the *shape* of the formula, not just the multiplication. (c) Add one clause to all five
content axes' band 2/3: whether a retracted behaviour counts, and which way.

**Also found, below the top 3, cheap to fix:**
- `rubric.md:62-63`: "band 2 is the band the level mapping actually reads. Every row of **the
  table above**..." — the level-mapping table is *below*, at `:133-140`. The aggregation section
  was inserted above it (`:97-100`) and the back-reference was not updated.
- Band-1 clauses on `requirements_scoping` (`:182`) and `capacity_cost_estimation` (`:210`) turn
  on "only after being asked twice". `prompts.md` allows the diagnostic probe "at most once per
  item", so **"asked twice" is unreachable in the diagnostic** and those clauses are dead text in
  the instrument that will run first.
- `prompts.md:318` rejects a `derived_quantity` that "appears as a substring of the prompt text".
  Short numeric strings collide: a `P7` candidate who correctly derives "about 5 percent of a
  node" is rejected as an echo because the prompt contains "5 percent". Compare normalised
  numbers in context, not substrings.
- "Do not reward being right about policy while producing no design. Correct and useless is below
  bar" (`prompts.md:259-260`) is a band-placement rule — it decides `D4`/`high_level_design` —
  and it exists **only in the grader prompt**, while `rubric.md:3-4` claims to be "the judge's
  spec and the scorecard's source of truth". Move it into the `high_level_design` cells.

## B6. Sign-off

**What I would refuse to let ship as-is:**

1. **The level claim**, in any form, on either tier — already the pack's own position
   (`:142-148`), and I am adding two reasons it does not yet have: the mock-path contradiction
   between `:115-117` and `:121-122`, and the floor-effect argument in B5. Showing a percentile
   while hiding the level claim does not avoid this: the percentile reads the same composite.
2. **Bands 0 and 1 as written**, because the 0/1 line decides the "any axis < 1.00" clause and
   four of my fourteen cells turned on it.
3. **Appendix B with the `$0.47`/"~6,000" sentence and the missing shuffle derivation**, because
   `model_answer`s are written from it and the judge is anchored on them.

**Would I put my name on this rubric as legitimate? Yes — on the axes and on the band 2/3 cells.
No on the level mapping.** The caveat has two parts. First, the six cells I applied 14 times are
the most operable interview rubric I have read in this format: the Required/Indicators structure
works, the band-1 cells name observable things instead of adjectives, the derived-quantity cap is
the right mechanism and is correctly written ("of their own" is load-bearing and they got it
right), and `communication_collaboration` band 2 scores behaviour rather than polish, which is
rare. Second, the *scoring* is more trustworthy than the *verdict*: everything above the
per-item scores — aggregation, composite, level — is where I would not sign. That is the better
failure to have, because per-item scores are what you calibrate against hand-scored sessions, and
the verdict layer is cheap to change once you have them.

## B7. Epistemic status

**Checkable facts** (anyone can verify from the files; no judgement):
- `rubric.md:521-524` states ~6,000 tok/s and derives $0.47/M, which follows from 4,700 (B3).
- `rubric.md:456` promises a corrected shuffle figure; Appendix B contains no shuffle derivation.
- `rubric.md:115-117` vs `:121-122`: in the one-scenario mock every axis has one assessing item,
  so the insufficient-signal rule excludes every axis from the level claim.
- `rubric.md:62-63` says "the table above" for a table that is below.
- Bands 0 and 1 have no Required/Indicators split and no precedence rule, while bands 2 and 3 do.
- Three of six band-3 required clauses are the same behaviour (a number moving a decision).
- `requirements_scoping` and `communication_collaboration` share 3 of 4 items in
  `questions.json`; all six axes have exactly 4 items.
- `prompts.md` `first_raised_by` has no value for "the prompt asked for it".
- Numeric truth recomputes stated inputs to stated results, so all four of Appendix B's
  announced corrections (omitted terms) fall outside it; `F3`'s 11h passes it.
- All Appendix B arithmetic I recomputed is otherwise correct; the batch-1 floor is 10.50ms vs
  10.4ms stated.
- `review-protocol.md:19` says 5 answers; the set has 7.

**Domain judgement, which I expect a rubric practitioner to mostly share:**
- Bands 0/1 are where inter-rater disagreement concentrates, not 2/3, and the author stopped one
  band short of finishing a defect they diagnosed correctly twice.
- The band-3 required clause selects for answer shape ("...so I'd hold X below Y") in a 60-second
  format.
- "Correct and useless is below bar" belongs in `rubric.md`, not only in the grader prompt.
- The 14 Part A scores themselves. I would expect ~70-80% exact agreement with another careful
  reviewer and disagreement concentrated on the four cells I flagged as 0v1 / 1v2, plus `H4`
  deep_dive and `N7` tradeoff.

**Guesses about interview practice that need a human to confirm:**
- That the six axes match what a real design loop scores (B1). I have not run loops; nothing in
  this report should be weighted as observation of real interview practice, and that applies to
  every sentence in B1 and B4 regardless of the confidence it is written with.
- The **magnitude** of the floor effect in B5 defect 1. The mechanism is arithmetic, the
  parameters (how a real candidate splits 60 seconds between two axes) are a guess. My ~1.50 axis
  mean is an illustration, not a prediction, and 20 hand-scored sessions would settle it in a day.
- Whether band-1 cells read as diagnostic or insulting. Not my competence; the pack already asks
  for this at `:410-412`.
- Whether `communication_collaboration` bands 0/1 would actually penalise a non-native speaker.
  I can show the clauses are fluency-shaped; whether that translates into a score gap needs real
  transcripts from real speakers.
- The A100 bandwidth figure (~2.0 TB/s) in B2 is recalled, not cited. The argument needs only
  that A100 and H100 differ by more than the ~4% slack between $1.57 and $1.50, which is safe,
  but check the number before quoting it.

**What I had to assume because the pack did not say:**
- That `addresses_prompt` would be true for `N7` (it engages the prompt's stated recall floor,
  just not the binding constraint). If the gate is meant to fire there, say so in `:86-93`,
  because the gate's own wording says it tests "the answer's binding constraint and decision"
  while the enforced check only tests whether the quoted constraint is in the prompt.
- That a behaviour performed and then withdrawn still scores the content axis (`H4`). Genuinely
  undefined; I scored 3 and expect to be out-voted.
- That the lowest matching band wins when bands 0 and 1 both match (`J2`). Nothing says this.
- That `F3`'s and `J2`'s items may or may not be the same item as others in the set. The set says
  not to infer it and I did not; I scored `J2` and `N7` independently and only noticed afterwards
  that they share a prompt verbatim, which is visible in the set rather than inferred.
- That the diagnostic, not the mock, ships first. `prompts.md:371-380` implies it; the rubric
  does not say, and it changes which of my defect-1 findings is urgent.

**Where I am most likely wrong, per my own brief:** I have a bias toward structure for its own
sake. The band-3 "required clause plus indicators" structure may already be as mechanical as a
rubric can be before it stops measuring judgment, and my recommendation to add a `terms_included`
assertion to `derivation_steps` pushes further in the direction I am biased toward — it makes the
grader a formula checker, and a candidate who reasons correctly in an unusual decomposition will
fail it. Someone who cares more about measuring judgment than about reliability should review
that suggestion specifically. My AI-infrastructure depth is also dated: treat B2 and the A100
figure as prompts for the domain reviewers, not as findings.
