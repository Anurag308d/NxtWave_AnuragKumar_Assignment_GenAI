"""Grounding: load the curated source pack and retrieve the facts relevant to
each lesson section with a tiny BM25 retriever (pure Python, no vector DB
needed for ~40 facts). Yes, the lesson about RAG is itself built with RAG."""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

from . import config

_STOP = set("""a an the of to and or in on for is are be by with as it this that from at its
into not only than then so do does how what why when which their there these those can""".split())


@dataclass
class Fact:
    id: str
    tag: str
    text: str

    def line(self) -> str:
        return f"[{self.id}] {self.text}"


@dataclass
class SourcePack:
    topic_slug: str
    facts: list[Fact]
    misconceptions: list[Fact]
    key_points: list[Fact]

    def facts_text(self) -> str:
        return "\n".join(f.line() for f in self.facts)

    def misconceptions_text(self) -> str:
        return "\n".join(f.line() for f in self.misconceptions)

    def key_points_text(self) -> str:
        return "\n".join(f.line() for f in self.key_points)


def slugify(topic: str) -> str:
    t = topic.lower()
    if "rag" in re.findall(r"[a-z]+", t) or "retrieval" in t:
        return "rag"
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def load_source_pack(topic: str) -> SourcePack | None:
    path = config.SOURCES_DIR / f"{slugify(topic)}.md"
    if not path.exists():
        return None
    facts, mis, keys = [], [], []
    for raw in path.read_text(encoding="utf-8").splitlines():
        parts = [p.strip() for p in raw.split("|")]
        if len(parts) < 2:
            continue
        fid = parts[0]
        if re.fullmatch(r"F\d+", fid) and len(parts) >= 3:
            facts.append(Fact(fid, parts[1], " | ".join(parts[2:])))
        elif re.fullmatch(r"M\d+", fid):
            mis.append(Fact(fid, "misconception", " | ".join(parts[1:])))
        elif re.fullmatch(r"K\d+", fid):
            keys.append(Fact(fid, "key", " | ".join(parts[1:])))
    return SourcePack(slugify(topic), facts, mis, keys)


def _tok(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in _STOP and len(w) > 1]


class BM25:
    def __init__(self, docs: list[Fact], k1: float = 1.5, b: float = 0.75):
        self.docs = docs
        self.toks = [_tok(d.text + " " + d.tag) for d in docs]
        self.avgdl = sum(map(len, self.toks)) / max(1, len(self.toks))
        self.df = Counter(w for t in self.toks for w in set(t))
        self.N, self.k1, self.b = len(docs), k1, b

    def search(self, query: str, k: int = 6) -> list[Fact]:
        q = _tok(query)
        scores = []
        for i, toks in enumerate(self.toks):
            tf = Counter(toks)
            s = 0.0
            for w in q:
                if w not in tf:
                    continue
                idf = math.log(1 + (self.N - self.df[w] + 0.5) / (self.df[w] + 0.5))
                s += idf * tf[w] * (self.k1 + 1) / (tf[w] + self.k1 * (1 - self.b + self.b * len(toks) / self.avgdl))
            scores.append((s, i))
        scores.sort(reverse=True)
        return [self.docs[i] for s, i in scores[:k] if s > 0]


def retrieve_for_outline(pack: SourcePack, outline: list[dict], k: int = 6) -> dict[str, list[str]]:
    """Return {section_title: [fact lines]} so each section is written from its own evidence."""
    bm = BM25(pack.facts)
    out = {}
    for sec in outline:
        query = f"{sec.get('title', '')} {sec.get('goal', '')} {' '.join(sec.get('points', []))}"
        out[sec.get("title", "section")] = [f.line() for f in bm.search(query, k)]
    return out
