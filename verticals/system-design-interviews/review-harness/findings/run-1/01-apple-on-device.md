# REVIEWER 1 — on-device / memory-constrained inference

Domain: inference on hardware you cannot change. Owns `rubric.md` Appendix B derivations and
the three `inference_serving` capacity scenarios.

Files read: `review-harness/personas/01-apple-on-device.md`, `review-harness/review-protocol.md`,
`review-harness/README.md`, `review-harness/blind-scoring-set.md`, `rubric.md`, `questions.json`
(4 items in full), `prompts.md` (grader section), `calibration-plan.md` (agreement targets only).

Not read, per instruction: `calibration-plants.json`, `dry-run-report.md`, `findings/*`.
**Partial de-blinding did occur anyway — see B7, it is a harness finding.**

---

# PART A — BLIND SCORING

## Answer 1 (`A01`)

```
Answer 1 / capacity_cost_estimation: 1
  cell clause applied: band 1 — "Gave a number with no derivation" / scoring contract
    "Below bar — appeared, but wrong, unquantified, generic"
  evidence: "Then I would tune the window empirically, watch the p99, and iterate until
    both numbers look healthy."
  admits another reading: yes — band 0, and it is close. The candidate produced no quantity
    of their own at all; the only number in the answer is "our 400 millisecond target",
    echoed from the prompt. Band 0's clause is "No quantity of any kind, in a scenario whose
    constraints were stated numerically", and taken literally that is satisfied, because the
    hard-cap section of the same axis defines a quantity as one "of their own" and explicitly
    names echoing the prompt as not counting. I scored 1 because something in the answer did
    depend on the number ("Given our 400 millisecond target I would bias toward latency"),
    and the scoring contract makes band 0 "nothing in the answer depended on it". The cell
    text and the cap text disagree. See B5 defect 1.
```

```
Answer 1 / tradeoff_articulation: 2
  cell clause applied: band 2 — "Named the axis of the trade-off in units ... stated which
    side of it this system should sit on and why, given the stated requirement, and
    acknowledged specifically what the choice gives up. Picked."
  evidence: "The trade-off is latency against throughput: a wider batch window buys you
    utilisation and spends time-to-first-token. Given our 400 millisecond target I would
    bias toward latency."
  admits another reading: yes — band 1, via "chose, but justified it with an unfalsifiable
    claim". The axis is named and a side is picked, which is band 2 cleanly. But the actual
    quantity the trade-off resolves to — the window width — is handed to "iterate until both
    numbers look healthy", and "look healthy" is unfalsifiable in a scenario whose stated
    premise is that both numbers are bad at once. A reviewer who reads the trade-off as
    unresolved rather than as resolved-in-direction lands on 1. Band 3 is not in question:
    no number of their own exists for it to resolve against.
```

## Answer 2 (`A03`, HNSW)

```
Answer 2 / capacity_cost_estimation: 1
  cell clause applied: band 1 — "Derived the number that decides the question, then proposed
    a design it rules out (computed 40TB raw, then chose an index that needs all of it
    resident) — the number was produced but not understood."
  evidence: "10 billion vectors at 1,024 dimensions in float32 is 4 kilobytes per vector,
    so about 40 terabytes raw. ... Given the recall requirement I would use HNSW"
  admits another reading: no. The arithmetic is correct (I verified: 1024 x 4 B = 4096 B;
    10e9 x 4096 B = 40.96 TB) and the churn figure is correct (200M/10B = 2%), so a
    clause-counting grader is tempted by band 2. But band 2 requires "Named which constraint
    binds ... and showed why the others have slack", which never happens — 40TB is produced
    and then dropped — and the band-1 cell describes this answer almost verbatim. HNSW at
    M=32 needs the full-precision vectors plus ~256 B/vector of layer-0 links resident,
    i.e. >43 TB of RAM. Unusually unambiguous cell.
```

```
Answer 2 / tradeoff_articulation: 1
  cell clause applied: band 1 — "chose, but justified it with an unfalsifiable claim
    ('it's more scalable', 'it's industry standard', 'it's more flexible')"
  evidence: "because it has the best recall-latency curve of the ANN families — typically
    0.95-plus recall at single-digit millisecond latency"
  admits another reading: yes — band 2, and I expect reviewers to split here. The case for 2:
    "tune efSearch to land inside the 50 millisecond budget" is a genuine axis in units
    (recall vs p99 ms) with a side picked (hold recall, spend latency). The case for 1, which
    I believe: the prompt's explicit demand was "tell me what the choice costs you", and the
    answer names no cost at all — not memory, not build time, not the delete/rebuild
    behaviour under 2% daily churn. "Best recall-latency curve of the ANN families" asserts
    dominance, which is the opposite of naming a trade-off. Band 2 lists three clauses
    ("named the axis", "picked", "acknowledged what it gives up") and the rubric nowhere says
    whether band 2 is conjunctive — band 3 explicitly declares one required clause and band 2
    declares nothing. Read conjunctively this is 1; read as any-of, it is 2. See B4.
```

## Answer 3 (`A03`, IVF-PQ)

```
Answer 3 / capacity_cost_estimation: 2
  cell clause applied: band 2 — "Named which constraint binds — memory capacity vs memory
    bandwidth vs compute vs network vs dollars — and showed why the others have slack."
  evidence: "about 40 terabytes raw, which makes memory the binding constraint here. Latency
    has slack — 50 milliseconds is generous for an approximate lookup"
  admits another reading: yes — band 3, and this is the most consequential split in the set.
    The band-3 required clause is "the result changed the design ... and they said so". A
    grader can read "which makes memory the binding constraint here" plus a compressing index
    as exactly that. I score 2 because of ordering and provenance: the index is chosen in the
    first clause of the answer and justified by "it's what most billion-scale deployments
    run", and the sizing arrives afterwards as corroboration. The number did not rule out an
    architecture — popularity selected it and the number was then found to agree. No
    compressed footprint is computed (the pack's own model answer does: ~64 B/vector =
    ~640 GB, a 64x reduction), so nothing resizes the fleet. Also worth recording: this
    answer is visibly less decorated than Answer 2 and scores higher, which is the rubric
    working as designed.
```

```
Answer 3 / tradeoff_articulation: 1
  cell clause applied: band 1 — "chose, but justified it with an unfalsifiable claim ... 'it's
    industry standard'" (and the hard cap: no trade-off axis named explicitly => <= 1)
  evidence: "I'd go with IVF-PQ — it's what most billion-scale deployments run."
  admits another reading: no, or barely. "Memory binds, latency has slack" is constraint
    identification, not a trade-off — it asserts the two do not trade here. The axis this
    choice actually sits on is compression ratio vs recall@10, and the entire acknowledgement
    of it is "keep an eye on recall", against a prompt that stated 0.9 as a floor and asked
    what the choice costs. The hard cap applies on its own terms.
```

## Answer 4 (`A08`)

```
Answer 4 / requirements_scoping: 1
  cell clause applied: band 1 — "recited a generic checklist unconnected to this scenario";
    reached via the relevance gate, "A behaviour performed on the wrong problem scores at most
    band 1 on every axis, however well executed."
  evidence: "The problem is that a fixed batch size makes time-to-first-token depend on batch
    fill rather than on compute."
  admits another reading: yes — band 0. The item asked two direct questions ("what exactly are
    you protecting, and what is the first number you would want?") and the answer answers
    neither: nothing is named as protected, no request class is distinguished, no number is
    requested, nothing is cut or bounded. Band 0's clauses — "Began designing from the prompt
    as given", "never bounded the problem" — all fit. I scored 1 only because "I would track
    p99 time-to-first-token and inter-token latency as separate series" is an NFR-shaped
    statement and is, by accident, the right instinct for this scenario. Note the structural
    problem: the relevance gate clamps to <= 1 and therefore cannot distinguish "answered a
    different question well" from "no requirements behaviour at all", while the level mapping
    treats any 0 as below-senior and tolerates up to two 1s. The gate's output lands on the
    wrong side of a cliff by the grader's discretion. See B5 defect 1.
```

```
Answer 4 / capacity_cost_estimation: 1
  cell clause applied: band 1 — "Used a number that contradicts a constraint stated in the
    prompt" AND "Computed something irrelevant (storage for a latency-bound problem)".
  evidence: "across four H100s at 3.35 terabytes per second that is roughly 13 terabytes per
    second aggregate, so one decode step floors near 10 milliseconds"
  admits another reading: yes — band 3, absent the relevance gate, and that is the point of
    this answer. Clause by clause it passes band 2 (derived 140 GB, 13.4 TB/s, ~10 ms — none
    of which appear in the prompt; arithmetic correct: 70e9 x 2 B = 140 GB, 4 x 3.35 = 13.4
    TB/s, 140/13,400 = 10.4 ms) and it supplies a textbook `band3_consequence` quote ("so I
    would size the admission window at 20 to 25 milliseconds against the budget, rather than
    picking a batch size"). Two independent things make it band 1 even before relevance: the
    prompt states **eight nodes of eight H100s**, so the correct aggregate is 8 x 3.35 = 26.8
    TB/s and the floor is ~5.2 ms, not 10 ms; and a decode-step floor is an inter-token
    latency, not a TTFT, so it is the wrong quantity for a TTFT problem. The quantity this
    prompt demands is KV per token x 100,000 (~32 GB for one request) or the 100k prefill
    time, neither of which appears. "the budget" is referenced but no budget is stated in
    this prompt — it is imported from elsewhere.
```

## Answer 5 (`A09`)

```
Answer 5 / capacity_cost_estimation: 1
  cell clause applied: band 1 — "Gave a number with no derivation" (the 55-cent figure, which
    is the number that answers the question). Band 2's first clause, "Derived the binding
    quantity from assumptions stated out loud", fails: the load-bearing assumptions are never
    stated.
  evidence: "Against the dollar fifty ceiling that clears comfortably; I would expect to land
    somewhere near 55 cents. ... The ceiling only starts to bind if the 8B share drops below
    roughly 20 percent, so that is the number I would watch."
  admits another reading: yes — band 2, and I expect most reviewers and most graders to say 2
    or 3. The arithmetic that is shown is correct (0.7 x 0.1 + 0.3 x 1 = 0.37; 0.5 x 0.1 +
    0.5 x 1 = 0.55; 70/8 = 8.75 ~ "an order of magnitude"; 400/70 = 5.7 ~ "five to six
    times"). The defect is in the arithmetic that is not shown, and in one claim that
    contradicts the rest:
      - "0.37 of all-70B" is compared to a dollar ceiling without ever stating the all-70B
        $/M. Working backwards from "near 55 cents" implies a baseline of $1.49/M — i.e. the
        baseline was silently set equal to the ceiling. Appendix B's own derivation gives
        $0.37/M of raw compute for the 70B, which would make the blended figure $0.14/M.
      - The 400B is assigned zero share without saying so, in a scenario that states three
        models in production. That is the assumption the answer is most sensitive to.
      - "binds below roughly 20 percent 8B share" is false on the answer's own numbers. With
        no 400B traffic the blended ratio is 1 - 0.9s; at s = 0.2 that is 0.82 x 1.49 =
        $1.22/M, and even at s = 0 it is $1.49/M — under the ceiling at every split. Routing
        away from the 8B cannot breach the ceiling. The ceiling actually binds on the 400B
        share: 0.37 + 4.7y >= 1.007 gives y ~ 13.5%. The candidate watched the wrong number.
    I score 1 because the one sensitivity claim they volunteered is wrong and the decisive
    assumption is invisible. Critically, the rubric gives me no clean clause for this: band 1
    covers "off by >100x" and "contradicts a constraint stated in the prompt", but there is
    no clause anywhere on this axis for numbers that contradict each other. See B5 defect 1.
```

```
Answer 5 / high_level_design: 0
  cell clause applied: band 0 — "No end-to-end path. ... Could not say what happens to a
    single request from arrival to response."
  evidence: "If 70 percent goes to the 8B, blended cost is 0.7 times a tenth plus 0.3 times
    one, which is 0.37"
  admits another reading: yes — band 1, if a grader reads "if 70 percent goes to the 8B" as a
    routing design. I do not: there is no router, no classifier, no confidence threshold, no
    cascade, no escalation path, no fallback, no placement of anything on the A100s or the
    H100s, and no answer at all to the second half of the question ("what do you measure to
    know you have not quietly made the product worse" — the answer measures cost share, not
    quality). This is a cost model with a routing split as an input, not a design. Band 1
    requires a design that fails; there is no design. The grader prompt's rule "Do not reward
    being right about policy while producing no design" points the same way.
```

## Hardest cell to apply

**`capacity_cost_estimation`, band 2.** Not the 2/3 boundary — that one was mechanical in all
five answers, because the bolded required clause reduces it to a yes/no with a quote attached.

Band 2 lists three behaviours — derive the binding quantity from assumptions stated out loud;
arithmetic within ~2–3x; name which constraint binds and show the others have slack — and the
rubric never says whether they are conjunctive. Band 3 goes out of its way to declare exactly
one required clause and demote the rest to indicators; band 2 gets no such rule, so the
reader has to invent one. It decided three of my ten cells:

| Answer | derives? | arithmetic OK? | names what binds? | any-of | all-of |
| --- | --- | --- | --- | --- | --- |
| 2 (HNSW) | yes | yes | no | 2 | 1 |
| 3 (IVF-PQ) | yes | yes | yes | 2 | 2 |
| 5 (routing) | partly | shown parts yes, unshown parts no | wrong one | 2 | 1 |

I applied all-of, because the axis definition's own one-line summary ends "and identifies the
binding constraint", which reads as a requirement rather than a bonus. A reviewer who applies
any-of scores Answers 2 and 5 one band higher than I did. That is two of five answers moving
on an unstated convention, which will show up as 1-vs-2 disagreement, not 2-vs-3 — and
`calibration-plan.md` targets exact agreement >= 50% per axis, so this alone could sink it.

---

# PART B — CRITIQUE

## B1. Axis legitimacy

**Directly: five of the six are axes I recognise from scorecards I have written. The sixth,
`capacity_cost_estimation`, is legitimate *in this domain* and I would not defend it as a
general system-design axis.** My one substantive objection is that in constrained-hardware
work `capacity_cost_estimation` and `tradeoff_articulation` are not independent measurements:
the number *is* the trade-off argument. When the memory budget is fixed, "what do you give up"
and "what does it cost" are the same sentence. The blind set shows the coupling empirically —
in Answers 1, 2 and 5 the two axis scores moved together, for one underlying reason each time.
Six axes therefore gives roughly five axes' worth of information and prices numeracy twice,
which inflates the profile of a numerate-but-inarticulate candidate and deflates the reverse.

**What my answer rests on.** Running a hardware-adjacent design loop, and writing scorecards
in a format with named dimensions. That is real experience of *the category*, not of this
pack's six labels, and it is experience of one domain's loop — not of a hosted-API or
multi-tenant loop, where my instincts are weak by my own account.

**What would change my mind:** 30 real scorecards in which numeracy and trade-off scores
decorrelate (Spearman well under ~0.6). If they decorrelate, the two axes measure different
things and I am wrong. If they do not, collapse them and spend the sixth slot on something the
pack currently cannot see.

Credit where due: the pack does not over-claim here. Departure note 2 in `rubric.md` admits six
was chosen because "a six-mark scorecard is readable as a share artifact and a three-mark one
is not — a product constraint, honestly a product constraint, not a claim about how real loops
score". That is the right disclosure and it is rarer than it should be. Treat my B1 as a
hypothesis for a human, per `review-harness/README.md`'s own warning about exactly this
section.

One coverage check I expected to fail and did not: I went looking for a missing axis on
"knowing what you would have to measure before committing", which is the first thing I score
in my own loop. It is already inside `deep_dive_failure_modes` band 3 ("said what signal would
tell them it is failing in production") and `capacity_cost_estimation` band 3 ("Stated
assumptions as assumptions and flagged which one the answer is most sensitive to"). No gap.

## B2. Scenario realism — `inference_serving` only

### `batch-window-vs-ttft-budget` — realistic-but-wrong-in-one-detail

The failure mode is real and is the right one to teach: static batching makes both utilisation
and tail latency bad simultaneously, and "raise the batch size" is genuinely what people reach
for. The `bad` answer's second form ("autoscale the replicas") is also real.

**The single thing most wrong: the prompt does not state prompt length, arrival rate, or
concurrency, and TTFT is dominated by prefill, which is a function of prompt length.** The item
is posed as a capacity question and scored on `capacity_cost_estimation`, but the input that
determines the answer is absent. Using the pack's own Appendix B numbers (4 H100s, ~1.6 PFLOPS
achieved), a 2,000-token prefill is 2 x 70e9 x 2,000 = 280 TFLOP = ~175 ms — 44% of the whole
400 ms budget for one request. A fixed batch of 32 such prompts is 8.96 PFLOP = ~5.6 s of
prefill, which does not reproduce the stated 1.2 s p99 at all. So the stated numbers either
imply much shorter prompts than any realistic LLM workload, or they do not co-occur. A
candidate who does the arithmetic properly discovers the scenario is underdetermined; a
candidate who recites the decode-step floor sails through. That inverts the signal the item
exists to measure, which is precisely the failure my brief tells me to look for ("a scenario
whose numbers cannot co-occur teaches the candidate to stop checking").

Fix: state a prompt-length distribution (e.g. "prompts average 800 tokens") and an arrival
rate. Then the item becomes answerable and the `good` answer's "sizes the batch *window*
against the 400ms budget" has something to be sized against.

Second, smaller: the `model_answer`'s headline derivation is a **decode** step floor used to
size a **TTFT** budget. These are different budgets — the pack knows this, it says so two
paragraphs later in Appendix B and the model answer ends by splitting the two series. Sizing
the admission window at ~2 decode steps is a defensible heuristic (admit on a step boundary),
but it is not the number that explains a 1.2 s p99 and it does not demonstrate that 400 ms is
reachable. As written, the item's gold answer teaches the judge to accept an ITL derivation as
a TTFT argument — and blind Answer 4 is that teaching coming back around.

### `kv-cache-admission-control` — realistic

The best item of the three and the one I would keep unchanged in framing. Two request classes
with a 95/5 split, long-context work destroying short-traffic tail latency at peak, and a
prompt that refuses to let the candidate design before naming what is protected — that is how
the problem actually arrives, and "two SLOs, not one blended p99" is the right thing to be
testing. The `bad` answer (LRU vs LFU) is the wrong turn people really take.

**The single thing most wrong is in the `model_answer`, not the prompt: "against 80 gigabytes
of HBM per card, most of which is already holding weights" is false for the stated topology.**
On a node of eight H100s with the 70B sharded TP=8, weights are 140/8 = 17.5 GB per card —
22% of the card, not "most" — leaving ~62 GB/card, so ~500 GB of free HBM per node. The
conclusion (admission control, not eviction; partition capacity by class) is still correct, but
it is correct for a different reason than the one given: 500 GB per node holds roughly fifteen
32 GB long requests, so the problem is not that 32 GB is unavailable, it is that admitting long
requests consumes the KV budget and the prefill queue that the 95% depend on. The model answer
teaching the judge is arguing a capacity impossibility where the real mechanism is contention.
"No replacement policy recovers 32 gigabytes" overstates in the same direction.

Also: the prompt says the long requests "push the short ones out of cache", which conflates two
different mechanisms — eviction of reusable prefix-cache blocks, and preemption/recompute of
in-flight sequence KV. The remedy differs between them, and the `bad` answer's blanket dismissal
of replacement policy is too confident if the mechanism is prefix-cache eviction, where
protecting a shared system-prompt prefix is a legitimate partial answer. Say which one it is.

### `heterogeneous-fleet-routing` — not realistic as a capacity item

The routing problem and the measurement half are real and well-chosen — "a 70 percent-correct
router can hold average quality flat while destroying one segment" is the genuinely
discriminating insight and the `bad` answer (route on prompt length, measure aggregate quality)
is the real failure. I would keep the item and rewrite the numbers.

**The single thing most wrong: the designed answer is not derivable from the stated inputs.**
The `model_answer` concludes "blended cost falls to roughly ... about 37 percent of serving
everything on the 70B. That tells me the dollar fifty ceiling is reachable, with room to
spare." 37% of what? No all-70B $/M baseline is given anywhere in the prompt or the answer, so
a ratio is being compared to a dollar figure. Both endpoints are defensible and they give
opposite verdicts:

- Appendix B's own 70B raw-compute figure, $0.37/M => blended $0.14/M, and the $1.50 ceiling
  clears by 10x. The scenario is trivial and finance's constraint is decorative.
- A plausible all-in figure of ~$4/M (utilisation losses, redundancy, prefill, replicas,
  margin) => blended $1.48/M, exactly at the ceiling. The scenario is knife-edge.

A candidate cannot tell which world they are in, and the item is scored on
`capacity_cost_estimation`. Fix: state the current blended cost ("you are at $2.10 per million
today").

Two more, both load-bearing:

1. **The stated A100/H100 heterogeneity is never used.** It is in the prompt and in the item's
   name, and it appears in neither `good` nor `model_answer` nor any followup. It is not a
   cosmetic omission: the A100 (80 GB, 2.0 TB/s) decodes roughly 1.7x slower per step than an
   H100 but rents for roughly half as much, so $/token on the two parts is close enough that
   *which model goes on which silicon* is the real design question — and the 8B fits one card
   with no tensor-parallel communication while the 400B (800 GB in bf16) needs ten or more
   H100s and crosses a node boundary. Either engage the heterogeneity or remove it from the
   prompt; leaving it stated-but-unscored teaches candidates that stated constraints are
   decoration.
2. **The 400B's share is never modelled** in `good` or `model_answer`, in a scenario that
   states three models in production. As shown in Part A, the ceiling binds on the 400B share
   (~13.5% on the answer's own ratios), not on the 8B share. The item's gold answer silently
   sets the expensive model's traffic to zero — the same unstated assumption blind Answer 5
   makes, which means the item cannot discriminate against it.

### `vector-index-at-10b` — realistic (reviewed because I scored it twice)

Numbers all check out (B3). Framing is right: memory eliminates the option space before
anything else, and the `bad` answer (HNSW on benchmark reputation) is the defensible-looking
real mistake. One gap: the `model_answer`'s rerank step — "rerank them against full-precision
vectors fetched from disk or a cache" — is where the stated p99 actually lives, and its cost is
never stated. A few hundred random 4 KB reads against 40 TB of NVMe is ~1–3 ms at high queue
depth but has a p99 tail of 1–10 ms per read under load; inside a 50 ms p99 budget that is
fine on average and is the most likely source of a tail violation. An at-bar answer should be
expected to say so, and the cell for it (`capacity_cost_estimation` band 3, "flagged which
assumption the answer is most sensitive to") already exists.

## B3. Arithmetic

Checked every derivation in Appendix B and in the four items I read. **Three are wrong, all in
the same direction: they understate long-context cost and overstate achievable efficiency.**

### Wrong 1 — prefill at long context is understated ~1.9x

`rubric.md` Appendix B: "Prefill ≈ `2 × params × prompt_tokens` FLOPs ... a 10k-token prompt on
70B = 1.4 PFLOP ... that is **~0.9 seconds**, and a 100k-token prompt is ~9 seconds."

The formula counts only the weight-multiply term and drops attention, which is quadratic in
sequence length. Using the pack's own 70B parameters (80 layers, head_dim 128, 64 query heads
=> hidden 8,192 — the same config its KV formula assumes), with causal masking:

- attention FLOPs ≈ `2 × layers × hidden × seq²` = 2 x 80 x 8,192 x (1e5)² = **13.1 PFLOP**
- linear term = 2 x 70e9 x 1e5 = **14 PFLOP**
- total ≈ **27.1 PFLOP** / 1.584 PFLOPS = **~17 seconds**, not ~9.

The crossover where attention equals the linear term is `seq = params / (layers × hidden)` =
70e9 / 655,360 ≈ **107,000 tokens**. So the rule is fine at 10k (1.5 PFLOP, ~0.95 s — the
stated 0.9 s is right) and is off by ~1.9x at 100k. That is the regime scenario
`kv-cache-admission-control` is entirely built on, and the error runs in the direction that
makes long-context contention look less severe than it is.

Fix: state the formula as `2 × params × tokens + 2 × layers × hidden × tokens²`, note the
crossover, and correct the 100k figure to ~17 s.

### Wrong 2 — "a fifth of a node's HBM" is off ~4x

`rubric.md` Appendix B: "100k tokens of context ≈ 32GB of KV for one request — comparable to a
fifth of a node's HBM".

32.77 GB / 640 GB (8 x 80 GB, the node the pack's own `kv-cache-admission-control` prompt
states) = **5.1%**. A fifth would be 160 GB, i.e. two cards, which is not a node under any
convention and contradicts both scenarios (4-GPU replicas in A01, 8-GPU nodes in A08). Fix:
"about 5% of an eight-card node's HBM, and about 40% of a single card's" — the per-card framing
is the one that carries the intuition anyway.

### Wrong 3 — the decode floor omits KV reads, and the whole $/token chain inherits it

`rubric.md` Appendix B: "a step floors at ≈ 140/13,400 s ≈ **10ms** ... Batch 64 therefore
yields ~6,000 tok/s aggregate off the same weight read ... the inter-token latency a user sees
is nearly flat in batch size until compute saturates."

A decode step reads the weights **once** and the KV cache **once per sequence**. At batch 64
with 2,000-token contexts, using the appendix's own 320 KB/token: 64 x 2,000 x 320 KB = **41
GB** of KV on top of 140 GB of weights.

- step = (140 + 41) / 13,400 = **13.5 ms**, not 10 ms
- tok/s = 64 / 0.0135 = **4,740**, not ~6,000
- $/M = $0.00222/s / 4,740 tok/s x 1e6 = **$0.47/M**, not $0.37/M

At the 8,000-token contexts a hosted API actually sees, KV is 168 GB — larger than the weights
— the step is **23 ms**, and the claim that ITL is "nearly flat in batch size" fails well before
compute saturates. Add realistic achieved bandwidth (70–80% of peak for a decode step, not
100%) and the raw floor is ~$0.62/M. So the quoted $0.37/M is optimistic by **1.3–1.7x** before
any of the caveats the appendix already lists.

Two consequences: `heterogeneous-fleet-routing`'s cost model rests on this chain, and the
appendix's "nearly flat in batch size" is the sentence a candidate will repeat in an interview
where the interviewer knows it is only true at short context. Fix: write the floor as
`(weight_bytes + batch × context × kv_per_token) / aggregate_bandwidth`, state an achieved-
bandwidth fraction, and bound "nearly flat" by the context length where KV bytes reach weight
bytes (here: batch x context ≈ 427,000 token-slots).

### Checked and correct — do not change these

| Derivation | Verified |
| --- | --- |
| KV/token, 70B: `2 × 80 × 8 × 128 × 2 B` = 327,680 B ≈ 320 KB | correct, and the GQA parameters are coherent — 80 layers / 8 KV heads / head_dim 128 is a real 70B-class config, not an invented one |
| KV/token, 8B: 32 layers, 8 KV heads, 128, bf16 = 131,072 B = 128 KB | correct and coherent |
| 100k context => 32 GB KV for one request | correct (32.77 GB) |
| 70B bf16 = 140 GB; 4 x 3.35 = 13.4 TB/s; 140/13,400 = 10.4 ms | correct **as a weights-only, batch-1, zero-communication floor** — see Wrong 3 |
| 10k prefill = 1.4 PFLOP; 4 x 990 TFLOPS x 40% = 1.584 PFLOPS; = 0.88 s | correct; 40% MFU is a reasonable-to-conservative prefill assumption |
| H100 dense BF16 ~990 TFLOPS | correct (989.4) |
| $2/GPU-hr x 4 = $8/hr = $0.00222/s | correct |
| Vector item: 4 KB/vector; 40.96 TB raw; 64 B/vector => 640 GB; ~10 machines; 2% churn | all correct |

### Two things I could not verify

- **The NVIDIA $0.09/M reference** ("120B open model at 66 tokens/sec/user", third-party,
  April 2026). I cannot check it, and the appendix presents it as a "useful independent
  reference point" next to its own $0.37/M for a *smaller* model without reconciling the 4x
  gap. A reader concludes one of the two is wrong. The likely reconciliation is FP8/FP4 weights
  plus much larger batch, which is exactly the thing a candidate should be made to notice.
  Either reconcile it in one sentence or drop it.
- **$2/GPU-hour.** The appendix already flags this as "a market-rate assumption that must be
  re-verified, not a cited figure". Correct handling; I have no better number to offer.

### On the sparsity TFLOPS question (my brief asks)

**Yes, it is a trap for the reader as currently written.** Appendix B leads with the vendor
page's sparsity figures — "BF16 1,979 TFLOPS; FP8 3,958 TFLOPS" — and the dense correction
arrives in a subordinate clause. A reader retains the bold number, not the caveat, and 1,979
BF16 TFLOPS is unachievable on any dense transformer. The appendix's own derivations then
correctly use ~990. Fix: state dense first and relegate the sparsity figures to a parenthetical
("the vendor page's headline figures are 2x these, quoted with structured sparsity, and are not
reachable on a dense model"). Cheap fix, and this appendix is read by candidates who will quote
it at a panel.

## B4. The band 2/3 boundary

**In roughly the right place, but it is not the boundary that will break this instrument, and
it is one clause short of safe.**

Where it is right: the "band 3 has ONE required clause" correction is the single best decision
in the rubric. It made the 2/3 call mechanical in all ten cells I scored — did a number the
candidate produced change a stated decision, yes or no, with a quote. The conjunctive version
would have been unapplicable in a 60-second answer, and the pack found that itself by
dry-running its own gold answers, which is the right way to find it.

Where it is wrong: **band 3 does not require the behaviour to have been performed
*correctly*.** The required clause is that the result changed a design decision, and a
confidently wrong derivation satisfies it as cleanly as a right one. Blind Answer 4 is the
proof — it hands the grader a perfect `band3_consequence` quote ("so I would size the admission
window at 20 to 25 milliseconds ... rather than picking a batch size") on top of a derivation
that uses four H100s where the prompt says eight-per-node and computes an ITL for a TTFT
problem. The only thing standing between that answer and a 3 is the relevance gate, and the
relevance gate is lexical (B5 defect 1). Band 2 requires "arithmetic within ~2–3x"; band 3
says "All of band 2" and so inherits it, but nothing anywhere requires the *configuration* to
match the prompt or the numbers to be mutually consistent.

Too harsh or too generous: **too generous, in one specific way** — it rewards the form of
numeric reasoning over its soundness, which is the exact failure mode my corner of this field
exists to prevent. A fluent wrong derivation that drives a decision outscores a correct
derivation that does not. In a domain where you cannot autoscale out of a bad estimate, that
ranking is backwards.

Where the real breakage is: **the 0/1 and 1/2 boundaries on `capacity_cost_estimation`.** Three
independent reasons, all demonstrated in Part A:

1. Band 2's three clauses have no declared conjunction rule while band 3 declares one — moves
   two of five answers by a whole band (see "hardest cell").
2. Band 0 and the axis's hard cap disagree about what a "quantity" is. The cap says "of their
   own" and names prompt-echoing as not counting; band 0 says "no quantity of any kind". A
   candidate who echoes and derives nothing is simultaneously 0 and 1 (Answer 1).
3. The relevance gate's "<= 1" collapses 0 and 1 for every off-problem answer (Answer 4),
   and the level mapping puts a cliff between them: any axis at 0 => below the senior bar,
   while two axes at 1 is still at-bar. The verdict therefore turns on a distinction the gate
   explicitly refuses to make.

If the agreement study finds disagreement, my prediction is it concentrates at 1-vs-2 on
`capacity_cost_estimation`, not at 2-vs-3. `calibration-plan.md` is set up to see this — it
reports per-axis and refuses a single aggregate number, which is correct — but
`rubric.md`'s "What needs a practitioner's review" list names the 2/3 boundary as "the whole
instrument" and does not mention 1/2 at all. That prioritisation is wrong.

## B5. Top 3 defects, ranked

### 1. Band 3 is reachable by arithmetic that is wrong, and nothing penalises self-contradiction

**File:** `rubric.md` axis 2 bands 1–3 (the `capacity_cost_estimation` table) and the relevance
gate section; `prompts.md` STEP 1 and the code-enforced validation table.

**What is wrong.** Three gaps compound:

- Band 1 catches numbers that are "off by >100x" or that "contradict a constraint stated in the
  prompt". It has **no clause for numbers that contradict each other.** Blind Answer 5 walks
  straight through: every shown calculation is right, the baseline is invisible, and the one
  volunteered sensitivity claim ("the ceiling binds below ~20% 8B share") is false on its own
  numbers. The grader is given no cell to put that in, so it lands on 2.
- Band 3 requires only that the result changed a decision. Nothing requires the derivation to
  use the prompt's stated hardware. Blind Answer 4 derives a 10 ms floor from four H100s in a
  scenario that states eight per node, and supplies an ideal consequence quote.
- The only backstop is the relevance gate, which is enforced as **"reject if
  `prompt_constraint_engaged` is not a verbatim substring of the prompt"**
  (`prompts.md` validation table). That is a lexical test. For Answer 4 the grader can quote
  "p99 time-to-first-token on the short traffic triples" verbatim from the A08 prompt, set
  `addresses_prompt = true`, and the gate never fires — because the prompt happens to contain
  TTFT language and the answer happens to be about TTFT, while the actual mechanism (per-class
  KV capacity) is nowhere in the answer. The gate tests vocabulary overlap and is documented as
  testing "where the decision landed".

**Why it matters.** This is the top defect because it is the one that lets a flattering grade
through on the axis the pack is most exposed on, and because a candidate graded 3 for a wrong
derivation is actively harmed — they will repeat it at a panel where someone checks. The pack
is otherwise unusually well defended against flattery; this is the hole in it.

**What I would do.**
1. Add to band 1: *"Produced numbers that contradict each other, or quoted a cost or ratio whose
   baseline was never stated."*
2. Add to band 2 as a precondition, not a clause: *"the derivation uses the configuration stated
   in the prompt."* Band 3 inherits it via "All of band 2".
3. Replace the lexical relevance gate with a semantic one the item author writes: add
   `binding_mechanism` to each item in `questions.json` as an allowlist (A08:
   `{kv_capacity_per_class, admission_control, class_isolation}`), make the grader emit the
   mechanism its score rests on, and clamp when it is not in the set. Keep the verbatim-quote
   check as well; it catches a different failure. This stays code-enforceable, which is the
   property the pack rightly insists on.
4. Reconcile band 0's "no quantity of any kind" with the cap's "of their own" — say
   *"no quantity of their own, and no stated dependence on any quantity"* for band 0.

### 2. Appendix B's inference derivations are systematically optimistic in the long-context direction

**File:** `rubric.md` Appendix A/B boundary onwards — the prefill paragraph, the "fifth of a
node's HBM" clause, and the decode/tokens-per-second/$ chain.

**What is wrong.** Three errors, all quantified in B3, all pointing the same way: prefill at
100k understated ~1.9x (attention FLOPs dropped; ~17 s, not ~9 s), 32 GB of KV called "a fifth
of a node's HBM" when it is ~5% of the node the pack itself specifies, and a decode floor that
omits KV reads so that 10 ms / 6,000 tok/s / $0.37 per million should be ~13.5 ms / ~4,740 /
~$0.47 at 2,000-token context and worse at realistic context and achieved bandwidth.

**Why it matters.** Appendix B's own framing is the argument: "If any of these is wrong, the
model answer teaching the judge is wrong, which is worse than a missing number." These feed
`heterogeneous-fleet-routing`'s cost model and `kv-cache-admission-control`'s capacity argument
directly, and the errors are concentrated in long-context — the one regime the pack has built a
scenario around. It is second rather than first only because it is a straight correction with
no design implications, where defect 1 needs a mechanism change.

**What I would do.** Apply the three corrections in B3; add the achieved-bandwidth fraction and
the KV term to the floor formula so the two scenarios inherit a correct model; bound "nearly
flat in batch size" by the context length where KV bytes reach weight bytes; lead with dense
TFLOPS and demote the sparsity figures.

### 3. `heterogeneous-fleet-routing`'s designed answer is not derivable from its prompt

**File:** `questions.json`, item `heterogeneous-fleet-routing` (`prompt`, `good`,
`model_answer`).

**What is wrong.** The answer compares a ratio ("37 percent of serving everything on the 70B")
to a dollar ceiling with no baseline $/M stated anywhere, and the two plausible baselines give
opposite verdicts ($0.14/M, trivially clear; or $1.48/M, knife-edge). The 400B's share is
silently zero in a scenario that states three models in production, and the ceiling actually
binds on that share (~13.5%), not on the 8B's. The stated A100/H100 mix appears in no `good`,
`model_answer`, or followup.

**Why it matters.** It is one of four items carrying `capacity_cost_estimation` (25% of that
axis's coverage) and one of four carrying `high_level_design`, and as written it cannot
discriminate the exact failure blind Answer 5 commits — because the gold answer commits the
same omission. An item whose model answer shares the candidate's blind spot is worse than no
item: it trains the judge to accept it.

**What I would do.** State the current blended cost in the prompt. Model all three shares in
`good` and `model_answer`, and make the 400B-share threshold the band-3 "number to watch".
Either make the A100/H100 split a real part of the answer ($/token on the two parts is within
roughly 20%, so placement is a genuine decision, and the 8B fits one card while the 400B
crosses a node boundary) or cut it from the prompt. Add a followup: "what is the all-70B cost
per million today, and how do you know?"

**Runner-up, flagged because it is cheap to fix:** `batch-window-vs-ttft-budget` states no
prompt length or arrival rate, so its capacity question is underdetermined and its stated p99
is not reproducible from its own numbers (B2).

## B6. Sign-off

**What I would refuse to let ship as-is:**

1. **Appendix B of `rubric.md`.** It is the judge's teaching material and it is candidate-
   facing in effect; three of its inference derivations are wrong. One afternoon's work.
2. **`heterogeneous-fleet-routing` as a `capacity_cost_estimation` item.** It can ship as a
   `high_level_design` / measurement item today. It cannot ship as a capacity item while its
   own answer's cost claim is underivable.
3. **The claim that the 2/3 boundary is "the whole instrument"** (`rubric.md`, "What needs a
   practitioner's review", item 1) — without the 1/2 and 0/1 boundaries on
   `capacity_cost_estimation` added to that list. Calibrating the wrong boundary first wastes
   the practitioner hours `calibration-plan.md` budgets.

**Would I put my name on this rubric as legitimate? Not the file as it stands — yes to the
instrument inside it.**

The six axes, the four bands, the band-3 required-clause rule, the derived-quantity cap, the
relevance gate's intent, the `assessed: false` mechanism, the insistence that caps live in code
and not in a prompt, and the explicit "where this rubric departs from its sources" section: I
would sign all of that, and the honesty of the departure notes and the "what needs a
practitioner's review" list is better than most internal rubrics I have worked from. What I
will not sign is Appendix B, which is part of `rubric.md`, and which currently teaches three
wrong numbers in the regime the pack cares most about. Fix the arithmetic and add a correctness
precondition to band 2, and the answer is yes without qualification.

**Caveat on my own sign-off:** it covers the rubric's structure and its arithmetic, which I can
check. It does not cover whether a real loop scores these six things — see B7.

## B7. Epistemic status

### Checkable facts — verify with a calculator and the pack's own stated parameters, no domain access needed

- All three Appendix B errors (B3): the 100k prefill understatement (~17 s vs ~9 s), "a fifth of
  a node's HBM" (5.1%, not 20%), the decode floor's missing KV term (13.5 ms vs 10 ms at
  batch 64 x 2,000 tokens, and the $0.47 vs $0.37 per million that follows). Each is one line
  of arithmetic from numbers the pack itself states.
- Blind Answer 5's internal contradiction: "the ceiling binds below ~20% 8B share" is false
  against the same answer's "0.37 of baseline = 55 cents". Under their own numbers the ceiling
  is never breached by any 8B/70B split.
- Blind Answer 4 uses four H100s where its prompt states eight per node.
- `kv-cache-admission-control`'s "most of which is already holding weights": 17.5 GB of 80 GB
  under TP=8, i.e. 22%.
- `heterogeneous-fleet-routing` states an A100/H100 mix that appears in none of its `good`,
  `model_answer`, or `followups`; and states three models while its answer models two.
- Band 2 of `capacity_cost_estimation` declares no conjunction rule where band 3 declares one.
- The relevance gate is enforced as a verbatim-substring check (`prompts.md` validation table).
- The KV formulas, the GQA parameters, the vector-index sizing, the 10k prefill figure, the
  dense TFLOPS figure and the $/GPU-hour conversion are all correct. I checked them all; the
  pack's arithmetic is right more often than it is wrong.

### Domain judgement — practitioners in constrained/served inference would mostly share

- KV reads belong in any decode bandwidth model, and "ITL is nearly flat in batch size" holds
  only while batch x context keeps KV bytes below weight bytes. High confidence.
- Attention FLOPs cannot be dropped from a prefill estimate above a few tens of thousands of
  tokens. High confidence; the crossover I derived (~107k for this config) is arithmetic, the
  judgement is that it matters.
- Achieved decode bandwidth is 70–80% of peak, not 100%, and TP adds per-layer all-reduces
  (order 1–2 ms per token at TP=4 and small batch, latency- not bandwidth-dominated). Confident
  on the shape; the exact fraction is kernel- and shape-dependent and I did not model this
  pack's specific case, so treat my $0.62/M as an illustration, not a number to publish.
- HNSW holding full-precision vectors at 10B is not viable, and it degrades under high delete
  churn. High confidence; this is also what the item's own `bad` answer says.
- A100 vs H100 $/output-token is close enough that placement is a real decision rather than a
  foregone one. Medium confidence — it depends on rental pricing I have not re-verified, and
  pricing moves.
- TTFT is prefill-dominated and a decode-step floor is the wrong quantity to size a TTFT budget
  with. High confidence.

### Guesses about interview practice — a human must confirm these

- **All of B1.** Whether a real loop scores these six axes, and specifically whether
  `capacity_cost_estimation` and `tradeoff_articulation` are separable in this domain or whether
  the pack is pricing numeracy twice. I have run a hardware-adjacent loop and I have written
  scorecards with named dimensions; I have not operated *this* taxonomy, and
  `review-harness/README.md` is right that a persona prompt will assert an answer here
  confidently regardless. My Spearman-under-0.6 falsification test is the usable part; the
  opinion is not.
- Whether band 3's "the result changed the design" is what interviewers actually reward, or
  whether they reward something adjacent and harder to score — the candidate noticing that the
  number they need is unobtainable and saying what they would measure first. In my experience of
  the category that second behaviour is the stronger staff signal, and this rubric scores it
  only as an unbolded indicator. I believe this fairly strongly and I cannot evidence it.
- Whether two axes can be scored fairly from a 60-second voice answer at all. Blind Answer 5
  scored 0 on `high_level_design` from me because it answered the cost half of a two-part prompt
  and not the design half — and under the level mapping any axis at 0 sends the verdict below
  the senior bar. Whether that is a correct read of the candidate or an artefact of a 60-second
  budget is not something I can tell from the pack. Worth a human's attention before the level
  claim ships, since it is the share artifact.
- Whether band 1 reads as diagnostic or insulting. I did not evaluate this; I am the wrong
  reviewer for it and my brief does not cover it.

### My own blind spots, as my brief requires me to state

- **I have not run a multi-tenant hosted API.** I reviewed none of
  `multi-tenant-token-limiter-placement`, `gpu-credit-ledger-consistency`, or the quota and
  noisy-neighbour material, and my instincts about abuse, quota and fairness are weaker than
  they feel from inside. My B2 verdict on `heterogeneous-fleet-routing` is confident about its
  cost half and should be discounted on its measurement half (per-segment quality, shadow
  traffic, escalation rate) — that part reads right to me, but I am not the reviewer who knows.
- **I over-weight arithmetic relative to communication.** Concretely: I scored blind Answer 1 a
  2 rather than a 3 on `tradeoff_articulation` and flagged that it admits 1, and the thing I
  penalised — "tune the window empirically, watch the p99, and iterate" — is how a competent
  engineer actually talks about an unknown. A communication-weighted reviewer may well score
  that answer higher than I did, and if the panel splits on Answer 1, I am the likely outlier
  and the rubric cell is probably fine.
- I own Appendix B in this review, which means I went looking for errors there and found three.
  The base rate of my finding errors in a section I was told to audit is not evidence that the
  rest of the pack is clean. I spot-checked the vector item and it was correct.

### What I had to assume because the pack does not say

| Assumption | Why I needed it | Risk if wrong |
| --- | --- | --- |
| Hidden size 8,192 and 80 layers for the 70B | the attention-FLOPs correction and the TP all-reduce estimate | low — taken from the pack's own KV parameters (80 layers, head_dim 128, 64 q heads), so it is internally consistent by construction |
| Tensor parallelism = GPUs per replica/node (TP=4 in A01, TP=8 in A08) | per-card weight footprint, aggregate bandwidth, the "most of which is already holding weights" check | **medium — this is the most load-bearing unstated input in the pack.** Under TP=2 with pipeline stages, my A08 finding softens considerably. The items should state the parallelism strategy |
| "Cache" in `kv-cache-admission-control` means in-flight sequence KV, not reusable prefix cache | whether "no replacement policy recovers 32 GB" holds, and whether the `bad` answer's dismissal of LRU/LFU is fair | **medium — the right answer differs between the two mechanisms.** The prompt should say which |
| 2,000- and 8,000-token contexts for the batch-64 KV illustration | the decode-floor correction | low for the shape, high for the specific numbers — the pack states no context length for its own batch-64 example, which is part of the defect |
| "Cost" in `heterogeneous-fleet-routing` means marginal serving cost, not list price | the baseline critique | low — the item's own `bad` answer names list-price pricing as a failure, so this reading is the intended one |
| Decode-time achieved bandwidth of 70–80% of peak | the $/M range | medium — kernel- and shape-dependent; illustrative only |

### Disclosure: the blind set is partially de-blinded, and not by my choice

I did not open `calibration-plants.json`, `dry-run-report.md`, or `findings/`, and I saw no
expected scores. But I could infer plant *structure* from files I was told to read, which
probably affected my Answer 4 scoring and may affect everyone's:

- `rubric.md`'s relevance-gate section says "Added because a plant exposed this" and names
  "plant 08b is the control". `prompts.md` says the same. The blind set labels its fourth answer
  `A08`. So I knew before reading it that A08 is the relevance-gate test and that the gate
  is expected to fire — which is exactly the judgement the blind set is measuring.
- Answers 2 and 3 are both labelled `A03` with the same prompt. A matched pair is a visible
  signal that one is the strong version and one the weak, which anchors the comparison between
  them instead of scoring each on its own.
- The session's own git log, which the harness put in my context unprompted, contains
  "Plants: split 03 into 03a/03b, add 08b negative control".

**Fix before the next run:** give the blind set opaque IDs with no relationship to the plant
file, do not place two answers to the same prompt adjacent (or at all, in one run), and move
`rubric.md`'s plant commentary into a file reviewers are not asked to read. My A08 scores should
be treated as the least independent thing in this report.
