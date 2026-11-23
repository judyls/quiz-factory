# FINDINGS — Reviewer 4, large-scale training and data infrastructure

Reviewed: `blind-scoring-set.md`, `rubric.md`, `questions.json`, `prompts.md`, `CONFIG.md`,
and `calibration-plan.md` (greps only, for aggregation and per-axis reliability).

Not read, per protocol: `calibration-plants.json`, `dry-run-report.md`, anything in
`review-harness/findings/`. I saw no expected-score content. `rubric.md:48-54` and
`prompts.md:331-334` refer to those files and state that 5 of 24 reference answers failed a
band and that plant 08b is a negative control; that is all I know about them, and it came
from files I was told to read.

Part A was completed and written before `questions.json` or `prompts.md` were opened.

---

# PART A — BLIND SCORING

## Answer 1 — `A01` (continuous batching, no arithmetic)

```
Answer 1 / capacity_cost_estimation: 1
  cell clause applied: "Gave a number with no derivation"
  evidence: "Given our 400 millisecond target I would bias toward latency."
  admits another reading: yes — band 0, and the case is strong. The candidate derived
    nothing whatsoever, and the rubric's own hard cap (rubric.md:157) exists precisely to
    stop a prompt echo from counting. I scored 1 rather than 0 on one specific clause:
    band 0 requires that "nothing in the answer depended on it" (rubric.md:24), and the
    direction of their entire recommendation rests on the 400ms figure. That is a quantity
    doing work, even though no arithmetic occurred. A second reviewer reading band 0's
    first clause ("No quantity of any kind") literally will score 0. This cell cannot be
    applied consistently — see B4 and D2.
```

```
Answer 1 / tradeoff_articulation: 2
  cell clause applied: "Named the axis of the trade-off in units ... stated which side of
    it this system should sit on and why, given the stated requirement, and acknowledged
    specifically what the choice gives up. Picked."
  evidence: "The trade-off is latency against throughput: a wider batch window buys you
    utilisation and spends time-to-first-token. Given our 400 millisecond target I would
    bias toward latency."
  admits another reading: no. Band 3 is cleanly out: the cell requires the trade-off be
    "resolved against a number they produced", and the candidate explicitly substitutes
    measurement for estimation ("I would tune the window empirically"). That is the correct
    engineering instinct and the wrong interview behaviour, and the rubric scores it
    correctly. Band 1 is also out — the justification is falsifiable and tied to a stated
    requirement.
```

## Answer 2 — `A03` (HNSW)

```
Answer 2 / capacity_cost_estimation: 1
  cell clause applied: "Derived the number that decides the question, then proposed a
    design it rules out (computed 40TB raw, then chose an index that needs all of it
    resident) — the number was produced but not understood."
  evidence: "10 billion vectors at 1,024 dimensions in float32 is 4 kilobytes per vector,
    so about 40 terabytes raw. ... Given the recall requirement I would use HNSW"
  admits another reading: yes — band 2, and I expect disagreement here. The arithmetic is
    derived, stated out loud, and correct (1,024 × 4 B = 4,096 B; × 1e10 = 4e13 B). A
    reviewer weighting "derived the binding quantity from assumptions stated out loud" will
    score 2. I score 1 because band 2 also requires "Named which constraint binds ... and
    showed why the others have slack", which never happens, and because the band-1 clause
    above is written almost verbatim against this answer. Two of the band-1 clauses fire,
    and no band-2 clause is fully satisfied.
  secondary: "typically 0.95-plus recall at single-digit millisecond latency" is the
    recited-statistic failure named at rubric.md:165-166.
```

```
Answer 2 / tradeoff_articulation: 1
  cell clause applied: "chose, but justified it with an unfalsifiable claim ('it's more
    scalable', 'it's industry standard', 'it's more flexible')"
  evidence: "I would use HNSW, because it has the best recall-latency curve of the ANN
    families"
  admits another reading: yes — band 0. No alternative is ever named; "the ANN families" is
    a gesture at alternatives, not consideration of one. I scored 1 because comparative
    language is present, which band 0 requires to be absent ("No comparative language
    anywhere in the answer"). Note the hard cap (rubric.md:243) also caps this at 1: a
    dominance claim across two units is not naming an axis the system must sit on a side
    of. The prompt asked "tell me what the choice costs you" and the answer names no cost
    at all — not memory, not build time, not HNSW's well-known weakness under the stated
    2%/day churn.
```

## Answer 3 — `A03` (IVF-PQ)

```
Answer 3 / capacity_cost_estimation: 2
  cell clause applied: "Named which constraint binds — memory capacity vs memory bandwidth
    vs compute vs network vs dollars — and showed why the others have slack."
  evidence: "about 40 terabytes raw, which makes memory the binding constraint here.
    Latency has slack — 50 milliseconds is generous for an approximate lookup — and 200
    million changes a day is about 2 percent, which is an ingest-volume question rather
    than a throughput one."
  admits another reading: YES — band 3, and this is the single most important flag in my
    Part A. Every literal element of band 3 can be argued: a number was produced, memory
    was named as binding, and IVF-PQ is the compressing index, so a charitable reader says
    the number drove the choice. I score 2 on ordering: the decision is announced in the
    first clause of the answer, before any arithmetic, and justified by popularity ("it's
    what most billion-scale deployments run"). That is exactly the pattern rubric.md:31-33
    rules out — "sizes the system correctly and then proposes the architecture they were
    always going to propose". Decisive for me: the number that would actually close the
    argument — PQ's compressed footprint — is never computed, so 40TB is named as binding
    and then dropped. Two reviewers will split on this cell and the split will be real.
```

```
Answer 3 / tradeoff_articulation: 1
  cell clause applied: "chose, but justified it with an unfalsifiable claim ... 'it's
    industry standard'"
  evidence: "I'd go with IVF-PQ — it's what most billion-scale deployments run."
  admits another reading: yes — band 2, if a reviewer counts "memory is binding / latency
    has slack / churn is an ingest question" as naming axes in units. I do not: that is a
    resource-slack inventory, not a trade-off. No axis is named that this design sits on a
    side of, and the cost of PQ — recall loss, the one thing the 0.9 floor protects — gets
    four words ("keep an eye on recall"). The hard cap at rubric.md:243 applies.
  note: Answer 3 is the better engineering answer than Answer 2 and scores lower on this
    axis. I believe that is correct under the rubric and worth the pack knowing: the
    instrument rewards articulation over correctness on this axis by design.
```

## Answer 4 — `A08` (the A01 answer delivered to the A08 prompt)

```
Answer 4 / requirements_scoping: 1
  cell clause applied: "recited a generic checklist unconnected to this scenario"
  evidence: "The problem is that a fixed batch size makes time-to-first-token depend on
    batch fill rather than on compute."
  admits another reading: yes — band 0 is at least as defensible. The prompt asks two
    direct questions ("what exactly are you protecting, and what is the first number you
    would want?") and the answer addresses neither. Nothing is bounded, nothing is cut, no
    requirement is quantified from this scenario, and the 95/5 context mix — the whole
    scenario — never appears. I scored 1 because one relevant non-functional idea does
    surface ("I would track p99 time-to-first-token and inter-token latency as separate
    series"), which is a real requirements distinction for this problem. The relevance gate
    (rubric.md:62-64) caps this at 1 regardless.
```

```
Answer 4 / capacity_cost_estimation: 1
  cell clause applied: "A behaviour performed on the wrong problem scores at most band 1 on
    every axis, however well executed. Correct arithmetic about a constraint this scenario
    does not have is band 1, not band 2" (rubric.md:62-64). Also: "Used a number that
    contradicts a constraint stated in the prompt."
  evidence: "across four H100s at 3.35 terabytes per second that is roughly 13 terabytes
    per second aggregate, so one decode step floors near 10 milliseconds"
  admits another reading: no, not under the rubric as written — and this is the cell the
    rubric handles best. The arithmetic is real, derived, correct (140 GB / 13.4 TB/s =
    10.4 ms) and it changed a design decision, which is band-3 execution. It is also about
    four H100s in a prompt that states eight nodes of eight, and about decode bandwidth in
    a prompt whose binding constraint is KV capacity under a 5% long-context class. Two
    independent clauses pin it to 1. Without the relevance gate this answer scores 3, which
    is a good demonstration that the gate earns its place.
```

## Answer 5 — `A09` (routing)

```
Answer 5 / capacity_cost_estimation: 1
  cell clause applied: "Gave a number with no derivation" — and the stronger spirit of
    "Used a number that contradicts a constraint stated in the prompt."
  evidence: "Against the dollar fifty ceiling that clears comfortably; I would expect to
    land somewhere near 55 cents."
  admits another reading: YES — band 2, and I think a grader following this rubric
    literally lands on 3. The relative-cost model is derived out loud and the ratio
    arithmetic is right (0.7 × 0.1 + 0.3 × 1 = 0.37; the 50-50 case gives 0.55), and the
    answer even supplies band 3's reversal-threshold indicator. I score 1 on three
    checkable failures:
      (a) The prompt names THREE models. The blended model silently drops the 400B, which
          the candidate itself calls "five to six times worse than the 70B". Put a third of
          the non-8B traffic on the 400B and blended cost is 0.7(0.1) + 0.2(1) + 0.1(5.7)
          = 0.84 of baseline, 2.3× their figure. The dominant cost term is assumed away
          without acknowledgement.
      (b) "near 55 cents" has no derivation. It requires an unstated all-70B baseline of
          ~$1.49/M ($0.55 / 0.37). The pack's own Appendix B derives $0.37/M for a 70B on
          4 H100s — 4× apart. Neither figure is stated as an assumption.
      (c) The reversal threshold is contradicted by the candidate's own arithmetic. With
          blended ratio r(s) = 0.1s + (1 − s) = 1 − 0.9s, at an 8B share of 20% r = 0.82,
          i.e. $1.22/M against a $1.50 ceiling. The ceiling requires r > 1.0, which is
          impossible in their model at any 8B share. "The ceiling only starts to bind if
          the 8B share drops below roughly 20 percent" is not a derived threshold; it is a
          plausible-sounding number.
    Band 2 requires "Arithmetic within ~2–3×". The headline figure is outside that once the
    400B is restored, and the figure actually compared to the ceiling is undetermined. I
    hold 1, but I expect to be the outlier on this cell and the disagreement is the finding
    — the rubric has no clause for "internally consistent arithmetic resting on a silently
    dropped term", which is the most common real failure in cost modelling I have seen.
```

```
Answer 5 / high_level_design: 0
  cell clause applied: "No end-to-end path. Named technologies without connecting them.
    Could not say what happens to a single request from arrival to response."
  evidence: "The ceiling only starts to bind if the 8B share drops below roughly 20
    percent, so that is the number I would watch."  (the answer's closing sentence; no
    component is named anywhere in it)
  admits another reading: yes — band 1, if a reviewer treats "if 70 percent goes to the 8B"
    as an implied routing design. I score 0 because every band-1 clause presupposes that a
    design was offered ("A box diagram that does not satisfy the requirements", "Components
    named by brand", "Added a cache ... by reflex"), and none can be applied to an answer
    containing no components. There is no router, no classifier, no confidence threshold,
    no escalation or fallback path. The prompt's second question — "what do you measure to
    know you have not quietly made the product worse?" — is answered with a cost metric,
    not a quality one. The answer is a spreadsheet, not a design.
```

## Hardest cell to apply

**`capacity_cost_estimation`, band 3** — specifically the required clause "the result
changed the design".

It asks for a counterfactual and a transcript does not contain counterfactuals. To apply it
I have to decide whether a number caused a decision or ratified one, and the only evidence
available is word order. Word order is a bad proxy, and Answers 3 and 5 prove it in both
directions: Answer 3 states its conclusion before the arithmetic and is the stronger
answer; Answer 5 does the arithmetic first and reaches a figure that does not follow from
it. A candidate who says "so that rules out X, therefore Y" emits a perfect
`band3_consequence` quote (prompts.md:295) whether or not the number did any work.

Band 2's "Named which constraint binds ... and showed why the others have slack" is by
contrast the best-written clause in the file: observable, checkable, and it discriminated
Answer 2 from Answer 3 immediately. The fix for band 3 is in B4.

---

# PART B — CRITIQUE

## B1. Axis legitimacy

**Mostly yes, and incomplete for the domain the pack claims.** The six axes are a
legitimate decomposition of a *serving and request-path* design round. They under-fit a
training-infrastructure round, and the pack's own best content proves it.

Two behaviours a training-side round turns on have no axis:

1. **Verification.** The dedup item's `good` field requires the candidate to name "the
   trust problem as a verification gap" and propose "a measurable check rather than a
   better algorithm" (`questions.json`, `training-data-dedup-and-shuffle.good`). That is
   the single most load-bearing behaviour in the item and nothing scores it. It is not
   `deep_dive_failure_modes` — a verification gap is not a failure mode, it is the absence
   of a way to detect one. The same item's best follow-up ("A shard is found to be corrupt
   three months after the run. What can you say about the run?") probes a dimension the
   scorecard cannot report.
2. **Lifecycle and lineage.** What this system looks like in eighteen months: corpus
   versioning, backfill, migration, data provenance. In training infra this is the axis, not
   a sub-point. The pack handles it as content inside one item.

I would not add axes — six is already a product constraint honestly declared
(`rubric.md:318-324`). I would fold verification into `deep_dive_failure_modes` band 2
explicitly ("named what signal would reveal the failure, not only the failure") rather than
leave it unscorable.

On the pack's own open question (`rubric.md:342-345`, whether `capacity_cost_estimation`
deserves axis status or is subsumed by trade-offs): **keep it.** I have interviewed people
who can do the arithmetic and cannot make a call, and people who make good calls
innumerately. Those are different failures with different remedies, and collapsing them
would lose the more actionable half. Answers 1 and 3 in the blind set separate exactly this
way, which is weak evidence for the axis from inside the instrument.

**What this rests on:** running and interviewing for training-infrastructure roles, and
being on the receiving end of design rounds in this category. I have not seen a frontier
lab's actual scoring sheet and I am not claiming one exists in this shape. My confidence is
high on "verification is what a training-side interviewer probes" and low on "this is how
the round is formally scored".

**What would change my mind:** two or three real scored transcripts from training-side
loops. If verification and lineage show up folded into design and deep-dive scores rather
than called out, my B1 complaint is cosmetic and should be dropped.

## B2. Scenario realism — my three items

### `training-data-dedup-and-shuffle` — realistic-but-wrong-in-one-detail

The arrival is excellent. "Nobody trusts the shuffle" is exactly how this problem arrives —
not as a spec but as a loss of confidence, and I have been in that room. "Reproducible down
to the exact batch six months later" is a real requirement stated in real words. Nine days
of dedup is plausible. These are good instincts and the item is worth keeping.

**The single thing most wrong: the prompt treats the 4 PB corpus and the dataset the 2,000
GPUs read as the same artifact. They are different artifacts with different sizes, and
every other problem in the item follows from that conflation.**

Dedup and shuffle operate on the raw corpus. Training reads post-dedup, post-tokenization
shards. 4 PB is coherent only as a raw crawl or multimodal store: 4 PB of *text* at ~4
bytes/token is ~1e15 tokens, roughly 50× larger than any publicly described frontier text
corpus; 15T tokens of tokenized text is about 60 TB, not 4 PB. So "2,000 GPUs will read it
during training" is describing the wrong object, and a practitioner's first question —
"4 PB of what, before or after tokenization?" — has no answer in the prompt. Fix: state the
corpus as raw and the training set as derived, or drop to a scale where one artifact is
plausibly both.

Three secondary faults, each actionable:

- **"Deduplication" without exact or near.** These are different jobs with different costs.
  Exact dedup at 4 PB is a hash-and-group — one corpus pass, hours to a day. Near-dup via
  MinHash/LSH is the nine-day job. The stated nine days is only coherent under near-dup,
  the distinction decides whether nine days is reasonable, and `terms` lists both
  "near-duplicate" and "MinHash" while neither `good` nor `model_answer` mentions either.
  The item's own vocabulary list knows something its reference answer does not.
- **A per-epoch global shuffle is slightly off-key at 4 PB.** At that scale you are doing
  roughly one pass; the shuffle is an ingest-time operation by construction and per-epoch
  reshuffling is a multi-epoch regime's problem. The tension the item wants is more natural
  at ~400 TB with 20 epochs. As stated, a strong candidate's correct first move is "we
  don't have epochs in the sense your question assumes", and the follow-up tree has no
  branch for that.
- **Batch-exact reproducibility across restarts is missing entirely.** At 2,000 GPUs over a
  multi-week run you will take dozens of restarts. Manifest plus seed plus ordering function
  does *not* give batch-exact replay unless the loader position is checkpointed with model
  state and the ordering function is a pure function of (seed, epoch, global_step) that is
  independent of worker count — change the reader count on an elastic restart and a naive
  sharded loader silently changes batch composition. This is the hard part of the stated
  requirement, it is squarely on `deep_dive_failure_modes` (one of the item's two scored
  axes), `terms` includes "checkpoint", and the reference answer omits it.

### `annotation-throughput-vs-agreement` — realistic

The best-constructed item in the pack. The arrival is right (a VP, 30 seconds, not an ML
person), the failure mode in `bad` is the real one, and making the register the measurement
is the correct call. I would not change the scenario. The problem is in the reference
answer — see B3.

### `eval-infra-per-commit-cost` — realistic

50,000 graded evals on every commit at 40 commits/day is an aggressive but entirely real
research ask, and "produce the number before the opinion" is the right thing to score. The
thing most wrong is an omission in the prompt that the reference answer then inherits: **it
never says what model the judge is.** The judge is roughly half the fleet (B3), so a
candidate cannot produce a defensible figure, and the model answer disposes of it in three
words ("plus the judge calls"). Add "the judge is the same 70B" (or an 8B) to the prompt.

## B3. Arithmetic

### Checked and correct

- Appendix B KV/token: 2 × 80 × 8 × 128 × 2 B = 327,680 B. ✓ 100k tokens = 32.8 GB. ✓
- 8B KV/token: 2 × 32 × 8 × 128 × 2 B = 131,072 B = 128 KiB. ✓
- Decode floor: 140 GB / 13.4 TB/s = 10.4 ms; ~96 tok/s single stream. ✓
- Prefill: 2 × 70e9 × 1e4 = 1.4 PFLOP; / 1.584 PFLOPS = 0.88 s; 100k → 8.8 s. ✓
- Token economics: 4 × $2/hr = $0.00222/s; / 6,000 tok/s = $0.37/M. ✓ internally.
- Dedup item shuffle: 4e15 B / 1e11 B/s = 40,000 s = 11.1 h. ✓ arithmetically.
- Eval item chain: 1e8 tokens / 600 s = 166,667 tok/s; / 6,000 = 27.8 → 28 replicas = 112
  GPUs; × $2 × (1/6) h = $37.3/commit; × 40 = $1,493/day; × 365 = $545k/yr. ✓ all of it.
- Vector item: 64 B/vector × 1e10 = 640 GB. ✓
- Blind-set Answer 5 ratios: 0.37 and 0.55. ✓ (conclusions drawn from them are not — Part A)

### Wrong — 1. Appendix B, "a fifth of a node's HBM" (`rubric.md:405-406`)

> 100k tokens of context ≈ **32GB of KV for one request** — comparable to a fifth of a
> node's HBM

32.8 GB against a node of 8 × 80 GB = 640 GB is **5.1%, not 20% — off by 3.9×**. No reading
rescues it: 1/20 of an 8-GPU node, 1/10 of a 4-GPU TP group, 2/5 of a single card. The
item this appendix exists to support gets it right —
`kv-cache-admission-control.model_answer` says "roughly 32 gigabytes of KV — against 80
gigabytes of HBM per card", which is the correct 40%-of-a-card framing. So Appendix B
contradicts its own model answer on the quantity the A08 scenario turns on, and Appendix B
is what goes into the grader's context (`prompts.md:184-185`). Fix the appendix to the
per-card framing.

### Wrong — 2. Appendix B's decode floor ignores KV reads (`rubric.md:409-418`)

The derivation reads weights only. A decode step also reads the KV cache for every
sequence in the batch, and that term scales with batch × context:

- Crossover: 140e9 / 327,680 = **427,246 token-slots**. Beyond that, KV traffic exceeds
  weight traffic. At batch 64 that is **6,676 tokens of context per request.**
- At batch 64 and the 2,000-token context A08 calls typical: KV = 64 × 2,000 × 327,680 =
  41.9 GB. Step = (140 + 41.9) GB / 13.4 TB/s = **13.6 ms, not 10 ms.** Aggregate
  **4,713 tok/s, not ~6,000** — 27% optimistic.
- Cost follows: $0.00222/s ÷ 4,713 tok/s = **$0.47 per million**, not $0.37.
- At 32k context, batch 64 needs 671 GB of KV against 320 GB of HBM on 4 H100s, so the
  configuration is not feasible at all.

This makes the appendix's stated reason wrong, not just its figure: "the inter-token latency
a user sees is nearly flat in batch size until compute saturates" holds only in the
short-context, small-batch corner. ITL degrades with batch size because of the KV term,
well before compute saturates. The economic argument for continuous batching survives — it
is just 4,700 tok/s off one weight read instead of 6,000. Add the KV term to the derivation
and state the context length it assumes. Two blind-set answers and three model answers
reason off the 6,000 figure, so this propagates.

### Wrong — 3. The dedup model answer's 11 hours counts half the I/O

> A true global shuffle of 4 petabytes means writing 4 petabytes — at even 100 gigabytes a
> second of sustained I/O that is on the order of 11 hours

A shuffle reads 4 PB and writes 4 PB. If 100 GB/s is the shared sustained figure the
sentence calls it ("sustained I/O", not "write bandwidth"), the floor is 8e15 / 1e11 =
**80,000 s = 22 hours**, and a two-stage distributed shuffle that spills intermediates is
2× that again. "Even 100 GB/s" is rhetorically conservative while the byte count is
optimistic by 2–4×, so the answer's caution points the wrong way.

Separately, **100 GB/s is pessimistic as a capability** for storage feeding 2,000
accelerators; several hundred GB/s to low TB/s is the normal range. At 500 GB/s the
read+write shuffle is ~4.4 hours, and "not something you do every epoch" gets considerably
weaker. The conclusion is robust *only because* the bandwidth assumption is low, and the
answer never flags that the assumption is carrying it — the exact behaviour
`rubric.md:155` asks for ("flagged which one the answer is most sensitive to").

### Wrong — 4. The dedup item's `good` field demands arithmetic that disproves its own premise

`good` requires the candidate to "do the read-bandwidth arithmetic for 2,000 readers". The
`model_answer` never does it. That is a reference answer failing a clause of its own
criterion, in the same JSON object — and `prompts.md:272-274` feeds both to the grader.

Worse, I did the arithmetic and it shows the quantity has enormous slack. Training a
70B-class model: ~6 × params FLOP/token = 4.2e11; 2,000 H100s at 990 TFLOPS × 40% MFU =
7.9e17 FLOPS → **1.9M tokens/s**; at 2–4 bytes/token that is **3.8–7.5 GB/s cluster-wide,
or 4–8% of the 100 GB/s the same answer invokes.**

So aggregate read bandwidth is not the bottleneck and cannot be. The real data-loading
problem at this scale is access *pattern*: a global shuffle implies random reads across 4
PB, and what hurts is IOPS, per-object metadata operations, small-read amplification, and
per-shard hotspotting. That is also the better reason why shuffle-once-into-shards is
right — it converts random reads into sequential ones — and the followup "2,000 GPUs are at
60 percent utilisation waiting on data. Where is the bottleneck?" has an honest answer
(IOPS, metadata, or the CPU decode/augment step) that the reference answer cannot reach,
because it has framed the whole item as a bytes-moved budget. The `good` field currently
points candidates at the one quantity with the most slack. Replace "read-bandwidth
arithmetic" with "shows that aggregate bandwidth has slack and names what actually starves
the readers".

I will say plainly that this finding cost me something: see B7.

### Wrong — 5. The eval item understates cost ~3–6×, in three independent places that all point the same way

The chain is arithmetically perfect and the cost model is wrong, which is the dangerous
combination for an item whose `good` says "the number is the argument".

- **The judge is omitted.** A judge pass over a 2,000-token generation is prefill-dominated:
  2 × 70e9 × 2,000 = 2.8e14 FLOP each; × 50,000 = 1.4e19 FLOP; / 1.584 PFLOPS per 4-GPU
  replica = 8,838 replica-seconds; to fit in 600 s needs **14.7 replicas = 59 GPUs, a 53%
  addition** to the stated 112. "Plus the judge calls" is hiding half the fleet. (If the
  judge is an 8B this nearly vanishes — which is why the prompt must say.)
- **Elasticity is assumed and never stated.** $1,493/day is correct only if 112 GPUs
  materialise for exactly 10 minutes, 40 times a day. 40 commits inside an 8-hour workday
  is one per 12 minutes against a 10-minute gate, so occupancy is near-continuous and
  Poisson bursts need 2–3× headroom to hold a 10-minute p99. Reserved capacity for working
  hours is the realistic shape, and accelerator capacity is not elastic at 10-minute
  granularity. That alone is ~3×.
- **The 6,000 tok/s input is 27% optimistic** (finding 2 above): 36 replicas, not 28.

Stacked, the honest range is roughly **$1,500/day at the stated assumptions to ~$10,000/day
reserved-with-judge**, i.e. $545k to ~$3.5M/year. The model answer takes the floor of a 6×
range and calls it "roughly". The pack's own design rule requires the assumption stated out
loud (`questions.json._meta.design_rules`); it states the $/GPU-hour and omits the two
assumptions that move the answer more. Fix: state elasticity explicitly, name the judge
model, and quote a range.

### Wrong — 6. The annotation reference answer's leverage claim is unsupported and probably backwards

Two claims:

> the model sees maybe 200,000 comparisons' worth of usable preference even though we paid
> for 400,000

and, from `good`: "raising agreement is worth more than raising volume".

Working it through the standard symmetric-flip model. Cohen's κ = 0.62 on balanced binary
comparisons gives observed agreement p_o = 0.5 + 0.62 × 0.5 = **0.81**. Two independent
annotators with per-annotator flip rate ε agree with probability 1 − 2ε(1 − ε), so
2ε(1 − ε) = 0.19 → **ε ≈ 0.106**. Effective sample size under label noise scales as
(1 − 2ε)² = **0.62**.

- The "half" figure is invented: 0.62, not 0.50. 400,000 comparisons at κ = 0.62 are worth
  ~248,000 clean ones, not 200,000.
- The leverage claim inverts the magnitudes. Lifting κ from 0.62 to 0.80 (p_o = 0.90,
  ε = 0.053) raises the factor to 0.80 — a **1.29× gain**. Doubling the pool is a **2×
  gain**. Doubling volume is worth more, and the VP's instinct is better than the reference
  answer allows.
- The answer's own correct sentence ("doubling the team doubles both the signal and the
  noise") *supports* doubling: at fixed noise rate, effective N is linear in N.

What survives is the second-order argument the answer also makes — 120 unramped annotators
drag agreement down for a quarter or two — and that is the honest case. But it is a
temporary cost against a permanent gain, which makes "I would rather spend the headcount
somewhere better" a much closer call than stated. **This matters more than the other
findings because the item's whole purpose is persuading a non-expert, and the model answer
teaches the grader to reward a confident quantitative claim that does not hold.** Fix: drop
"worth more than", keep the sequencing argument, and make the real case — the onboarding
dip plus the fact that noisy pairs are not merely attenuating but actively teach a reward
model the wrong boundary, which is the strongest honest argument and the one the answer
never makes.

### Not checkable by me

H100 NVL (94 GB / 3.9 TB/s), the $0.09/M third-party benchmark, the vLLM 60–80% → <4%
figures. All three are sourced and the vLLM one is correctly dated and caveated
(`rubric.md:439-441`) — that is good practice and rarer than it should be.

## B4. The band 2/3 boundary

**Right in intent, in the wrong place in form, and currently unapplicable as the required
clause is written.**

The intent — behaviour is 2, consequence is 3 — is the correct discrimination and I would
defend it against someone who called it stylistic. The form fails because "the result
changed the design" is a counterfactual and a transcript has no counterfactuals. I had to
fall back on word order in Part A, which split Answers 3 and 5 in a direction word order
does not justify (see the hardest-cell note). `prompts.md:295` makes this concrete: a
candidate saying "so that rules out X, therefore Y" emits a valid `band3_consequence`
whether or not the number did any work, and a grader cannot tell the difference.

Not too harsh and not too generous — **unfalsifiable**, which is worse, because it drifts
with the grader's charity and the calibration plan's κ will show it as noise spread across
every axis rather than as a located defect.

**Concrete fix: promote one existing indicator to the required clause.** Band 3 should
require a **named counterfactual** — the threshold at which the decision flips, or what the
candidate would do if the number came out differently. It is already in the cell as an
indicator ("Named the condition under which they would reverse the decision ('if
long-context share goes above ~20%, this flips')"), it is observable, quotable, and
substring-checkable, and it is the behaviour that actually distinguishes someone who used a
number from someone who decorated with one.

One caveat that must ship with the fix: Answer 5 supplies a reversal threshold and it is
fabricated (Part A, finding (c)). So the promoted clause needs a correctness check, not
just a presence check — the grader must verify the threshold follows from the candidate's
own stated numbers. That is checkable arithmetic, which is exactly what you want a
code-side validator doing.

## B5. Top 3 defects, ranked

### 1. Appendix B is wrong in two places and it is the file that teaches the grader

`rubric.md:405-406` (KV as "a fifth of a node's HBM", off 3.9×) and `rubric.md:409-418`
(decode floor omits the KV read term: 13.6 ms not 10 ms, 4,713 tok/s not 6,000, $0.47/M not
$0.37/M at batch 64 and 2k context).

**Why it matters:** Appendix B is pasted into the grader's context (`prompts.md:184-185`)
and is the arithmetic the model answers are built on. A grader holding 6,000 tok/s as ground
truth will mark a candidate who correctly says 4,700 as wrong, and the rubric's own band-1
clause "off by >100× without noticing" means the grader is being asked to police arithmetic
it has been given incorrectly. The "fifth of a node" error is in the quantity the entire
A08 scenario turns on, and the model answer for that item already contradicts it.

**Fix:** correct both; state the context length the throughput figure assumes; add the
crossover (batch × context > ~427,000 token-slots and KV traffic exceeds weight traffic) as
one line, because it is the fact that makes long-context admission control a capacity
problem and it is more useful than the figure it replaces.

### 2. The diagnostic's follow-up probes hand over the answer, and the validator then clamps the candidate for using it

`prompts.md:321` clamps any axis to ≤1 when `first_raised_by == "interviewer"`.
`prompts.md:158-61` (Prompt 1, rule 1) forbids supplying a consideration the candidate has
not raised. `prompts.md:162` (Prompt 2, rule 5) forbids hinting. But the fixed `followups`
in `questions.json` violate all of that, by construction:

- "How often does dedup run compared to how often you train?" — this *is* the priority
  argument. The candidate need only agree.
- "How many bytes does that move per epoch, and how long does it take?" — supplies the
  I/O-budget framing the item exists to test.
- "How much storage is that for a run, and for the 40 runs you compare?" — supplies the
  refutation of reproducibility-by-storage.
- "What is our flake rate, and what happens to the merge queue when the gate trips?" —
  hands over the entire `bad`-field insight for the eval item.

These are leading questions containing their own answers, they fire exactly when the
candidate is below bar, and whatever the candidate then produces is attributable to the
interviewer and clamped. The result: the probe cannot rescue signal, it can only confirm the
clamp, and the transcript now contains the reference answer's key idea in the interviewer's
mouth — which also contaminates the `contrast` generation.

**Why it matters:** this is a measurement defect in the layer that produces the share
artifact, and it is invisible to the plant suite, because plants test the grader against
fixed transcripts rather than the probe's effect on live ones.

**Fix:** rewrite the non-"at bar" probes to create room without naming the consideration.
"How often does dedup run compared to how often you train?" becomes "What is the cadence of
each of those three things?" — same room, no answer supplied. Then add a plant whose
transcript contains an answer produced only after a leading probe, with the required outcome
being the clamp.

### 3. One training-infrastructure item out of twelve, behind a scorecard that claims to read AI infrastructure

`questions.json._meta`: `training_data` is 2 of 12, and one of those two
(`annotation-throughput-vs-agreement`) is a communication item about an annotation pipeline.
Actual training-infrastructure engineering content: **1 item of 12.** Ten of twelve are
serving, request path, quota, or retrieval.

Absent entirely: parallelism strategy and collective communication (TP/PP/DP/FSDP, what the
interconnect costs you); checkpointing against MTBF at scale, which is the cleanest capacity
problem in the whole domain — a 400B model's weights plus optimizer state is multiple TB per
checkpoint, and checkpoint size × frequency against node failure rate is exactly the
arithmetic this rubric wants; straggler and failure handling across a 2,000-GPU run
(goodput, not throughput); gang scheduling and preemption on a shared fleet; data loader
design. Those are the canonical training-infra design problems.

**Why it matters, precisely** — and I want to be fair to the pack here, because `CONFIG.md`
says 12 is a diagnostic and 40 is the target bank, which is reasonable:

- The 12-item diagnostic is nonetheless what produces the six-axis level claim and the
  percentile. A candidate whose loop is training-side gets read on one relevant item and
  will be under-scored on `high_level_design` and `deep_dive_failure_modes` for reasons
  that are about item mix, not ability.
- **A specific, falsifiable prediction.** `calibration-plan.md:156` measures Cronbach's α
  across the 4 items of each axis and names `communication_collaboration` as the likeliest
  low-α culprit. I would bet against that. `high_level_design` and
  `deep_dive_failure_modes` each have three request-path items and
  `training-data-dedup-and-shuffle` as the lone batch-data outlier. α assumes the four items
  measure one construct; a 4 PB offline pipeline and a 60,000-session streaming path do not
  draw on the same knowledge, so α will be depressed by item domain rather than by cell
  quality — and the plan will read that as a rubric defect and tune the wrong thing. If α
  comes back lowest on those two axes with the dedup item as the weakest-correlating item,
  this is confirmed.

**Fix, in order of cost:** (a) re-scope the public claim to serving and platform
infrastructure, which is what the pack actually covers and which is a defensible,
differentiated claim; (b) when the 40-scenario bank is built, hold training infra to at
least 8 of 40 with checkpointing-vs-MTBF and parallelism/interconnect among them; (c) in
the meantime, report per-item domain alongside per-axis scores so a domain-driven α dip is
diagnosable rather than mistaken for a bad cell.

### Also worth fixing, below the top three

- **Two code-side validators can reject a correct output forever, with no retry bound
  stated.** `prompts.md:315` rejects when `derived_quantity` is a substring of the prompt —
  but a legitimately derived quantity can coincidentally share digits with the prompt
  ("2,000 GPUs" in the dedup prompt against a derived "2,000 readers at 50 MB/s"). Substring
  matching on numerals is the wrong test; it should match the full quantity-with-unit, and
  `prompts.md:327` ("reject-and-re-ask, not repair") needs a retry bound with a logged
  terminal state. `prompts.md:324` has the same shape in the other direction: a strong
  candidate whose answer genuinely resembles `model_answer` makes the contrast's trigram
  overlap with the transcript exceed its overlap with `model_answer`, so the best sessions
  fail the provenance check.
- **The relevance gate collapses two very different answers onto the same score.** Answer 4
  is numerate, correct, and about the wrong problem; a silent answer is about nothing. Both
  land at 1, and the report tells the candidate the same thing. A `wrong_problem` flag on
  the output — reported separately rather than mixed into the band — would preserve the
  clamp while making the feedback usable. The gate itself is a genuinely good invention and
  I would keep it; Answer 4 scores 3 without it.

## B6. Sign-off

**Would I put my name on this rubric as legitimate? Yes.** It is better than most internal
rubrics I have worked with: it is grounded in named sources, it states where it departs from
them and why (`rubric.md:301-333`), it lists what it cannot validate by desk research
(`rubric.md:336-358`), it declares the one axis that exists for product reasons as a product
decision, and it puts its anti-flattery rules in code rather than in politeness
(`prompts.md:307-329`). The band-2 clauses are observable. The relevance gate is a real
invention. I would sign the rubric.

**The caveat:** my yes is on the 24 cells and the scoring contract, not on Appendix B, and
not on band 3 as currently phrased. Appendix B is wrong in two places and it is the part
that reaches the grader; band 3's required clause is unfalsifiable from a transcript. Fix
those two and my yes is unqualified.

**What I would refuse to let ship as-is:**

1. **Appendix B**, until the KV term and the "fifth of a node" figure are corrected.
   Shipping a grader that holds wrong arithmetic as ground truth and polices candidate
   arithmetic against it is the worst defect in the pack.
2. **`training-data-dedup-and-shuffle`'s `model_answer`**, until it (a) distinguishes exact
   from near dedup, (b) stops demanding read-bandwidth arithmetic that proves bandwidth has
   slack, and (c) addresses batch-exact reproducibility across restarts, which is the actual
   hard part of its own stated requirement and sits on one of its two scored axes. As it
   stands it fails a clause of its own `good` field, which is checkable in ten seconds by
   anyone who reads the two fields together.
3. **`annotation-throughput-vs-agreement`'s quantitative leverage claim.** Unsupported, and
   backwards on magnitude under the standard noise model (1.29× from κ 0.62 → 0.80 against
   2× from doubling). Teaching a grader to reward a confident wrong number, in the one item
   whose subject is persuading a non-expert, is the worst possible place for it.
4. **The leading follow-up probes**, for the reason in B5.2.

Everything else I would ship and iterate on.

## B7. Epistemic status

### Checkable facts — verify these without me

- Appendix B's "a fifth of a node's HBM" is off by 3.9× (32.8 GB vs 128 GB). Arithmetic.
- The decode floor omits KV reads. 13.6 ms vs 10 ms at batch 64 / 2k context; crossover at
  batch × context ≈ 427,000 token-slots. Arithmetic from Appendix B's own KV figure.
- Appendix B contradicts `kv-cache-admission-control.model_answer` on the same quantity.
  Read the two side by side.
- The dedup `model_answer` does not contain the read-bandwidth arithmetic its `good` field
  requires. Same JSON object, two fields.
- 4 PB of text is ~1e15 tokens, ~50× published frontier corpus scale. Division.
- Training read demand for 2,000 GPUs on a 70B is 3.8–7.5 GB/s, i.e. 4–8% of 100 GB/s.
  Arithmetic, given 6 × params FLOP/token and 40% MFU — both stated assumptions, both
  conventional.
- A global shuffle moves 8 PB, not 4 PB, so 11 h is 22 h at the same assumed bandwidth.
- The eval judge adds ~59 GPUs, +53% on the stated 112. Arithmetic, conditional on the judge
  being 70B — which the prompt does not say, and that is itself the finding.
- Blind-set Answer 5's reversal threshold contradicts its own arithmetic: r(0.2) = 0.82 of
  baseline, and the ceiling needs r > 1.0, so it can never bind. Algebra.
- Answer 5's "55 cents" implies a $1.49/M all-70B baseline, 4× Appendix B's $0.37/M.
- κ 0.62 → p_o = 0.81 → ε ≈ 0.106 → effective-N factor 0.62; κ 0.80 gives 0.80. Ratio
  1.29× against 2× for doubling volume.
- `training_data` is 2 of 12 items in `_meta`; 1 of 12 is training-infrastructure
  engineering. Counting.
- The followup probes name the considerations that Prompt 1 rule 1 and Prompt 2 rule 5
  forbid naming. Read the two files together.

### Domain judgement — most practitioners in my area would share these

- 4 PB and "what 2,000 GPUs read" are different artifacts, and conflating them is the item's
  central fault. High confidence.
- "Deduplication" unqualified as exact or near is a real underspecification and the nine-day
  figure only makes sense under near-dup. High confidence.
- Batch-exact reproducibility across elastic restarts is the hard part of that requirement
  and its omission is the reference answer's biggest substantive gap. High confidence — this
  is the thing I have actually been unable to answer to a research lead.
- Data loading at this scale starves on IOPS, metadata operations and access pattern, not
  aggregate bandwidth. High confidence, and it cost me something to write (below).
- 100 GB/s is pessimistic for storage behind 2,000 accelerators. Moderate confidence; it
  varies enormously by deployment and I would not fight someone who said 100 GB/s is what
  their cluster actually sustains under a shuffle's access pattern. The finding that matters
  is that the conclusion is sensitive to it and the sensitivity is unflagged.
- Accelerator capacity is not elastic at 10-minute granularity, so the eval cost is
  understated ~3×. High confidence on the direction, moderate on the multiple.
- Keeping `capacity_cost_estimation` as its own axis. Confident, and it is a judgement, not
  a fact.

### Guesses about interview practice — a human must confirm these

- **That verification and lineage are what a training-side interviewer probes, and that
  their absence from the axes is a real gap (B1).** This is my experience of the category,
  not knowledge of any employer's scoring. It is the finding most likely to be wrong and it
  is weighted accordingly: I did not ask for new axes.
- **That the band 2/3 counterfactual fix would improve inter-rater agreement.** Reasoned
  from having applied the cell five times and found it unfalsifiable. Unvalidated. Test it
  on the plants.
- **That the item mix will systematically under-read training-side candidates.** Follows
  from the counting fact, but the magnitude is a guess. The α prediction in B5.3 is the
  falsifiable version; run it.
- **Whether a candidate's correct "we don't have epochs at this scale" response would be
  rewarded or penalised** by a real interviewer. I think rewarded. The follow-up tree has
  no branch for it, so right now it is penalised by the instrument.

### Where I was wrong, and about what

**The persona I was given says my formative instinct is "at this scale I/O is the design,
think in bytes moved per epoch", and that I have a near-allergic reaction to pipelines that
assume data movement is free. The dedup reference answer encodes exactly that instinct — it
frames the whole item as an I/O budget — and I came to it predisposed to agree.** When I
actually did the arithmetic the `good` field demands, it came out against me: aggregate read
bandwidth for 2,000 GPUs is 4–8% of the assumed figure, with enormous slack, and the
bytes-moved frame is the right lens for the one-time shuffle and the wrong lens for the
steady-state read path, where the binding term is access pattern. The reference answer
reaches the right design for a half-wrong reason, and so would I have, unchecked. B3
finding 4 is the one I would most want a second training-infra practitioner to check,
because it is the one where my prior and my result disagree.

I also flagged in advance that I would probably under-rate the serving scenarios and find
fewer real faults in them. On review that was accurate in one direction and not the other:
the serving model answers (`batch-window-vs-ttft-budget`, `kv-cache-admission-control`,
`heterogeneous-fleet-routing`) are the strongest content in the pack and I found nothing
substantively wrong with them, while Appendix B — the shared arithmetic underneath them — is
where I found the two worst errors. That is a throughput person's bias showing up as a
strength rather than a weakness, and I note it so it can be discounted appropriately. On
`vector-index-at-10b`'s rerank path specifically — a few hundred full-precision fetches from
40 TB on disk inside a 50 ms p99 across a ten-machine fanout — I think it is tight and I am
**not** competent to say whether it closes. Give that one to a reviewer who has run a
latency-sensitive serving path.

### What I had to assume because the pack did not say

- That `axes_to_score` for a diagnostic item is exactly the item's two `axes`, so
  `high_level_design = 0` on blind-set Answer 5 is a real finding rather than a
  not-assessed. `prompts.md:206-215` supports this, and A09's `axes` include it.
- That the blind-set answers are single-turn, unprobed responses to a 60-second item, with
  no interviewer utterances withheld. If an interviewer probe preceded any of them, my
  `first_raised_by` reasoning and possibly two scores change.
- That the judge in `eval-infra-per-commit-cost` is the same 70B as the generation model.
  Unstated; the figure swings by ~50% on it.
- That 100 GB/s in the dedup answer is shared read+write sustained bandwidth, not
  write-only. The sentence says "sustained I/O", which is why I read it that way; if
  write-only is meant, the 11 h is right for the write leg and the finding becomes "it
  should say so and should add the read leg".
- That the 4 PB corpus is text. If it is multimodal, my token-scale objection weakens
  considerably and the realism verdict on that item improves — but the raw-versus-training-
  set conflation stands either way.
- Corpus-version frequency, which is the number that actually justifies the reference
  answer's "leave dedup at nine days". The follow-up asks the candidate for it; the model
  answer never produces it. I assumed it is low enough that the priority holds, and I agree
  with the priority. But the reference answer asserts it rather than deriving it, which is
  the behaviour the rubric scores as band 1 elsewhere.

### On the reference answer's priority order, since I own it

**Reproducibility → shuffle → dedup is the right outcome and the wrong decomposition.**

Dedup last is correct and the stated reason is correct: it runs per corpus version, not per
run. I would make that call.

But reproducibility and shuffle are not separable items 1 and 2 — they are the same fix. You
cannot record "the manifest, the seed, and the ordering function" as a reproducibility
artifact when the ordering function is the thing nobody trusts; you would be faithfully
regenerating an order you cannot defend. The dependency runs the other way: define and
verify the ordering function, and determinism plus a recordable artifact fall out of it. The
correct framing is one fix with two benefits, not two fixes in priority order.

And on "what breaks first", which is the prompt's actual question, I would answer
differently from the reference. **The shuffle breaks first, because it is actively wrong
now.** An untrusted shuffle corrupts every run currently in flight and every comparison
between them. Missing reproducibility is a *reporting* gap — it stops you re-deriving what
happened, but it does not make today's run wrong. The reference answer ranks the reporting
gap above the live corruption, and I think it has that backwards.

One overclaim to fix: "it is days of work, not weeks" for content-addressing. Content-
addressing 4 PB means hashing 4 PB — another full corpus pass, ~11 h of pure read at the
answer's own assumed bandwidth, plus a rewrite if the shards are not already laid out for
it. Days of *engineering* effort, plausibly. Free, no. The answer presents reproducibility
as the cheap fix, and its cheapness is the load-bearing claim in its own priority argument.

---

**Reviewer 4. Part A completed before Part B. No expected-score material was read.**
