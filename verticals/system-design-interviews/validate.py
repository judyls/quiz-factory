#!/usr/bin/env python3
"""Structural and numeric-propagation checks for the content pack.

Run from this directory:  python3 validate.py

Why this exists: run 2 of the review harness found that three of the four numbers
corrected in `rubric.md` Appendix B never left it. The model answers, the grader's worked
example and one fixture still carried the superseded figures, so the pack went on teaching
numbers it had already established were wrong. Appendix B is only the source of truth if
something checks that it propagated.

The RETRACTED registry below is the mechanism. When a number in Appendix B is corrected,
add the old string here with a note. Anything that reintroduces it fails the build.
"""

import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent

AXES = [
    "requirements_scoping",
    "capacity_cost_estimation",
    "high_level_design",
    "deep_dive_failure_modes",
    "tradeoff_articulation",
    "communication_collaboration",
]

# A retracted figure, the files it must not reappear in, and why. The pattern is matched
# case-insensitively against prose. Keep the note: it is what makes a failure actionable.
RETRACTED = [
    (r"6,?000 (output )?tok(ens|/s)", "throughput: weights-only decode floor; KV-corrected is ~4,700 tok/s"),
    (r"\b112 (GPUs|H100)", "eval-infra fleet at the stale throughput; corrected is ~141"),
    (r"\$?0\.37 per million|\$0\.37/M", "token cost that follows from 6,000 tok/s; corrected is $0.47"),
    (r"floors? (around|near|at) 10(\.4)? millisecond", "decode floor omitting KV reads; corrected is ~12ms at batch 32"),
    (r"a fifth of (a )?(node|HBM|the card)", "KV-vs-node-HBM overstatement; 32.8GB is 5.1% of a 640GB node"),
    (r"most(ly)? (of which is |)(already |)holding weights", "implies >50%; weights are 35GB of each 80GB card (44%)"),
    (r"on the order of 11 hours|about 11 hours", "shuffle counting writes only; a global shuffle moves 2xS, so ~22h"),
    (r"(~|about |roughly )9 seconds", "prefill omitting attention FLOPs; corrected is ~17s at 100k"),
    (r"half a million a year|544,580", "eval-infra annual cost at the stale throughput"),
    (r"141 GPUs", "eval-infra fleet counting generation output only; with the judge call and prefill it is ~243"),
    (r"690,000|\$0\.69M", "eval-infra annual cost before the judge call and prefill were counted; ~$1.18M"),
]

# Fixtures whose premise is that they reproduce another string exactly. Checked, not trusted.
VERBATIM = [("plant-10-verbatim-model-answer", "training-data-dedup-and-shuffle", "model_answer")]

MAX_WORDS = 185  # ~60 seconds of speech


def main() -> int:
    fail: list[str] = []
    def bad(msg): fail.append(msg)

    questions = json.loads((HERE / "questions.json").read_text())["questions"]
    plants = json.loads((HERE / "calibration-plants.json").read_text())["plants"]
    qs = {q["id"]: q for q in questions}
    ps = {p["id"]: p for p in plants}
    rubric = (HERE / "rubric.md").read_text()
    prompts = (HERE / "prompts.md").read_text()

    # --- structure
    if len(questions) != 12:
        bad(f"expected 12 questions, found {len(questions)}")
    coverage = {a: 0 for a in AXES}
    for q in questions:
        for field in ("id", "persona", "track", "prompt", "terms", "good", "bad", "model_answer"):
            if not q.get(field):
                bad(f"{q['id']}: missing engine field {field!r}")
        for a in q.get("axes", []):
            if a not in coverage:
                bad(f"{q['id']}: unknown axis {a!r}")
            else:
                coverage[a] += 1
        if not re.search(r"\d", q["model_answer"]):
            bad(f"{q['id']}: model_answer contains no number — the hard rule")
        n = len(q["model_answer"].split())
        if n > MAX_WORDS:
            bad(f"{q['id']}: model_answer is {n} words, over the {MAX_WORDS}-word speech budget")
        labels = [f.get("if") for f in q.get("followups", [])]
        if len(labels) != len(set(labels)):
            bad(f"{q['id']}: duplicate followup 'if' labels {labels} — probe selection is non-deterministic")
    for a, c in coverage.items():
        if c != 4:
            bad(f"axis {a} covered by {c} items, expected 4")

    # --- plants
    for p in plants:
        if p["targets"] not in qs:
            bad(f"{p['id']}: targets unknown item {p['targets']!r}")
        for a in p.get("required_outcome", {}):
            if a not in AXES and a != "relevance_gate":
                bad(f"{p['id']}: required_outcome names unknown axis {a!r}")

    # --- fixtures that claim to be verbatim copies
    for pid, qid, field in VERBATIM:
        if pid not in ps:
            bad(f"VERBATIM: no such plant {pid!r}"); continue
        got = " ".join(t["text"] for t in ps[pid]["transcript"]).strip()
        want = qs[qid][field].strip()
        if got != want:
            bad(f"{pid} is not verbatim {qid}.{field} — its premise is that it is. "
                f"Regenerate it from the model answer rather than editing it.")

    # --- retracted figures must not reappear anywhere
    corpus = {
        "rubric.md": rubric,
        "prompts.md": prompts,
        "questions.json": json.dumps(questions, ensure_ascii=False),
        "calibration-plants.json": json.dumps(plants, ensure_ascii=False),
    }
    for pattern, note in RETRACTED:
        for fname, text in corpus.items():
            for m in re.finditer(pattern, text, re.I):
                ctx = text[max(0, m.start() - 70):m.end() + 70].replace("\n", " ")
                # Appendix B and the harness notes quote the retracted figures on purpose,
                # to show what was wrong. Those quotations are always adjacent to a marker.
                if re.search(r"not the|rather than|stale|superseded|retracted|first version|"
                             r"corrected|wrong|would be|instead of|run 2 found|was stated as|"
                             r"omitt|implies|it is \*\*|counting only|gives", ctx, re.I):
                    continue
                bad(f"{fname}: retracted figure {m.group(0)!r} reappears — {note}\n      ...{ctx}...")

    # --- rubric invariants the harness has twice found broken
    # Bands 2 and 3 are decided by a declared required clause; band 0 by a declared single
    # test; band 1 is the residual and must NOT acquire conditions. See "Band precedence".
    if (n := rubric.count("**Required:**")) != 6:
        bad(f"rubric.md has {n} band-2 '**Required:**' clauses; expected exactly 6")
    if (n := rubric.count("**Band 0 only if:**")) != 6:
        bad(f"rubric.md has {n} 'Band 0 only if:' tests; expected exactly 6 (one per axis)")
    if (n := rubric.count("**Residual —")) != 6:
        bad(f"rubric.md has {n} band-1 residual markers; expected exactly 6")
    if "score = 1" not in rubric or "band_0_test(axis)" not in rubric:
        bad("rubric.md: the band precedence block is missing")
    if "axis_score[a] = mean(" not in rubric:
        bad("rubric.md: the aggregation rule is missing")
    if "scored on the answer's final state" not in rubric:
        bad("rubric.md: no retraction rule (best state vs final state)")

    print(f"checked {len(questions)} questions, {len(plants)} plants, "
          f"{len(RETRACTED)} retracted figures, {len(VERBATIM)} verbatim fixtures")
    if fail:
        print(f"\nFAILED ({len(fail)}):", file=sys.stderr)
        for f in fail:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
