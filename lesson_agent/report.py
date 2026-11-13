"""Write the run outputs: final lesson, every attempt, rejection log (md + json)."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from . import config
from .rubric import RUBRIC


def _mark(p: bool) -> str:
    return "PASS" if p else "**FAIL**"


def rejection_log_md(state: dict) -> str:
    h = state["history"]
    out = [f"# Rejection Log: {state['topic']}", "",
           f"- Run ID: `{state['run_id']}`",
           f"- Final status: **{'SHIPPED' if state['status'] == 'shipped' else 'NOT SHIPPED (flagged for human review)'}**",
           f"- Attempts: {len(h)} (max {1 + config.MAX_RETRIES})",
           f"- Deliberate error injection: {state.get('inject_mode') or 'off'}",
           f"- Learned rules applied from memory: {len(state.get('rules', []))}", ""]
    if state.get("rules"):
        out.append("## Rules applied from memory (self-evolving prompt)")
        out += [f"- ({r['check_id']}, {r['source']}, v{r['version']}) {r['rule']}" for r in state["rules"]] + [""]

    out += ["## Summary across attempts", "", "| Check | Dimension | " + " | ".join(f"Attempt {x['attempt']}" for x in h) + " |",
            "|---|---|" + "---|" * len(h)]
    for cid, (name, dim, kind, _) in RUBRIC.items():
        row = [next(r for r in x["results"] if r["id"] == cid)["passed"] for x in h]
        out.append(f"| {cid} {name} | {dim} | " + " | ".join(_mark(p) for p in row) + " |")
    out.append("")

    for x in h:
        failed = [r for r in x["results"] if not r["passed"]]
        out += [f"## Attempt {x['attempt']}: {x['verdict']}", "",
                f"Stats: {x['stats']['words']} words, Flesch {x['stats']['flesch_reading_ease']}, "
                f"avg sentence {x['stats']['avg_sentence_words']} words.", ""]
        if x.get("planted"):
            out += ["**Deliberately injected errors (to test the evaluator):**"] + [f"- {p}" for p in x["planted"]] + [""]
        if not failed:
            out += ["All checks passed.", ""]
        for r in failed:
            out += [f"### {r['id']} {r['name']}: FAILED", f"- Why: {r['reason']}"]
            out += [f"- Evidence: {e}" for e in r["evidence"][:6]]
            if r.get("fix"):
                out.append(f"- Fix requested: {r['fix']}")
            out.append("")
        if x.get("changes"):
            c = x["changes"]
            out += ["### What changed on this retry",
                    f"- Fixed checks: {', '.join(c['fixed']) or 'none'}",
                    f"- Still failing: {', '.join(c['still_failing']) or 'none'}",
                    f"- Newly failing (regressions): {', '.join(c['newly_failing']) or 'none'}",
                    f"- Lines added / removed: {c['lines_added']} / {c['lines_removed']}",
                    f"- Stats before -> after: {c['stats_before']} -> {c['stats_after']}"]
            out += [f"- Offending text from {q['check']}: \"{q['quote']}\" -> {q['now']}" for q in c["offending_text"][:8]]
            out.append("")
    if state.get("new_rules"):
        out += ["## New rules learned after this run"] + [f"- ({r['check_id']}) {r['rule']}" for r in state["new_rules"]] + [""]
    out += ["## Event trace", "```"] + state.get("events", []) + ["```"]
    return "\n".join(out)


def write_outputs(state: dict) -> Path:
    d = config.OUTPUTS_DIR / state["run_id"]
    (d / "attempts").mkdir(parents=True, exist_ok=True)
    banner = "" if state["status"] == "shipped" else (
        "> **NOT SHIPPED.** This is the best attempt after all retries; see rejection_log.md.\n\n")
    (d / "lesson_final.md").write_text(banner + state["final_lesson"], encoding="utf-8")
    for x in state["history"]:
        (d / "attempts" / f"attempt_{x['attempt']}.md").write_text(x["lesson"], encoding="utf-8")
    (d / "rejection_log.md").write_text(rejection_log_md(state), encoding="utf-8")
    slim = {k: state.get(k) for k in ("run_id", "topic", "inject_mode", "status", "plan", "rules", "new_rules", "events")}
    slim["attempts"] = [{k: v for k, v in x.items() if k != "lesson"} for x in state["history"]]
    (d / "run.json").write_text(json.dumps(slim, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    latest = config.OUTPUTS_DIR / "latest"
    shutil.rmtree(latest, ignore_errors=True)
    shutil.copytree(d, latest)
    return d
