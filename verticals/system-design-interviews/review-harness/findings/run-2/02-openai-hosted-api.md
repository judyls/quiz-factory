# REVIEWER 2 — hosted multi-tenant LLM API — run 2

Staff engineer, request path. Nine years on large-scale request serving, the last four on a
public paid multi-tenant LLM API. Everything below about interview practice is "in my
experience of this category" or "reported", never a claim about any employer's process.

**Contamination statement:** I did not open `calibration-plants.json`, `dry-run-report.md`,
`calibration-plan.md`, or anything else in `findings/`. I also deliberately did not open
`review-harness/generate-blind-set.py`, which is not on the off-limits list but reads the
plants file. Part A was scored and written before I opened `questions.json` or `prompts.md`;
nothing in Part B changed a Part A score. Order of reading: persona → protocol →
blind-scoring-set → rubric → (Part A written) → questions.json → prompts.md.

---

# PART A — BLIND SCORING

## Answer `D4` — model routing under a cost ceiling

```
Answer D4 / capacity_cost_estimation: 3
  cell clause applied: "the result changed the design: ... forced an admission-control
    policy, or revealed that the stated SLO is unachievable at the stated budget — and
    they said so"
  evidence: "That is over the one-fifty ceiling. ... To get under the ceiling I need the
    400B share below about 4 percent. That is the number I would hold the routing policy to."
  admits another reading: yes — band 2, and the reading is specific. Band 2's Required
    clause is "named which constraint binds — memory capacity vs memory bandwidth vs
    compute vs network vs dollars". D4 never names one of those five; it names a cost
    *driver* ("cost per token tracks weight bytes read") and then a binding *term inside
    the budget* (the 400B share). A reviewer who reads the band-2 required clause as a
    closed list of five will say band 2 is unsatisfied and therefore band 3 cannot be
    reached. I score 3 because the band-3 required clause is satisfied twice over
    (ceiling shown unachievable at the proposed mix; a policy threshold derived from it),
    and because the rubric says band 3 is "All of band 2, ... and" with only the bolded
    clause mandatory. This is a cell-interaction defect, not a judgement call — see B5.
```

My own check of the arithmetic, since I scored it: 0.7×0.1 + 0.25 + 0.05×5.7 = 0.605;
0.605 × $2.60 = $1.573 ✓. Threshold: with 70B held at 25% and the 400B share x,
blend = 0.325 + 5.6x; ≤ 1.50/2.60 = 0.5769 gives x ≤ 4.5%. "Below about 4 percent" is
correct and conservative in the right direction.

```
Answer D4 / high_level_design: 0
  cell clause applied: "No end-to-end path. ... Could not say what happens to a single
    request from arrival to response."
  evidence: "That is the number I would hold the routing policy to."  (the only
    design-adjacent utterance in the answer; there is no component, no classifier, no
    cascade, no fallback, and the prompt's second half — "what do you measure to know you
    have not quietly made the product worse" — is not answered at all)
  admits another reading: yes — band 1, and I expect reviewers to split here. Band 1's
    cell presupposes that a design exists and is defective ("a box diagram that does not
    satisfy the requirements already stated", "components named by brand", "added a cache
    ... by reflex"). None of those describe D4, because D4 contains no diagram. The
    *scoring contract* line for band 1 is "appeared, but wrong, unquantified, generic" —
    and the one design statement here is neither generic nor unquantified, it is a sharp
    4% policy bound. So the rubric has no cell for "no design offered, but the arithmetic
    implies a precise policy", and reviewers will resolve that by temperament. I score 0
    because band 0's text is literally true of this transcript and because the grader
    prompt's own instruction — "Do not reward being right about policy while producing no
    design. Correct and useless is below bar" (prompts.md:258-259) — points down, not up.
```

## Answer `F3` — 4PB corpus: dedup, shuffle, reproducibility

```
Answer F3 / high_level_design: 3
  cell clause applied: "the design visibly follows from the numbers or the requirement cut
    rather than from a template — the component boundary is where it is *because* of a
    quantity they computed"
  evidence: "at even 100 gigabytes a second of sustained I/O that is on the order of 11
    hours, so it is not something you do every epoch. I would shuffle once into shards at
    ingest and do cheap in-shard shuffling plus shard-order randomisation per epoch"
  admits another reading: yes — band 2. Two routes to it. (a) The quantity that sets the
    boundary is itself understated: 4PB of global shuffle is a read *and* a write, so at
    100 GB/s it is ~22 hours, not 11 — the identical omission rubric.md:456-457 says it
    already corrected once in its own appendix. A reviewer who treats the boundary-setting
    number as wrong may decline the band-3 "because of a quantity they computed" clause,
    though ~2× keeps it inside the band-2 "~2–3×" tolerance. (b) The 2,000-GPU read path —
    arguably "the component that does the actual work" under band 2's indicator — is never
    designed: no shard-to-rank assignment, no loader, no read throughput per GPU. I still
    score 3: the required clause is met twice (the 11-hour figure sets the shuffle
    boundary; the explicit cut of dedup off the critical path reorders the whole pipeline),
    and band 3's "Chose the simpler design and said what they gave up" is also present.
```

```
Answer F3 / deep_dive_failure_modes: 2
  cell clause applied: "Required: picked the genuinely hard component and named a concrete
    failure mode of *this* design — not of distributed systems in general — with its
    mitigation."
  evidence: "which is where the trust problem probably comes from: nobody has measured the
    resulting distribution. I would add a verification job that samples it."
  admits another reading: yes — band 3, and this is my second-least-confident cell. The
    band-3 required clause is "a failure mode they found changed the design", and
    "nobody measured the distribution → shuffle once at ingest + add a sampling verifier"
    can be read as exactly that. I score 2 because what the candidate found is the *cause
    of the symptom the prompt already stated* ("nobody trusts the shuffle"), not a failure
    mode they surfaced themselves — and because for an axis whose own definition lists
    "partial failure, backpressure, overload, retry amplification, idempotency, eviction,
    head-of-line blocking", none of those appear: no straggler or hot-shard contention
    across 2,000 readers, no restartability of a 9-day job that dies on day 8, no
    alignment of checkpoint resume with data-stream position. The rubric gives the grader
    no rule for distinguishing "diagnosed the stated symptom" from "found a new failure
    mode", and that is where reviewers will diverge.
```

## Answer `J2` — vector index, IVF-PQ

```
Answer J2 / capacity_cost_estimation: 2
  cell clause applied: "Required: named which constraint binds — memory capacity vs memory
    bandwidth vs compute vs network vs dollars — and supported it with a quantity they
    derived, arithmetic within ~2–3×." (band 3 declined: the number did not change the
    design, it followed it)
  evidence: "10 billion vectors at 1,024 dimensions in float32 is 4 kilobytes each, so
    about 40 terabytes raw, which makes memory the binding constraint here."
  admits another reading: yes — band 3. The sizing is correct (10e9 × 4,096 B = 40.96 TB),
    the binding constraint is named outright, the slack on the other constraints is shown,
    and IVF-PQ *is* the design that a 40TB memory bound implies — so a reviewer can say the
    number did change the design. I score 2 because causation is only visible in a
    transcript through ordering and explicit linkage, and here both run the other way: the
    index is chosen in sentence one, before any sizing, and justified by popularity ("it's
    what most billion-scale deployments run"), with the 40TB arriving afterwards and never
    connected to compression. That is the band-3 rule's own canonical failure
    (rubric.md:30-33) and Appendix A's "scores what was said, not what was probably meant".
```

```
Answer J2 / tradeoff_articulation: 1
  cell clause applied: "Or chose, but justified it with an unfalsifiable claim ('it's more
    scalable', 'it's industry standard', 'it's more flexible')."
  evidence: "I'd go with IVF-PQ — it's what most billion-scale deployments run."
  admits another reading: yes — band 0. Band 0's lead clauses are also all true: "No
    alternative considered. Presented one design as the design." HNSW, flat search and
    reranking are never mentioned; the prompt's direct instruction ("tell me what the
    choice costs you") is answered with "keep an eye on recall", which names the cost of
    product quantization without ever stating it as a cost. The only comparative language
    in the answer is about constraint slack, not about design alternatives. I score 1
    because band 1's "chose with an unfalsifiable justification" is the more specific
    clause and a choice was made; either way the hard cap pins this ≤ 1, since no trade-off
    axis is named. Reviewers who weight band 0's "no comparative language anywhere" will
    land on 0, and that 0-vs-1 split costs 0.25 of an axis score — see B4.
```

## Answer `H4` — agent fan-out, 12 tools, side effects

```
Answer H4 / deep_dive_failure_modes: 2
  cell clause applied: "Required: picked the genuinely hard component and named a concrete
    failure mode of *this* design ... with its mitigation." (band 3 declined: the design
    did not change — the mitigation was proposed and then withdrawn)
  evidence: "The actual bug is that retrying the whole turn re-executes side effects, so we
    are duplicating emails and double-charging. I would put an idempotency key on each
    logical operation, generated once per turn."
  admits another reading: yes — both 3 and 1, which is why I nominate this as the hardest
    cell in the set (below). For 3: the analysis is unprompted, precise, and is verbatim
    the rubric's own band-3 example ("an idempotency key added because the retry path
    double-charges"); nothing in the deep-dive cell says a later retraction voids a
    behaviour already demonstrated. For 1: the design the candidate actually ends on
    contains the double-charge bug, and tool-layer retries do not fix it — a timeout does
    not tell you whether the charge landed. I score 2 strictly: band 2's required clause is
    satisfied with a clean quote, and band 3's required clause ("a failure mode they found
    changed the design") is factually unsatisfied because the change was reversed inside
    the same transcript. The rubric has no retraction rule, and that absence is the finding.
```

```
Answer H4 / communication_collaboration: 1
  cell clause applied: "Collapsed at the first push — abandoned a correct design because it
    was questioned, with no attempt to defend it."
  evidence: "Yeah, you know what, that is probably fine actually. ... Let's go with that."
  admits another reading: no. This is the single clearest cell in the set: zero defence,
    zero reason offered, no weighing, and a correct position dropped on one unargued
    objection. The grader prompt's "Abandoning a correct position with no defence and
    repeating a correct position with no engagement are both below bar" (prompts.md:267-269)
    confirms the direction. Separate concern, not a scoring ambiguity: the interviewer turn
    that produces this behaviour is not one of the item's five `followups` probes — see B5.
```

## Answer `P7` — KV cache, long vs short context

```
Answer P7 / requirements_scoping: 3
  cell clause applied: "cut scope in a way that visibly changed the design — dropped a
    requirement, relaxed a consistency guarantee, or deferred a feature, and said what the
    cut bought" + "Asked the one question whose answer would most change the architecture"
  evidence: "Out of scope: tuning the eviction policy. No policy frees 32 gigabytes; this
    is about admitting long requests against a reserved share of memory." (and, for the
    requirement split: "a 400 millisecond p99 time-to-first-token for the 95 percent, and
    the long-context 5 percent held to its own, worse target rather than blended into one
    p99")
  admits another reading: yes — band 2. A reviewer can hold that splitting one p99 into two
    SLOs is a requirement *restatement* rather than a cut, and that the only explicit cut
    (eviction tuning) excludes a *solution*, not a requirement — the band-3 text says
    "dropped a requirement ... or deferred a feature", and an eviction policy is neither.
    I score 3: refusing a blended p99 is a real relaxation of the stated requirement with a
    stated purchase (the 5% get a worse target so the 95% get 400ms), and the first number
    requested is the one quantity in the problem that moves the architecture.
```

```
Answer P7 / capacity_cost_estimation: 3
  cell clause applied: "the result changed the design: ... forced an admission-control
    policy"
  evidence: "that's about 320 kilobytes a token, so a 100,000-token request is around 32
    gigabytes ... No policy frees 32 gigabytes; this is about admitting long requests
    against a reserved share of memory."
  admits another reading: no. The derivation is correct to the byte (2 × 80 × 8 × 128 × 2 B
    = 327,680 B = 320 KiB/token; × 100,000 = 32.8 GB), it is not copied from the prompt,
    memory capacity is named as binding ("on cards that are mostly holding weights
    already"), and the conclusion is causally linked to the number in one sentence. The
    rejected alternative (fixed batching) is ruled out against the prompt's own peak
    structure, so the relevance gate does not fire. Cleanest 3 in the set.
```

## Answer `N7` — vector index, HNSW

```
Answer N7 / capacity_cost_estimation: 1
  cell clause applied: "Derived the number that decides the question, then proposed a
    design it rules out (computed 40TB raw, then chose an index that needs all of it
    resident) — the number was produced but not understood."
  evidence: "about 40 terabytes raw ... Given the recall requirement I would use HNSW"
  admits another reading: yes — band 2, and I want to be precise about why I decline it.
    The 40TB is correctly derived and the 2% churn figure is correct, so a reviewer
    crediting the band-2 "quantity they derived, arithmetic within ~2–3×" plus reading
    "Given the recall requirement" as naming a binding constraint will score 2. I score 1
    for two independent reasons: (i) recall is not one of the five constraint categories
    the band-2 Required clause lists, and the answer never says which of the three stated
    constraints binds — it restates all three; (ii) the band-1 cell contains a clause that
    reads as though written about this answer, including the parenthetical. HNSW at M=32
    holds full-precision vectors plus ~128-256 B/vector of links, i.e. ~42-43 TB resident;
    "shard across machines" distributes the cost without noticing it, and 200M daily
    changes is the second thing HNSW handles worst.
```

```
Answer N7 / tradeoff_articulation: 2
  cell clause applied: "Required: named the axis of the trade-off in units — ... recall vs
    p99 ... — and picked a side."
  evidence: "I would use HNSW, because it has the best recall-latency curve of the ANN
    families — typically 0.95-plus recall at single-digit millisecond latency."
  admits another reading: yes — band 1, and this is the most consequential ambiguity I
    found in Part A. Band 1 route: the trade-off that was named and resolved (recall vs
    latency) is not the trade-off this scenario turns on (recall vs memory/dollars at
    40TB), so the relevance gate's spirit — "A behaviour performed on the wrong problem
    scores at most band 1 on every axis" — arguably fires. It will not fire in *code*,
    because the candidate quotes the prompt's own recall and latency constraints, so
    `addresses_prompt` comes back true and `prompt_constraint_engaged` validates. I score 2
    because the required clause is literally and fully satisfied: an axis in units, plus a
    side, plus a parameter setting to land inside the budget. Band 3 is declined cleanly —
    the trade-off is resolved against a remembered benchmark range, not against the 40TB
    the candidate produced, and the prompt's "tell me what the choice costs you" is never
    answered. Note the inversion this produces against J2: the answer that picks the index
    that works scores 1 on this axis and the answer that picks the one that does not
    scores 2. That is the rubric behaving as designed (it scores articulation, not
    correctness) and it is still worth the pack's attention — see B4.
```

## Answer `W7` — eval infra cost

```
Answer W7 / requirements_scoping: 1
  cell clause applied: band 1 by the scoring contract's "appeared, but ... generic" —
    requirement handling appears only as pass-through acceptance of the asker's spec. No
    band-1 exemplar in the cell fits exactly; see the ambiguity note.
  evidence: "Okay so 50,000 times 2,000 is 100 million tokens. Divided by 600 seconds that
    is 166,666 tokens per second." (the 50,000, the 10 minutes, the 40 commits and the
    merge gate are consumed as divisors and never treated as negotiable; nothing is
    declared out of scope, nothing is cut, no requirement is prioritised)
  admits another reading: yes — band 0, and I came close to scoring it. Band 0's text is
    almost exactly on target: "Began designing from the prompt as given. ... never named a
    non-functional requirement, never bounded the problem. Treated an underspecified
    prompt as a specification." The only thing holding it off 0 is that the requirement
    figures do appear and the answer depends on them, which contradicts band 0's "nothing
    in the answer depended on it". So the 0/1 line here turns on whether using a
    requirement as an arithmetic input counts as "naming" it — the rubric does not say, and
    its own hard-cap table asserts "Band 0 vs 1 must be distinguishable from the
    transcript" (rubric.md:350). It is not, here. I score 1.
```

```
Answer W7 / communication_collaboration: 1
  cell clause applied: "Answered a different, easier question than the one asked and did
    not acknowledge the substitution."
  evidence: "There is also cold start on the replicas which I have not accounted for, and
    sharding overhead. Storage for the results is negligible. Network egress depends on
    where the judge runs."
  admits another reading: yes — band 2. The prompt asks two things; the costing half is
    answered competently, with exposed assumptions and correct arithmetic, and a reviewer
    can read the caveat list as the band-3 indicator "Surfaced their own uncertainty with
    its boundary", which makes landing at 1 look harsh. I score 1 because band 2's Required
    clause is "answered the question that was actually asked", and the question's second
    half — "tell me what you would push back on", addressed to a named research-engineer
    audience — is not answered at all. What is offered instead is a list of gaps in the
    candidate's own estimate, which is not pushback on the requester; the substitution is
    never acknowledged. The $544,580/yr figure is delivered with no statement of what it
    means or what to do about it, to an audience for whom that is the whole point.
```

Arithmetic in W7, checked because I scored it: 100e6/600 = 166,667 ✓; /6,000 = 27.8 → 28
replicas × 4 = 112 GPUs ✓; 112 × (1/6) h = 18.67 GPU-h × $2 = $37.33 ✓; × 40 = $1,493 ✓;
× 365 = $545k ✓. Every step is right. Two unstated assumptions it hides: per-second billing
(40 ten-minute bursts a day is a ~28% duty cycle on a 112-GPU fleet; reserved capacity costs
~3.6× the stated figure), and 6,000 tok/s per 4×H100 replica, which rubric.md Appendix B
itself revises down to ~4,700 at batch 64.

## Part A close — the single hardest cell to apply

**`H4` / `deep_dive_failure_modes`.** The rubric scores *behaviours*, and this transcript
contains a band-3 behaviour that the candidate then takes back. Every cell in the axis is
written in the past tense of appearance ("picked", "named", "found") with no rule for what
happens when a correct mitigation is proposed and withdrawn inside the same answer. Band 3's
required clause saves me — "a failure mode they found **changed the design**", and the
design reverted — but that is an accident of the clause's wording, not a rule the rubric
states, and it is the only thing standing between 2 and 3. A reviewer anchoring on "the
behaviour appeared, unprompted and precisely" scores 3; one anchoring on the design that was
actually shipped scores 1. The spread on this one cell is the full width of the instrument.
Runner-up: `D4` / `high_level_design`, where the 0-vs-1 choice is genuinely undetermined by
the text (see B4 on why the 0/1 boundary matters more than the pack thinks).

---

# PART B — CRITIQUE

## B1. Axis legitimacy

**Broadly yes, with one structural gap and one axis I would merge.** These six axes cover
what I actually write on a scorecard after a request-path round, and the "unprompted" clause
as the seniority discriminator matches how I separate senior from staff in my own notes.

Two disagreements:

1. **`capacity_cost_estimation` is not an independent axis in my domain.** In a request-path
   round, the number *is* how the trade-off is expressed — "the batch window is 25ms because
   the TTFT budget is 400ms" is one behaviour, not two, and I have never scored a candidate
   who was strong on the arithmetic and separately weak on the trade-off, or the reverse. In
   Part A, J2/N7 show the correlation directly: the same answer's capacity and trade-off
   scores move together for the same underlying reason. The pack's own open question list
   already names this (rubric.md:400-402) and I am confirming it from my side, not resolving
   it: six marks is a better share artifact than five, and that is a legitimate product
   reason to keep it.

2. **There is no axis for "does the design honour what was sold".** This is the gap that
   matters most in my domain and it currently has no home. The failure I reject candidates
   for most often is a technically immaculate limiter for a product whose pricing page
   promises something else — a perfect token bucket under a per-request plan, or a quota
   enforced in a unit no customer can predict. The pack *knows* this: it is the best beat in
   the limiter item's `good` field ("the quota as sold cannot express what a long-context
   tenant buys ... worth saying to the product owner", questions.json:181,183). But there is
   no cell that scores it. Today it has to be smuggled into `requirements_scoping` band 3 as
   a "scope cut" or into `communication_collaboration` as register, and both are poor fits —
   it is neither a cut nor a communication style, it is a correctness claim about the
   product. A candidate who nails it and a candidate who misses it can score identically.

**What my answer rests on:** loops I have run as an interviewer in this category, and
scorecards I have written. **What would change my mind on (1):** hand-scored sessions
showing the two axes diverging in practice — if they do, the split is real and I am
generalising from a domain where the numbers happen to be the argument. **What would change
my mind on (2):** nothing short of being told the product deliberately scopes out
commercial fit, which is a legitimate choice if stated.

## B2. Scenario realism — my four items

### `multi-tenant-token-limiter-placement` (questions.json:161-207) — realistic-but-wrong-in-one-detail

This is the best item in my set and the one I would use. Counting tokens not requests,
reserve-against-estimate-and-settle, gateway plus a second enforcement point, and the
"quota as sold is the wrong shape" observation are all the real content of the real problem,
and the `bad` field names the two failures I have genuinely seen and written postmortems
about: a per-request limiter at 100× shape variance, and a strongly consistent central
counter in the hot path. No notes on either.

**The single thing most wrong: the prompt withholds total fleet capacity, and that is the
one number the item's own `good` answer cannot be given without.** 800 tenants × 100,000
tokens/min = 80M tokens/min = 1.33M tokens/sec of *sold* quota. At Appendix B's own
KV-corrected ~4,700 output tok/s per 4×H100 replica, honouring that in output tokens needs
~284 replicas ≈ 1,135 H100s. No one runs that fleet for 800 tenants, so the quota is
oversubscribed by some large factor — and the factor is the whole problem. "Fair share" and
"noisy neighbour" (both in `terms`) are undefined without a denominator: fair share *of
what*? A candidate who asks "what is the fleet's aggregate token throughput, and what is our
oversubscription ratio?" is asking the single best question available in this item, and the
`model_answer` does not ask it, no `followups` branch rewards it, and `requirements_scoping`
is not even a scored axis here. As written, the item quietly teaches that limiter design is
a per-tenant bucket-sizing exercise. It is not; it is an allocation problem against a
denominator. Fix: either state the fleet's aggregate capacity in the prompt, or add a
`followups` branch — "What is our total token throughput, and what did we oversubscribe
by?" — and a beat in `good` for the candidate who asks.

Second, smaller: the prompt says tenants are "sold 100,000 tokens per minute" and never says
whether that counts input, output, or both. In my experience of this category that ambiguity
*is* the interesting part and should be withheld deliberately — but then `good` should credit
the candidate who asks, and it credits only noticing that output length is unknown at
admission, which is a different observation.

### `gpu-credit-ledger-consistency` (questions.json:208-254) — realistic-but-wrong-in-one-detail

Leases, bounded overdraft, lease timeout on scheduler death, idempotent debits so
reconciliation cannot double-charge: correct, and the `bad` field's diagnosis ("the failure
is not the consistency choice, it is never having sized the thing being protected") is
exactly the thing I probe for. The `at_bar_2` probe — "What is the first signal that
reconciliation is silently wrong?" — is the best probe in the pack.

**The single thing most wrong: the model answer's $11 bounds the wrong quantity, and a
candidate who repeats it has not understood the exposure.** Credits are debited *per
GPU-second*, i.e. continuously over a job's life, not once at admission. The 20 × 1,000
GPU-second = 20,000 GPU-second ≈ 5.6 GPU-hour ≈ $11 figure is arithmetically right
(questions.json:230) and it bounds only the credits held in un-reconciled *admission* leases
at one instant. The exposure that actually hurts is accrual while the ledger is degraded:
every running job keeps burning, and nothing debits. On a 2,000-GPU fleet, a 10-minute
ledger outage is 1.2M GPU-seconds = 333 GPU-hours ≈ **$667 at the same $2/GPU-hour** — 60×
the figure the model answer teaches, and it scales with fleet size and outage duration, not
with lease size or scheduler count. Shrinking the lease, which the model answer offers as
the control ("If the number came out at 11,000 dollars instead of 11, I would shrink the
lease"), does nothing about it. Also note a single real job can be 512 GPUs for 6 hours =
11M GPU-seconds, four orders of magnitude larger than the 1,000-GPU-second lease, so the
lease model as described cannot even cover one job's accrual — the lease has to be drawn
continuously during the run, which is a different design with a different failure mode
(what happens to a running job when its scheduler cannot renew? kill it, or let it run
unmetered?). None of this appears in `good`, `bad`, `model_answer` or `followups`, and the
prompt does not state fleet size, so the candidate cannot compute it even if they see it.

**Second defect in the same item: the prompt gives away the discriminating insight.** It
says the 150ms "is affordable — but it also means the ledger is in the path of every job
start" (questions.json:215). The `good` field then credits the candidate for "Names the real
risk as the availability coupling, not the 150 milliseconds" (questions.json:228) — which the
prompt has just said for them. All that is left is agreement, and `prompts.md`'s own
`first_raised_by` clamp exists precisely to stop credit for agreeing with something the item
supplied. Fix: end the prompt at "A strongly consistent ledger check adds about 150
milliseconds to admission. What consistency model do you pick, and what is the exposure if
you are wrong?" The candidate who says "150ms is fine, that is not the problem — the problem
is that nothing starts when the ledger is down" has then earned it.

### `streaming-delivery-and-deploys` (questions.json:255-301) — realistic

The problem as it actually arrives, and the `bad` field is the real failure twice over:
WebSocket for an upstream channel nobody needs plus sticky sessions, and — the one I have
actually paged on — reconnection implemented as a client retry that restarts generation.
"Not buffering generated tokens server-side is the specific omission that forces this" is
the right root cause. The reconnection arithmetic is correct: 1 − 0.96^1.5 = 5.94%, so
"roughly 6 percent" ✓.

**The single thing most wrong — and it is in the model answer, not the scenario:** "which at
60,000 concurrent is thousands of resumptions at any moment" (questions.json:277) confuses a
rate with a concurrency. 60,000 concurrent 90-second streams is an arrival rate of
60,000/90 = 667 streams/sec; at 5.94% that is **~40 breaks per second, ~2,400 per minute**,
and with a reconnect in flight for a second or two the *concurrent* resumptions are a few
dozen, not thousands. The honest sentence is "about 40 resumptions a second", which is still
plenty to make resumption a core feature, so the point survives being stated correctly.

Two things my domain would add, both absent from `good` and `model_answer`:

- **Billing for tokens the user never saw.** The design keeps generating into a server-side
  buffer while the client is away, so ~6% of answers are generated for a client that may
  never return. On a metered path you are charging for undelivered output; on an unmetered
  one you are paying for it. The `bad` field covers double-*billing* on restart but not
  billing for never-delivered tokens, and that is the one that shows up in a support ticket.
- **The `at_bar_1` probe has a boring answer as written.** "How long do you hold the buffer,
  and what does that cost at 60,000 concurrent?" — a ~500-token answer at ~4 B/token is ~2KB
  per stream, so 60,000 streams is ~120MB. Nothing. The expensive state is KV, at ~320
  KB/token: a 2,000-token context plus 500 generated is ~800MB of HBM per *paused*
  generation. Hold 30 seconds of resumption window at 40 breaks/sec and that is ~1,200
  paused streams ≈ 960GB of HBM ≈ 1.5 whole 8×H100 nodes held for people who may not come
  back. That is the design-forcing number, and it is why the model answer's choice to keep
  generating to completion rather than pausing is right — but the item never says so, so the
  probe currently rewards the cheap answer and the expensive one is invisible.

### `agent-retry-side-effects` (questions.json:588-633) — realistic

Best-constructed item in my set. The bug is located in the right place (whole-turn retry
re-executes side effects — a correctness bug, not a reliability one), the `bad` field names
the genuinely tempting wrong answer, and the "credit the part that is right before
disagreeing" beat in `good` is the behaviour I actually look for. The `proposes tool-layer
retries` probe — "The charge call timed out. Did it charge? What does your retry do?" — is
the probe I would ask.

**On the 21% figure and its independence assumption, since I was asked specifically.**
The arithmetic is right: 1 − 0.98^12 = 21.5%. The independence assumption is **not
defensible as a point estimate for real tool fan-out, and it is defensible as an upper
bound** — which is a different claim from the one the item makes. In a real fan-out,
timeouts correlate through: a shared turn-level deadline (the dominant term — if the
orchestrator's deadline is what fires, all 12 calls fail together and P(≥1) collapses toward
2%); a shared egress path, DNS, NAT and connection pool; orchestrator thread-pool or
pool-exhaustion stalls; and the same upstream model producing all 12 call arguments, so a
slow or malformed generation degrades them as a group. The true figure lies somewhere in
**[2%, 21.5%]**, and where it lies depends entirely on whether the timeout is per-call or
per-turn — which the prompt does not say. "Each tool times out about 2 percent of the time"
reads as per-call, so 21.5% is the right *stated* answer to the *stated* problem, and I would
not mark a candidate down for it.

What I would do is reward the candidate who flags it, and the item currently cannot. The
rubric's own band 3 asks for exactly this behaviour — "Stated assumptions as assumptions and
flagged which one the answer is most sensitive to" (rubric.md:212) — and `good`
(questions.json:608) credits only "Computes the compound failure probability", with no beat
for the independence assumption and no `followups` branch for a candidate who challenges it.
At-bar answer I would want: "21% if the 12 failures are independent — they probably are not,
they share a deadline and an egress path, so it could be as low as 2% — but it does not
matter, because duplicate charges are a correctness bug at any rate." Note that the item's
*conclusion* is assumption-sensitive in a way the item does not admit: "this is the normal
path, not an edge case" is true at 21% and false at 2%. The fix is cheap — add
`{"if": "questions the independence assumption", "probe": "Say they share a deadline. Does
your conclusion change?"}` and a beat in `good` — and it converts a correct-arithmetic item
into one that discriminates on judgement.

One more number in this item nobody is using. With 12 independent tools, turn latency is the
max of 12: P(all 12 under their own p99) = 0.99^12 = 88.6%, so **~11% of turns run at or
above the single-tool p99 of 8 seconds**. Fan-out converts a per-tool p99 into roughly a
per-turn p89. That is the cleanest way to show a candidate why fan-out breaks tail-latency
intuition, and it is free — the numbers are already in the prompt.

## B3. Arithmetic

Checked: every number in my four items, every number in the Part A transcripts I scored, and
all of rubric.md Appendix B.

**Appendix B is now almost entirely correct.** I re-derived it line by line and confirm:
320 KiB/token for the 70B config ✓; 32.8GB for 100k tokens ✓; 5.12% of a 640GB node ✓;
40.96% of one 80GB card ✓; 128 KiB/token for the 8B config ✓; 140GB of bf16 weights ✓;
13.4 TB/s at TP=4 ✓; 10.5ms and ~95 tok/s at batch 1 ✓; 41.9GB of KV at batch 64 (30% of
weight bytes) ✓; 13.6ms and ~4,700 tok/s ✓; the prefill crossover at n = P/(d_model × L) =
70e9/655,360 = 106,812 ✓ (and the formula is right: 4n²d per layer for QK^T and AV, halved
for the causal mask, gives 2n²dL); 1.4/0.131/1.53 PFLOP at 10k ✓; 14/13.1/27.1 PFLOP at
100k ✓; 1.584 PFLOPS from 4 × 990 TFLOPS × 40% ✓; ~1.0s and ~17s ✓. The four corrections
the appendix documents (rubric.md:453-457) all land.

**One error remains, in the paragraph that was corrected (rubric.md:521-529).**

> "At ~6,000 output tok/s — the KV-corrected figure, not the weights-only 6,000 — that is
> ≈ $0.47 per million output tokens"

This is self-contradictory on its face: ~6,000 tok/s is the figure the appendix spends
rubric.md:476-494 establishing as the *weights-only* number, and ~4,700 is the KV-corrected
one. The sentence asserts that 6,000 is both. My calculation, both ways:

- 4 GPUs × $2/h = $8/h = $0.002222/s ✓ (as stated).
- At 6,000 tok/s: 6,000 × 3,600 = 21.6M tokens/hour → $8/21.6M = **$0.370 per million**.
- At 4,700 tok/s: 4,700 × 3,600 = 16.92M tokens/hour → $8/16.92M = **$0.473 per million**.

So **$0.47 is right and the rate attached to it is wrong**: the figure belongs to 4,700
tok/s. This looks like a half-applied edit from the correction pass — the number was
updated, the prose around it was not. Fix: "At ~4,700 output tok/s — the KV-corrected
figure, not the weights-only ~6,000 — that is ≈ $0.47 per million output tokens." It matters
because the $/million figure is the one the `heterogeneous-fleet-routing` item's whole cost
argument is anchored to, and because a candidate who learns "6,000 tok/s and $0.47" cannot
reproduce the derivation.

**Two numbers I cannot verify and would not ship unverified:** the $2/GPU-hour assumption
(the appendix already flags it as needing re-verification, correctly), and the "$0.09 per
million tokens for a 120B open model at 66 tokens/sec/user" attributed to a third-party
benchmark on the H100 page. I did not fetch the page. The appendix's own handling — quote
bandwidth and capacity, which are unambiguous, and treat the TFLOPS figure as
sparsity-inflated — is the right discipline.

**Errors found outside Appendix B**, all argued above: the "thousands of resumptions at any
moment" rate/concurrency confusion (questions.json:277); the $11 exposure bounding
admission-time leases rather than accrual (questions.json:230); 800 × 100,000 tokens/min =
1.33M tok/s of sold quota against an unstated fleet (questions.json:168); and in the Part A
material, F3's 11-hour shuffle figure counting writes but not reads (~22h), the same
omission rubric.md:456-457 corrected in its own appendix.

**Numbers I checked and found correct:** D4's blend and its 4% threshold; P7's KV
derivation; J2's and N7's 40TB; W7's entire cost chain through to $544,580/yr; H4's 21.5%;
the model answer's 5.94% stream-break rate; the vector item's 640GB at 64 B/vector and its
"compressed 60-fold" (4,096/64 = 64×).

## B4. The band 2/3 boundary

**The boundary is in the right place conceptually and it is not uniformly applicable. It is
crisp on two axes, too generous on one, and undecidable on two.**

- **Crisp:** `capacity_cost_estimation` and `requirements_scoping`. D4 and P7 were
  unhesitating 3s and J2 was an unhesitating 2, all on the same discriminator: did the
  number force the decision, visibly, in the candidate's own words. This is the boundary
  working exactly as designed, and I would not touch it.
- **Too generous at 2:** `tradeoff_articulation`. Band 2's required clause — an axis in
  units plus a side — is satisfied by N7, which is the item's own designated `bad` answer
  (questions.json:574). Naming "recall-latency curve" and picking HNSW clears the bar while
  ignoring the 40TB the same candidate just derived. I am not asking the rubric to score
  correctness over articulation; that choice is deliberate and sourced. I am saying band 2
  should require the axis named to be *the axis this scenario turns on*, which the
  `high_level_design` and `deep_dive` cells already demand of themselves ("the hard part of
  *this* problem", "a failure mode of *this* design"). One word — "the binding trade-off" —
  closes it.
- **Undecidable:** `deep_dive_failure_modes` and `communication_collaboration`, both for the
  same missing rule. Neither axis says what happens when a correct behaviour is performed
  and then withdrawn (H4 does both, in one transcript, on both axes). Add one line to the
  scoring contract: **a behaviour the candidate abandoned without weighing it scores the
  band the final position supports, not the band the behaviour reached.** That resolves H4
  deterministically to 2 on deep-dive and 1 on communication, which is where I landed by
  reading the band-3 clause very literally, and it should not take a close reading.

**The more important finding: for the public level claim, the 0/1 boundary has more leverage
than 2/3, and it has had none of the attention.** The pack invests heavily in 2/3
(rubric.md:398-399 calls it "the whole instrument") and asserts of 0/1 only that it "must be
distinguishable from the transcript" (rubric.md:350). But axis scores are means of 4 items
(rubric.md:107,124), so one grid step is 0.25, and the level mapping's first trigger is "any
axis < 1.00". A candidate scoring 1,1,1,1 on an axis has 1.00 and survives; 0,1,1,1 is 0.75
and is sent **below the senior bar** by a single 0-vs-1 call. That is the whole public status
claim turning on the most weakly specified boundary in the file. In Part A I hit two
coin-flip 0/1 calls out of fourteen cells (D4 `high_level_design`, W7
`requirements_scoping`) against one coin-flip at 2/3 — and in both, the band-1 cell's
exemplars described a defective version of a behaviour that was simply absent, which is a
writing problem with a cheap fix: give each band-1 cell a clause for "the behaviour was
replaced by something adjacent" rather than only for "the behaviour was done badly".

## B5. Top 3 defects, ranked

### 1. `rubric.md:133-140` — the level mapping cannot return "At the staff bar", and is not exhaustive

`rubric.md:139` says "Evaluate top-down; the first row that matches wins, so the three are
exhaustive and mutually exclusive by construction." Both halves of that sentence are false,
and the first one is a dead-code bug in the highest-stakes output in the pack.

*Staff is unreachable.* The staff row requires ≥5 axes ≥ 1.75, ≥2 axes ≥ 2.50,
`tradeoff_articulation` ≥ 1.75, no axis < 1.00. Every profile satisfying that also satisfies
the senior row (all axes ≥ 1.00 ✓; ≥4 axes ≥ 1.75 ✓, since 5 ≥ 4; tradeoff ≥ 1.75 ✓). The
senior row is evaluated first, so it always wins. **No candidate can ever be shown "At the
staff bar."**

*Not exhaustive.* Counterexample: axis scores (1.75, 1.75, 1.75, 1.60, 1.40, 1.40) with
tradeoff = 1.75. Below-senior row: no axis < 1.00, and only 2 axes < 1.50, so it does not
fire. Senior row: only 3 axes ≥ 1.75, needs 4 — does not fire. Staff row: does not fire.
The profile is unclassified, and since diagnostic axis scores land on multiples of 0.25
(rubric.md:124-125), this is a reachable profile, not a measure-zero edge case.

**Why it matters:** this table produces the public status claim on the share artifact, which
the pack itself calls the growth engine. The file already carries a strong warning that the
six *thresholds* are uncalibrated (rubric.md:142-148) — this is a different and more
embarrassing problem, because it is not a judgement call, it is wrong as written and a
reviewer can check it in two minutes.

**What I would do:** evaluate staff → senior → below (strongest first), or make the rows
mutually exclusive explicitly, and add a fourth catch-all row ("Approaching the senior bar")
for the gap. Then unit-test the mapping over the full 0.25 grid — 13^6 profiles is 4.8M
cases, a few seconds of compute — and assert that every profile classifies exactly once and
that every row is reachable. That test is cheaper to write than this paragraph.

### 2. `questions.json:215,228,230` — the ledger item's exposure number bounds the wrong thing, and the prompt hands over the insight

Two defects in the item I own, with one fix each. **(a)** The `model_answer`'s $11 bounds
credits held in un-reconciled admission leases; the real exposure under the same design is
unmetered accrual by already-running jobs while the ledger is degraded — ~$667 for a
10-minute outage on a 2,000-GPU fleet by the item's own $2/GPU-hour, scaling with fleet and
outage, and untouched by shrinking the lease. A single 512-GPU 6-hour job is 11M GPU-seconds
against a 1,000-GPU-second lease, so the lease must be renewed during the run — a design the
item does not describe and whose failure mode (scheduler cannot renew: kill the job, or let
it run free?) is the real question. **(b)** The prompt pre-states the discriminating insight
("which is affordable — but it also means the ledger is in the path of every job start"),
then `good` credits the candidate for producing it. That is the exact pattern
`prompts.md`'s `first_raised_by` clamp exists to prevent, except the leak is in the item
rather than in a probe, where no clamp can see it.

**Why it matters:** (a) teaches a candidate — and the grader, which sees `model_answer` —
that a bounded overdraft is an $11 problem, which is the wrong mental model for a credit
system metered per GPU-second; it is the "missing reconciliation" failure in the form of a
number that looks rigorous. (b) removes most of the item's discrimination: the answer is in
the question.

**What I would do:** cut the prompt after "adds about 150 milliseconds to admission"; add
fleet size to the prompt so the accrual exposure is computable; add a `good` beat and a
`followups` branch for accrual during degradation ("The ledger is down for ten minutes. What
did it cost, and what is still running?").

### 3. `questions.json:181` vs `:183` — `good` requires a beat `model_answer` does not contain, which can structurally fail the grader's contrast check

In the limiter item, `good` requires two enforcement points: "Places the check at the
gateway for cheap rejection **and a second enforcement point at the scheduler, because the
gateway cannot know queue depth**". The `model_answer` places the bucket at the gateway with
per-node leases and a central ledger, and never mentions the scheduler enforcement point.
The `followups` reinforce the missing beat ("You've put the quota check at the gateway. The
gateway can't see queue depth. So?" is the model pushback in prompts.md:123), so this is a
required beat of the reference solution that the reference answer omits.

**Why it matters:** it is not just an inconsistency in teaching material. `prompts.md:325`
specifies a code-enforced check — reject the grader's output "if `contrast.at_bar_answer`
does not cover at least one beat from `<reference>.good` that the candidate missed" — while
`prompts.md:272-274` requires the contrast to be generated **from `model_answer`** and never
from anything else. When the beat a candidate missed is the scheduler enforcement point, the
grader cannot satisfy both constraints without inventing content, so it either fails
validation or invents. `high_level_design` is one of this item's two scored axes, so this is
the likely path, not a corner.

**What I would do:** add the second enforcement point to `model_answer` (one clause: "and a
second check at the scheduler, because the gateway cannot see queue depth"), then add a
build-time lint asserting that every beat in `good` is traceable to `model_answer` for all
12 items. I checked this one item; the lint is what tells you about the other eleven.

**Two more I would fix but that did not make the top three:** the Appendix B
6,000-vs-4,700 tok/s contradiction (B3); and the blind set's own instructions — it says
"7 candidate answers" (blind-scoring-set.md:6) while the protocol says "each of the 5
answers" (review-protocol.md:16), and it instructs reviewers not to infer which answers
share an item (blind-scoring-set.md:15-16) while printing byte-identical item prompts for
J2 and N7, which tells every reviewer exactly that. Both are harness defects rather than
pack defects, but the second one leaks into the measurement this run exists for: knowing
two answers share an item invites comparative scoring, which is the opposite of independent.

## B6. Sign-off

**What I would refuse to let ship as-is:**

1. **The level claim**, for the reason in B5.1 — not because the thresholds are
   uncalibrated, which the file already says loudly, but because the mapping as written
   cannot emit its top band and leaves reachable profiles unclassified. Fix and unit-test
   the table; the existing "do not display a level claim" warning should stay until
   hand-scored sessions exist.
2. **`gpu-credit-ledger-consistency` as currently written** — the prompt gives away the
   insight and the reference answer teaches the wrong exposure. One editing pass, not a
   rewrite.
3. **The `communication_collaboration` scores from any blind set whose interviewer turns are
   not drawn from the item's own `followups`.** In the H4 transcript, "My teammate thinks
   retries at the tool layer handle this" is not one of the item's five probes, and in
   production Prompt 2 would have matched this candidate (number produced, bug located,
   idempotency proposed) to `at_bar_1` — "The email provider has no idempotency support.
   Now what?" — which does not test pushback-handling at all. So the collapse behaviour that
   cell measures cannot be elicited by the shipping diagnostic, and my score for it is
   uncalibrated against the product. Either add a pushback branch to the at-bar path of the
   four `communication_collaboration` items, or stop scoring that axis's 2/3 boundary from
   the 60-second diagnostic — which is the pack's own open question 3 (rubric.md:403-406),
   and I am answering it: band 3 needs a live push, and the diagnostic as specified never
   pushes on a correct answer.

**Would I put my name on this rubric as legitimate? Yes** — on the six axes, the band
structure, the required-clause-plus-indicators design, the hard caps, and the relevance
gate. The caps are the part I would defend hardest: "a quantity the candidate derived" and
"a named trade-off axis" are the two things that actually separate a numerate answer from a
fluent one, and enforcing them in code rather than in prompt text is the right call. The
`derivation_steps` recompute-in-code row is better than anything I have used.

**Caveats on that yes:** (1) with the level mapping fixed or removed; (2) band 2 on
`tradeoff_articulation` needs the one-word tightening in B4, or it will pass answers the
pack itself classifies as wrong; (3) the scoring contract needs a retraction rule, or two
graders will disagree by a full band on any transcript with a pushback turn in it; (4) I am
signing off on the axes as a *description of what the round scores*, not on the claim that
six independent marks are measurable from twelve 60-second answers — four items per axis
with one coin-flip 0/1 call each is a 0.25-wide band of noise sitting directly on the
"any axis < 1.00" trigger.

## B7. Epistemic status

**Checkable facts — anyone can verify these from the files in minutes, no domain knowledge:**

- The level mapping's staff row is unreachable under top-down evaluation, and the three rows
  are not exhaustive (counterexample given). Pure logic over rubric.md:133-140.
- rubric.md:523-524 is internally contradictory, and $0.47/million corresponds to 4,700
  tok/s, not 6,000 ($0.37). Arithmetic.
- The limiter item's `good` requires a scheduler enforcement point that `model_answer`
  omits, and prompts.md:272-274 vs :325 makes that combination unsatisfiable for the grader.
  Cross-file reading.
- The streaming model answer's "thousands of resumptions at any moment" is a rate stated as
  a concurrency; the rate is ~40/sec. Arithmetic: 60,000/90 × 0.0594.
- 800 × 100,000 tokens/min = 1.33M tok/s of sold quota, with no fleet capacity stated
  anywhere in the item. Arithmetic plus absence.
- H4's interviewer turn is not among `agent-retry-side-effects`'s five `followups`, which
  prompts.md:160-161 forbids the production system from generating. Textual comparison.
- Everything I report as verified in Appendix B, I recomputed myself and it holds.
- blind-scoring-set.md says 7 answers, review-protocol.md says 5; the set forbids inferring
  shared items while printing identical prompts for J2 and N7.

**Domain judgement — practitioners in multi-tenant request-path serving would mostly share
these, though they are not provable from the files:**

- The ledger exposure that matters is accrual during degradation, not admission-time leases.
  I am confident in the structure of this and the $667 depends on a fleet size I invented
  (2,000 GPUs) because the item states none. The *structure* is the finding, not the number.
- Timeout correlation in real tool fan-out, and the claim that a shared turn-level deadline
  dominates. I would defend this in a design review. The [2%, 21.5%] range is arithmetic;
  which end real systems sit at is judgement, and it varies by orchestrator.
- The KV cost of paused generations (~800MB per stream) being the real answer to the
  streaming `at_bar_1` probe, versus the trivial cost of buffered text.
- Billing for undelivered tokens being the omission in the streaming item.
- The missing "does the design honour what was sold" axis. Strongest of my domain
  judgements; it is the thing I most often fail candidates on and it has no cell.
- That `capacity_cost_estimation` and `tradeoff_articulation` are not independent in this
  domain. Held with moderate confidence and explicitly contradicted by the product
  rationale, which I accept as a legitimate counter-argument.

**Guesses about interview practice that need a human to confirm:**

- Whether `communication_collaboration` band 3 is reachable from a 60-second item at all.
  I claim it is not without a live push, from how the probe machinery is specified, not from
  having run this diagnostic on anyone.
- Whether the 0/1 boundary disagreement rate I hit (2 coin-flips in 14 cells) generalises.
  n=14, one rater, one run. The *mechanism* by which a 0/1 flip changes the public level
  claim is arithmetic and certain; the *rate* is a guess.
- Whether band-1 cells read as insulting rather than diagnostic (the pack's own open
  question 5). I have no read on this; I am not the right reader for it.
- Whether a real loop would accept `requirements_scoping` and `high_level_design` as
  separately scorable from one 60-second answer. D4 made me doubt it (a design axis scored
  on an answer containing no design) but one item is not evidence.

**What I had to assume because the pack did not say:**

- **Fleet capacity in the limiter item** (I assumed a generic hosted fleet and computed the
  implied oversubscription rather than asserting a ratio) and **fleet size in the ledger
  item** (assumed 2,000 GPUs, stated as an assumption everywhere I used it).
- **Whether the limiter's "100,000 tokens per minute" counts input, output, or both.** I
  assumed both, which is the most common commercial shape in my experience. If it is output
  only, the long-context tenant's 100,000-token *context* does not consume quota at all and
  the item's sharpest beat evaporates — so this ambiguity is load-bearing and the pack
  should resolve it or withhold it deliberately.
- **Per-call vs per-turn timeouts in the agent item.** I assumed per-call, which is what the
  wording implies and which is what makes 21.5% correct.
- **Whether the H4 interviewer turn is a production probe or a fixture artifact.** I scored
  it as part of the transcript, per the blind set's instruction, and flagged in B6 that I
  cannot tell which it is without opening the plants file, which I did not.
- **$2/GPU-hour** throughout, taken from the pack's own assumption, which the pack correctly
  marks as needing re-verification.
- **~4,700 tok/s per 4×H100 replica** where I needed a throughput figure, taken from
  Appendix B's KV-corrected derivation rather than from the 6,000 in the eval item.

**Where my persona's declared blind spot shows, as instructed.** I own the request path and
my sense of what is hard at PB scale is secondhand, so my Part A scores for F3 — the 4PB
corpus answer — are the ones I would discount most if another reviewer disagrees. I gave it
a 3 on `high_level_design`, which is my most generous score in the set, and I notice I may
have been impressed by the *shape* of the answer (prioritise, justify with a number, cut the
expensive thing) because it is the shape I reward in my own domain, without being able to
judge whether content-addressed shards plus manifest-and-seed is actually the standard move
or merely a plausible one. I also cannot judge whether the 2,000-GPU read path I called
"never designed" is genuinely the hard part of that problem or a detail a training-infra
engineer would consider obvious. Treat my F3 scores as the weakest two cells in this report.
Against my persona's other predicted bias, I do not think I under-rated the training-side
scenario — if anything the reverse — but my criticisms of it (the writes-not-reads shuffle
figure) are arithmetic I can check rather than judgement I cannot.
