# RUN 2 — answer key (off limits to reviewers)

`findings/` is off limits under the protocol, which is why this lives here. Regenerate the
set with `python3 generate-blind-set.py 2`; the mapping below is deterministic from the run
number.

| Label | Fixture | Source item |
| --- | --- | --- |
| `D4` | `plant-09-spiky` | `heterogeneous-fleet-routing` |
| `F3` | `plant-10-verbatim-model-answer` | `training-data-dedup-and-shuffle` |
| `J2` | `plant-03b-number-right-link-unstated` | `vector-index-at-10b` |
| `H4` | `plant-06-collapses-under-pushback` | `agent-retry-side-effects` |
| `P7` | `plant-08b-detour-then-on-problem` | `kv-cache-admission-control` |
| `N7` | `plant-03a-number-contradicts-design` | `vector-index-at-10b` |
| `W7` | `plant-04-correct-but-mute` | `eval-infra-per-commit-cost` |

## Why these seven

Run 1 scored five answers covering three axes. Two of the predictions this run exists to
test concern axes run 1 never scored, so the set was widened to cover all six.

- `N7` / `J2` (03a, 03b) bracket band 2 on capacity from both sides, and were in run 1 —
  they are the only answers comparable across runs.
- `D4` (09) **failed unanimously in run 1** — five reviewers scored 1,2,2,1,2 against an
  expected 3, its arithmetic was circular and its reversal threshold false under its own
  numbers. Rewritten since. This is the single most important re-test in the set.
- `F3` (10) and `H4` (06) are new: they carry `high_level_design` and
  `deep_dive_failure_modes`, which `calibration-plan.md` predicts will come back with the
  **lowest** per-axis reliability. Run 1 could not test that prediction at all.
- `P7` (08b) is the negative control added after run 1: the relevance gate must **not**
  fire. A reviewer who clamps it to 1 has reproduced the over-firing failure the control
  exists to catch.
- `W7` (04) and `H4` carry `communication_collaboration` — the axis whose bias question is
  the one queue item deliberately left for a human. What five reviewers do with it is
  evidence about the cell's clarity, **not** about the bias question.

## Expected outcomes

Held in `../../calibration-plants.json` (`required_outcome` per fixture). Deliberately not
duplicated here: a second copy is a second thing to drift.
