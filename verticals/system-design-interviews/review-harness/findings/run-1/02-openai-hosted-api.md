# REVIEWER 2 — hosted multi-tenant LLM API

Domain: request path, multi-tenancy, quota, streaming, retry semantics. Nine years in
large-scale request-path engineering, four on a paid multi-tenant LLM API.

Scenarios owned: `multi-tenant-token-limiter-placement`, `gpu-credit-ledger-consistency`,
`streaming-delivery-and-deploys`, `agent-retry-side-effects`.

**Contamination disclosure, read this first.** While grepping `calibration-plan.md` for the
agreement statistics (Part B material), line 122 of that file came back in the match list
and it contains an expected score for a plant: a row labelled "Number right, link unstated"
asserting `capacity_cost_estimation == 2` exactly. That description matches Answer 3 of the
blind set. My Part A score for that cell was already fixed at 2 before the grep, with the
post-hoc-ordering reasoning that appears below, but I cannot prove the ordering to you, so
treat Answer 3 / `capacity_cost_estimation` as **contaminated and excluded from the
inter-rater measurement**. My other nine cells are clean. I did not open
`calibration-plants.json`, `dry-run-report.md`, or anything in `findings/`.

Operational note for whoever re-runs this harness: `calibration-plan.md` is listed as
optional Part B reading but contains per-plant expected scores. Either strip them into a
separate file or move the file onto the do-not-read list.

---

# PART A — BLIND SCORING

## Answer 1 (`A01`)

```
Answer 1 / capacity_cost_estimation: 1
  cell clause applied: "Gave a number with no derivation ... Recited a spec figure
    without using it in an arithmetic step."
  evidence: "Given our 400 millisecond target I would bias toward latency. Then I would
    tune the window empirically, watch the p99, and iterate until both numbers look
    healthy."
  admits another reading: yes — band 0, on the clause "Chose between two options whose
    only real difference is a number, without computing either." Static vs continuous
    batching differ in exactly one number (the admission window) and he computes nothing,
    explicitly deferring it to empiricism. I scored 1 rather than 0 because band 0 says
    "No quantity of any kind" and a quantity does appear — the 400ms — and it is used
    directionally to pick a side, which is more than nothing. But the only quantity in the
    answer is the prompt's own, so the hard cap bites and 1 is the ceiling regardless. The
    0/1 line here rests entirely on whether an echoed number counts as "a quantity", and
    the rubric says one thing in the band-0 cell and the opposite in the cap. That is a
    defect, see B5.
```

```
Answer 1 / tradeoff_articulation: 2
  cell clause applied: "Named the axis of the trade-off in units — latency vs throughput
    ... stated which side of it this system should sit on and why, given the stated
    requirement, and acknowledged specifically what the choice gives up. Picked."
  evidence: "The trade-off is latency against throughput: a wider batch window buys you
    utilisation and spends time-to-first-token. Given our 400 millisecond target I would
    bias toward latency."
  admits another reading: yes — band 1, on "chose, but justified it with an unfalsifiable
    claim", or more precisely on the sources' named failure of not really deciding. "Bias
    toward latency" followed by "iterate until both numbers look healthy" is a soft
    commitment that reserves the right to want both, which is the thing the prompt's two
    simultaneously-bad numbers were constructed to deny him. I score 2 because the axis is
    named in units, the side is stated, and the cost (utilisation) is named — every band-2
    clause is literally satisfied. Band 3 is clearly not reached: no number of his own
    resolves the trade-off and no reversal condition is named.
```

## Answer 2 (`A03`, HNSW)

```
Answer 2 / capacity_cost_estimation: 1
  cell clause applied: "Derived the number that decides the question, then proposed a
    design it rules out (computed 40TB raw, then chose an index that needs all of it
    resident) — the number was produced but not understood."
  evidence: "10 billion vectors at 1,024 dimensions in float32 is 4 kilobytes per vector,
    so about 40 terabytes raw. ... Given the recall requirement I would use HNSW"
  admits another reading: no. This cell was written for this answer — the parenthetical in
    the band-1 cell is almost a transcript of it. The arithmetic is correct (1,024 × 4 B =
    4,096 B; 10e9 × 4 KB = 40 TB; 200M/10e9 = 2%) and derived rather than echoed, so the
    cap does not bind, but band 2 requires naming which constraint binds and he never
    does — the 40TB is computed and then abandoned. HNSW over uncompressed float32 at that
    scale also needs the graph resident on top of the vectors, so the real figure is worse
    than the one he computed and discarded.
```

```
Answer 2 / tradeoff_articulation: 1
  cell clause applied: "chose, but justified it with an unfalsifiable claim ... it's
    industry standard" — and failed band 2's "acknowledged specifically what the choice
    gives up."
  evidence: "I would use HNSW, because it has the best recall-latency curve of the ANN
    families — typically 0.95-plus recall at single-digit millisecond latency."
  admits another reading: yes — band 2, and this one is live. A reader can take
    "recall-latency curve" as naming the axis in units and "given the recall requirement"
    as picking the side, which satisfies two of the three band-2 clauses and defeats the
    `tradeoff_axis_named` cap. I score 1 because he states HNSW *dominates* on that axis
    rather than trading along it, and the prompt asked "tell me what the choice costs
    you" — the cost (memory, by a factor that makes the design impossible) is absent.
    But the cap's own gloss, "Listing advantages and disadvantages is not naming an axis",
    does not tell a grader what to do with a dominance claim stated in axis vocabulary.
    I expect reviewers to split on this cell.
```

## Answer 3 (`A03`, IVF-PQ) — CONTAMINATED, see disclosure

```
Answer 3 / capacity_cost_estimation: 2   [EXCLUDE FROM AGREEMENT MEASUREMENT]
  cell clause applied: "Named which constraint binds — memory capacity vs memory bandwidth
    vs compute vs network vs dollars — and showed why the others have slack."
  evidence: "about 40 terabytes raw, which makes memory the binding constraint here.
    Latency has slack — 50 milliseconds is generous for an approximate lookup — and 200
    million changes a day is about 2 percent, which is an ingest-volume question rather
    than a throughput one."
  admits another reading: yes — band 3, and the reading turns entirely on utterance order.
    Everything band 3 asks for is arguably present: memory binds, and IVF-PQ is the index
    you pick when memory binds. But he announces the index *first* and justifies it by
    convention — "it's what most billion-scale deployments run" — and the sizing arrives
    afterward. Under the band-3 rule as written ("performing the behaviour is band 2;
    letting the result of the behaviour alter the design is band 3") the number did not
    alter anything; it rationalised a choice already made on other grounds. He also never
    computes the PQ compression ratio, which is the quantity that would actually close the
    40TB gap. The rubric never states that ordering is the 2/3 discriminator, which is my
    main B4 finding.
```

```
Answer 3 / tradeoff_articulation: 1
  cell clause applied: "chose, but justified it with an unfalsifiable claim ('it's more
    scalable', 'it's industry standard')" — plus the hard cap: no trade-off axis named.
  evidence: "I'd go with IVF-PQ — it's what most billion-scale deployments run. ... and
    keep an eye on recall."
  admits another reading: yes — band 2. A reader can argue "memory binds, latency has
    slack" names the memory-vs-latency axis and picks a side. I score 1 because that is a
    binding-constraint statement, not a trade-off: he never says what PQ costs, and what
    PQ costs is recall — against a hard floor of 0.9 recall@10 stated in the prompt.
    "Keep an eye on recall" is the generic-monitoring move the rubric puts in band 1 on
    the deep-dive axis. The thing the prompt explicitly asked for ("tell me what the
    choice costs you") is the thing both A03 answers omit, in opposite directions.
```

## Answer 4 (`A08`)

```
Answer 4 / requirements_scoping: 1
  cell clause applied: Relevance gate — "A behaviour performed on the wrong problem scores
    at most band 1 on every axis, however well executed"; within band 1, "recited a generic
    checklist unconnected to this scenario."
  evidence: "The problem is that a fixed batch size makes time-to-first-token depend on
    batch fill rather than on compute."
  admits another reading: yes — band 0, on "never bounded the problem." The item asked two
    direct scoping questions — "what exactly are you protecting, and what is the first
    number you would want?" — and he answers neither. He never names the short-traffic
    tenant, never names the long-context share as the number he wants, never says anything
    is out of scope. I score 1 because the behaviour did appear in a recognisable form
    (he separates TTFT and ITL into distinct budgeted series, which is quantified-NFR
    work) and the gate's own wording — "at most band 1 ... however well executed" —
    implies that competent work on the wrong problem lands at 1 rather than 0. A grader
    reading the band-0 cell literally will say 0. Reviewers will split here, and the gate
    and the band-0 cell need reconciling.
```

```
Answer 4 / capacity_cost_estimation: 1
  cell clause applied: Relevance gate, plus band 1's "Used a number that contradicts a
    constraint stated in the prompt."
  evidence: "across four H100s at 3.35 terabytes per second that is roughly 13 terabytes
    per second aggregate"
  admits another reading: no. The arithmetic itself is right and matches Appendix B
    (140 GB / 13.4 TB/s ≈ 10 ms), and in isolation it would be a clean band 2 — but the
    prompt says "eight nodes of eight H100s" and he computes against TP=4, and the whole
    derivation answers A01's batch-fill question rather than A08's cache-contention one.
    Nothing in the answer touches KV residency, long-context share, or isolation between
    request classes, which is what the prompt made the point. This is the relevance gate
    working exactly as designed, and it is the one cell in my set I scored without
    hesitation.
```

## Answer 5 (`A09`)

```
Answer 5 / capacity_cost_estimation: 2
  cell clause applied: "Derived the binding quantity from assumptions stated out loud ...
    Arithmetic within ~2–3×. Named which constraint binds ... vs dollars."
  evidence: "blended cost is 0.7 times a tenth plus 0.3 times one, which is 0.37 — so
    about 37 percent of what all-70B serving costs."
  admits another reading: yes — band 1, strongly, and this was the hardest call in the set.
    Three things are wrong inside an answer whose headline arithmetic is right. (i) The
    "somewhere near 55 cents" has no derivation; working backwards, 0.37 × X = 0.55 implies
    an all-70B baseline of $1.49/M, i.e. he silently assumes the baseline equals the
    ceiling and then concludes he is under the ceiling. That is band 1's "Gave a number
    with no derivation", applied to the only absolute figure in the answer. (ii) The 400B
    model is dropped from the blend entirely although the prompt puts it in production;
    with a 10% 400B share the blend goes from 0.37 to 0.84 of baseline, which more than
    doubles it. (iii) His stated watch-metric is wrong by his own model: with cost ratio
    1 − 0.9s in the 8B share s, the ratio at s = 0.2 is 0.82, nowhere near the ceiling, so
    "the ceiling only starts to bind if the 8B share drops below roughly 20 percent" is
    false under his own arithmetic — it never binds until s ≈ 0. I score 2 because the
    rubric's band-2 clauses are all satisfied and the rubric provides no band-1 clause for
    "correct ratio, fabricated absolute, internally inconsistent sensitivity threshold".
    That gap is a B5 finding. From my seat this answer is below bar: he cannot tell me the
    ceiling in his own units, and he would alert on the wrong number.
```

```
Answer 5 / high_level_design: 0
  cell clause applied: "No end-to-end path. Named technologies without connecting them.
    Could not say what happens to a single request from arrival to response."
  evidence: "If 70 percent goes to the 8B, blended cost is 0.7 times a tenth plus 0.3
    times one, which is 0.37"
  admits another reading: yes — band 1, for a reader who treats "if 70 percent goes to the
    8B" as implying a router and scores the implied design as one that does not satisfy the
    requirements. I score 0 because there is no component anywhere in the answer: no
    classifier, no cascade, no confidence threshold, no escalation or fallback path, no
    shadow evaluation, and nothing at all answering the prompt's second half ("what do you
    measure to know you have not quietly made the product worse"). Appendix A permits 0
    only on an axis the item asked about; this item asked, in the prompt's own first five
    words. Worth flagging downstream: one axis at 0 sends the level mapping straight to
    "below the senior bar", so a 60-second answer that spends its whole budget on a cost
    model and omits the mechanism is hard-failed by a single cell. I believe that is the
    right outcome here, but it makes the 0/1 line on `high_level_design` unusually
    high-stakes for a 60-second instrument.
```

## Hardest cell to apply

**`capacity_cost_estimation`, the 1/2 boundary, on Answer 5.** Band 1 is written for
answers that are wrong at the top level — no derivation, off by 100×, irrelevant, or
self-contradicting the chosen design. Band 2 is written for answers that derive the binding
quantity and name what binds. Answer 5 does both at once: the ratio derivation is correct
and explicit, the only absolute number in it is invented, and the sensitivity threshold it
offers as the thing to monitor is false under its own model. The rubric has no cell for
partially-load-bearing arithmetic, and the clause that comes closest — "the number was
produced but not understood" — sits inside a band-1 example about choosing a design the
number rules out, which is not what happened. I scored 2 by applying the band as written
and I think a careful reviewer could land on 1 with equal justification. Runner-up:
Answer 3's 2/3 boundary, where the only evidence distinguishing the bands is the order the
sentences came in.

---

# PART B — CRITIQUE

## B1. Axis legitimacy

**Five of the six correspond to what I weight when I write a debrief. One does not, and one
is missing.**

The one that does not earn separate status is `capacity_cost_estimation`. In my own
debriefs numeracy is never a line item; it is the evidence I use to decide whether a
trade-off claim is real. "We'll shard it" and "we'll shard it because one tenant's minute
of quota is 1,670 tokens a second and a single long request eats all of it" are not two
scores, they are a weak and a strong instance of the same score. The rubric half-concedes
this — `rubric.md:420` lists it as "the single most likely place this rubric is wrong" —
and its own band 3 collapses the two axes anyway, since
`capacity_cost_estimation` band 3 requires the number to change a decision and
`tradeoff_articulation` band 3 requires the decision to rest on a number they produced.
Those are the same observation scored twice, which inflates the composite for numerate
candidates and double-penalises innumerate ones. I would keep six axes for the product
reason the pack states honestly at `rubric.md:383` (a six-mark scorecard is shareable), but
I would stop pretending the two are independent in the level mapping.

The one that is missing, for my domain specifically, is **operability**: what you would
measure, what the alert is, what the degraded mode looks like, how you would know in
production before a customer tells you. That is where I personally make the senior/staff
call on request-path candidates, and the rubric scatters it into band-3 indicators on axes 4
and 6 ("said what signal would tell them it is failing", "the first signal that
reconciliation is silently wrong") where it can never be the thing that distinguishes a 2
from a 3, because the band-3 indicators are explicitly non-required (`rubric.md:44`).

`requirements_scoping` and `communication_collaboration` are also substantially correlated
in a 60-second format — both are largely measuring whether the candidate structured the
answer before speaking — which matters for the agreement statistics, because correlated
axes will look like better instrument reliability than the instrument has.

**What my answer rests on.** Running and debriefing loops in request-path and
infrastructure roles, and writing the scorecards. That is real experience of the category,
not knowledge of any named employer's rubric, and it is one person's weighting of a round
whose weighting varies by interviewer more than any of us like to admit.

**What would change my mind.** Evidence that a real scorecard in this category carries
capacity math as its own line rather than as evidence under trade-offs. If three people who
own hiring rubrics say it does, I am wrong and axis 2 stays as is. Conversely, if the first
50 graded sessions show `capacity_cost_estimation` and `tradeoff_articulation` with a
per-candidate correlation above ~0.8, that is this finding confirmed from the data and the
level mapping should stop gating on both.

## B2. Scenario realism — my four

### `multi-tenant-token-limiter-placement` — **realistic**

The strongest item in the pack from my seat. It gets the central thing right: the unit. 100×
shape variance with a per-request limiter is the single most common real mistake in this
category and the `bad` field names it precisely, including the reason it is common ("it is
the limiter nearly every API starts with"). The second `bad` — a strongly consistent central
counter in the hot path — is also a failure I have been on call for. The prompt withholds
correctly: it says "what does it count?" without hinting that input and output tokens are
different questions, and `good` requires the candidate to find that themselves. The quota
arithmetic is right (100,000/60 = 1,666.7, "about 1,670").

**The single thing most wrong:** `good` and `model_answer` never require the candidate to
name **concurrency** as a limiter unit. Tokens-per-minute is necessary and insufficient — it
does not bound in-flight requests, queue depth, or KV residency, which is why real hosted
APIs ship a concurrent-request or in-flight-token limit *alongside* TPM. A tenant inside
1,670 tok/s who opens 400 simultaneous 100k-context requests is compliant and has taken the
fleet; that is the shape nobody designs for, and it is the shape I would most want to see a
staff candidate find. As written, a candidate who raises it gets no credit path and may be
marked down for not matching `model_answer`'s token-bucket framing.

Secondary: 800 tenants × 1,670 tok/s = 1.33M tok/s of sold capacity, which against Appendix
B's ~6,000 tok/s per 4-GPU replica is ~222 replicas, ~890 H100s, to honour the quota if
everyone used it at once. Nobody provisions that, so the item's real commercial question is
the **oversubscription ratio** — the quota is sold on the assumption it is not used — and
neither `good` nor `followups` ask for it. The `at bar` probe "One tenant is 40 percent of
total traffic and is inside their limit. Is the system fair?" circles it without naming it.

### `gpu-credit-ledger-consistency` — **realistic-but-wrong-in-one-detail**, and the detail
is the number the item is built around

Right lesson, wrong arithmetic. The lesson — size the thing you are protecting before you
accept an availability coupling to protect it — is exactly right, and the `bad` field's
framing ("The failure is not the consistency choice, it is never having sized the thing
being protected") is the most useful sentence in the pack. The lease arithmetic is also
internally correct: 20 × 1,000 GPU-s = 20,000 GPU-s = 5.56 GPU-hr ≈ $11.11 at $2/GPU-hr.

**The single thing most wrong:** a 1,000-GPU-second lease is not a lease, it is a round trip
with extra steps, so the $11 that makes the choice "obviously correct" is off by two to
three orders of magnitude. Credits are debited *per GPU-second*, so a 64-GPU job running one
hour consumes 230,400 GPU-seconds — 230× the entire lease. A scheduler holding 1,000
GPU-seconds is back at the ledger before the first job finishes starting, which defeats the
stated purpose of getting the ledger out of the admission path. To actually keep it out you
need leases in the 10^5–10^6 GPU-second range, which puts the overdraft bound at
**$1,100–$11,000 per scheduler**, or $22k–$220k across 20 — and that is a number a finance
partner will push back on, which is where the interesting conversation starts. The item
currently teaches the candidate to pick a lease size that makes the dollar figure small
rather than deriving it from job size.

Compounding this, the prompt withholds the one piece of information needed to size the
lease: **nothing states job size or duration.** It gives scheduler count, team count, the
2-second start SLO and the 150ms ledger cost, all of which are about admission, and none of
which lets you compute a draw-down rate. Add a clause — "jobs are typically 8 to 512 GPUs
for 20 minutes to 12 hours" — and the item becomes answerable as designed.

Two further gaps in my area of skepticism. First, the prompt conflates **admission-time
authorization with continuous metering**: "a ledger check adds about 150 milliseconds to
admission" is an authorization framing, while "credits debited per GPU-second" is a metering
one, and the real design is reserve-at-admission (requested GPUs × max wall clock) and
settle-on-completion. That reserve-and-settle shape is absent from `good`. Second, and this
is the thing I would fail a candidate for missing: **`good` never asks what happens when the
settle never arrives.** It covers scheduler death reclaiming a lease, but not a job that
dies, is preempted, or loses its node mid-run, leaving a reservation with no terminating
event. Every credit system I have worked on has a reconciliation sweeper for exactly that,
and it is where the real bugs live.

### `streaming-delivery-and-deploys` — **realistic-but-wrong-in-one-detail**; the prompt
gives too much away

Transport choice, 4%/min mobile drop, six deploys a day, and 90-second generations are all
plausible and the SSE-vs-WebSocket-plus-sticky-sessions `bad` is a real pattern I have
reviewed more than once. The reconnection arithmetic is correct: 1 − 0.96^1.5 = 5.94%, so
"roughly 6 percent" checks out.

**The single thing most wrong:** the prompt names the failure for the candidate. "tell me
what happens to an in-flight stream when a node goes away mid-generation" hands over both
the failure mode and the fact that it is the point of the item, which converts the
interesting question (does the candidate connect "six deploys a day" to "every in-flight
stream is on a process that is about to die"?) into a reading-comprehension exercise. Drop
the second clause and ask only "pick your transport"; the deploy rate is already in the
prompt and finding it is the signal.

Three content gaps, in order of how much they matter to me:

1. **Nobody pays for the abandoned stream.** `bad` covers double-billing on restart, and
   `good` covers what the user sees when resumption fails, but neither covers the case I
   actually litigate: a client disconnects at 4%/min, generation continues so that a
   reconnect can resume, and the client never returns. At 60k concurrent that is ~3,600
   streams generating for nobody at any time — ~6% of the fleet burned on output no one
   reads, and tokens billed that the user never saw. The real design decision is the
   disconnect grace period before aborting generation, and it is a capacity decision, not a
   transport one. It is nowhere in the item.
2. **The buffer cost probe has a surprising answer the item does not state.** The `at bar`
   probe asks "How long do you hold the buffer, and what does that cost at 60,000
   concurrent?" At ~50 tok/s over 90s that is ~4,500 tokens ≈ 18 KB of text per stream, so
   60k concurrent is **~1.1 GB** — free. A candidate who says buffering is too expensive is
   wrong by three orders of magnitude, and that is a clean discriminator, but `good` gives
   the judge no number to grade against.
3. "Thousands of resumptions at any moment" in `model_answer` is wrong, see B3.

### `agent-retry-side-effects` — **realistic**, and the single best-targeted item in my four,
but the 21% does not rest on a defensible independence assumption

This is the right problem, arriving the right way: a teammate with a plausible fix that
treats a correctness bug as a reliability bug. The `bad` field is accurate — tool-layer
retries are genuinely tempting and genuinely do not address that a timed-out charge may have
succeeded — and the retry-amplification-across-two-layers point is a real production failure.
Framing it as "what do you say to them" is the right way to make `communication_collaboration`
observable in 60 seconds.

**The single thing most wrong: the 21% figure, and specifically the fact that the pack never
says what it assumes.**

The arithmetic is right under its assumption: 1 − 0.98^12 = 0.2153, so "about 21 percent" is
correct **if and only if** the 12 timeouts are mutually independent. They are not, and this
is not a pedantic objection — it is the single most load-bearing unstated assumption in the
pack.

Why independence fails for real tool fan-out, in the order the failures actually arrive:
the 12 calls in a turn are concurrent and share the orchestrator's event loop, connection
pool, DNS resolution, TLS session cache and egress path; several tools commonly sit behind
the same provider or the same gateway; and a measured "2% timeout rate" is nearly always a
marginal rate over a window that includes incident periods, which is a mixture distribution,
not a Bernoulli one. Field timeouts arrive in bursts: most turns see zero, a minority see
five at once.

The consequence is directional and the pack should state it. **With per-call marginals fixed
at 2%, positive correlation strictly reduces the fraction of turns with at least one
timeout.** The true value lies in [2%, 21.5%]: 21.5% is attained only at perfect
independence, 2% at perfect correlation. So 21% is an **upper bound on turn-level failure
rate**, not an estimate of it, and `model_answer` presents it as the latter.

Why this matters more than a missing caveat. The `good` field makes the multiplication "the
move that reframes the whole conversation", which makes the *correctness argument contingent
on the rate*. It is not. A duplicate card charge is a correctness bug at 0.1% per turn; the
rate sets the urgency and the blast radius, nothing else. So the better answer — "multiplied
out it's about 21% if they're independent, and they are not, so call it somewhere between 2%
and 20%; either way whole-turn retry re-executes a charge and that is a correctness bug at
any rate" — is **strictly stronger than `model_answer` and will score worse against `good`,**
because `good` rewards the multiplication and the band-3 clause rewards a number having
changed the design. A candidate who correctly refuses to let the number be load-bearing gets
penalised for it. That is the inversion I would fix first in this item.

Concretely: state the independence assumption in `model_answer`, give the range, add a
`good` clause crediting correlation, and add a followup — "Would you expect those 12
timeouts to be independent?" — which is a better `at bar` probe than either of the two
currently there.

Two smaller realism notes. The prompt states "p99 tool latency is 8 seconds" and a 2%
timeout rate but never the **timeout value**, which is the number you need to design the
"shared timeout budget across the fan-out" that `model_answer` asks for. (The two stated
figures are at least consistent: a 2% timeout rate puts the threshold near p98, hence at or
below 8s.) And the prompt never says whether the fan-out is **parallel or sequential**,
which determines whether a shared budget is even feasible — 12 tools at 8s p99 is 8 seconds
concurrent or 96 seconds serial, and those are different products. One clause fixes it.

## B3. Arithmetic

**Checked and correct:** KV per token 2 × 80 × 8 × 128 × 2 B = 327,680 B ≈ 320 KB, and 100k
tokens ≈ 32.8 GB; the 8B-class figure 2 × 32 × 8 × 128 × 2 = 131,072 B = 128 KB; the decode
floor 140 GB / 13.4 TB/s = 10.4 ms and ~96 tok/s single-stream; batch 64 → ~6,100 tok/s;
prefill 2 × 70e9 × 1e4 = 1.4 PFLOP against 4 × 990 TFLOPS × 40% = 1.58 PFLOPS → 0.88 s, and
~8.8 s at 100k; $2/GPU-hr × 4 = $0.00222/s ÷ 6,000 tok/s = $0.37/M output tokens; the limiter's
1,670 tok/s; the ledger's 20,000 GPU-s = 5.56 GPU-hr = $11.11; the streaming 1 − 0.96^1.5 =
5.94%; and 1 − 0.98^12 = 21.5%. All fine as arithmetic.

**Three I believe are wrong.**

1. **`rubric.md`, Appendix B, KV cache section — "comparable to a fifth of a node's HBM" is
   wrong under every reading of "node" in this pack.** 32.8 GB against an 8×H100 node (640 GB)
   is 5.1%; against the 4-H100 replica the pack uses elsewhere (320 GB) it is 10.2%; against
   a single H100 (80 GB) it is 41%. "A fifth" matches 160 GB, which is two GPUs and is not a
   unit the pack uses. `questions.json` item A08 says "eight nodes of eight H100s", so node =
   640 GB and the error is ~4×. Fix to "about 5 percent of an eight-GPU node, or 40 percent
   of a single H100's HBM" — and note the 40% version makes the admission-control argument
   much more forcefully than the current wording does.

2. **`questions.json`, `streaming-delivery-and-deploys`, `model_answer` — "thousands of
   resumptions at any moment" overstates instantaneous concurrency by about two orders of
   magnitude.** My calculation: 60,000 concurrent sessions with a 4%/min hazard gives
   60,000 × 0.04/60 = **40 breaks per second**, i.e. ~3,600 per 90-second window. If a
   resumption completes in roughly a second, ~40 are in flight at any moment, not thousands.
   The 6% and the 3,600-per-window figures are right; "at any moment" is the wrong
   quantifier attached to them. This matters because model answers are reference context for
   the grader, so a candidate who correctly says "about 40 a second" is being compared
   against a reference that says thousands.

3. **Blind-set Answer 5's 20% threshold is internally inconsistent, and the rubric has no
   cell that catches it.** With cost ratio = 0.1s + (1 − s) = 1 − 0.9s in the 8B share s, and
   his own implied all-70B baseline of ~$1.49/M, the $1.50 ceiling binds only as s → 0: at
   s = 0.2 the ratio is 0.82 (~$1.22/M). "The ceiling only starts to bind if the 8B share
   drops below roughly 20 percent" is therefore false under his own model. I raise it in B3
   rather than only in Part A because the rubric's band-1 cell has no clause for a wrong
   *sensitivity* figure — only for wrong magnitudes and irrelevant computations — so a
   grader applying the cell as written cannot mark it down.

**One observation about Appendix B rather than an error in it,** and it is my domain's
version of "the limiter counts the wrong unit": Appendix B's token economics are entirely in
**$/M output tokens**, and A09 asks the candidate to route against a blended ceiling in those
units. But by Appendix B's own numbers prefill dominates the bill for prompt-heavy traffic.
A 10k-in / 500-out request at TP=4 costs 0.88 s × 4 GPUs = 3.5 GPU-s ≈ **$0.0020** of
prefill against 500 output tokens at $0.37/M ≈ **$0.00019** of decode — roughly **10× more
input-side than output-side**. A ceiling denominated in output tokens is therefore not
controllable by routing alone; it moves with the input:output ratio, which the product
controls and the infra team does not. If the pack wants to teach "quotas and prices must
count the cost driver" — and it should, it is the most transferable lesson in the whole
multi-tenancy track — Appendix B should carry the prefill-vs-decode cost split explicitly,
and A09's `good` should credit a candidate who tells finance the ceiling is in the wrong
unit. That is a content addition, not a correction.

## B4. The band 2/3 boundary

**Right intent, wrong place for two of my cells, and unapplicable in one.**

The intent — behaviour is 2, consequence is 3 — is correct and it is the best single decision
in this rubric. The band-3-has-one-required-clause correction at `rubric.md:44` is also
right, and the reason given (five reference answers could not reach the band they exist to
teach) is the kind of finding that only comes from actually dry-running it.

Three problems, from applying it ten times:

1. **The boundary is decided by utterance order and the rubric does not say so.** Answer 3
   is the case: the content that would earn a 3 is all present, but the index was chosen and
   justified by convention before the sizing appeared. I scored 2 because the number did not
   alter a decision that had already been made. A different reviewer will read the same
   sentences as a 3 because every clause is satisfied somewhere in the paragraph. **Add the
   clause explicitly:** "a number offered after a choice already justified on other grounds
   is band 2; band 3 requires the number to precede the choice or to visibly revise it."
   That single sentence would have removed my hardest 2/3 call, and it generalises to all
   six axes.

2. **Band 3 on `capacity_cost_estimation` is structurally much harder to reach in the
   60-second diagnostic than in the 45-minute mock, and the percentile blends them.** Band 3
   wants the number to have ruled out an architecture — but every diagnostic prompt states
   its constraints numerically, and the derived-quantity cap correctly refuses to credit
   echoed numbers. So in the diagnostic the candidate must derive a *new* quantity and have
   it change a decision, inside 60 seconds, which is close to the ceiling of the format. The
   same band label means two different difficulties in the two products. Either exclude
   diagnostic band 3 from the composite or publish separate distributions.

3. **The 0/1 boundary is in worse shape than the 2/3 boundary and nobody is looking at it.**
   Two of my ten cells turned on it (Answer 1 / capacity, Answer 4 / requirements) and in
   both the rubric contradicts itself. Band 0 on `capacity_cost_estimation` says "No quantity
   of any kind" while the hard cap says the test is a quantity **of the candidate's own**;
   an answer with only echoed numbers satisfies band 0's text and band 1's cap at the same
   time. Similarly, the relevance gate's "at most band 1 ... however well executed" implies
   competent-but-off-problem work floors at 1, while band 0's "never bounded the problem"
   describes the same answer. This matters more than it looks: the level mapping sends **any
   axis at 0** straight below the senior bar, so the 0/1 line is the highest-stakes boundary
   in the instrument and it is the one with no stated discriminator. The rubric's own hard-cap
   table demands "Band 0 vs 1 must be distinguishable from the transcript"; by its own
   standard, two of these cells fail.

Not too harsh, not too generous. Under-specified in exactly the places where two readers
will differ, which is what the harness was built to detect.

## B5. Top 3 defects, ranked

### 1. Roughly half the `followups` state the insight instead of creating room for it — and the attribution clamp then penalises the candidate for using it

**Files:** `questions.json` (`agent-retry-side-effects` followup 3;
`gpu-credit-ledger-consistency` followup 1; `multi-tenant-token-limiter-placement`
followup 3; `streaming-delivery-and-deploys` followup 3) against `prompts.md` Prompt 1
rule 1 and the Attribution row of the validation table.

**What is wrong.** Prompt 1's first hard rule is "NEVER supply a consideration the candidate
has not raised ... you do not hint at the answer's shape", with a worked example of the
failure. Several probes do precisely what that rule forbids:

- "One in five turns hits this. Is it still an edge case?" — **states the 21%**, the number
  `good` calls "the move that reframes the whole conversation".
- "What is the overdraft worth in dollars if you are wrong? Compare it to the cost of the
  ledger being down for an hour." — that is the `good` field read aloud, both halves of it.
- "You do not know the output length at admission. What do you charge?" — hands over the
  reserve-and-reconcile insight that `good` requires the candidate to find.
- "The user has seen 400 tokens and reconnects. Do they see them again, and who pays for
  them?" — hands over the double-billing insight.

In every case the `if` condition fires on a *below-bar* answer, so the leak lands on exactly
the candidate who had not found it.

**Why it matters.** Two ways, and they point opposite directions, which is the worst
property a probe can have. Pedagogically the probe rescues a below-bar candidate, which
Prompt 1 forbids by name ("If the candidate is far from the bar, do NOT rescue the session").
Scoring-wise the validation table then clamps that axis to ≤ 1 via
`first_raised_by == "interviewer"` — so the probe teaches and punishes at once, and the item
never declares which it is for. In the diagnostic it is worse, because Prompt 2 carries no
equivalent of Prompt 1 rule 1 at all, so nothing in the live path prevents it.

**What I would do.** Rewrite every probe whose `if` is a below-bar condition so it states a
*situation*, never a conclusion. The two good models are already in the pack:
"Tenant A sends 2,000 short requests, tenant B sends 10 long ones. Both are inside the limit.
Who is using the fleet?" and "The charge call timed out. Did it charge? What does your retry
do?" Both create room without supplying anything. For the four above: "Is 2 percent per tool
the same as 2 percent per turn?"; "How much is the overdraft you are preventing worth?";
"When do you know the output length?"; "The user has seen 400 tokens and reconnects. What
happens?" Then add Prompt 1 rule 1 to Prompt 2 verbatim, and add a lint over
`questions.json` that fails any probe containing a numeral not present in its own prompt.

### 2. The 21% compound-timeout figure asserts independence silently, and `good` makes the correctness argument contingent on it

**File:** `questions.json`, `agent-retry-side-effects` — `good` ("Computes the compound
failure probability, which is the move that reframes the whole conversation") and
`model_answer` ("12 tools at 2 percent each means something times out on about 21 percent of
turns — one in five").

**What is wrong.** 1 − 0.98^12 = 21.5% requires mutual independence across 12 concurrent
calls that share an event loop, a connection pool, an egress path, and frequently a
provider. With the per-call marginal fixed at 2%, positive correlation strictly lowers the
fraction of turns containing at least one timeout, so the defensible statement is **2% to
21.5%, with 21.5% as the independence upper bound.** The pack states the upper bound as a
point estimate and flags no assumption.

**Why it matters.** Three compounding reasons. (i) It is the one number in my four items a
practitioner will challenge in the first thirty seconds, and the pack's credibility with this
cohort rests on numbers surviving that. (ii) `model_answer` makes the bug's severity
*depend* on the rate ("So whole-turn retry is not a rare path"), when a duplicate card charge
is a correctness bug at any rate — so the pack teaches the weaker form of its own argument.
(iii) It inverts the grading: a candidate who says "about 21% if independent, and they
aren't, so lower — but it's a correctness bug either way" is better than `model_answer` and
scores worse against `good`, because `good` rewards the multiplication and band 3 rewards a
number having changed a decision. The rubric's own band-3 indicator — "Stated assumptions as
assumptions and flagged which one the answer is most sensitive to" — is failed by the gold
answer on the most contestable assumption in it.

**What I would do.** Three edits. In `model_answer`: "Multiply it out — 12 tools at 2 percent
is about 21 percent of turns if the timeouts are independent, and they won't be, since
they share a network path and often a provider, so call it somewhere between 5 and 20
percent. It doesn't matter much which, because a duplicate charge is a correctness bug at
any rate; the rate only tells me how fast finance finds out." In `good`: add a clause
crediting a candidate who questions independence or who decouples the bug from the rate. In
`followups`: replace the leaking probe with "Would you expect those 12 timeouts to be
independent?"

### 3. The lease size in `gpu-credit-ledger-consistency` is too small to do the job, so the $11 that makes the lesson land is off by two to three orders of magnitude

**File:** `questions.json`, `gpu-credit-ledger-consistency` — `prompt`, `good`,
`model_answer`.

**What is wrong.** Credits are debited per GPU-second. A 64-GPU job running one hour is
230,400 GPU-seconds, so a 1,000-GPU-second lease is exhausted 230× over inside the first
job — the scheduler is back at the ledger immediately and the ledger is still in the
admission path, which is the exact coupling the design existed to remove. A lease that
actually works is 10^5–10^6 GPU-seconds, putting the overdraft bound at $1,100–$11,000 per
scheduler and $22k–$220k across 20. Separately, the prompt never states job size or
duration, so a candidate cannot derive the lease size even if they want to; and it conflates
admission-time authorization ("adds about 150 milliseconds to admission") with continuous
metering ("debited per GPU-second"), when the real pattern is reserve-at-admission and
settle-on-completion.

**Why it matters.** This item carries the pack's best lesson — size the thing you are
protecting before you accept an availability coupling to protect it — and it demonstrates
that lesson with a number chosen to make the answer look easy rather than derived from the
workload. A practitioner will spot it, and when they do, the lesson is what gets discredited.
It also hides the genuinely hard design question: at $22k of exposure you cannot wave it
away, so you need per-team lease sizing, tiered leases by team spend, or a tighter sweeper —
which is the staff-level conversation this item should be provoking.

**What I would do.** Add job scale to the prompt ("jobs run 8 to 512 GPUs for 20 minutes to
12 hours"). Rewrite `model_answer` to derive the lease from job size rather than assert it,
land on a four-or-five-figure exposure, and keep the existing and excellent "if the number
came out at 11,000 dollars instead of 11, I would shrink the lease, not change the model" —
which now becomes the actual decision rather than a hypothetical. Add a `good` clause for
reserve-and-settle, and one for **what happens when the settle never arrives** (job
preempted, node lost, scheduler killed mid-job) — a reconciliation sweeper with a staleness
bound. That omission is the thing I would most want a candidate to volunteer and the pack
currently does not ask for it.

### Also worth fixing, below the top three

- **`prompts.md` validation table, "Derived-quantity integrity": `reject if derived_quantity
  appears as a substring of the prompt text` is a string test on a numeric concept, and it
  fails both ways.** It over-fires on legitimate derivations that land on a stated number —
  sanity-checking your arithmetic against the prompt's figure is the behaviour the axis
  wants, and in `multi-tenant-token-limiter-placement` a candidate deriving "100,000 tokens
  a minute is 1,670 a second" may well have "100,000" in the reported field and be rejected
  for it. And it is trivially bypassed by formatting: "1670" vs "1,670", "0.1 seconds" vs
  "100 milliseconds", "40 TB" vs "40 terabytes". Normalise numerals and units before
  comparing, and test the derivation's *inputs* rather than its output string.
- **`rubric.md` level mapping double-gates on correlated axes.** "At the staff bar" requires
  `tradeoff_articulation ≥ 2` and ≥ 2 axes at 3, and band 3 on both axes 2 and 5 requires
  essentially the same observation (a number the candidate produced resolving a decision).
  Numerate candidates get two 3s from one behaviour. Either make axis 5's band 3 satisfiable
  without a number, or stop counting both toward the "≥ 2 axes at 3" threshold.
- **`questions.json` `axis_coverage`:** `capacity_cost_estimation` is scored on 4 of 12
  items, and `agent-retry-side-effects` — which contains the pack's most contestable
  number — is not one of them. So the 21% is reference context the judge grades *against*
  on two other axes, with no instruction to accept a different rate. Either score the axis
  on that item or tell the grader explicitly that `model_answer`'s rate is one defensible
  value among several.

## B6. Sign-off

**Would I put my name on this rubric as legitimate? Yes.** With caveats, and the caveats are
about the items, not the rubric.

What earns the yes: the band language is genuinely observable rather than adjectival; the
hard caps are real engineering rather than prompt-politeness, and the file says so in exactly
those words; the relevance gate is the single most important thing in here and it has a
negative control; the "Where this rubric departs from its sources" and "What needs a
practitioner's review" sections state the weaknesses I would otherwise have had to find,
which is rarer than it should be. The band-3-has-one-required-clause correction is evidence
somebody actually ran the thing against its own reference answers and believed the result
over their own design.

**What I would refuse to let ship as-is:**

1. The four `followups` that state the insight, un-rewritten. They break Prompt 1's own first
   rule in the live path and then the attribution clamp penalises the candidate for the leak.
   Cheapest fix in the pack and the most direct damage if shipped.
2. The 21% without its independence assumption stated in `model_answer`. It is the number
   this reviewer was asked to check and it does not survive the check as written.
3. The $11 lease exposure as the pack's showcase for "size what you are protecting". Right
   lesson, number that does not survive contact with real job sizes.
4. "A fifth of a node's HBM" in Appendix B. Four-times error in the appendix whose stated
   purpose is that a practitioner can check every line in under a minute.
5. Any **level claim** derived from the 60-second diagnostic, until the thresholds are
   calibrated. `rubric.md` already calls them "invented to be defensible, not calibrated" and
   the highest-stakes unvalidated numbers in the pack, and I agree. Two of my ten blind cells
   turned on an under-specified 0/1 boundary, and a single 0 sends a candidate below the
   senior bar. Report axis profiles, not levels, until there is n ≥ 50 per axis.

What I would not block on: the six-axis structure, the composite, or `capacity_cost_estimation`
having its own column. I think that last one is wrong (B1) but it is a defensible product
decision made with its eyes open, not an error.

## B7. Epistemic status

### Checkable facts — verify these without asking anyone

- `1 − 0.98^12 = 0.2153`, so "about 21 percent" is correct **under independence**. That the
  figure is an upper bound rather than a point estimate under positive correlation with fixed
  marginals is also a mathematical fact, not a judgement.
- `2 × 80 × 8 × 128 × 2 B = 327,680 B`; 100k tokens = 32.8 GB; 32.8 GB is 5.1% of 640 GB,
  10.2% of 320 GB, 41% of 80 GB. **"A fifth of a node's HBM" is wrong** under every
  definition of "node" the pack uses. Appendix B.
- 60,000 concurrent × 0.04/60 = **40 breaks per second**, 3,600 per 90-second window.
  "Thousands of resumptions at any moment" is wrong by ~100× read as concurrency.
  `streaming-delivery-and-deploys` `model_answer`.
- A 64-GPU, 1-hour job = 230,400 GPU-seconds vs a 1,000-GPU-second lease. The lease cannot
  keep the ledger out of the admission path. `gpu-credit-ledger-consistency`.
- Blind-set Answer 5: cost ratio 1 − 0.9s, so at s = 0.2 the ratio is 0.82 and the ceiling
  does not bind. The answer's stated 20% threshold is false under its own model.
- Prefill vs decode cost from Appendix B's own figures: $0.0020 vs $0.00019 for a 10k-in /
  500-out request at TP=4 — ~10× input-side. Arithmetic is mine from their inputs; the
  *implication* for ceiling units is judgement, below.
- **Internal contradictions**, verifiable by reading two files side by side: Prompt 1 rule 1
  vs four `followups`; band 0 "No quantity of any kind" vs the derived-quantity cap; the
  relevance gate's "at most band 1, however well executed" vs band 0's "never bounded the
  problem"; the substring test in the validation table being format-sensitive.

### Domain judgement — practitioners in multi-tenant request-path work would mostly share

- A requests-per-minute limiter under 100× shape variance is the characteristic real failure
  in this category, and the `bad` field naming it is correct.
- **Concurrency is a missing limiter unit** in `multi-tenant-token-limiter-placement`.
  Tokens-per-minute does not bound in-flight requests or KV residency. I am confident; I
  would not be surprised to find a practitioner who thinks TPM plus admission-control depth
  covers it.
- Tool timeouts in a concurrent fan-out are **positively correlated in practice**. This is
  the load-bearing judgement behind my #2 defect. It is from operating these systems, not
  from a measurement I can hand you. Someone with per-tool timeout traces could settle it in
  an afternoon, and that is the right way to settle it.
- **Reserve-and-settle, and what happens when the settle never arrives,** is the real shape
  of a credit system and its absence from `good` is a genuine gap. High confidence.
- The **abandoned-stream billing case** (generation continues for a client that never
  reconnects; ~6% of a 60k fleet; tokens billed for output nobody read) is a real problem
  and a real omission. High confidence.
- `capacity_cost_estimation` is evidence for trade-off quality rather than a separate axis
  (B1). This is my weighting of a round, held with moderate confidence, and it is contested
  among people I would consider peers.

### Guesses about interview practice — a human must confirm these

- **All of B1.** Whether a real loop in this category scores these six axes, and whether
  numeracy appears as its own line on a scorecard, is institutional knowledge I do not have
  from the inside for any employer. My basis is running and debriefing loops in
  infrastructure roles and writing the scorecards; that is one practitioner's weighting of a
  round whose weighting varies by interviewer. The harness README is right that this is the
  most dangerous output in the set, and a persona prompt will assert it confidently anyway.
  Weight it as one opinion, not as a finding.
- Whether the "missing operability axis" would be recognised as a gap or as my own hobby
  horse. I think the former; I would not bet much.
- Whether `streaming-delivery-and-deploys` "gives it away" too much. This rests on my sense
  of how much a 60-second prompt should withhold, which is calibrated to the interviews I
  run, not to this product's format. A 60-second instrument may need to give more away than
  a 45-minute round to be answerable at all — that is a product question I cannot settle.
- Whether band-1 cells read as diagnostic or insulting. Not my competence. The rubric already
  flags it as needing one practitioner and one person who recently failed a loop; I agree and
  I am neither.
- The level-mapping thresholds. Entirely uncalibrated and I have no basis for an opinion
  beyond "do not ship a level claim off ten blind cells", which is a measurement argument
  rather than an interview-practice one.

### What I assumed because the pack did not say

- **Node = 8 H100s = 640 GB HBM**, taken from A08's "eight nodes of eight H100s". Appendix B
  uses "node" without defining it, and its "fifth of a node" claim is only coherent at
  160 GB. My error-magnitude claim depends on this reading.
- **$2/GPU-hour**, carried from Appendix B, which flags it as a market-rate assumption
  needing re-verification. Every dollar figure I quote inherits that.
- **The agent fan-out is concurrent.** `agent-retry-side-effects` does not say. My
  correlation argument is weaker if the 12 calls are serial, since they then share less
  in-flight state — though they still share the provider and the network path.
- **Credits are metered continuously rather than reserved at admission** in
  `gpu-credit-ledger-consistency`. The prompt says both things. My lease-sizing arithmetic
  assumes the metering reading; under a pure authorization reading the lease would be sized
  in job-slots and the $11 would be a different kind of wrong rather than a magnitude error.
- **~50 output tokens/sec and ~4 bytes/token** for the streaming buffer estimate. Both are
  conventional and the conclusion (buffering is ~1 GB, i.e. free) survives a 5× error in
  either.
- **Blind-set answers are single-shot with no interviewer turns.** No probes appear in the
  transcripts, so I scored every absence as absence. If the real sessions had probes stripped
  out, several of my 0s and 1s are wrong and the `first_raised_by` clamp would have applied.

### My stated blind spot, declared

My persona brief says I over-rate the request path and that my sense of PB-scale training
infrastructure is secondhand. That is accurate and it shaped this report: I reviewed four
request-path items, and `training-data-dedup-and-shuffle`,
`annotation-throughput-vs-agreement`, and `eval-infra-per-commit-cost` are untouched by me
and should be weighted at zero from this report rather than read as uncriticised. I also
notice that three of my four items came out with "right lesson, under-derived number", which
is the pattern someone looking for request-path rigour would find whether or not it is the
pack's dominant failure mode. Check that against the other reviewers: if nobody else reports
it, it is probably my lens.
