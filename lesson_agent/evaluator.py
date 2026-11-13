"""Evaluator agent: runs the full rubric on one lesson draft.

Order: cheap deterministic checks first, then the LLM judge and the simulated
learner. All checks always run (no early exit) so the regenerator gets the
COMPLETE list of problems in one go, which saves retries.
"""
from __future__ import annotations

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
        results.append(_to_result(cid, judge.get(cid)))

    learner = llm.chat_json(
        prompts.LEARNER_SYSTEM,
        prompts.LEARNER_USER.format(lesson=lesson, judge_memory=_judge_memory_block(judge_examples, ["J5"])),
        model=config.EVALUATOR_MODEL, temperature=config.EVALUATOR_TEMPERATURE, role="learner", max_tokens=2000)
    confusions = learner.get("confusions") or []
    blocking = [c for c in confusions if str(c.get("severity", "")).lower().startswith("block")]
    understood = bool(learner.get("understood_main_idea", True))
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
            f"No blocking confusion ({len(confusions)} minor). Learner summary: {learner.get('ravi_explains_it', '')}",
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
