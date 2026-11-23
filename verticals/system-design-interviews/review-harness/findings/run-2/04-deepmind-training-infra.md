# REVIEWER 4 — large-scale training and data infrastructure (run 2)

Persona: `review-harness/personas/04-deepmind-training-infra.md`. Badge is shorthand for the
problem domain, not a claim about any employer's interview practice. Nothing below asserts
what any named company asks.

**Blinding note.** I did not open `calibration-plants.json`, `dry-run-report.md`,
`calibration-plan.md`, or anything under `findings/`. I also chose not to open
`review-harness/generate-blind-set.py`, which is not on the forbidden list but is generated
*from* the plants file and could carry label→fixture mapping. No contamination to declare.

**Set/protocol contradiction, declared up front.** `review-harness/blind-scoring-set.md:3`
says "7 candidate answers"; `review-harness/review-protocol.md:23` says "For each of the 5
answers". There are 7. I scored all 7 (14 cells). A reviewer who followed the protocol
literally would have left two answers unscored, and the harness would silently lose those
cells from the agreement measurement.

---

# PART A — BLIND SCORING

## Answer `D4` — heterogeneous fleet routing

```
Answer D4 / capacity_cost_estimation: 3
  cell clause applied: "All of band 2, unprompted, and the result changed the design: the
    number ruled out an architecture, resized a fleet, moved a component, forced an
    admission-control policy, or revealed that the stated SLO is unachievable at the stated
    budget — and they said so."
  evidence: "the 5 percent on the 400B contributes 0.285 of baseline while the whole 70
    percent on the 8B contributes 0.07, so the big model's sliver costs four times what the
    small model saves. To get under the ceiling I need the 400B share below about 4 percent.
    That is the number I would hold the routing policy to."
  admits another reading: yes — band 2. Band 2's required clause asks the candidate to name
    "which constraint binds — memory capacity vs memory bandwidth vs compute vs network vs
    dollars." D4 never recites that taxonomy; it asserts "cost per token tracks weight bytes
    read" and then works in dollars. A grader reading band 2's required clause as a
    checklist of those five words scores this 2 (or, under the rubric's own "a correct
    number with no statement of what it binds is also band 1", even 1). I score 3: the
    derivation is theirs, the blend recomputes ($0.605 × $2.60 = $1.573, matching "near one
    fifty-seven"), and it produced a policy threshold that did not exist before.
  note: the threshold itself is asserted, not derived. Re-deriving it: to reach $1.50 the
    blend must fall to 1.50/2.60 = 0.577 of baseline; with the freed share going to the 70B
    the blend is 0.37 + 4.7x, so x = 4.4%; to the 8B it is 0.325 + 5.6x, so x = 4.5%.
    "About 4 percent" is a safe rounding but ~10% off the derivable figure, and neither D4
    nor the model answer shows that step.
```

```
Answer D4 / high_level_design: 1
  cell clause applied: band 1 — "A box diagram that does not satisfy the requirements
    already stated ... or ignores a constraint from the prompt." Applied via the grader
    rule that resolves it: "Do not reward being right about policy while producing no
    design. Correct and useless is below bar." (prompts.md:247)
  evidence: "That is the number I would hold the routing policy to." — and nothing else.
    There is no router, no cascade or confidence mechanism, no path for a single request,
    and no answer at all to the prompt's second half ("what do you measure to know you have
    not quietly made the product worse?").
  admits another reading: yes — band 0, and I think band 0 is the more literal application
    of `rubric.md` alone. Band 0 says "No end-to-end path ... Could not say what happens to
    a single request from arrival to response," which is exactly true here, while every
    band-1 clause presupposes that a design was offered and is wrong. The cell has no clause
    for "strong numeric analysis, zero design content," which is this transcript. I score 1
    because `prompts.md:247` resolves it to "below bar" = band 1 — but note that the
    deciding clause lives in `prompts.md` and not in the file the rubric calls "the judge's
    spec and the scorecard's source of truth" (`rubric.md:4`). Two reviewers with only the
    rubric will split 0/1 here.
```

## Answer `F3` — 4PB dedup and shuffle

```
Answer F3 / high_level_design: 3
  cell clause applied: "All of band 2, and the design visibly follows from the numbers or
    the requirement cut rather than from a template — the component boundary is where it is
    because of a quantity they computed."
  evidence: "A true global shuffle of 4 petabytes means writing 4 petabytes — at even 100
    gigabytes a second of sustained I/O that is on the order of 11 hours, so it is not
    something you do every epoch. I would shuffle once into shards at ingest and do cheap
    in-shard shuffling plus shard-order randomisation per epoch"
  admits another reading: yes — band 2, on two independent grounds. (a) The quantity the
    boundary rests on is wrong by 2×: a shuffle reads the corpus and writes it, so 4PB is
    8PB of movement and ~22 hours at 100 GB/s, not 11. This is the identical omission
    `rubric.md:457` records as one of four errors found in the appendix's first version
    ("the shuffle figure counted writes but not reads"). (b) The 2,000 readers never appear
    in the design — no shard count against reader count, no per-reader throughput, no hot
    shard, no resume-after-failure. The item's own `good` field names "Distinguishes
    corpus-scale I/O from the bandwidth the GPUs actually need to stay fed" as the
    distinguishing behaviour, and it is absent. I still score 3: the band-3 required clause
    is satisfied verbatim and unprompted, and band 3 nowhere requires the design-driving
    quantity to be *correct*. That is a rubric defect, not a candidate credit — see B4.
  structural note: this item scores only `high_level_design` and `deep_dive_failure_modes`,
    so there is no cell anywhere on this item in which a 2× I/O error can be docked.
```

```
Answer F3 / deep_dive_failure_modes: 2
  cell clause applied: "Required: picked the genuinely hard component and named a concrete
    failure mode of *this* design — not of distributed systems in general — with its
    mitigation."
  evidence: "which is where the trust problem probably comes from: nobody has measured the
    resulting distribution. I would add a verification job that samples it."
  admits another reading: yes — band 3, and I expect this to be a split. Band 3's required
    clause ("a failure mode they found changed the design") is literally satisfied: they
    diagnosed an unmeasured-distribution failure and added a component for it, unprompted.
    I score 2 because the mitigation is "add a job that samples it" — measurement, which
    band 1 deprecates by name ("we'd monitor it") — and because at 2,000 readers the
    failure modes that decide the system are untouched: stragglers, a reader dying
    mid-epoch, whether the deterministic ordering survives a checkpoint restore mid-epoch
    (the actual hard case in the reproducibility requirement), and what you can say about a
    run when a shard is later found corrupt. One level deep on one thing is band 2.
```

## Answer `J2` — vector index

```
Answer J2 / capacity_cost_estimation: 2
  cell clause applied: "Required: named which constraint binds — memory capacity vs memory
    bandwidth vs compute vs network vs dollars — and supported it with a quantity they
    derived, arithmetic within ~2–3×."
  evidence: "10 billion vectors at 1,024 dimensions in float32 is 4 kilobytes each, so
    about 40 terabytes raw, which makes memory the binding constraint here"
  admits another reading: no. It cannot be 3: the index choice is stated *before* the
    sizing ("I'd go with IVF-PQ — it's what most billion-scale deployments run"), which is
    precisely the pattern `rubric.md:31` names as arithmetic rather than judgment. The
    compressed footprint that would make 40TB load-bearing is never computed. It is not 1:
    40TB is derived, is not in the prompt, and the binding constraint is named, with the
    slack on the others shown ("50 milliseconds is generous", churn is "an ingest-volume
    question rather than a throughput one").
```

```
Answer J2 / tradeoff_articulation: 1
  cell clause applied: "Or chose, but justified it with an unfalsifiable claim ('it's more
    scalable', 'it's industry standard', 'it's more flexible')." Also the hard cap: "if no
    trade-off axis was named explicitly, tradeoff_articulation ≤ 1."
  evidence: "I'd go with IVF-PQ — it's what most billion-scale deployments run." ... "keep
    an eye on recall."
  admits another reading: yes — band 0. Band 0's clauses all fit too ("No alternative
    considered. Presented one design as the design"), and the rubric gives no precedence
    rule between a band-0 clause and a band-1 clause that both match. I score 1 because the
    band-1 clause is the more specific match and because the cap is written as "≤ 1", not
    "= 0". The prompt's second half — "tell me what the choice costs you" — is never
    answered: PQ's cost is recall, which is the one thing the 0.9 floor protects, and it is
    not mentioned.
```

## Answer `H4` — agent retries and side effects

```
Answer H4 / deep_dive_failure_modes: 2
  cell clause applied: "Required: picked the genuinely hard component and named a concrete
    failure mode of *this* design — not of distributed systems in general — with its
    mitigation."
  evidence: "The actual bug is that retrying the whole turn re-executes side effects, so we
    are duplicating emails and double-charging. I would put an idempotency key on each
    logical operation, generated once per turn."
  admits another reading: yes — and this is the cell I nominate as hardest (below). Band 3
    is defensible: the required clause is satisfied word for word by the rubric's own
    example ("an idempotency key added because the retry path double-charges"), unprompted,
    with correct supporting arithmetic (1 − 0.98^12 = 21.5%). Band 1 is also defensible:
    the design the candidate *finishes with* is tool-layer retries with no idempotency key,
    no budget, no backoff — which is band 1's named failure ("Proposed retries with no
    budget, no backoff, and no circuit breaker") and does not fix the double-charge, since
    a timeout says nothing about whether the charge landed. I score 2: the depth behaviour
    appeared competently on the genuinely hard thing, but the failure mode they found did
    not end up changing the design, so band 3's required clause fails at the level of the
    transcript as a whole. The rubric never says whether an axis is scored on the best state
    of an answer or its final state, and that question is worth two bands here.
```

```
Answer H4 / communication_collaboration: 1
  cell clause applied: "Collapsed at the first push — abandoned a correct design because it
    was questioned, with no attempt to defend it."
  evidence: "Yeah, you know what, that is probably fine actually. ... Let's go with that."
  admits another reading: yes — band 2, on the text of the cell. Band 2's required clause
    permits conceding: "either conceding and saying what changes or holding the position
    with a reason rather than with volume." This candidate conceded *and* said what changes
    *and* gave a reason ("each tool handles its own failure, which is cleaner separation
    anyway"), so a literalist scores 2. Band 2 as written does not require the concession to
    be correct, and that is the defect. I score 1 because the concession abandons the
    correctness bug they had just identified without engaging it at all. Note again that
    the resolving language is in `prompts.md:252` ("what matters is whether anything was
    WEIGHED"), not in the rubric cell.
```

## Answer `P7` — long-context KV admission

```
Answer P7 / requirements_scoping: 3
  cell clause applied: "All of band 2, and cut scope in a way that visibly changed the
    design — dropped a requirement, relaxed a consistency guarantee, or deferred a feature,
    and said what the cut bought."
  evidence: "Out of scope: tuning the eviction policy. No policy frees 32 gigabytes; this is
    about admitting long requests against a reserved share of memory."
  admits another reading: no. The two binding requirements are named with units ("a 400
    millisecond p99 time-to-first-token for the 95 percent", the 5% "held to its own, worse
    target rather than blended into one p99"), one thing is explicitly cut, and the cut's
    consequence is stated. The band-3 indicator "asked the one question whose answer would
    most change the architecture" is also present as "the first number I want is KV bytes
    per token". They also raised and rejected batching against the prompt's own evidence,
    which `prompts.md:225` explicitly protects from the relevance gate.
```

```
Answer P7 / capacity_cost_estimation: 3
  cell clause applied: "the result changed the design: the number ... forced an
    admission-control policy ... and they said so."
  evidence: "With 80 layers, 8 KV heads, head dimension 128 in bfloat16, that's about 320
    kilobytes a token, so a 100,000-token request is around 32 gigabytes"
  admits another reading: yes — band 2, weakly. The derivation is right (2 × 80 × 8 × 128 ×
    2 B = 327,680 B; × 100,000 = 32.8 GB, matching rubric.md:468) but the claim it carries
    is stated at the wrong level of the hierarchy: "on cards that are mostly holding
    weights already" and "No policy frees 32 gigabytes" are card-level phrasing for a
    node-level quantity. On the prompt's eight-H100 nodes, 32.8GB is 5.1% of a node's
    640GB (rubric.md:470), and under tensor parallelism the KV for one request is split
    across the ranks, so no single card is asked for 32GB. A grader who checks the claim
    against the hardware in the prompt can call this a number produced but not fully
    understood and score 2. I score 3: the quantity is theirs, correct, and it forced the
    policy. Also absent, though only an indicator: the layer/head/head_dim figures are
    asserted for "a 70-billion-parameter model" without being flagged as assumptions.
```

## Answer `N7` — vector index (same item as `J2`)

```
Answer N7 / capacity_cost_estimation: 1
  cell clause applied: "Derived the number that decides the question, then proposed a design
    it rules out (computed 40TB raw, then chose an index that needs all of it resident) —
    the number was produced but not understood."
  evidence: "about 40 terabytes raw. ... Given the recall requirement I would use HNSW"
  admits another reading: no — band 1 is overdetermined here, by two independent routes.
    (1) The clause above matches verbatim; a plain HNSW graph needs the vectors resident,
    plus roughly M×2×4 B ≈ 256 B/vector of graph (~2.5TB at M=32) on top of 40TB, and the
    item's own model answer rules HNSW out for exactly this reason. (2) Even ignoring HNSW,
    band 2's required clause is not met: the candidate recites the constraints but never
    says which one *binds*, and the rubric is explicit that "a correct number with no
    statement of what it binds is also band 1". The "0.95-plus recall at single-digit
    millisecond latency" figure is also a recalled benchmark statistic from a different
    scale, used in no arithmetic step.
```

```
Answer N7 / tradeoff_articulation: 2
  cell clause applied: "Required: named the axis of the trade-off in units — latency vs
    throughput, cost vs tail latency, recall vs p99 ... — and picked a side."
  evidence: "because it has the best recall-latency curve of the ANN families — typically
    0.95-plus recall at single-digit millisecond latency"
  admits another reading: yes — band 1, strongly, and this is my second-most-likely split.
    Band 1 includes "named a trade-off that isn't one in this scenario". Recall-versus-
    latency is a real axis but it is the one with slack here: 50 ms is generous and the
    candidate says nothing about it binding. The live axis is recall versus memory footprint
    (and recall versus rebuild cost under 2%/day churn), and the prompt's explicit question
    — "tell me what the choice costs you" — is never answered. I score 2 because band 2's
    required clause is satisfied as written (an axis, in units, plus a side) and indicators
    do not block a 2. The rubric has no clause for "named a real axis that is not the
    binding axis", which is distinct from both "named a non-axis" and "named the axis" —
    see B5.
```

## Answer `W7` — evaluations per commit

```
Answer W7 / requirements_scoping: 0
  cell clause applied: "Began designing from the prompt as given. Never asked what the
    system must do, never named a non-functional requirement, never bounded the problem.
    Treated an underspecified prompt as a specification."
  evidence: "Okay so 50,000 times 2,000 is 100 million tokens. Divided by 600 seconds that
    is 166,666 tokens per second." — then costing, then caveats, and no requirement named,
    nothing scoped out, nothing asked. The prompt says "tell me what you would push back
    on" and the candidate pushes back on nothing.
  admits another reading: yes — band 1, and I expect most reviewers to land there. The
    trailing list ("cold start on the replicas which I have not accounted for, and sharding
    overhead ... Network egress depends on where the judge runs") reads to a lenient grader
    as naming non-functional considerations, which would make it band 1's "produced
    requirements, but they are unquantified". I score 0 because those are caveats on the
    candidate's own estimate, not requirements of the system, and the band-0 clause fits
    sentence for sentence. The 0/1 boundary here is genuinely ill-defined: both bands
    describe a candidate who produced *something*, and neither has a clause for "costed the
    request faithfully and never questioned it".
```

```
Answer W7 / communication_collaboration: 1
  cell clause applied: "Answered a different, easier question than the one asked and did not
    acknowledge the substitution."
  evidence: "The judge calls add more depending on which judge model. There is also cold
    start on the replicas which I have not accounted for ... Storage for the results is
    negligible."
  admits another reading: yes — band 2. The prompt has two halves and the candidate answers
    one of them competently; a grader who reads "tell me what you would push back on" as
    colour rather than as part of the question scores 2. I score 1 because the pushback half
    *is* the question for an item whose stated persona is the internal customer, and because
    the register is never adjusted — the answer is delivered in replicas and GPU-hours to a
    research engineer, with no translation into what the gate buys or costs them. Worth
    flagging structurally: this answer hits a band-3 *indicator* ("surfaced their own
    uncertainty with its boundary") while failing band 2's required clause. The rubric
    handles that correctly — score 1 — but graders will find it counterintuitive and drift
    up.
```

## Hardest cell to apply

**`H4` / `deep_dive_failure_modes`.** The candidate produces a textbook band-3 finding and
then withdraws it under one push. Nothing in `rubric.md` or `prompts.md` says whether an
axis is scored on the strongest state of the answer or on the state it ends in, and the two
readings are two bands apart (3 vs 1). The code-enforced validation does not close it
either: `band3_consequence` need only be a verbatim quote showing a decision changing, and
the only consistency check on it is numeric ("reject a `band3_consequence` whose threshold
or conclusion contradicts the candidate's own figures elsewhere in the transcript",
prompts.md:331). A retracted non-numeric consequence passes every row. Two reviewers who
read "the result of the behaviour changed a design decision" as a claim about the utterance
versus a claim about the finished design will disagree on this transcript every time.

---

# PART B — CRITIQUE FROM MY DOMAIN

## B1. Axis legitimacy

**Mostly yes, with one axis I would merge and one I would split.** The six correspond
recognisably to what a design round produces evidence about, and the decision to score
*consequence* rather than *behaviour* is the right instinct.

Two objections. First, `capacity_cost_estimation` and `tradeoff_articulation` are not
independent in this domain: in training and fleet work the trade-off *is* the number, and
the rubric's own band-3 cell for trade-offs requires it to be "resolved against a number
they produced" — i.e. band 3 on trade-offs presupposes band 2-3 on capacity. Scoring them
as separate axes double-counts arithmetic and makes a numerate-but-undecided candidate look
balanced when they have one strength. I would keep both (the diagnostic value of a separate
estimation mark is real) but stop treating the composite as a mean of six independent
things. Second, `high_level_design` as written cannot distinguish "no design" from "bad
design", which cost me a band on `D4` — see B5.

**What my answer rests on:** hiring and interviewing for training-infrastructure and
data-platform roles, where I have written and argued scorecards, plus reading the published
guidance this rubric cites. **I have not run a frontier-lab AI-infra loop and I am not
describing any employer's process.** Treat this as a practitioner's view of what evidence a
design conversation actually leaves behind, not as testimony about interview practice.
**What would change my mind:** twenty real scored transcripts showing that estimation and
trade-off marks diverge in practice rather than co-moving. If they co-move at r > 0.8, I am
wrong about the double-counting being harmless and the merge becomes mandatory.

## B2. Scenario realism — my three

### `training-data-dedup-and-shuffle` — realistic-but-wrong-in-one-detail

**The single thing most wrong: 4PB is raw-crawl scale, and the item attaches it to the
per-epoch training read path, which inverts its own teaching point.**

A trainable, tokenized corpus at frontier scale is ~15-30T tokens, which at 2 bytes per
token id is 30-60TB, or 60-120TB at 4 bytes. 4PB is 50-100× that — it is the scale of a
pre-filter web crawl, not of the shards 2,000 GPUs read. The consequence is not cosmetic.
The model answer's central move is "a global shuffle ... moves 8 [PB]; at 100 gigabytes a
second that is about 22 hours. That is what says 'not every epoch'." Run the same
calculation on the trainable corpus: 2 × 80TB = 160TB, which at 100 GB/s is **27 minutes**.
A per-epoch global shuffle of the tokenized corpus is *affordable*, so the one insight the
item exists to teach is an artefact of applying a raw-crawl number to a post-processing
stage. The item half-notices this — "tokens are tiny, so the training read path is an IOPS
and access-pattern problem" — but applies the observation only to bandwidth, never to the
size of the thing being shuffled.

Fix, cheapest first: say what the 4PB is. Either "4 petabytes of raw crawl, which dedups and
tokenizes down to about 60 terabytes of shards" (now the three-stage pipeline is explicit
and the shuffle question becomes *which* stage you shuffle, which is a better question), or
state that the corpus is multimodal, where 4PB of trainable data is genuinely plausible and
the per-epoch argument holds as written.

Three more, smaller:

- **"Deduplication" never says exact or near.** The `terms` list contains both
  "near-duplicate" and "MinHash", so the item's vocabulary presumes near-dup, but the prompt
  does not say and neither does the model answer. They are different cost classes: exact
  dedup is a hash-and-sort pass bounded by the same I/O as the shuffle; near-dup is
  shingling plus LSH banding plus candidate-pair verification, which is where nine days
  comes from and which scales with candidate density, not with bytes. A candidate who opens
  with "exact or near? because nine days only makes sense for near" is doing the right
  thing and gets no credit path: it is not in `good`, not in `followups`, and
  `requirements_scoping` is not one of this item's axes.
- **"Dedup stays at nine days, off the critical path" is too absolute, and the `bad` field
  punishes the better answer.** Nine days is off the *run's* critical path and squarely on
  the *corpus iteration* path: it is the latency of every data-mixture experiment, which is
  where a large share of model quality actually comes from. A candidate who says "nine days
  gates my data experiments, so I would make dedup incremental per shard so a mix change
  does not re-dedup the world" is giving a better answer than the model answer — and today
  it looks like the `bad` field's named failure ("Optimises the nine-day dedup job first").
  The `bad` field should distinguish *optimising dedup because it is the biggest number*
  from *restructuring dedup because it is the iteration bottleneck*.
- **The 2,000 GPUs are scenery.** Nothing in `good` or `model_answer` requires the candidate
  to say anything about the read fan-out beyond "it is small", and the only probe that
  touches it is an `at_bar_2` escalation. At 2,000 readers the tail is the system: hot
  shards, a straggler reader holding a step barrier, and whether the deterministic ordering
  can be resumed mid-epoch after a restart. That last one is the actual hard case inside
  the reproducibility requirement and the pack never asks for it.

**The 100 GB/s assumption, and the 11-hour figure (my assignment).** 100 GB/s sustained is
*reasonable as an achieved shuffle rate* and *pessimistic as a storage ceiling* — a
cluster feeding 2,000 accelerators typically has aggregate storage bandwidth in the TB/s
range, but a shuffle is a many-to-many record scatter, and 10-30% of streaming peak is the
normal achieved fraction. The real problem is that the pack never says which it is, and the
rubric's own band-2 indicator asks candidates to state exactly that assumption out loud.

The arithmetic: 11 hours is wrong (writes only) and 22 hours is a **single-pass lower
bound**, not an estimate. 4PB / 100 GB/s = 40,000 s = 11.1 h per pass; read + write = 8PB =
22.2 h. But a single-pass scatter at this scale needs one open output stream per destination
shard — 100,000 shards of 40GB each means 100,000 concurrent write streams per worker, which
is not implementable — so real implementations are hierarchical or two-pass. A two-pass
external shuffle moves 16PB (read 4, spill-write 4, spill-read 4, write 4) = 160,000 s =
**~44 hours**, before any allowance for failure and retried tasks over a two-day job. So the
corrected appendix figure is still optimistic by 2×, in the same direction as the error it
fixed.

**Priority order (reproducibility first, shuffle second, dedup last) — my answer: nearly,
but I would reorder the first move.** Reproducibility-by-determinism is the right fix and it
is cheap, and leaving dedup last is right. But it is a fix for *future* runs. Nothing is
"breaking first" about reproducibility — it has been broken silently for some time, and the
urgent question is what that has already cost: if the shuffle is not what people believe it
is, every run comparison currently in flight may be invalid. So my first move is the
measurement, not the manifest: sample the current shuffle's output and quantify how
non-random it is, because that one cheap job decides whether completed runs must be
discarded. The model answer puts verification third, as a follow-on inside the shuffle
section. Days of manifest engineering before you know whether your existing results are
real is the wrong order. This is a judgement call and a reasonable practitioner could take
the other side — but it is a real disagreement with the reference answer, and a candidate
who makes my argument should not be scored below one who makes the model answer's.

### `eval-infra-per-commit-cost` — realistic

**The single thing most wrong: the model answer bills ten minutes of a 112-GPU fleet and
never says whether that capacity is reserved — and in a cost-negotiation item, that is the
whole number.**

40 commits × 10 minutes = 400 GPU-fleet-minutes per day, so a dedicated 112-GPU fleet runs
at a **28% duty cycle**. If the capacity is reserved, which it is in every environment I
have worked in, the bill is 112 × 24 × $2 = **$5,376/day ≈ $1.96M/year** — 3.6× the model
answer's "about half a million a year". The $37-per-commit figure is only true on true
per-second elastic H100 capacity, 40 times a day, which is a strong assumption stated
nowhere in `good`, `bad`, or `model_answer`. For an item whose entire content is a number
taken to a research lead, the unstated utilisation assumption is a bigger error than any
arithmetic in it.

Two more:

- **Commits do not arrive uniformly.** Two commits landing inside the same ten-minute window
  either double the fleet or break the ten-minute gate. The prompt states both numbers and
  the item never scores the queueing problem between them — and `capacity_cost_estimation`
  is not one of this item's axes.
- **"One 2,000-token generation" is ambiguous between prompt and output tokens**, and the
  model answer silently treats all 100M as generated output. That is the right reading for
  the expensive case, but in my experience you would say "2,000 output tokens", and in an
  item that is one number long the ambiguity is load-bearing.

### `annotation-throughput-vs-agreement` — realistic

Volumes check out: 200,000 / 120 annotators ≈ 1,667 per annotator per month ≈ 10 an hour,
which is plausible for preference comparisons. The `good` field's refusal to claim that
agreement work beats volume on effective sample size is the most intellectually honest thing
in the pack, and the sequencing-and-compounding argument is the right argument.

**The single thing most wrong: it is labelled `requirements_scoping` and affords none of
that axis's band-2 behaviours.** Band 2 requires "the two or three requirements that
actually bind for *this* scenario, with a number or a unit on each — a latency target, a
tenant count, a cost ceiling, a recall floor". None of those categories exists in a
30-second verbal persuasion item: there is no system to scope, nothing to cut, no NFR to
quantify. The closest the model answer comes is "six weeks" and "a quarter to a third",
which are a project timeline and an effect size. This item is 1 of only 4 items feeding
`requirements_scoping`, so **25% of that axis score comes from an item that structurally
cannot produce the signal** — and under the aggregation rule in `rubric.md:107` that lands
directly in the level claim.

Secondary: the prompt says "You have about 30 seconds" while `_meta.answer_budget_seconds`
is 60. `communication_collaboration` band 2 requires the candidate to have answered "inside
the time available" — the two files disagree about what that is.

## B3. Arithmetic

Checked: everything in Appendix B, plus the numbers in all seven blind answers and in the
model answers for the six items they come from.

**Wrong, with my calculation:**

1. **`rubric.md:523-525`, token economics — the stated rate contradicts the derived cost.**
   The text reads "At ~6,000 output tok/s — the KV-corrected figure, not the weights-only
   6,000 — that is ≈ $0.47 per million output tokens", which is self-contradictory on its
   face, and the figure it uses is the one the same appendix corrects 15 lines earlier. The
   KV-corrected rate is 4,700 tok/s (rubric.md:485). My calculation: 4 GPUs × $2/hr = $8/hr;
   4,700 tok/s × 3,600 s = 16.92M tokens/hr; $8 / 16.92 = **$0.473 per million**, which is
   the $0.47 printed. At the 6,000 the sentence names, $8 / 21.6M = **$0.370 per million**.
   So the cost figure is right and the rate attached to it is wrong. Fix the sentence to say
   4,700.

2. **`questions.json`, `eval-infra-per-commit-cost.model_answer` uses the throughput figure
   the rubric corrects.** "A four-H100 replica serving a 70B model does on the order of
   6,000 tokens a second" is the weights-only number. On the pack's own corrected 4,700:
   166,667 / 4,700 = 35.5 → 36 replicas → **144 GPUs**, 24 GPU-hours, **$48 per commit**,
   $1,920/day, **~$700k/year** — not 28 replicas, 112 GPUs, $37, ~$500k. The pack's two
   files disagree about the same quantity, and the model answer is the one that teaches the
   judge.

3. **Separately, 4,700 is itself the wrong regime for this workload, in the other
   direction.** 4,700 tok/s is a batch-64 latency-serving figure. An eval sweep has no
   per-request SLO — only a ten-minute wall clock — so you batch as large as memory allows.
   At batch 256, 2k context: KV = 256 × 2,000 × 320 KB = 167.8 GB against 140 GB of weights,
   so the step floors at (140 + 167.8) / 13,400 = 23.0 ms, giving 256 / 0.023 ≈ **11,100
   tok/s** — 16 replicas, **64 GPUs**, ~$21 per commit. The honest statement is that this
   item's cost varies by ~2.3× on a batch-size assumption that no file in the pack states,
   which is precisely the sensitivity flag `capacity_cost_estimation` band 3 asks candidates
   for and the pack does not model.

4. **The shuffle figure is still optimistic after its correction** — ~44 h for a two-pass
   external shuffle versus the 22 h in `questions.json` and `rubric.md:457`. Derivation in
   B2 above.

5. **`4PB` is inconsistent with a tokenized text corpus by 50-100×** — derivation in B2.

**Checked and correct** (I re-derived each; recording them so nobody re-does the work):
KV/token 2 × 80 × 8 × 128 × 2 B = 327,680 B ≈ 320 KB; 100k context = 32.8 GB = 5.1% of a
640 GB node and 41% of one 80 GB card; decode floor at batch 1 (140.66/13,400 = 10.49 ms,
95 tok/s) and at batch 64 (KV 41.9 GB, 181.9/13,400 = 13.6 ms, 4,716 tok/s); prefill
crossover 70e9/(8192 × 80) = 106,812 tokens; the prefill table (10k: 1.4 + 0.13 = 1.53
PFLOP ÷ 1.58 PFLOPS = 0.97 s; 100k: 14 + 13.1 = 27.1 PFLOP = 17.2 s); 1.58 PFLOPS from 4 ×
990 × 0.4; PQ at 64 B/vector = 640 GB; 10B × 1,024 × 4 B = 40 TB; 1 − 0.98^12 = 21.5%; the
D4 blend 0.605 × $2.60 = $1.573; W7's chain (100M tokens, 166,667 tok/s, 27.8 → 28 replicas,
112 GPUs, 18.67 GPU-hours, $37.33, $1,493/day, $544,580/yr) — all internally correct.

One near-miss worth a clarifying parenthetical rather than a fix: the attention term
`2 × n² × d_model × layers` *already* carries the causal halving (QK^T and AV are
4n²·d·L together, halved to 2n²·d·L), so the parenthetical "halved for the causal mask"
reads like an instruction to halve again, which would give 6.55 PFLOP instead of the correct
13.1. The table is right; the note invites a reader to double-halve it.

And one number I cannot verify: the "roughly $0.09 per million tokens for a 120B open model
... attributed to a third-party benchmark dated April 2026" (rubric.md:526). Not checkable
from here; it is also 5× below the pack's own $0.47 floor for a smaller model, so if it is
quoted anywhere public it needs its utilisation and hardware assumptions attached.

## B4. The band 2/3 boundary

**Neither too harsh nor too generous: under-determined, in one specific and fixable
direction.** It scores the *speech act* of consequence rather than the consequence. The
single required clause — "the result of the behaviour changed a design decision" — does not
require the change to be **correct**, **retained**, or **proportionate**, and my Part A hit
all three gaps:

- *Not correct:* `F3` earns a 3 on `high_level_design` because its component boundary
  follows from a computed quantity. The quantity is 2× low, and because this item scores
  only design and deep-dive, there is no cell in which to notice.
- *Not retained:* `H4` satisfies the clause with an idempotency key it then withdraws.
- *Not proportionate:* `F3` satisfies the deep-dive clause by adding a sampling job —
  monitoring, which band 1 deprecates by name.

The boundary itself sits in the right place: across 14 cells I used the full range (0 ×1,
1 ×5, 2 ×4, 3 ×4) without reaching for the middle, and the four 3s all felt like 3s. It is
the *evidence standard* for the required clause, not the clause's position, that needs work.

**The validation table cannot close these, and I want to be precise about why, because it is
the pack's headline defence.** The Numeric-truth row recomputes `derivation_steps`: stated
inputs → stated result. Run it against `F3`: inputs "4PB, 100 GB/s", op "4e15/1e11", result
"11 hours". It **passes** — 11.1 h is exactly what those inputs give. The error is in the
*model* (a shuffle also reads), not the arithmetic. Now look at `rubric.md:457`: all four
errors found in the appendix's first version were omitted terms — KV reads, attention FLOPs,
shuffle reads, and the KV-vs-node comparison. **Every one of them would have passed the
Numeric-truth check**, because each was internally consistent arithmetic over an incomplete
model. The pack's main anti-flattery mechanism is blind to the exact error class the pack has
itself experienced four times.

Three changes I would make:

1. Require the band-3 consequence to **survive to the end of the transcript**. Add a
   `consequence_retracted` field and clamp the axis to 2 when the candidate abandons it
   without engaging the objection. This is one field and it resolves my hardest cell.
2. Give each numeric item a machine-checkable **required-terms list** alongside its model
   answer (shuffle: reads AND writes; decode: weights AND KV; prefill: dense AND attention),
   and check `derivation_steps` for term completeness, not only arithmetic. This is the only
   change that catches the error class in `rubric.md:457`.
3. State in **`rubric.md`** — not only in `prompts.md` — that correct policy with no design
   is band 1, and that a concession must engage the objection to count as band 2. Both of my
   two-band splits (`D4`/`high_level_design`, `H4`/`communication_collaboration`) are
   resolved in `prompts.md` and unresolved in the file the rubric calls the source of truth.

## B5. Top 3 defects, ranked

### 1. The code-enforced numeric check validates arithmetic, not physical models — and the pack's own error history is entirely model errors

**File:** `prompts.md:328` (Numeric truth row), with `rubric.md:457` as the evidence.

**What is wrong:** the check recomputes stated inputs into a stated result. All four errors
the appendix records from its first version were *omitted terms* with internally consistent
arithmetic, and all four would pass. `F3` in the blind set demonstrates it live: "4 petabytes
... at 100 gigabytes a second ... on the order of 11 hours" recomputes perfectly and is
half the right answer.

**Why it matters:** this row is described as "the actual anti-flattery mechanism", and the
pack's confidence in its own numbers rests on it. It cannot catch the only error class the
pack has actually produced. Worse, it will read as *having* caught it, because the rejection
rate for that check will be near zero.

**What I would do:** add a required-terms list per numeric item, checked for completeness,
as in B4.2. Start with the four derivations the appendix already corrected — those are the
regression tests you have already paid for.

### 2. `requirements_scoping` is measured mostly on items that cannot afford it

**File:** `questions.json`, `_meta.axis_coverage.requirements_scoping`
(`kv-cache-admission-control`, `inline-safety-classifier-budget`,
`eval-infra-per-commit-cost`, `annotation-throughput-vs-agreement`).

**What is wrong:** three of the four are "what do you say to this person" persuasion items.
`annotation-throughput-vs-agreement` contains no system requirement of any kind — no latency
target, tenant count, cost ceiling or recall floor, which are the four examples the band-2
cell gives — and `eval-infra-per-commit-cost` affords the axis only through the ten-minute
gate. Only `kv-cache-admission-control` is a scope-a-system item. Meanwhile the axis is
defined entirely in terms of eliciting, quantifying and cutting system requirements.

**Why it matters:** under `axis_score = mean(assessed items)` (rubric.md:107), one
non-affording item is 25% of the axis, and the level mapping reads axis scores directly
("any axis < 1.00" sends a candidate below the senior bar). My Part A is the demonstration:
`W7`/`requirements_scoping` is the only 0 I gave, and I expect other reviewers to score it 1
— a full band of disagreement on an item where the axis has little to grip.

**What I would do:** either relabel `annotation-throughput-vs-agreement` to score
`communication_collaboration` + `tradeoff_articulation` (sequencing agreement work before
volume *is* a trade-off with a named axis and a chosen side), or add a fourth genuinely
scoping-shaped item. The cheapest fix is the relabel.

### 3. `training-data-dedup-and-shuffle` attaches a raw-crawl byte count to the training read path, which inverts its own teaching point — and its axis pair makes the arithmetic unscoreable

**File:** `questions.json`, `training-data-dedup-and-shuffle` (prompt, `good`,
`model_answer`); `rubric.md:457`.

**What is wrong:** two coupled problems. (a) 4PB is 50-100× a tokenized text corpus; on a
realistic ~80TB of shards a per-epoch global shuffle costs ~27 minutes, so the model
answer's "that is what says 'not every epoch'" does not follow. (b) The item scores
`high_level_design` + `deep_dive_failure_modes`, while `good` and `model_answer` are
dominated by I/O arithmetic — so the one place a candidate's shuffle budget could be marked
right or wrong does not exist on this item. The same structural problem applies to
`eval-infra-per-commit-cost`, whose model answer is almost entirely a capacity derivation on
an item that does not score capacity.

**Why it matters:** this is the pack's only training-infrastructure design item, and its
central number is attached to the wrong pipeline stage. A strong candidate who says "4PB of
*tokenized* data is not a thing; which stage is this?" is making the best observation
available and there is no cell to reward it.

**What I would do:** say what the 4PB is — "4 petabytes of raw crawl, which dedups and
tokenizes to about 60 terabytes of shards" — which also turns the shuffle question into the
better question of *which stage you shuffle*. Then add `capacity_cost_estimation` to this
item's axes (it already has the best capacity content in the pack), and state exact-versus-
near dedup in the prompt. Separately: 2 of 12 items touch training at all, and only this one
is a training-infrastructure design problem — see the sign-off.

## B6. Sign-off

**Would I refuse to let anything ship as-is? Yes, three things.**

1. **The level claim**, for the reason already in the rubric's own warning box
   (`rubric.md:142`). I am a sixth reviewer declining it. My added reason is specific:
   under `mean(assessed items)` one mismatched item is 25% of an axis, and defect 2 above
   shows `requirements_scoping` has at least one. A public status claim should not rest on
   an axis whose items cannot all produce the signal.
2. **The two numbers in defect-3 territory**: the 4PB framing and the eval-infra throughput
   figure that contradicts the rubric's own appendix. Both are in model answers, which means
   both teach the judge.
3. **`rubric.md:523`'s "~6,000 output tok/s — the KV-corrected figure"**, which is
   self-contradictory in one sentence and sits in the appendix whose stated purpose is that
   "a practitioner reviewer should be able to check each in under a minute". It took me under
   a minute, and it is the paragraph a reader will quote.

**Would I put my name on this rubric as legitimate? Yes.** It is better than most internal
scorecards I have seen written by people who do run loops, principally because it scores
consequence rather than behaviour, states its own departures from its sources, and keeps a
visible list of what it has not validated.

**The caveat, in one sentence:** I am signing off on the axes and the band definitions, not
on the level mapping, not on the item-to-axis assignments, and not on the claim that this
pack covers AI infrastructure — 2 of 12 items touch training and only 1 is a
training-infrastructure design problem, with nothing at all on distributed training,
collective communication, or checkpoint-and-restart at fleet scale, which is the single most
common real failure mode of a 2,000-GPU run and appears in this pack only as the word
"checkpoint" in one `terms` list.

## B7. Epistemic status

**Checkable facts — arithmetic and internal contradictions. Confident; a reader can verify
each in a minute.**
- `rubric.md:523` says "~6,000 output tok/s — the KV-corrected figure" while the appendix
  derives 4,700 fifteen lines earlier, and the $0.47/M it states follows from 4,700
  ($8/hr ÷ 16.92M tok/hr), not from 6,000 ($0.370/M).
- `questions.json` `eval-infra` uses 6,000 tok/s; on the pack's corrected figure the fleet
  is 144 GPUs and ~$700k/yr, not 112 and ~$500k.
- `F3`'s 11-hour shuffle omits reads; the correct single-pass figure is 22 h.
- 4PB is 50-100× a tokenized text corpus (20T tokens × 2-4 B = 40-80 TB), and at that scale
  the per-epoch shuffle the item rules out costs ~27 minutes.
- `blind-scoring-set.md:3` says 7 answers, `review-protocol.md:23` says 5.
- `annotation-throughput-vs-agreement` says "about 30 seconds",
  `_meta.answer_budget_seconds` is 60.
- The Numeric-truth check passes `F3`'s derivation (4e15/1e11 = 11.1 h is exactly right from
  those inputs), and would have passed all four errors listed at `rubric.md:457`.
- Everything I list as "checked and correct" in B3, which is most of Appendix B.

**Domain judgement a training-infrastructure practitioner would mostly share. Confident in
direction, arguable in magnitude.**
- A two-pass external shuffle at 4PB moves ~16PB, so ~44 h, not 22 — the 22 h assumes a
  single-pass scatter whose fan-out is not implementable at this shard count. Another
  practitioner might argue for a hierarchical implementation closer to 1.5 passes; nobody
  would defend 22 h as an estimate rather than a floor.
- 100 GB/s is reasonable as an *achieved* shuffle rate, pessimistic as a storage ceiling,
  and should be labelled as one or the other.
- An eval fleet billed at 28% duty cycle costs ~3.6× the quoted figure if reserved; the
  direction is not in doubt, the multiple depends on a procurement model the pack does not
  state.
- Exact versus near dedup are different cost classes and the conflation is a real tell.
- At 2,000 readers, stragglers and mid-epoch resume determinism are the failure modes that
  decide the system, and the pack does not ask for them.
- My reordering of the model answer's priorities (measure the shuffle before building the
  manifest) is the one item here I would call a genuine judgement call rather than a
  finding; a reasonable practitioner takes the other side.

**Guesses about interview practice — need a human who runs loops.**
- B1 in its entirety. I have interviewed and written scorecards for training-infrastructure
  roles; I have not run a frontier-lab AI-infra loop and I am not describing anyone's
  process. My claim that estimation and trade-offs co-move and double-count is a hypothesis
  with a stated test (r > 0.8 across twenty scored transcripts), not an observation.
- Whether band 1's bluntness reads as diagnostic or insulting. No view worth having.
- Whether `communication_collaboration` is scorable from 60 seconds. `H4` suggests yes *when
  the item embeds pushback* and `W7` suggests the register half is barely observable
  without it — but two transcripts is not evidence.
- Whether a real interviewer would score `D4` 0 or 1 on design. I argued 1 from
  `prompts.md`, and I would want a human to settle it, because it is the cleanest test of
  whether "no design" and "bad design" should share a cell.

**What I had to assume because the pack did not say.**
- That the 4PB is tokenized trainable data. This assumption is the whole of my strongest
  finding, and if the corpus is multimodal the finding collapses to "say so in the prompt".
- That "one 2,000-token generation" means 2,000 *output* tokens.
- That eval capacity is reserved rather than per-second elastic. If it is genuinely elastic
  at this size, the model answer's $37 is right and my 3.6× is wrong.
- That `prompts.md`'s grader rules are in force when applying `rubric.md` cells. Two of my
  fourteen cells depend on it. If the rubric is meant to stand alone, both become splits.
- A batch size for the eval throughput figure, since no file states one. I used 64 (the
  appendix's) and 256 (what I would actually run), and the answer moves by 2.3×.
- That `review-harness/generate-blind-set.py` was safe to leave unopened rather than safe to
  read. If other reviewers read it and I did not, that is a difference between our runs.

**Where I expect to be wrong, as my persona predicts.** I have not run a hosted,
latency-sensitive, multi-tenant serving path, and my instincts about p99s and admission
control are weaker than my instincts about throughput. Three of the seven answers I scored
(`P7`, `J2`, `N7`) are serving- and retrieval-side, and I gave `P7` two 3s — the most
generous pair in my sheet — which is consistent with my documented bias running the other
way for once. But treat my `P7` and `H4` cells as the ones most likely to be wrong, and note
that I found no fault at all in `kv-cache-admission-control` or
`multi-tenant-token-limiter-placement`, which may mean they are sound or may mean I am not
the reviewer who would see it. My training-side findings are the ones I would defend hardest.
