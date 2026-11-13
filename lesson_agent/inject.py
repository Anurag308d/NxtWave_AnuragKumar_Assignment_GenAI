"""Deliberate error injection, used to PROVE the evaluator works (demo + tests).

The injected text is planted into the first generated draft. The evaluator
must reject the draft and name the problem; the regenerate step must then
remove it. Injected attempts are excluded from memory learning.
"""
from __future__ import annotations

import re

INJECTIONS = {
    # Classic misconceptions M01 + M02 + M03 -> must be caught by J1 (factual accuracy)
    "factual": ("How Does It Work",
                "Here is the secret: RAG works by retraining the language model on your documents every time "
                "you ask a question. This permanently changes what the model knows, so it never makes a mistake again."),
    # Unexplained jargon + unexpanded acronym -> must be caught by D5 + D6 (and usually J5)
    "jargon": ("How Does It Work",
               "Behind the scenes, the retriever runs cosine similarity over a dense HNSW index to rank the candidates."),
    # Hard vocabulary -> must be caught by D4 (and usually D2/D3)
    "vocabulary": ("Why Does It Matter",
                   "Furthermore, organisations leverage this paradigm to facilitate robust and seamless knowledge "
                   "utilisation, thereby ascertaining comprehensive coverage of multifaceted enterprise corpora."),
}


def inject(lesson: str, mode: str = "factual") -> tuple[str, list[str]]:
    modes = list(INJECTIONS) if mode == "all" else [m.strip() for m in mode.split(",")]
    planted = []
    for m in modes:
        if m not in INJECTIONS:
            raise ValueError(f"Unknown injection mode '{m}'. Use one of {list(INJECTIONS)} or 'all'.")
        heading, text = INJECTIONS[m]
        # insert right after the first paragraph under the target heading
        pat = re.compile(rf"(^#{{1,3}}[^\n]*{re.escape(heading)}[^\n]*\n+(?:[^\n]+\n)*?[^\n]+\n)", re.I | re.M)
        new, n = pat.subn(lambda mm: mm.group(1) + "\n" + text + "\n", lesson, count=1)
        lesson = new if n else lesson + "\n\n" + text + "\n"
        planted.append(f"[{m}] {text}")
    return lesson, planted
