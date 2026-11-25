# REVIEWER 1 — on-device / memory-constrained inference — RUN 2

Persona: `review-harness/personas/01-apple-on-device.md`. Protocol:
`review-harness/review-protocol.md`.

**Files opened:** `review-harness/personas/01-apple-on-device.md`,
`review-harness/review-protocol.md`, `review-harness/blind-scoring-set.md`, `rubric.md`,
`questions.json`, `prompts.md`. **No off-limits file was opened** — not
`calibration-plants.json`, `dry-run-report.md`, `calibration-plan.md`, nor anything under
`findings/`. No contamination to disclose.

**Set-size discrepancy, noted before scoring:** `review-protocol.md:20` says "For each of
the 5 answers"; `blind-scoring-set.md:6` says "7 candidate answers". I scored all 7 (14
cells). If run 1 was given a 5-answer set, two cells are not comparable across runs — worth
checking before the agreement number is computed.

---

# PART A — Blind scoring

## Answer `D4` — (`capacity_cost_estimation`, `high_level_design`)

```
Answer D4 / capacity_cost_estimation: 3
  cell clause applied: "All of band 2, unprompted, and the result changed the design: the
    number ruled out an architecture, resized a fleet, moved a component, forced an
    admission-control policy, or revealed that the stated SLO is unachievable at the stated
    budget — and they said so."
  evidence: "That is over the one-fifty ceiling. ... To get under the ceiling I need the
    400B share below about 4 percent. That is the number I would hold the routing policy to."
  admits another reading: yes — band 2, and for a specific reason. His numbers are right
    (0.7x0.1 + 0.25 + 0.05x5.7 = 0.605; x$2.60 = $1.57; threshold 0.37 + 4.7x <= 0.5769
    gives x <= 4.4%, so "below about 4 percent" checks out) but one sentence is conceptually
    wrong: "the 5 percent on the 400B contributes 0.285 of baseline while the whole 70
    percent on the 8B contributes 0.07, so the big model's sliver costs four times what the
    small model saves." 0.07 is the 8B's cost contribution, not its saving — the 8B saves
    0.63 of baseline. A grader reading band 1's "the number was produced but not understood"
    clause strictly could land at 2. I score 3 because the threshold he derives is correct
    and it is the thing he commits the policy to. NOTE: this exact conflation is in the
    pack's own model answer and `good` field (see B3.3), so it will not be caught by a judge
    anchored on the reference.
```

```
Answer D4 / high_level_design: 0
  cell clause applied: "No end-to-end path. ... Could not say what happens to a single
    request from arrival to response."
  evidence: (nothing to quote — the axis never appears) "That is the number I would hold the
    routing policy to." is the whole of the design content; there is no router, no
    classifier, no cascade, no fallback, and no answer to the prompt's second half, "what do
    you measure to know you have not quietly made the product worse".
  admits another reading: yes — band 1, and this one is a pack inconsistency, not just my
    uncertainty. Every clause in band 1 of this axis is an error of *commission* (a diagram
    that misses a requirement, brand-named components, a reflex cache), so an answer that
    simply produces no design falls to 0 by elimination. Meanwhile `prompts.md:255` tells
    the grader "Do not reward being right about policy while producing no design. Correct
    and useless is below bar" — and "below bar" is band 1 in the scoring contract
    (`rubric.md:25`). So rubric.md says 0 and prompts.md says 1 for this exact transcript
    shape. I scored 0 because the protocol says to apply the rubric as written. This is a
    one-line fix and it will otherwise split graders every time.
```

## Answer `F3` — (`high_level_design`, `deep_dive_failure_modes`)

```
Answer F3 / high_level_design: 3
  cell clause applied: "All of band 2, and the design visibly follows from the numbers or
    the requirement cut rather than from a template — the component boundary is where it is
    because of a quantity they computed."
  evidence: "at even 100 gigabytes a second of sustained I/O that is on the order of 11
    hours, so it is not something you do every epoch. I would shuffle once into shards at
    ingest and do cheap in-shard shuffling plus shard-order randomisation per epoch"
  admits another reading: yes — band 2, if the grader penalises the number itself. His 11
    hours counts writes only; a global shuffle reads 4PB and writes 4PB, so it is ~22 hours
    (the pack's own model answer for this item says exactly that, and `rubric.md:456` lists
    the omitted-read error as one of four it corrected). The omission is 2x and in the
    conservative direction for his conclusion, so the decision it drives is unaffected; band
    3 on this axis does not require the quantity to be exact, only to be the reason the
    component boundary sits where it does. 3.
```

```
Answer F3 / deep_dive_failure_modes: 2
  cell clause applied: "Required: picked the genuinely hard component and named a concrete
    failure mode of *this* design — not of distributed systems in general — with its
    mitigation."
  evidence: "which is where the trust problem probably comes from: nobody has measured the
    resulting distribution. I would add a verification job that samples it."
  admits another reading: yes — band 3. The verification job is a mitigation he added
    because of a defect he located himself, which is structurally the band-3 pattern
    ("admission control added because the queue is unbounded"). I score 2 because the actual
    failure surface of this design is untouched: 2,000 readers contending on shards, a run
    dying at hour 40 and resuming mid-epoch, a lost or corrupted shard against the
    content-addressed manifest, dedup correctness. An unmeasured distribution is a missing
    measurement, not a failure mode, and the mitigation is monitoring rather than a design
    change. The 2/3 call here rests entirely on whether "nobody has measured it" counts as a
    failure mode — I believe it does not, and I expect reviewers to split.
```

## Answer `J2` — (`capacity_cost_estimation`, `tradeoff_articulation`)

```
Answer J2 / capacity_cost_estimation: 2
  cell clause applied: "Required: named which constraint binds — memory capacity vs memory
    bandwidth vs compute vs network vs dollars — and supported it with a quantity they
    derived, arithmetic within ~2-3x." Indicators: "showed why the other constraints have
    slack".
  evidence: "10 billion vectors at 1,024 dimensions in float32 is 4 kilobytes each, so about
    40 terabytes raw, which makes memory the binding constraint here. Latency has slack — 50
    milliseconds is generous for an approximate lookup"
  admits another reading: yes — band 3, weakly. 40TB is correct (40.96TB), it is derived not
    echoed, memory is correctly named as binding, and the index he picks (IVF-PQ) is the one
    the 40TB implies, so a grader can argue the number moved the design. I score 2 because
    he never states the compressed footprint, so the link from 40TB to PQ is asserted rather
    than derived — the quote carries no consequence, which `prompts.md:317` ("No consequence
    quote, no 3") independently blocks. Band 1's "computed 40TB raw, then chose an index that
    needs all of it resident" does NOT fire: PQ compresses, so his choice is consistent with
    his number.
```

```
Answer J2 / tradeoff_articulation: 1
  cell clause applied: "Or chose, but justified it with an unfalsifiable claim ('it's more
    scalable', 'it's industry standard', 'it's more flexible')." Reinforced by the hard cap:
    "if no trade-off axis was named explicitly, tradeoff_articulation <= 1".
  evidence: "I'd go with IVF-PQ — it's what most billion-scale deployments run." and, for
    the cost the prompt explicitly asked for, only "keep an eye on recall".
  admits another reading: yes — band 2. "keep an eye on recall" plus "memory the binding
    constraint" can be read as naming memory-vs-recall and picking a side. I score 1 because
    the prompt asks "tell me what the choice costs you" and he never says what PQ costs
    (recall loss from quantisation, and the rerank pass that buys it back); naming a quantity
    you will watch is not naming an axis you traded on.
```

## Answer `H4` — (`deep_dive_failure_modes`, `communication_collaboration`)

```
Answer H4 / deep_dive_failure_modes: 2
  cell clause applied: "Required: picked the genuinely hard component and named a concrete
    failure mode of *this* design ... with its mitigation." Band 3's required clause — "a
    failure mode they found changed the design" — is NOT satisfied at the end of the
    transcript.
  evidence: "The actual bug is that retrying the whole turn re-executes side effects, so we
    are duplicating emails and double-charging. I would put an idempotency key on each
    logical operation, generated once per turn." ... then: "Yeah, you know what, that is
    probably fine actually. ... Let's go with that."
  admits another reading: yes — both 3 and 1, and this is the single worst-specified cell in
    the set. (a) Band 3: his first turn is almost verbatim the rubric's own band-3 example
    ("an idempotency key added because the retry path double-charges"), it is unprompted, and
    his 21% compound-failure number (1 - 0.98^12 = 21.5%, correct) is what reframes the
    problem. (b) Band 1: he ends on a design that still double-charges — tool-layer retries
    do not fix a timeout that tells you nothing about whether the charge landed — so the
    failure mode he found changed nothing. I score 2 because the band-2 required clause is
    met outright and the band-3 required clause is not met at the end state. THE RUBRIC HAS
    NO RULE FOR THIS. `prompts.md:261-265` tells the grader how to handle collapse under
    pushback, but scopes it to the pushback behaviour; no cell says whether a retracted
    design change still satisfies a content axis's band-3 clause. See B5.4.
```

```
Answer H4 / communication_collaboration: 1
  cell clause applied: "Collapsed at the first push — abandoned a correct design because it
    was questioned, with no attempt to defend it."
  evidence: "Yeah, you know what, that is probably fine actually. If the retries live at the
    tool layer then each tool handles its own failure, which is cleaner separation anyway.
    Let's go with that."
  admits another reading: yes — band 2, and the band-2 cell as written permits it. Its
    required clause is "where the prompt contained pushback, engaged that specific objection,
    either conceding and saying what changes or holding the position with a reason rather
    than with volume." He conceded, said what changes (retries move to the tool layer), and
    gave a reason ("cleaner separation") — all three literally satisfied. The cell never
    requires the concession to be *correct*, so a graceful capitulation to a wrong objection
    scores at bar. I score 1 because band 1's clause is more specific and fits verbatim.
    This is a real hole: see B5.3.
```

## Answer `P7` — (`requirements_scoping`, `capacity_cost_estimation`)

```
Answer P7 / requirements_scoping: 3
  cell clause applied: "All of band 2, and cut scope in a way that visibly changed the
    design — dropped a requirement, relaxed a consistency guarantee, or deferred a feature,
    and said what the cut bought."
  evidence: "Out of scope: tuning the eviction policy. No policy frees 32 gigabytes; this is
    about admitting long requests against a reserved share of memory." Plus the class split:
    "say a 400 millisecond p99 time-to-first-token for the 95 percent, and the long-context 5
    percent held to its own, worse target rather than blended into one p99."
  admits another reading: yes — band 2. A strict reader can call "Out of scope: X" the band-2
    indicator ("stated at least one thing explicitly out of scope") rather than a band-3 cut.
    I score 3 because he does two separable things: he relaxes a requirement (de-blends the
    p99 and concedes a worse target for one class) and he kills a whole design direction with
    a number attached. His opening — considering fixed batching and rejecting it because "it
    would hurt all day, not only at the peak" — is the "neighbouring framing ruled out on the
    prompt's own evidence" case that `prompts.md:224` exempts from the relevance gate.
```

```
Answer P7 / capacity_cost_estimation: 3
  cell clause applied: "All of band 2, unprompted, and the result changed the design: ...
    forced an admission-control policy".
  evidence: "With 80 layers, 8 KV heads, head dimension 128 in bfloat16, that's about 320
    kilobytes a token, so a 100,000-token request is around 32 gigabytes ... this is about
    admitting long requests against a reserved share of memory."
  admits another reading: no. Arithmetic is exact (2 x 80 x 8 x 128 x 2 B = 327,680 B = 320
    KiB; x 100k = 32.8GB), the quantity is his own, and the consequence is in the quote.
    One imprecision I did not penalise, because the prompt does not state the parallelism:
    "on cards that are mostly holding weights already" overstates — 70B in bf16 is 140GB,
    which over 8 cards is 17.5GB of an 80GB card, 22%, not "mostly". He inherits this from
    the pack's own model answer; see B5.1.
```

## Answer `N7` — (`capacity_cost_estimation`, `tradeoff_articulation`)

```
Answer N7 / capacity_cost_estimation: 1
  cell clause applied: "Derived the number that decides the question, then proposed a design
    it rules out (computed 40TB raw, then chose an index that needs all of it resident) — the
    number was produced but not understood."
  evidence: "about 40 terabytes raw. ... Given the recall requirement I would use HNSW ... I
    would set M to 32 and efConstruction to 200"
  admits another reading: no. The band-1 clause fits almost word for word: HNSW holds
    full-precision vectors plus graph links resident, so his index needs the 40TB he just
    computed, plus roughly 10B x 32 x 2 x 4B ~ 2.5TB of neighbour lists at M=32. Band 2's
    required clause fails independently — he recites all three prompt constraints and never
    says which one binds. He also ignores that 200M daily changes is the case HNSW handles
    worst (in-place graph update and delete), and "0.95-plus recall at single-digit
    millisecond latency" is a recalled benchmark figure at a far smaller scale, used in no
    arithmetic step.
```

```
Answer N7 / tradeoff_articulation: 1
  cell clause applied: "chose, but justified it with an unfalsifiable claim"; and "named a
    trade-off that isn't one in this scenario" — he trades on latency, which the prompt's own
    50ms gives slack on, while the binding axis (memory, and rebuild cost under 2% daily
    churn) goes unmentioned.
  evidence: "I would use HNSW, because it has the best recall-latency curve of the ANN
    families — typically 0.95-plus recall at single-digit millisecond latency."
  admits another reading: YES — band 2, and this is the most important flag in my Part A. The
    band-2 required clause is "named the axis of the trade-off in units ... recall vs p99 ...
    and picked a side. Both halves, or it is band 1." He names recall-vs-latency, in units,
    and picks HNSW, so a literal grader scores 2. I score 1 because a "best curve" is a claim
    of dominance, not a side-pick: he gives up nothing, which is the one thing this axis
    exists to observe. The clause that would have caught it — "acknowledged specifically what
    the choice gives up" — is listed as an *indicator*, and indicators cannot block a 2. See
    B4.
```

## Answer `W7` — (`requirements_scoping`, `communication_collaboration`)

```
Answer W7 / requirements_scoping: 1
  cell clause applied: "recited a generic checklist unconnected to this scenario" / "Listed
    eight requirements and prioritised none."
  evidence: "There is also cold start on the replicas which I have not accounted for, and
    sharding overhead. Storage for the results is negligible. Network egress depends on where
    the judge runs."
  admits another reading: yes — band 0 ("Treated an underspecified prompt as a
    specification"), which describes what he did exactly. I score 1 rather than 0 on a
    technicality: this prompt is not underspecified — it states every number — so that clause
    does not strictly apply, and the caveat list is a scoping behaviour performed badly
    rather than absent. He accepts 50,000, every commit, and 10 minutes without testing any
    of them, which is the whole point of the item. Arithmetic all checks: 100M tokens / 600s
    = 166,666 tok/s; 27.7 -> 28 replicas -> 112 GPUs; 112 x (1/6)h = 18.67 GPU-h x $2 =
    $37.33; x40 = $1,492/day; x365 = $544,580.
```

```
Answer W7 / communication_collaboration: 1
  cell clause applied: "Answered a different, easier question than the one asked and did not
    acknowledge the substitution."
  evidence: "Okay so 50,000 times 2,000 is 100 million tokens." ... ending at "Network egress
    depends on where the judge runs." — the prompt's second half, "tell me what you would
    push back on", is never addressed, and the substitution is never named.
  admits another reading: yes — band 2, through a gap in the cell's wording. Band 2 requires
    "answered the question that was actually asked ... and where the prompt contained
    pushback, engaged that specific objection". The prompt here does not *contain* pushback;
    it *asks the candidate to produce* pushback, at a named stakeholder ("I am a research
    engineer"). The cell covers interviewer-to-candidate pushback only, so a grader can find
    its required clause satisfied by the cost answer alone. I score 1 because half the
    question went unanswered unacknowledged. Three of the twelve items pair
    `communication_collaboration` with a prompt of this shape; see B5.3.
```

## Hardest cell to apply

**`H4` / `deep_dive_failure_modes`** — whether a design change the candidate proposes and
then retracts still satisfies band 3's required clause, "a failure mode they found changed
the design". The cell's verb is in the past tense and the rubric never fixes a vantage
point: at minute one the clause is satisfied, at minute two it is not. The rubric's only
retraction rule (`prompts.md:261-265`, "Abandoning a correct position with no defence ... is
below bar") is scoped to the pushback axis, so a grader has to invent a policy for the
content axes. I can construct a defensible 1, 2 and 3 for this cell from the rubric as
written, which means it is not one cell but three. Runner-up: `N7` /
`tradeoff_articulation`, for the reason in B4.

---

# PART B — Critique from my domain

## B1. Axis legitimacy

**Yes for five of the six, and `capacity_cost_estimation` is the one I would defend hardest
— which is the opposite of the pack's own prediction** (`rubric.md:400-402` names it "the
single most likely place this rubric is wrong"). In a round where the subject is inference
or training infrastructure, the binding constraint genuinely is a scalar — HBM capacity,
HBM bandwidth, dollars per million tokens — and a candidate who cannot produce it cannot
have the trade-off conversation at all. Part A is evidence for this rather than against it:
`N7` and `J2` answer the same prompt, differ almost entirely in whether the 40TB was
*understood*, and the axis separated them cleanly where `tradeoff_articulation` did not.

**What my answer rests on:** roughly 150 hardware-adjacent system design loops in the
constrained-inference category, as an interviewer. That is a real base of experience and it
is narrow in a specific way: it is all problems where the memory budget is fixed and there
is no second node. I have not run a multi-tenant hosted API loop.

**What would change my mind:** evidence that the axis is not *separable* from
`tradeoff_articulation` in practice — specifically, a set of hand-scored sessions in which
the two axes' scores correlate above ~0.85. If they do, the pack is carrying two axes to
measure one behaviour, and the honest fix is to fold capacity into trade-offs and spend the
sixth slot elsewhere. That is a measurement, not an argument, and it should be run.

**Where I am reasoning from general description rather than loops I have run:** the level
mapping. I have never scored a candidate on a 0-3 scale with a threshold table, and I have
no basis for saying whether 1.75 and 2.50 are the right cut points. Weight my B1 answer on
the axes; discount me entirely on the thresholds. (The pack already concedes this at
`rubric.md:142-148`, and the five-reviewer split it reports there — 5 of 5 on the axes, 0 of
5 on the level claim — matches where my own confidence sits.)

## B2. Scenario realism — my three

### `batch-window-vs-ttft-budget` — **not realistic**, on the numbers

The *framing* is excellent and is the single best thing in the pack: "Both numbers are bad
at the same time" is exactly how this arrives in real life, and the `bad` field (raise the
batch size) is the real failure, not an invented one.

**Single thing most wrong: the three stated numbers cannot co-occur, and no arrival rate is
given, so the quantity the model answer calls the dominant term is not derivable from the
prompt.** Work it: one 4xH100 replica spends ~177ms of exclusive GPU compute prefilling a
2,000-token prompt (2 x 70e9 x 2,000 = 0.28 PFLOP at the appendix's own 1.584 PFLOPS), plus
~75ms per request of decode at batch 32 (12.0ms/step x 200 output tokens / 32), so ~252ms of
GPU time per request. At the stated 45% utilisation that is **1.8 requests/sec**, and a
static batch of 32 takes **~18 seconds** to fill — not 1.2 seconds. Inverting it: a 1.2s
p99 driven by fill time implies ~27 requests/sec, which needs **~7x** this replica's
capacity and would pin utilisation at 100% with an unbounded queue. The three numbers are
mutually inconsistent by about an order of magnitude whichever one you solve for. This is
the failure mode my brief says I care most about: a candidate who checks finds the scenario
incoherent, and a candidate who does not check is rewarded. Fix: state the arrival rate
(say 1.5 req/s/replica), drop utilisation to a value consistent with it, or say plainly that
"45% utilised" is MFU rather than busy-time — the prompt does not say which, and the two
differ by more than 2x.

### `kv-cache-admission-control` — **realistic, wrong in one detail**

This is the best item in the pack. The shape is right, and `bad` correctly identifies the
eviction-policy detour as the attractive wrong turn rather than a straw man.

**Single thing most wrong: the prompt states "eight nodes of eight H100s" and then nothing
in the item uses it, so KV-per-card is undecidable and the per-card comparison in the model
answer goes undetected.** Without a parallelism or replication topology, 32.8GB of KV for
one request cannot be placed: under TP=8 it is ~4.1GB per card, under one replica per card
it is 32.8GB against 80GB. The model answer picks the latter framing ("against 80 gigabytes
of HBM per card, most of which is already holding weights"), which is the inflation
Appendix B explicitly retracts at `rubric.md:469-473`. Secondary: "the long requests push
the short ones out of cache" needs ~15 concurrent long requests to exhaust a node's ~500GB
of non-weight HBM; the prompt gives a traffic *share* but no concurrency, so the stated
mechanism is not checkable from the stated facts. Add "TP=8 within a node" and a peak
concurrency figure and this item becomes airtight.

### `heterogeneous-fleet-routing` — **realistic, wrong in one detail**

**Single thing most wrong: the A100/H100 heterogeneity in the prompt is decorative.** The
reference cost model is purely parameter-count ("cost per token roughly tracks weight bytes
read"), so the fleet mix plays no role at all — yet A100 at ~2.0 TB/s versus H100 at 3.35
TB/s and a materially different $/GPU-hour is precisely what makes cost-per-token
*device-dependent*, and a candidate who raises it is answering a better question than the
reference does. Either make it load-bearing (which model lands on which silicon, and what
that does to the blend) or remove it; as written it is a constraint stated and then ignored,
which teaches the candidate to ignore stated constraints. Related, lower confidence: cost ∝
total parameters assumes the 400B is dense. At that scale production models are mixture-of-
experts, where decode cost tracks *active* weight bytes, so 5.7x is likely a large
overestimate — and a dense 400B in bf16 is 800GB, which does not fit the 4-GPU unit the rest
of the pack reasons about. Flagging as domain judgement, not fact.

## B3. Arithmetic

### Checked and correct

Appendix B is in much better shape than its own warning note suggests. All of these
recompute: KV/token `2 x 80 x 8 x 128 x 2 B = 327,680 B = 320 KiB`; 100k context = 32.8GB;
32.768/640 = **5.12%** of a node; 41% of one card; 8B-class 128 KiB/token. GQA parameters
are coherent — 8 KV heads with head_dim 128 and 64 query heads gives d_model 8192, which is
the figure the prefill section uses. Decode at batch 64: KV 41.94GB = 30.0% of 140GB,
(140+41.9)/13,400 = 13.6ms, 64/0.01357 = **4,716 tok/s**. Prefill crossover `70e9 /
(8192 x 80) = 106,812` tokens. Prefill table: 1.4 + 0.13 = 1.53 PFLOP -> 0.96s; 14 + 13.1 =
27.1 PFLOP -> 16.9s; attention share 48%. 4 x 990 TFLOPS x 40% = 1.584 PFLOPS. The
attention formula `2 x n² x d_model x layers` already carries the causal halving, and the
comment says so. Shuffle: 8PB at 100GB/s = 22.2 hours.

### Wrong — 1. `rubric.md:521-527`, the token-economics figure is self-contradictory

> "At ~6,000 output tok/s — the KV-corrected figure, not the weights-only 6,000 — that is
> ≈ $0.47 per million output tokens"

The parenthetical contradicts itself (both numbers are 6,000), and the two halves of the
sentence disagree. $0.0022/sec ÷ 6,000 tok/s = **$0.37/M**. The stated $0.47/M requires
**4,716 tok/s** — the KV-corrected figure from four paragraphs earlier. So the dollar figure
was recomputed and the prose was not. Fix the sentence to read "~4,700 output tok/s — the
KV-corrected figure, not the weights-only ~6,000".

### Wrong — 2. the decode floor is a true floor but is used as an achievable number

My brief asks whether the floor accounts for tensor-parallel communication. It does not, and
the omission is **small**: at batch 64, TP=4, d_model 8192, bf16, each all-reduce payload is
1.05MB, a ring all-reduce moves 1.5x that per rank = 1.57MB over 900GB/s NVLink ≈ 1.75µs,
and 2 collectives per layer x 80 layers = 160 calls ≈ 0.28ms of transfer plus ~1.1ms of
per-call latency, so **~1.4ms on a 13.6ms step, about 10%**. I would not rewrite the floor
for that. The real optimism is elsewhere and larger: the floor assumes **100% of peak HBM
bandwidth**. At a realistic 70% achieved, the step is **19.4ms** and aggregate throughput is
**~3,300 tok/s**, which moves raw compute cost to **~$0.67/M output tokens**. Calling it a
"floor" is correct and honest; *spending* it as a throughput number is not, and both the
token-economics paragraph and the `eval-infra-per-commit-cost` model answer do exactly
that. Add one sentence: "achieved bandwidth is typically 60-80% of peak, so the realistic
step is 1.3-1.6x this floor."

### Wrong — 3. `questions.json` `heterogeneous-fleet-routing`, `good` and `model_answer`

> "the 5 percent on the 400B costs four times what the whole 70 percent on the 8B saves"

This compares a cost *contribution* (0.285 of baseline) with another cost *contribution*
(0.07), and calls the second a saving. Moving 70% of traffic from the 70B to the 8B **saves
0.63 of baseline**, which is 2.7x *more* than the 400B sliver costs — so the sentence is
false as written, and `good`'s stronger form ("a few percent on the 400B outweighs the whole
70 percent saving on the 8B") is also false. The defensible statement is marginal: with
blend = `1 - 0.9a + 4.7c`, a point of 400B share costs 4.7 and a point moved to the 8B saves
0.9, so **a point of 400B share costs 5.2x what a point of 8B share saves**. Same
conclusion, correct method, and a different number (5.2, not 4).

### Wrong — 4. same item, `bad`: the intended discrimination is defeated by its own rounding

> "a candidate who only tunes the 70 percent never reaches the ceiling"

Solve it: with c fixed at 5%, `1.235 - 0.9a <= 0.5769` gives **a >= 73.1%**. The prompt says
"*about* 70 percent of current traffic would be served acceptably by the 8-billion model" —
and 73.1% is inside "about 70". So the answer the item is built to mark wrong is available
to a candidate who rounds in their own favour, and the grader has no basis to reject it.
Fix: state it as a cap — "no more than 70 percent can be served acceptably; treat that as
hard" — which forces the 400B share to be the only lever and makes the intended insight the
only route.

### Not an error, but Appendix B does not do what it scores

The prefill table gives "~1.0s" and "~17s" to one significant figure, and both rest on two
soft factors: a dense ~990 TFLOPS derived by halving a *sparsity* marketing figure the
vendor does not publish densely, and an assumed 40% achieved utilisation. Each is good to
maybe ±30%, so 17s is honestly 10-30s. On my brief's question — is quoting the sparsity
figure a trap even with the caveat? — yes, mildly: the caveat is clear but the derived
number then propagates through two multiplications into a table that reads as measured. The
rubric's own band 3 asks candidates to "flag which assumption the answer is most sensitive
to"; Appendix B should model that behaviour in its own table and currently does not. State
the prefill numbers as ranges and name MFU as the sensitive assumption.

### Documentation mismatch

`rubric.md:453-457` says four numbers were wrong and "Corrected below", naming the shuffle
figure as one of them. Appendix B contains no shuffle derivation — the corrected 8PB/22h
figure lives only in the `training-data-dedup-and-shuffle` model answer. Either move it into
the appendix or stop claiming it is there.

## B4. The band 2/3 boundary

**It is in roughly the right place, and it is not where this instrument is weakest.** I used
band 3 four times in 14 cells and in every case the required clause was quotable with the
consequence attached, which is the whole design intent; `D4`, `F3`/HLD, and both `P7` cells
each name a number and then a decision the number forced. The "ONE required clause, the rest
are indicators" refactor works as advertised here. I expect reviewer disagreement at the
2/3 boundary to be *lower* than the pack fears.

**The boundary that failed, repeatedly, is 1/2 — and the band-3 fix created it.** Demoting
clauses to indicators is the right move on five axes. On `tradeoff_articulation` it removed
the only clause that observes the behaviour the axis is named for: "acknowledged specifically
what the choice gives up" is now an indicator, and indicators cannot block a 2. So `N7`
("best recall-latency curve of the ANN families", nothing conceded, the binding constraint
untouched) literally satisfies the band-2 required clause — an axis in units, plus a pick —
while doing the opposite of articulating a trade-off. `J2` fails the same way from the other
direction. Both of my 1s on that axis are scores I believe and can be argued to 2 from the
cell text, and that is two of my four most likely disagreements with the other reviewers.

**Fix, and it is small:** move "acknowledged specifically what the choice gives up, in the
units of the axis named" from Indicators into Required on `tradeoff_articulation` only.
Three clauses, one axis. A trade-off in which nothing is given up is a preference, which is
what band 1 already says.

**Second, smaller:** the 0/1 boundary on `high_level_design` is unapplicable as written,
because every band-1 clause is an error of commission and an answer with no design at all
falls to 0 by elimination — while `prompts.md:255` says the same transcript is band 1. See
`D4` and B5.2.

## B5. Top 3 defects, ranked

### 1. Appendix B's corrections never propagated to the model answers — and the model answers are what teach the judge

**File:** `questions.json` (`batch-window-vs-ttft-budget`, `kv-cache-admission-control`,
`eval-infra-per-commit-cost` model answers), `prompts.md:291-293`, `rubric.md:521-527`.

**What is wrong:** `rubric.md:453-457` announces four corrected derivations. At least three
reference answers still carry the uncorrected versions.
- `batch-window-vs-ttft-budget`: "one decode step floors around 10 milliseconds" is the
  weights-only floor. At batch 32 with 2k context, KV adds 21.0GB, so it is ~12.0ms.
- `kv-cache-admission-control`: "32 gigabytes of KV — against 80 gigabytes of HBM per card,
  most of which is already holding weights" is the per-card inflation Appendix B retracts.
  Weights are 17.5GB of an 80GB card under TP=8 — 22%, not "most" — and the correct
  comparison is 5.12% of the node.
- `eval-infra-per-commit-cost`: "on the order of 6,000 tokens a second" per 4-H100 replica.
  At the corrected 4,716 the fleet is 36 replicas / 145 GPUs, ~$48/commit, ~$1,930/day,
  **~$705k/year** — not the "about half a million" the model answer teaches, a 30% miss on
  the item's headline number.
- `prompts.md:291-293`: the `derivation_steps` schema example is
  `{"inputs": "140 GB weights, 13.4 TB/s aggregate", "op": "140/13400", "result_stated": "10ms"}`
  — the weights-only derivation, shipped as the worked example the grader imitates.

**Why it matters:** this is the highest-leverage defect in the pack because of where the
errors sit. The judge reads `model_answer` and `good` and generates `contrast` from them
(`rubric.md:442-444`, `prompts.md:272-275`). An error there is not one wrong item — it is
the anchor for every grade on that item and the at-bar answer shown to every candidate who
misses it. And the error class is self-concealing: `rubric.md:490-492` says a candidate who
quotes the weights-only number is band 2 and one who notices the KV term is band 3, while
the reference answer for the item that scores that axis quotes the weights-only number. The
pack cannot detect this class of error, because the thing that would catch it is the thing
that is wrong. Evidence it is already propagating: `P7`, which I scored 3/3, reproduces the
model answer's "mostly holding weights" framing verbatim in substance.

**What I would do:** treat Appendix B as the single source of truth for every derivation and
re-derive all 12 model answers against it in one pass, with a test that fails if a model
answer states a decode-step time, a KV footprint, or a tok/s figure that does not reconcile
with the appendix. Fix the `prompts.md` schema example in the same change — it is three
tokens and it is the example the grader will copy.

### 2. `rubric.md` and `prompts.md` disagree on the floor for "correct but no design"

**File:** `rubric.md:249-250` (axis 3, bands 0 and 1) versus `prompts.md:255`.

**What is wrong:** `prompts.md` instructs the grader "Do not reward being right about policy
while producing no design. Correct and useless is below bar" — band 1 by the scoring
contract. `rubric.md`'s band-1 cell contains only errors of commission, so a transcript with
no design satisfies band 0's "No end-to-end path" and nothing in band 1. `D4` is exactly
this transcript, and the two files give it different scores.

**Why it matters:** it is a guaranteed inter-rater split on a cell that occurs often (a
numerate candidate who answers the arithmetic half of a two-part prompt and runs out of
time), and 0 versus 1 is not cosmetic — `rubric.md:135` sends any axis below 1.00 straight
below the senior bar, so this one cell decides a public status claim.

**What I would do:** add one clause to band 1 of `high_level_design`: "Produced a correct
decision or policy with no components and no request path — correct and useless." Then band
0 means the axis was never engaged and band 1 means it was engaged and failed, which is the
distinction `rubric.md:350` already requires of every 0/1 pair.

### 3. `communication_collaboration` band 2 scores the form of a concession and not its substance, and does not cover the prompt shape it is paired with

**File:** `rubric.md:326` (band 2 Required), against `questions.json`
`agent-retry-side-effects`, `eval-infra-per-commit-cost`,
`inline-safety-classifier-budget`, `annotation-throughput-vs-agreement`.

**What is wrong:** two holes in one clause.
(a) "either conceding and saying what changes or holding the position with a reason" is
satisfied by a *wrong* concession delivered politely. `H4` concedes to an objection that
does not address the bug, names what changes, and gives a reason — all three halves of the
required clause — while accepting a design that still double-charges cards.
(b) The clause only covers pushback that arrives *in the prompt*, aimed at the candidate.
Three of the four items on this axis instead ask the candidate to *generate* pushback at a
named stakeholder ("tell me what you would push back on", "I am a research engineer"). For
those, the required clause reduces to "answered the question" and the axis stops measuring
collaboration. `W7` answers half the question, never acknowledges dropping the other half,
and can be read as at bar.

**Why it matters:** `rubric.md:329-333` calls this the axis that carries the product. Two of
my four likely disagreements are on it, and both are the cell's wording rather than the
transcripts.

**What I would do:** add to Required — "where the prompt asks the candidate to push back on
a stakeholder's requirement, named the specific clause they are contesting and what they
propose instead" — and to band 1 — "conceded to an objection that does not address the
problem they had just identified, without testing it."

### 4. (Named, not ranked, because it is a gap rather than an error) No rule for a retracted design change

`rubric.md:277` and `rubric.md:212` require that a finding "changed the design" without
fixing when that is evaluated. `prompts.md:261-265` handles collapse under pushback but
scopes it to the pushback behaviour. A transcript where the candidate proposes the right fix
and then withdraws it is scoreable as 1, 2 or 3 on a content axis from the rubric as
written — I hit this on `H4` and it was the hardest cell in Part A. One sentence fixes it:
"Band 3 requires the design change to survive to the end of the session. A proposal the
candidate withdraws without testing the objection scores at most 2 on the content axis, and
the withdrawal is scored on `communication_collaboration`."

### 5. (Also unranked, lower confidence) The attribution clamp penalises the escalation it is paired with

`prompts.md:324` clamps an axis to ≤1 when `first_raised_by == "interviewer"`, and
`prompts.md:85-86` tells the interviewer to escalate on a strong candidate by taking
something away or doubling a constraint. A candidate who handles the escalation well is
performing the behaviour *on a constraint the interviewer introduced*. The schema carries one
`first_raised_by` per axis for the whole session, so a late escalation can clamp an axis the
candidate already earned unprompted. Scope the clamp to the consideration rather than the
session, or exempt probes labelled `at_bar_*`.

## B6. Sign-off

**Would I put my name on the rubric as legitimate? Yes** — on the six axes, the scoring
contract, the relevance gate, the derived-quantity cap, and the band-2/band-3 required-clause
structure. It is better than most internal rubrics I have worked from, the band-1 cells are
observable rather than adjectival, and the departures from its sources are stated instead of
smoothed. The one-line caveat: **not with `tradeoff_articulation` band 2 as currently
written** (B4), because that is the axis the level mapping gates at every level and its
required clause can be satisfied by an answer that gives nothing up.

**What I would refuse to let ship as-is:**

1. **Any model answer carrying a derivation Appendix B has superseded** (B5.1). This is the
   one I would actually block on. It is a day of work, it is checkable, and until it is done
   the judge is anchored on arithmetic the pack has already disowned.
2. **`batch-window-vs-ttft-budget` in its present form** (B2). Its three numbers cannot
   co-occur, and it sizes a TTFT budget from a decode floor while the pack's own [NIM]
   citation at `rubric.md:517-519` defines TTFT as queueing plus prefill. A 2k prefill is
   ~177ms, 44% of the stated 400ms budget, and the reference answer never computes it. Fix
   the arrival rate and add the prefill term.
3. **The level claim**, which I would not display, exactly as `rubric.md:142-148` already
   says. I have no standing on the thresholds (B1) and I am not adding a sixth unvalidated
   opinion to five; I note only that my Part A produced a 0 on one cell, which under
   `rubric.md:135` would by itself push a candidate below the senior bar on the strength of
   a single 60-second answer and a cell that two files score differently.

I would ship the diagnostic without the level claim, with the model answers re-derived, and
with `batch-window-vs-ttft-budget` held back pending its numbers.

## B7. Epistemic status

**Checkable facts — recompute these and you will get my answer or I am wrong:**
- `rubric.md:521-527` is internally inconsistent: $0.47/M requires 4,716 tok/s, the text
  says 6,000, and 6,000 gives $0.37/M. The parenthetical contradicts itself.
- The "four times what the small model saves" comparison in
  `heterogeneous-fleet-routing` (`good` and `model_answer`) compares two cost contributions
  and labels one a saving. The 8B saves 0.63 of baseline; the marginal ratio is 5.2, not 4.
- `a >= 73.1%` reaches the $1.50 ceiling with the 400B share fixed at 5%, which is inside the
  prompt's own "about 70 percent", so `bad`'s claim is false as stated.
- Three model answers carry derivations Appendix B supersedes, and `prompts.md:291-293`
  ships the weights-only derivation as the grader's worked example.
- `rubric.md` band 0/1 of `high_level_design` and `prompts.md:255` assign different bands to
  the same transcript shape.
- Appendix B contains no shuffle derivation despite `rubric.md:453-457` saying it is there.
- Everything in the "checked and correct" list of B3, including every Appendix B derivation
  I could recompute, and the arithmetic in `D4`, `H4`, `P7`, `N7`, `J2` and `W7`.
- `questions.json` axis coverage is internally consistent: 4 items per axis, and `_meta`'s
  `axis_coverage` matches the per-item `axes` exactly.

**Domain judgement a constrained-inference practitioner would mostly share:**
- The ~7x inconsistency in `batch-window-vs-ttft-budget`. The arithmetic is checkable; the
  input I had to assume is not (see below), so the *size* of the inconsistency is judgement
  even though its existence is not.
- That calling 13.6ms a floor is right but spending it as throughput is wrong, and that
  60-80% of peak HBM bandwidth is the honest achieved range.
- That ~1.4ms of TP=4 all-reduce overhead at batch 64 is real but not worth rewriting the
  floor for. I would expect agreement on the conclusion and argument about my per-call
  latency figure.
- That the A100/H100 heterogeneity is decorative as the item is written.
- That TTFT is dominated by queueing and prefill, not by the decode step.
- Lower confidence within this bucket: that a 400B-class production model is MoE, so cost ∝
  total params is the wrong cost model. Confident about current practice, less confident
  that it is the right simplification for a 60-second teaching item.

**Guesses about interview practice that need a human to confirm:**
- B1's claim that `capacity_cost_estimation` deserves axis status. I believe it from my own
  loops, which are all in one corner of the category, and the pack's own instinct runs the
  other way. The correlation test I propose in B1 settles it; my opinion does not.
- Whether a real panel would score `H4` at 2 or 3 on failure modes — whether, in practice,
  interviewers score the analysis or the end state. I have a view and no data.
- Whether any of the band 1/2 boundaries I flagged would actually split human reviewers, or
  only split graders reading the cell text literally. My Part A is one reviewer's evidence
  on this and should be weighted as such.
- Everything about the level thresholds, per B1.

**What I had to assume because the pack did not say:**
- **Output length.** My replica-capacity arithmetic for `batch-window-vs-ttft-budget`
  assumes 200 output tokens per request. The prompt states no output length. I checked 50
  and 200 and the inconsistency stays above 10x, so the finding is robust to this, but the
  specific "1.8 req/s" depends on it.
- **Achieved utilisation.** I used the appendix's own 40% MFU for prefill. At 60% the
  inconsistency is ~12x instead of ~15x.
- **Parallelism topology.** I assumed TP=8 within a node for `kv-cache-admission-control`
  and TP=4 for `batch-window-vs-ttft-budget` (the latter is stated, the former is not). The
  per-card KV finding depends on this assumption, and that the assumption is *needed* is
  itself the finding.
- **What "45 percent utilised" measures.** I read it as GPU busy time. If it means MFU the
  numbers move by more than 2x and the item needs to say which.
- **Whether `A100` pricing differs from H100 in the pack's cost model.** Nothing states it,
  so I assumed the $2/GPU-hour figure in Appendix B applies to both, which is almost
  certainly wrong and is part of why I call the heterogeneity decorative.

**My known biases, from my own brief, stated so they can be discounted:** I over-weight
arithmetic precision relative to communication — four of my five B5 defects are numeric or
cell-wording, and only one concerns the communication axis, which the pack itself calls the
one that carries the product. A reviewer from a product or hiring background should be
trusted over me on whether `communication_collaboration` is scorable from 60 seconds at all.
And my instincts about multi-tenancy, quota and noisy neighbours are weaker than they feel,
so I deliberately did not review `multi-tenant-token-limiter-placement` or
`gpu-credit-ledger-consistency` and have no opinion on them worth recording.
