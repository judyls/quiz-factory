# BLIND SCORING SET

Five candidate answers. For each, score **only the axes listed** against `../rubric.md`,
0-3, and give the one clause of the cell you applied plus a verbatim quote.

**You are being measured too.** Five reviewers score these independently. Where you
disagree with each other, the rubric cell is badly written — that is the finding. Do not
hedge to a middle band to be safe; if a cell genuinely admits two readings, score the one
you believe and say explicitly that it admits two.

Labels are opaque and the order is arbitrary. Expected scores have been withheld on
purpose, and nothing in the set tells you which answers share an item. Do not try to infer
either.


---

## Answer `K7`

**Item prompt as given to the candidate:**

> Retrieval over 10 billion embeddings at 1,024 dimensions, stored as float32. The p99 budget for the retrieval step is 50 milliseconds, recall at 10 must stay at or above 0.9, and about 200 million vectors change every day. Pick an index and tell me what the choice costs you.

**Axes to score (only these):** `capacity_cost_estimation`, `tradeoff_articulation`

**Candidate transcript:**

**CANDIDATE:** Let me size it first. 10 billion vectors at 1,024 dimensions in float32 is 4 kilobytes per vector, so about 40 terabytes raw. Our p99 budget is 50 milliseconds and we need recall at 10 of at least 0.9. 200 million vectors change daily, which is about 2 percent churn. Given the recall requirement I would use HNSW, because it has the best recall-latency curve of the ANN families — typically 0.95-plus recall at single-digit millisecond latency. I would set M to 32 and efConstruction to 200, then tune efSearch to land inside the 50 millisecond budget. We would shard across machines and replicate for availability.


---

## Answer `M2`

**Item prompt as given to the candidate:**

> We serve a 70-billion-parameter model on replicas of four H100s. Our p99 time-to-first-token target is 400 milliseconds. Right now we use a fixed batch size of 32: p99 time-to-first-token is sitting at 1.2 seconds, and the GPUs are only 45 percent utilised. Both numbers are bad at the same time. What do you change first, and what number tells you it worked?

**Axes to score (only these):** `capacity_cost_estimation`, `tradeoff_articulation`

**Candidate transcript:**

**CANDIDATE:** So the issue here is that static batching couples latency to batch fill time rather than to actual work. I would move to continuous batching, so the scheduler admits requests at each decode step instead of waiting for a full batch to assemble. I would also separate prefill from decode scheduling, because a long prefill in the same step blocks every decode queued behind it. The trade-off is latency against throughput: a wider batch window buys you utilisation and spends time-to-first-token. Given our 400 millisecond target I would bias toward latency. Then I would tune the window empirically, watch the p99, and iterate until both numbers look healthy. I would also want solid observability on queue depth so we can see where the time is actually going.


---

## Answer `R9`

**Item prompt as given to the candidate:**

> Three models in production: 8 billion, 70 billion, and 400 billion parameters, on a mixed fleet of A100s and H100s. We are at two dollars sixty per million output tokens today, everything on the 70B, and finance has given you a blended ceiling of one dollar fifty. Offline evaluation says about 70 percent of current traffic would be served acceptably by the 8-billion model; a few percent genuinely needs the 400B. How do you route, and what do you measure to know you have not quietly made the product worse?

**Axes to score (only these):** `capacity_cost_estimation`, `high_level_design`

**Candidate transcript:**

**CANDIDATE:** Cost per token tracks weight bytes read, so against the 70B the 8B is roughly a tenth and the 400B about five to six times more. Baseline is two sixty. At 70 percent on the 8B, 25 on the 70B and 5 on the 400B, the blend is 0.7 times 0.1, plus 0.25, plus 0.05 times 5.7 — about 0.6 of baseline, so near one fifty-seven. That is over the one-fifty ceiling. And the reason is not the small model: the 5 percent on the 400B contributes 0.285 of baseline while the whole 70 percent on the 8B contributes 0.07, so the big model's sliver costs four times what the small model saves. To get under the ceiling I need the 400B share below about 4 percent. That is the number I would hold the routing policy to.


---

## Answer `T4`

**Item prompt as given to the candidate:**

> Retrieval over 10 billion embeddings at 1,024 dimensions, stored as float32. The p99 budget for the retrieval step is 50 milliseconds, recall at 10 must stay at or above 0.9, and about 200 million vectors change every day. Pick an index and tell me what the choice costs you.

**Axes to score (only these):** `capacity_cost_estimation`, `tradeoff_articulation`

**Candidate transcript:**

**CANDIDATE:** I'd go with IVF-PQ — it's what most billion-scale deployments run. On sizing: 10 billion vectors at 1,024 dimensions in float32 is 4 kilobytes each, so about 40 terabytes raw, which makes memory the binding constraint here. Latency has slack — 50 milliseconds is generous for an approximate lookup — and 200 million changes a day is about 2 percent, which is an ingest-volume question rather than a throughput one. I'd shard the index across machines and replicate for availability, and keep an eye on recall.


---

## Answer `W6`

**Item prompt as given to the candidate:**

> Same 70-billion-parameter model, eight nodes of eight H100s. 95 percent of requests carry about 2,000 tokens of context; 5 percent carry about 100,000. At the daily peak, the long requests push the short ones out of cache and p99 time-to-first-token on the short traffic triples. Before you design anything: what exactly are you protecting, and what is the first number you would want?

**Axes to score (only these):** `requirements_scoping`, `capacity_cost_estimation`

**Candidate transcript:**

**CANDIDATE:** The problem is that a fixed batch size makes time-to-first-token depend on batch fill rather than on compute. 70 billion parameters in bfloat16 is 140 gigabytes of weights; across four H100s at 3.35 terabytes per second that is roughly 13 terabytes per second aggregate, so one decode step floors near 10 milliseconds, and that same step serves the whole batch. So I would move to continuous batching and size the admission window at 20 to 25 milliseconds against the budget, rather than picking a batch size. The trade-off is explicit: a wider window buys throughput and spends tail latency, and at this target I spend throughput. I would track p99 time-to-first-token and inter-token latency as separate series.
