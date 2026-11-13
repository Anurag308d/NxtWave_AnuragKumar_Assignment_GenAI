"""The agentic workflow as an explicit LangGraph state machine.

    load_memory -> plan -> retrieve -> generate -> [inject_error] -> evaluate
                                          ^                              |
                                          |------ revise (fail) ---------|
                                                                         |
                                                    ship / human_review -+-> learn -> END

The loop always terminates: at most 1 + MAX_RETRIES generations.
"""
from __future__ import annotations

import difflib
import json
import re
import time
import uuid
from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from . import config, prompts
from .evaluator import evaluate, failures_as_feedback
from .inject import inject
from .memory import Memory
from .rubric import RUBRIC, lesson_stats
from .sources import load_source_pack, retrieve_for_outline


class State(TypedDict, total=False):
    run_id: str
    topic: str
    inject_mode: str | None
    pack: Any
    plan: dict
    retrieved: dict
    rules: list[dict]
    judge_examples: dict
    attempt: int
    lesson: str
    planted: list[str]
    results: list[dict]
    learner: dict
    history: list[dict]
    status: str          # "shipped" | "human_review"
    final_lesson: str
    new_rules: list[dict]
    events: list[str]


DEFAULT_SECTIONS = [
    {"title": "Before We Start", "goal": "motivate", "points": []},
    {"title": "What Is RAG?", "goal": "definition", "points": ["retrieve then generate", "open-book exam analogy"]},
    {"title": "Why Does It Matter?", "goal": "problem and benefits", "points": ["knowledge cutoff", "private documents", "hallucination", "no retraining", "sources"]},
    {"title": "How Does It Work?", "goal": "steps", "points": ["chunking", "embedding", "vector database", "retrieval", "augmentation", "generation"]},
    {"title": "A Full Example", "goal": "end-to-end", "points": []},
    {"title": "Where Is It Used?", "goal": "uses and limits", "points": ["support chatbots", "limits: wrong retrieval"]},
    {"title": "Key Words", "goal": "glossary", "points": []},
    {"title": "Quick Recap", "goal": "summary", "points": []},
    {"title": "Check Yourself", "goal": "quiz", "points": []},
]


def _log(state: State, msg: str) -> list[str]:
    print(f"  {msg}")
    return (state.get("events") or []) + [f"{time.strftime('%H:%M:%S')} {msg}"]


def _rules_block(rules: list[dict]) -> str:
    if not rules:
        return ""
    lines = "\n".join(f"- {r['rule']}" for r in rules)
    return f"LESSONS LEARNED FROM PAST REVIEWS (follow these too):\n{lines}\n"


def _facts_block(retrieved: dict) -> str:
    out = []
    for sec, facts in retrieved.items():
        out.append(f"## For section '{sec}':\n" + ("\n".join(facts) or "(no specific facts)"))
    return "\n".join(out)


def change_summary(prev: dict, cur_lesson: str, cur_results: list[dict]) -> dict:
    """What changed between two attempts, measured, not guessed."""
    prev_status = {r["id"]: r["passed"] for r in prev["results"]}
    cur_status = {r["id"]: r["passed"] for r in cur_results}
    fixed = [c for c in cur_status if not prev_status.get(c, True) and cur_status[c]]
    still = [c for c in cur_status if not prev_status.get(c, True) and not cur_status[c]]
    new = [c for c in cur_status if prev_status.get(c, True) and not cur_status[c]]
    # Were the exact offending sentences removed?
    quotes = []
    for r in prev["results"]:
        if r["passed"]:
            continue
        for ev in r.get("evidence", [])[:4]:
            q = re.sub(r"^\W+|\s*\(.*?\)\s*$|\s*->.*$", "", ev).strip().strip('"')
            if len(q.split()) >= 4:
                quotes.append({"check": r["id"], "quote": q[:160],
                               "now": "removed/rewritten" if q[:60].lower() not in cur_lesson.lower() else "STILL PRESENT"})
    d = list(difflib.unified_diff(prev["lesson"].splitlines(), cur_lesson.splitlines(), lineterm="", n=0))
    return {"fixed": fixed, "still_failing": still, "newly_failing": new,
            "lines_added": sum(1 for l in d if l.startswith("+") and not l.startswith("+++")),
            "lines_removed": sum(1 for l in d if l.startswith("-") and not l.startswith("---")),
            "stats_before": prev["stats"], "stats_after": lesson_stats(cur_lesson), "offending_text": quotes}


def build_graph(llm, memory: Memory):
    # ------------------------------------------------------------- nodes ---
    def load_memory(state: State) -> State:
        rules = memory.active_rules()
        ex = memory.judge_examples()
        ev = _log(state, f"[memory] {len(rules)} learned rule(s) loaded for the generator; "
                         f"{sum(map(len, ex.values()))} past failure example(s) loaded for the evaluator")
        return {"rules": rules, "judge_examples": ex, "events": ev,
                "pack": load_source_pack(state["topic"]), "attempt": 0, "history": []}

    def plan(state: State) -> State:
        pack = state["pack"]
        keys = pack.key_points_text() if pack else "what it is, why it matters, how it works"
        try:
            p = llm.chat_json(prompts.PLANNER_SYSTEM,
                              prompts.PLANNER_USER.format(topic=state["topic"], learner=prompts.LEARNER_PROFILE,
                                                          key_points=keys, template=prompts.LESSON_TEMPLATE),
                              model=config.GENERATOR_MODEL, temperature=0.4, role="planner", max_tokens=2000)
            if not p.get("sections"):
                raise ValueError("empty plan")
        except Exception as e:  # never let planning failure kill the run
            p = {"title": f"Introduction to {state['topic']}", "sections": DEFAULT_SECTIONS,
                 "analogy": "open-book exam", "running_example": "a college rulebook chatbot", "terms_to_define": []}
            print(f"  [plan] planner failed ({e}); using default outline")
        ev = _log(state, f"[plan] '{p.get('title')}' with {len(p['sections'])} sections; analogy: {p.get('analogy', '')[:80]}")
        return {"plan": p, "events": ev}

    def retrieve(state: State) -> State:
        pack = state["pack"]
        if not pack:
            ev = _log(state, "[retrieve] no source pack for this topic -> lesson will be UNGROUNDED (flagged)")
            return {"retrieved": {}, "events": ev}
        r = retrieve_for_outline(pack, state["plan"]["sections"])
        n = len({f for v in r.values() for f in v})
        ev = _log(state, f"[retrieve] {n} distinct source facts retrieved across {len(r)} sections (BM25)")
        return {"retrieved": r, "events": ev}

    def generate(state: State) -> State:
        attempt = state["attempt"] + 1
        pack = state["pack"]
        common = dict(topic=state["topic"], learner=prompts.LEARNER_PROFILE,
                      misconceptions=pack.misconceptions_text() if pack else "(none)",
                      style=prompts.STYLE_RULES, template=prompts.LESSON_TEMPLATE,
                      learned_rules=_rules_block(state.get("rules", [])))
        if attempt == 1:
            user = prompts.GENERATOR_USER.format(plan=json.dumps(state["plan"], indent=1, ensure_ascii=False),
                                                 facts=_facts_block(state["retrieved"]), **common)
            label = "generate"
        else:
            prev = state["history"][-1]
            user = prompts.REVISE_USER.format(failures=failures_as_feedback_from_dicts(prev["results"]),
                                              facts=pack.facts_text() if pack else "", lesson=prev["lesson"], **common)
            label = f"regenerate (retry {attempt - 1}/{config.MAX_RETRIES})"
        lesson = llm.chat(prompts.GENERATOR_SYSTEM, user, model=config.GENERATOR_MODEL,
                          temperature=config.GENERATOR_TEMPERATURE, role="generator", max_tokens=4096)
        lesson = re.sub(r"^```(?:markdown|md)?\s*|\s*```$", "", lesson.strip())
        ev = _log(state, f"[{label}] attempt {attempt}: {lesson_stats(lesson)['words']} words")
        return {"lesson": lesson, "attempt": attempt, "planted": [], "events": ev}

    def inject_error(state: State) -> State:
        lesson, planted = inject(state["lesson"], state["inject_mode"])
        ev = _log(state, f"[inject] planted {len(planted)} deliberate error(s) into attempt {state['attempt']}")
        return {"lesson": lesson, "planted": planted, "events": ev}

    def evaluate_node(state: State) -> State:
        results, learner = evaluate(llm, state["lesson"], state["topic"], state["pack"], state.get("judge_examples", {}))
        rd = [r.to_dict() for r in results]
        failed = [r.id for r in results if not r.passed]
        rec = {"attempt": state["attempt"], "lesson": state["lesson"], "results": rd, "learner": learner,
               "planted": state.get("planted", []), "stats": lesson_stats(state["lesson"]),
               "verdict": "PASS" if not failed else "REJECT"}
        if state["history"]:
            rec["changes"] = change_summary(state["history"][-1], state["lesson"], rd)
        memory.log_attempt(state["run_id"], state["attempt"], rd, injected=bool(state.get("planted")))
        ev = _log(state, f"[evaluate] attempt {state['attempt']}: {len(results) - len(failed)}/{len(results)} checks passed"
                         + (f" -> REJECTED ({', '.join(failed)})" if failed else " -> PASSED"))
        return {"results": rd, "learner": learner, "history": state["history"] + [rec], "events": ev}

    def ship(state: State) -> State:
        ev = _log(state, f"[ship] lesson passed all {len(RUBRIC)} checks on attempt {state['attempt']}")
        return {"status": "shipped", "final_lesson": state["lesson"], "events": ev}

    def human_review(state: State) -> State:
        best = min(state["history"], key=lambda h: (sum(1 for r in h["results"] if not r["passed"]), -h["attempt"]))
        ev = _log(state, f"[human_review] retries exhausted; best = attempt {best['attempt']} -> NOT shipped, flagged for a human")
        return {"status": "human_review", "final_lesson": best["lesson"], "events": ev}

    def learn(state: State) -> State:
        memory.mark_rules_applied([r["id"] for r in state.get("rules", [])])
        new_rules = []
        for cid in memory.checks_needing_rules():
            name, _, _, desc = RUBRIC[cid]
            reasons = "\n".join(f"- {x}" for x in memory.recent_failure_reasons(cid))
            try:
                out = llm.chat_json(prompts.DISTILL_SYSTEM,
                                    prompts.DISTILL_USER.format(check_id=cid, check_name=name, check_desc=desc, reasons=reasons),
                                    model=config.EVALUATOR_MODEL, temperature=0.2, role="distiller", max_tokens=300)
                rule = str(out.get("rule", "")).strip()
            except Exception as e:
                print(f"  [learn] could not distil rule for {cid}: {e}")
                continue
            if rule:
                memory.add_rule(cid, rule, "auto")
                new_rules.append({"check_id": cid, "rule": rule})
        failed = [r["id"] for r in state["results"] if not r["passed"]]
        memory.log_run(state["run_id"], state["topic"], state["attempt"], state["status"] == "shipped", failed,
                       state.get("inject_mode"), getattr(llm, "usage", None).__dict__ if getattr(llm, "usage", None) else {})
        ev = _log(state, f"[learn] {len(new_rules)} new rule(s) learned from repeated failures" +
                  "".join(f"\n      + ({r['check_id']}) {r['rule']}" for r in new_rules))
        return {"new_rules": new_rules, "events": ev}

    # ----------------------------------------------------------- routing ---
    def after_generate(state: State) -> str:
        return "inject_error" if state.get("inject_mode") and state["attempt"] == 1 else "evaluate"

    def after_evaluate(state: State) -> str:
        if all(r["passed"] for r in state["results"]):
            return "ship"
        if state["attempt"] >= 1 + config.MAX_RETRIES:
            return "human_review"
        return "generate"

    g = StateGraph(State)
    for name, fn in [("load_memory", load_memory), ("plan", plan), ("retrieve", retrieve), ("generate", generate),
                     ("inject_error", inject_error), ("evaluate", evaluate_node), ("ship", ship),
                     ("human_review", human_review), ("learn", learn)]:
        g.add_node(name, fn)
    g.set_entry_point("load_memory")
    g.add_edge("load_memory", "plan")
    g.add_edge("plan", "retrieve")
    g.add_edge("retrieve", "generate")
    g.add_conditional_edges("generate", after_generate, {"inject_error": "inject_error", "evaluate": "evaluate"})
    g.add_edge("inject_error", "evaluate")
    g.add_conditional_edges("evaluate", after_evaluate, {"ship": "ship", "human_review": "human_review", "generate": "generate"})
    g.add_edge("ship", "learn")
    g.add_edge("human_review", "learn")
    g.add_edge("learn", END)
    return g.compile()


def failures_as_feedback_from_dicts(results: list[dict]) -> str:
    from .rubric import CheckResult
    return failures_as_feedback([CheckResult(**r) for r in results])


def new_run_state(topic: str, inject_mode: str | None = None) -> State:
    return {"run_id": time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:4], "topic": topic,
            "inject_mode": inject_mode, "events": []}
