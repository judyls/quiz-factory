# RESEARCH NOTES — competitive and pricing facts

**Gathered 2026-11-16 via web search. Re-verify every number on the vendor's own page
before putting it in public copy or a pricing decision.** Most of this came from
third-party aggregators and affiliate comparison sites, which are frequently stale, and
several sources contradicted each other.

---

## 1. The system design incumbent: Hello Interview

- Official pricing page showed **1-month access ~$47** (struck from $59) and **lifetime
  ~$279** (struck from $349), covering System Design, Low-Level Design, Concurrency, and
  Behavioral courses plus Guided Practice. The page carried no date.
- Reviews from around October 2026 describe it as **one-time purchase, not auto-renewing**,
  with a free core and Premium from ~$47.
- A separate source described **session-based pricing** — mini-sessions ~$50, standard
  sessions ~$90–120 — which most likely refers to their **human mock-interview coaching**
  rather than the course. Treat as the human-mock anchor.
- "Up to 20% off" promotions appear regularly, so effective prices run lower.

**Why it matters:** this is the credibility anchor and the price ceiling. Their model is
*courses + human mocks*. Human mocks don't scale, cost ~$90–120, and can't be taken at 11pm
the night before an onsite. That's the gap.

Sources: [hellointerview.com/pricing](https://hellointerview.com/pricing) ·
[hellointerview.com/premium](https://hellointerview.com/premium) ·
[Hello Interview pricing 2026](https://prachub.com/resources/hellointerview-pricing) ·
[Hello Interview review 2026](https://prachub.com/resources/hellointerview-review-2026) ·
[systemdesignhandbook.com](https://www.systemdesignhandbook.com/?p=2799) ·
[Exponent vs Hello Interview](https://prachub.com/resources/exponent-vs-hello-interview)

---

## 2. The AI mock-interview field: cheap, crowded, and **not doing system design**

Pricing observed across the category:

| Tool | Reported price |
| --- | --- |
| Mock Interview: AI Coach (iOS) | Free trial (3 interviews); Pro $7.99/mo (60 credits), $59.99/yr (900 credits) |
| Huru | from ~$8.25/mo annual |
| Final Round AI | free first mock; ~$59.50/mo Pro (billing complaints noted in reviews) |
| Verve AI | Standard listed at $14.45/yr flat, 5 copilot sessions + unlimited mock interviews |
| Mockin 2.0 | $9 one-time 24-hour pass; $25/mo |
| Interviewing.io | freemium, generous free tier, positioned premium; per-session pricing not listed |

**The key finding — this is the whole wedge:** these tools are overwhelmingly **behavioral
and general-role**. One roundup explicitly notes a tool's scenario list excludes coding and
system design rounds. Interviewing.io was the only one flagged as technical and
engineer-focused.

So: **AI mocks exist and are cheap, but not for system design. System design prep exists and
is credible, but its mocks are human and expensive.** Nothing occupies the overlap, and the
AI-infra flavor of it is emptier still.

One roundup noted its prices were checked in October 2026 and change often.

Sources: [Best AI mock interview tools 2026](https://favtutor.com/best-ai-mock-interview-tools-2026/) ·
[Best AI interview prep tools 2026](https://fast.io/resources/best-ai-interview-prep-tools-2026/) ·
[Mock Interview: AI Coach](https://apps.apple.com/app/id6777384270) ·
[Huru](https://www.itechguides.com/products/huru/) ·
[Final Round AI](https://1-1uh.pages.dev/blog/finalround-ai/) ·
[Verve AI pricing](https://www.capterra.com/p/10034349/Verve-AI-Interview-Copilot/) ·
[Mockin 2.0 pricing](https://toolradar.com/tools/mockin-2-0/pricing) ·
[Interviewing.io pricing](https://toolradar.com/tools/interviewing-io/pricing)

---

## 3. What frontier-lab system design rounds reportedly ask

**All of this is from third-party prep and aggregator sites, not official company sources.
Treat as reported, never as confirmed, and never claim in copy that a named company asks a
specific question.**

Recurring Anthropic-associated themes:
- **Inference batching** — "design an inference batching system," including a reported
  variant with a 100ms batch target, explicit capacity math, overload control, and
  multi-model scheduling.
- **Model serving infrastructure** — described as a frequent question.
- **Low-latency GPU inference APIs** — multi-tenancy, SLO/SLI definition, model rollout,
  observability, cost control, and follow-ups probing GPU throughput and memory efficiency
  without missing latency targets.

OpenAI-associated (thinner evidence):
- A **GPU credit management system**.
- **Design the OpenAI Playground**.
- LLM serving infrastructure appears in generic roundups without sourcing.

**Two observations that shape the product:**

1. One guide notes the questions use **AI framing over classic infrastructure cores** —
   "GPU cluster," "inference batch," "model binary," but the underlying skills are capacity
   math, queueing, backpressure, multi-tenancy, consistency. This is the honest
   differentiator: teach the framing, drill the judgment.
2. Anthropic's question bank is described as **small relative to big tech but expanding**.
   A small bank means deep coverage is achievable — 40 well-built scenarios can plausibly
   cover the space, which is not true for a FAANG-wide product.

**Competitive warning:** `prachub.com` is already indexing company-specific ML system design
questions at the individual-question level. The list is not defensible. The rubric, the
calibrated grader, and the worked at-bar answers are.

Sources: [Anthropic system design interview (Exponent)](https://www.tryexponent.com/blog/anthropic-system-design-interview) ·
[Anthropic system design interview (Educative)](https://www.educative.io/blog/anthropic-system-design-interview) ·
[What to expect in the Anthropic system design interview](https://www.designgurus.io/answers/detail/what-to-expect-in-the-anthropic-system-design-interview) ·
[systemdesignhandbook.com Anthropic guide](https://www.systemdesignhandbook.com/guides/anthropic-system-design-interview/) ·
[Anthropic ML system design questions](https://prachub.com/companies/anthropic/categories/ml-system-design) ·
[Design a low-latency GPU inference service](https://prachub.com/interview-questions/design-a-low-latency-gpu-inference-service) ·
[Design a batched LLM inference service](https://prachub.com/interview-questions/design-a-batched-llm-inference-service-assuming-each-batch-takes-100-ms) ·
[AI engineer interview questions](https://www.tryexponent.com/blog/ai-engineer-interview-questions)

---

## 4. Summary for the GTM agent

| Fact | Implication |
| --- | --- |
| System design prep anchors at $47–$279 one-time | A $89 sprint and $249 lifetime are credible, not cheap-looking |
| Human mocks cost $90–120/session | Unlimited AI mocks at $89/month is an easy comparison to win |
| AI mock tools are $8–60/mo and behavioral | Don't price against them; you're not in their category |
| Nobody does AI-infra system design mocks | The wedge is real, and narrow enough to own |
| Frontier-lab question banks are small and expanding | 40 deep scenarios can credibly cover it |
| Aggregators already index the questions | Compete on rubric depth and worked answers, not on the list |
| Buyer's stake is a six-figure level band | Price with confidence; under-pricing reads as low quality |
