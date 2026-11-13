"""Command line entry point.

  python main.py run                          # generate -> evaluate -> regenerate for "Introduction to RAG"
  python main.py run --inject factual         # plant a deliberate error to show the evaluator catching it
  python main.py run --topic "..."            # any topic (grounded only if sources/<slug>.md exists)
  python main.py feedback D5 "Always define 'query' in Key Words"   # human feedback -> memory rule
  python main.py memory                       # show what the system has learned so far
  python main.py reset-memory
  python main.py graph                        # print the workflow graph (mermaid)
  add --mock to `run` to test everything offline without an API key
"""
from __future__ import annotations

import argparse
import json
import sys

from rich.console import Console
from rich.table import Table

from lesson_agent import config
from lesson_agent.graph import build_graph, new_run_state
from lesson_agent.llm import get_llm
from lesson_agent.memory import Memory
from lesson_agent.report import write_outputs
from lesson_agent.rubric import RUBRIC

console = Console()


def cmd_run(a):
    llm = get_llm(mock=a.mock)
    mem = Memory(a.memory_db) if a.memory_db else Memory()
    graph = build_graph(llm, mem)
    console.rule(f"[bold]Lesson agent: {a.topic}")
    console.print(f"generator={config.GENERATOR_MODEL}  evaluator={config.EVALUATOR_MODEL}  "
                  f"max_retries={config.MAX_RETRIES}  inject={a.inject or 'off'}  mock={a.mock}")
    state = graph.invoke(new_run_state(a.topic, a.inject), {"recursion_limit": 50})
    out = write_outputs(state)

    t = Table(title="Rubric results per attempt")
    t.add_column("Check")
    for x in state["history"]:
        t.add_column(f"Attempt {x['attempt']}")
    for cid, (name, *_r) in RUBRIC.items():
        cells = []
        for x in state["history"]:
            p = next(r for r in x["results"] if r["id"] == cid)["passed"]
            cells.append("[green]PASS" if p else "[red]FAIL")
        t.add_row(f"{cid} {name}", *cells)
    console.print(t)
    shipped = state["status"] == "shipped"
    console.print(f"[bold {'green' if shipped else 'yellow'}]{'SHIPPED' if shipped else 'NOT SHIPPED (human review)'}"
                  f"[/] after {state['attempt']} attempt(s).  Outputs: {out}")
    if hasattr(llm, "usage"):
        console.print(f"LLM calls: {llm.usage.calls}, tokens: {llm.usage.prompt_tokens + llm.usage.completion_tokens}, "
                      f"by role: {llm.usage.by_role}")
    return 0 if shipped else 2


def cmd_feedback(a):
    if a.check_id not in RUBRIC:
        console.print(f"[red]Unknown check {a.check_id}. Use one of {list(RUBRIC)}")
        return 1
    rid = Memory().add_rule(a.check_id, a.rule, source="human")
    console.print(f"Saved human rule #{rid} for {a.check_id}. It will be applied on the next run.")
    return 0


def cmd_memory(a):
    s = Memory().stats()
    t = Table(title="Runs")
    for c in ("run", "attempts", "shipped", "final failed", "inject"):
        t.add_column(c)
    for r in s["runs"]:
        t.add_row(r["id"], str(r["attempts"]), "yes" if r["shipped"] else "no", r["final_failed"], r["injected"] or "-")
    console.print(t)
    console.print("Failures per check (excluding injected demo errors):", s["failure_counts"])
    t2 = Table(title="Learned rules (self-evolving prompt)")
    for c in ("id", "check", "source", "ver", "active", "applied", "fails since", "rule"):
        t2.add_column(c)
    for r in s["rules"]:
        t2.add_row(str(r["id"]), r["check_id"], r["source"], str(r["version"]), str(r["active"]),
                   str(r["times_applied"]), str(r["fails_since_created"]), r["rule"])
    console.print(t2)
    if a.json:
        print(json.dumps(s, indent=2, default=str))
    return 0


def cmd_graph(a):
    llm = get_llm(mock=True)
    print(build_graph(llm, Memory()).get_graph().draw_mermaid())
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Self-evaluating lesson content generator")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--topic", default="Introduction to RAG (Retrieval-Augmented Generation)")
    r.add_argument("--inject", default=None, help="factual | jargon | vocabulary | all (comma list ok)")
    r.add_argument("--mock", action="store_true", help="offline mock LLM, no API key needed")
    r.add_argument("--memory-db", default=None)
    r.set_defaults(fn=cmd_run)
    f = sub.add_parser("feedback")
    f.add_argument("check_id")
    f.add_argument("rule")
    f.set_defaults(fn=cmd_feedback)
    m = sub.add_parser("memory")
    m.add_argument("--json", action="store_true")
    m.set_defaults(fn=cmd_memory)
    sub.add_parser("reset-memory").set_defaults(fn=lambda a: (Memory().reset(), console.print("memory cleared"), 0)[2])
    sub.add_parser("graph").set_defaults(fn=cmd_graph)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
