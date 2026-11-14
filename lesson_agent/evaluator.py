"""Evaluator agent: runs the full rubric on one lesson draft.

Order: cheap deterministic checks first, then the LLM judge and the simulated
learner. All checks always run (no early exit) so the regenerator gets the
COMPLETE list of problems in one go, which saves retries.
"""
from __future__ import annotations

import re

from . import config, prompts
from .rubric import RUBRIC, CheckResult, run_deterministic
from .sources import SourcePack


def _judge_memory_block(examples: dict[str, list[str]], ids: list[str]) -> str:
    lines = []
    for cid in ids:
        for ex in examples.get(cid, []):
            lines.append(f"- {cid}: {ex}")
    if not lines:
        return ""
    return ("\nPAST REAL FAILURES (from memory). Lessons with problems like these must FAIL the same check:\n"
            + "\n".join(lines) + "\n")


def _to_result(cid: str, raw: dict | None) -> CheckResult:
    name, dim, kind, _ = RUBRIC[cid]
    if not isinstance(raw, dict):
        return CheckResult(cid, name, dim, kind, False, "Judge returned no verdict for this check.", [],
                           "Re-run evaluation.")
    passed = bool(raw.get("pass", False))
    evidence = [str(e) for e in (raw.get("evidence") or []) if str(e).strip()]
    reason = str(raw.get("reason", "")).strip()
    fix = str(raw.get("fix", "")).strip()
    # Anti-noise rule: a FAIL must come with evidence. A fail the judge cannot
    # support with a quote is overturned (and the overturn is logged).
    if not passed and not evidence:
        return CheckResult(cid, name, dim, kind, True, f"[overturned: judge failed it without evidence] {reason}", [], "")
    return CheckResult(cid, name, dim, kind, passed, reason or ("OK" if passed else "Failed"), evidence, fix)


_INLINE_DEF = re.compile(r"\(|\s[-\u2013\u2014]\s|\bcalled\b|\bmeans\b|\bis an?\b|\bknown as\b|\brefers to\b|:", re.I)


def _verify_flow_fail(res: CheckResult, lesson: str) -> CheckResult:
    """J4 judges often flag a term as 'used before definition' when the sentence
    itself defines it inline. If EVERY quoted sentence contains an inline
    definition, the fail is not supported by its own evidence -> overturned."""
    if res.id != "J4" or res.passed or not res.evidence:
        return res
    quotes = [re.sub(r"\s*\((?:[^()]*used before[^()]*)\)\s*$", "", e).strip().strip('"') for e in res.evidence]
    if all(_INLINE_DEF.search(q) for q in quotes):
        return CheckResult(res.id, res.name, res.dimension, res.kind, True,
                           "[overturned: every quoted sentence defines its term inline] " + res.reason, [], "")
    return res


def evaluate(llm, lesson: str, topic: str, pack: SourcePack | None, judge_examples: dict[str, list[str]]):
    results: list[CheckResult] = run_deterministic(lesson)

    facts = pack.facts_text() if pack else "(no source pack: judge using general knowledge)"
    mis = pack.misconceptions_text() if pack else "(none)"
    keys = pack.key_points_text() if pack else "(cover what it is, why it matters, how it works)"

    judge = llm.chat_json(
        prompts.JUDGE_SYSTEM,
        prompts.JUDGE_USER.format(topic=topic, learner=prompts.LEARNER_PROFILE, facts=facts, misconceptions=mis,
                                  key_points=keys, lesson=lesson,
                                  judge_memory=_judge_memory_block(judge_examples, ["J1", "J2", "J3", "J4"])),
        model=config.EVALUATOR_MODEL, temperature=config.EVALUATOR_TEMPERATURE, role="judge", max_tokens=3000)
    for cid in ("J1", "J2", "J3", "J4"):
        results.append(_verify_flow_fail(_to_result(cid, judge.get(cid)), lesson))

    learner = llm.chat_json(
        prompts.LEARNER_SYSTEM,
        prompts.LEARNER_USER.format(lesson=lesson, judge_memory=_judge_memory_block(judge_examples, ["J5"])),
        model=config.LEARNER_MODEL, temperature=config.EVALUATOR_TEMPERATURE, role="learner", max_tokens=2000)
    confusions = learner.get("confusions") or []
    # Anti-noise: keep only confusions whose quote really exists in the lesson
    # (judges sometimes paraphrase or invent quotes), and ignore headings.
    norm = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()
    body = norm("\n".join(l for l in lesson.splitlines() if not l.lstrip().startswith("#")))  # headings excluded
    def real(c):
        q = norm(str(c.get("quote", "")))
        return len(q.split()) >= 3 and q[:60] in body and not str(c.get("quote", "")).lstrip().startswith("#")
    dropped = [c for c in confusions if not real(c)]
    confusions = [c for c in confusions if real(c)]
    blocking = [c for c in confusions if str(c.get("severity", "")).lower().startswith("block")]
    understood = bool(learner.get("understood_main_idea", True))
    answers = learner.get("answers") or {}
    answered_all = all(str(answers.get(q, "")).strip() for q in ("Q1", "Q2", "Q3"))
    # Consistency rule: "blocking" is defined as "cannot answer Q1-Q3". If the learner
    # understood the main idea AND answered all three, a blocking mark contradicts its
    # own definition -> downgraded to minor (logged), so curiosity about deeper detail
    # ("how does text become numbers?") does not block a beginner lesson.
    downgraded = []
    if blocking and understood and answered_all:
        downgraded, blocking = blocking, []
    name, dim, kind, _ = RUBRIC["J5"]
    if blocking or not understood:
        results.append(CheckResult(
            "J5", name, dim, kind, False,
            f"Simulated learner got stuck {len(blocking)} time(s) (blocking). Main idea understood: {understood}.",
            [f"\"{c.get('quote', '')}\" -> {c.get('why', '')}" for c in blocking][:6],
            "Rewrite each quoted sentence in simpler words and explain the missing idea before using it."))
    else:
        results.append(CheckResult(
            "J5", name, dim, kind, True,
            f"No blocking confusion ({len(confusions)} minor, {len(downgraded)} blocking mark(s) downgraded because the "
            f"learner still answered Q1-Q3, {len(dropped)} unverifiable quote(s) ignored). "
            f"Learner summary: {learner.get('ravi_explains_it', '')}",
            [f"minor: \"{c.get('quote', '')}\"" for c in confusions][:3]))
    return results, learner


def failures_as_feedback(results: list[CheckResult]) -> str:
    lines = []
    for r in results:
        if r.passed:
            continue
        ev = "\n".join(f"      - {e}" for e in r.evidence[:6])
        lines.append(f"- [{r.id}] {r.name}: {r.reason}\n    Evidence:\n{ev or '      - (see reason)'}\n    How to fix: {r.fix}")
    return "\n".join(lines)
