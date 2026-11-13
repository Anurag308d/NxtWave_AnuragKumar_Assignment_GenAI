"""Persistent, self-evolving memory (SQLite, one file, survives across runs).

What it stores
  runs           - one row per pipeline run (topic, attempts, shipped or not)
  check_events   - every check result of every attempt (the raw evaluation log)
  learned_rules  - "lessons learned" injected into the GENERATOR prompt
                   (source = 'auto' when distilled from repeated failures,
                    source = 'human' when a reviewer adds feedback)
  judge_examples - concrete past failures shown to the EVALUATOR, so the rubric
                   gets sharper (it learns what a real failure looks like)

How it evolves
  After each run, any check that has failed >= RULE_PROMOTION_THRESHOLD times
  in total and has no active rule yet gets a new rule, distilled by an LLM from
  the actual failure reasons. Rules that keep failing after promotion get
  re-distilled (rule v2 replaces v1). Rules that have been applied in several
  runs with zero failures of their check stay active as proven rules.
"""
from __future__ import annotations

import json
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs(
  id TEXT PRIMARY KEY, ts REAL, topic TEXT, attempts INT, shipped INT,
  final_failed TEXT, injected TEXT, usage TEXT);
CREATE TABLE IF NOT EXISTS check_events(
  run_id TEXT, attempt INT, check_id TEXT, passed INT, reason TEXT, evidence TEXT, ts REAL,
  injected INT DEFAULT 0);
CREATE TABLE IF NOT EXISTS learned_rules(
  id INTEGER PRIMARY KEY AUTOINCREMENT, check_id TEXT, rule TEXT, source TEXT,
  active INT DEFAULT 1, version INT DEFAULT 1, created_ts REAL, times_applied INT DEFAULT 0,
  fails_since_created INT DEFAULT 0);
CREATE TABLE IF NOT EXISTS judge_examples(
  id INTEGER PRIMARY KEY AUTOINCREMENT, check_id TEXT, example TEXT, ts REAL);
"""


class Memory:
    def __init__(self, path: Path | str = config.MEMORY_DB):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._db() as db:
            db.executescript(SCHEMA)

    @contextmanager
    def _db(self):
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        try:
            yield con
            con.commit()
        finally:
            con.close()

    # ------------------------------------------------------------- reads ---
    def active_rules(self) -> list[dict]:
        with self._db() as db:
            rows = db.execute("SELECT * FROM learned_rules WHERE active=1 ORDER BY id DESC LIMIT ?",
                              (config.MAX_ACTIVE_RULES,)).fetchall()
        return [dict(r) for r in rows]

    def judge_examples(self) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        with self._db() as db:
            for r in db.execute("SELECT check_id, example FROM judge_examples ORDER BY id DESC"):
                lst = out.setdefault(r["check_id"], [])
                if len(lst) < config.MAX_JUDGE_EXAMPLES_PER_CHECK:
                    lst.append(r["example"])
        return out

    def failure_counts(self) -> dict[str, int]:
        with self._db() as db:
            rows = db.execute("SELECT check_id, COUNT(*) n FROM check_events WHERE passed=0 AND injected=0 GROUP BY check_id").fetchall()
        return {r["check_id"]: r["n"] for r in rows}

    def recent_failure_reasons(self, check_id: str, limit: int = 6) -> list[str]:
        with self._db() as db:
            rows = db.execute("SELECT reason, evidence FROM check_events WHERE check_id=? AND passed=0 AND injected=0 "
                              "ORDER BY ts DESC LIMIT ?", (check_id, limit)).fetchall()
        return [f"{r['reason']} | evidence: {r['evidence'][:300]}" for r in rows]

    def stats(self) -> dict:
        with self._db() as db:
            runs = [dict(r) for r in db.execute("SELECT id, ts, topic, attempts, shipped, final_failed, injected FROM runs ORDER BY ts")]
            rules = [dict(r) for r in db.execute("SELECT * FROM learned_rules ORDER BY id")]
            per_attempt = [dict(r) for r in db.execute(
                "SELECT run_id, attempt, SUM(1-passed) AS fails FROM check_events GROUP BY run_id, attempt ORDER BY ts")]
        return {"runs": runs, "rules": rules, "failure_counts": self.failure_counts(), "per_attempt": per_attempt}

    # ------------------------------------------------------------ writes ---
    def log_attempt(self, run_id: str, attempt: int, results: list[dict], injected: bool = False) -> None:
        """Store every check result. Attempts with a deliberately injected error
        are logged (for the audit trail) but NOT learned from, so demo runs do
        not pollute the self-evolving rules."""
        now = time.time()
        with self._db() as db:
            db.executemany(
                "INSERT INTO check_events VALUES (?,?,?,?,?,?,?,?)",
                [(run_id, attempt, r["id"], int(r["passed"]), r["reason"], json.dumps(r.get("evidence", []))[:2000],
                  now, int(injected)) for r in results])
            if injected:
                return
            for r in results:
                if not r["passed"]:
                    db.execute("UPDATE learned_rules SET fails_since_created = fails_since_created + 1 "
                               "WHERE active=1 AND check_id=?", (r["id"],))
                    if r["kind"] == "llm" and r.get("evidence"):
                        db.execute("INSERT INTO judge_examples(check_id, example, ts) VALUES (?,?,?)",
                                   (r["id"], f"{r['reason']} Evidence: {'; '.join(r['evidence'])[:400]}", now))

    def mark_rules_applied(self, rule_ids: list[int]) -> None:
        if not rule_ids:
            return
        with self._db() as db:
            db.executemany("UPDATE learned_rules SET times_applied = times_applied + 1 WHERE id=?",
                           [(i,) for i in rule_ids])

    def log_run(self, run_id: str, topic: str, attempts: int, shipped: bool, final_failed: list[str],
                injected: str | None, usage: dict) -> None:
        with self._db() as db:
            db.execute("INSERT OR REPLACE INTO runs VALUES (?,?,?,?,?,?,?,?)",
                       (run_id, time.time(), topic, attempts, int(shipped), json.dumps(final_failed),
                        injected or "", json.dumps(usage)))

    def add_rule(self, check_id: str, rule: str, source: str = "auto") -> int:
        with self._db() as db:
            prev = db.execute("SELECT MAX(version) v FROM learned_rules WHERE check_id=?", (check_id,)).fetchone()["v"] or 0
            db.execute("UPDATE learned_rules SET active=0 WHERE check_id=? AND source='auto' AND ?='auto'",
                       (check_id, source))
            cur = db.execute("INSERT INTO learned_rules(check_id, rule, source, version, created_ts) VALUES (?,?,?,?,?)",
                             (check_id, rule, source, prev + 1, time.time()))
            return cur.lastrowid

    def checks_needing_rules(self) -> list[str]:
        """Checks that failed often enough and either have no auto rule, or whose
        auto rule did not stop the failures (so it should be rewritten)."""
        counts = self.failure_counts()
        active = {r["check_id"]: r for r in self.active_rules()}
        need = []
        for cid, n in counts.items():
            if n < config.RULE_PROMOTION_THRESHOLD:
                continue
            rule = active.get(cid)
            if rule is None:
                need.append(cid)
            elif rule["source"] == "auto" and rule["fails_since_created"] >= config.RULE_PROMOTION_THRESHOLD + 1:
                need.append(cid)  # rule is not working -> re-distil (v2, v3 ...)
        return need

    def reset(self) -> None:
        self.path.unlink(missing_ok=True)
        with self._db() as db:
            db.executescript(SCHEMA)
