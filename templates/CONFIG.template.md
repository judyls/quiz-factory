# CONFIG — <<VERTICAL NAME>>

> Copy to `verticals/<slug>/CONFIG.md` and fill. This is the first artifact of any new
> vertical. Nothing else gets written until the gates below pass.
> Doctrine lives in `playbook/QUIZ-FACTORY.md` — read it first.

## Step 0 — Qualification gates

Score each. **Fewer than 4 of 5 strong: stop and tell the user the vertical is weak, and
why.** Do not build a quiz for a cohort that fails this.

| Gate | Score (strong / weak / none) | Evidence |
| --- | --- | --- |
| **1. Dated pain** — a specific, scheduled, high-stakes event | | |
| **2. Status at stake** — the result says something about competence they'd show others | | |
| **3. Credible rubric** — the skill scores on axes a practitioner would recognize | | |
| **4. Proven spend** — they already pay someone for this, at a price you can anchor to | | |
| **5. Public watering hole** — they congregate somewhere observable | | |

**Verdict:** `__ / 5` → build / stop

Gate 4 needs a real source — a competitor pricing page, a coaching rate, a course price.
If you can't find one, go find it before writing a single question. Never be the one
teaching a cohort that their problem is worth money.

## Config

```yaml
vertical:            # the named market
cohort:              # who precisely. Not "engineers" — a level band, a situation, a timeline
dated_pain:          # the scheduled event, and what it decides for them
status_currency:     # what the result confers, phrased as they'd say it
scored_axes:         # 4-7. Observable, not dispositional. >=1 must be communication-facing
share_artifact:      # describe the image. What does a professional attach their name to?
price_anchor:        # what they pay today, WITH a source and a date
paid_product:        # what the quiz graduates into. MUST be a practice loop, not content
retention_bridge:    # the second use of the same engine after the dated event passes
kill_metric:         # the numbers that, if unmet by week 4, mean stop
```

## Competitive gap

One paragraph: what exists, what it costs, and the specific overlap nobody occupies.
If you can't name an empty overlap, the positioning isn't ownable yet — narrow the cohort
until it is.

## The honest differentiator

The true thing you can say that a hyped competitor can't. This cohort will check.

## Kill thresholds

Set actual numbers, sourced from the prior quiz's data where it exists
(`playbook/VIRALITY-TEARDOWN.md`), not from industry averages, which are mostly fiction.

| Metric | Threshold | By when |
| --- | --- | --- |
| Quiz completion / started | | |
| Share / completion | | |
| Reveal → signup | | |
| First → second session | | |
| Free → paid | | |
