"""Offline tests (no API key). Run: python -m pytest -q"""
import pytest

from lesson_agent import mock_llm
from lesson_agent.graph import build_graph, new_run_state
from lesson_agent.inject import inject
from lesson_agent.memory import Memory
from lesson_agent.rubric import run_deterministic
from lesson_agent.sources import load_source_pack

GOOD = mock_llm._GOOD


def by_id(results):
    return {r.id: r for r in results}


def test_good_lesson_passes_all_deterministic_checks():
    res = by_id(run_deterministic(GOOD))
    assert all(r.passed for r in res.values()), [ (r.id, r.reason) for r in res.values() if not r.passed]


def test_jargon_injection_is_caught():
    bad, _ = inject(GOOD, "jargon")
    res = by_id(run_deterministic(bad))
    assert not res["D5"].passed and "HNSW" in res["D5"].reason
    assert not res["D6"].passed


def test_hard_vocabulary_is_caught():
    bad, _ = inject(GOOD, "vocabulary")
    res = by_id(run_deterministic(bad))
    assert not res["D4"].passed


def test_missing_section_is_caught():
    bad = GOOD.replace("## Check Yourself", "## Some Questions")
    res = by_id(run_deterministic(bad))
    assert not res["D1"].passed and not res["D9"].passed


def test_long_sentence_is_caught():
    long = " ".join(["the model reads the text"] * 10) + "."
    res = by_id(run_deterministic(GOOD.replace("## Quick Recap", long + "\n\n## Quick Recap")))
    assert not res["D3"].passed


def test_source_pack_loads():
    pack = load_source_pack("Introduction to RAG")
    assert len(pack.facts) >= 30 and len(pack.misconceptions) >= 5 and len(pack.key_points) == 7


@pytest.mark.parametrize("mode", [None, "factual"])
def test_full_loop_terminates_and_ships(tmp_path, mode):
    mem = Memory(tmp_path / "m.db")
    g = build_graph(mock_llm.MockLLM(), mem)
    st = g.invoke(new_run_state("Introduction to RAG", mode), {"recursion_limit": 50})
    assert st["status"] == "shipped"
    assert 1 < st["attempt"] <= 3  # first draft is rejected, retry fixes it
    first = {r["id"]: r["passed"] for r in st["history"][0]["results"]}
    if mode == "factual":
        assert first["J1"] is False  # evaluator caught the planted misconception


def test_memory_learns_rule_after_repeated_failures(tmp_path):
    mem = Memory(tmp_path / "m.db")
    for _ in range(2):
        build_graph(mock_llm.MockLLM(), mem).invoke(new_run_state("Introduction to RAG"), {"recursion_limit": 50})
    assert mem.active_rules(), "a rule should be distilled after the same check failed twice"


def test_injected_failures_do_not_teach_memory(tmp_path):
    mem = Memory(tmp_path / "m.db")
    build_graph(mock_llm.MockLLM(), mem).invoke(new_run_state("Introduction to RAG", "factual"), {"recursion_limit": 50})
    assert "J1" not in mem.failure_counts()
