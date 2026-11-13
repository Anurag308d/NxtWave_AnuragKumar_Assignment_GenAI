"""Streamlit demo UI:  streamlit run app.py
Shows the agent loop live (node by node), the rubric per attempt, the final
lesson, the rejection log and what the memory has learned."""
import pandas as pd
import streamlit as st

from lesson_agent import config
from lesson_agent.graph import build_graph, new_run_state
from lesson_agent.llm import get_llm
from lesson_agent.memory import Memory
from lesson_agent.report import rejection_log_md, write_outputs
from lesson_agent.rubric import RUBRIC

st.set_page_config(page_title="Self-Evaluating Lesson Generator", layout="wide")
st.title("Self-Evaluating Lesson Generator")
st.caption(f"Generator: `{config.GENERATOR_MODEL}`  |  Evaluator: `{config.EVALUATOR_MODEL}`  |  "
           f"Max retries: {config.MAX_RETRIES}  |  Rubric: {len(RUBRIC)} hard pass/fail checks")

with st.sidebar:
    topic = st.text_input("Topic", "Introduction to RAG (Retrieval-Augmented Generation)")
    inject = st.multiselect("Inject a deliberate error into draft 1", ["factual", "jargon", "vocabulary"])
    mock = st.checkbox("Offline mock LLM (no API key)", value=False)
    go = st.button("Run agent", type="primary")
    st.divider()
    st.subheader("Rubric")
    for cid, (name, dim, kind, desc) in RUBRIC.items():
        st.markdown(f"**{cid}** {name}  \n<small>{dim} · {kind}</small>", unsafe_allow_html=True)

mem = Memory()

if go:
    graph = build_graph(get_llm(mock=mock), mem)
    state = new_run_state(topic, ",".join(inject) or None)
    final = dict(state)
    with st.status("Running agent loop ...", expanded=True) as box:
        for update in graph.stream(state, {"recursion_limit": 50}, stream_mode="updates"):
            for node, delta in update.items():
                final.update(delta or {})
                if delta and delta.get("events"):
                    st.write(f"`{node}` → {delta['events'][-1].split(' ', 1)[1]}")
        box.update(label=f"Done: {final['status'].upper()} after {final['attempt']} attempt(s)",
                   state="complete" if final["status"] == "shipped" else "error")
    write_outputs(final)
    st.session_state["final"] = final

final = st.session_state.get("final")
if final:
    tabs = st.tabs(["Final lesson", "Rubric per attempt", "Rejection log", "Attempts", "Memory"])
    with tabs[0]:
        if final["status"] != "shipped":
            st.warning("Not shipped: best attempt shown, flagged for human review.")
        st.markdown(final["final_lesson"])
    with tabs[1]:
        rows = []
        for cid, (name, dim, kind, _) in RUBRIC.items():
            row = {"check": f"{cid} {name}", "dimension": dim, "type": kind}
            for x in final["history"]:
                r = next(r for r in x["results"] if r["id"] == cid)
                row[f"attempt {x['attempt']}"] = "PASS" if r["passed"] else "FAIL"
            rows.append(row)
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        for x in final["history"]:
            with st.expander(f"Attempt {x['attempt']}: {x['verdict']}"):
                for r in x["results"]:
                    icon = "✅" if r["passed"] else "❌"
                    st.markdown(f"{icon} **{r['id']} {r['name']}**: {r['reason']}")
                    for e in r["evidence"][:4]:
                        if not r["passed"]:
                            st.markdown(f"> {e}")
    with tabs[2]:
        st.markdown(rejection_log_md(final))
    with tabs[3]:
        for x in final["history"]:
            with st.expander(f"Attempt {x['attempt']} ({x['stats']['words']} words, {x['verdict']})"):
                st.markdown(x["lesson"])

with st.expander("What the memory has learned (persists across runs)", expanded=not final):
    s = mem.stats()
    st.write("Failures per check (excluding injected demo errors):", s["failure_counts"])
    if s["rules"]:
        st.dataframe(pd.DataFrame(s["rules"])[["id", "check_id", "source", "version", "active", "times_applied",
                                               "fails_since_created", "rule"]], hide_index=True, use_container_width=True)
    if s["runs"]:
        st.dataframe(pd.DataFrame(s["runs"]), hide_index=True, use_container_width=True)
