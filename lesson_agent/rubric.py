"""The rubric: hard pass/fail checkpoints. No partial credit.

Two kinds of checks:
  * DETERMINISTIC (D*) - plain Python. Free, instant, 100% repeatable. Used for
    everything that can be measured: structure, length, readability, sentence
    length, hard words, jargon defined, acronyms expanded, examples, quiz.
  * LLM-JUDGE (J*) - a separate evaluator model for things only a reader can
    judge: factual accuracy vs the source pack, key-point coverage, quality of
    examples, teaching flow, and a simulated beginner learner.

A lesson SHIPS only if every check passes.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from . import config


@dataclass
class CheckResult:
    id: str
    name: str
    dimension: str
    kind: str  # "deterministic" | "llm"
    passed: bool
    reason: str
    evidence: list[str] = field(default_factory=list)
    fix: str = ""

    def to_dict(self):
        return asdict(self)


# id -> (name, dimension, kind, what it checks)
RUBRIC = {
    "D1": ("Required sections present", "coherent teaching flow", "deterministic",
           "Has all sections: What is, Why it matters, How it works, Example, Key Words, Recap, Check Yourself."),
    "D2": ("Readability (Flesch >= %d)" % config.MIN_FLESCH_READING_EASE, "beginner-friendly language", "deterministic",
           "Flesch Reading Ease of the lesson body is at least the threshold (plain English)."),
    "D3": ("Short sentences", "beginner-friendly language", "deterministic",
           f"Average sentence <= {config.MAX_AVG_SENTENCE_WORDS} words and no sentence > {config.MAX_SENTENCE_WORDS} words."),
    "D4": ("No hard / fancy words", "beginner-friendly language", "deterministic",
           "None of the banned difficult words (utilize, leverage, paradigm ...) are used."),
    "D5": ("Every technical term is in Key Words", "clear, no unexplained jargon", "deterministic",
           "Each technical term used in the lesson is defined in the Key Words section."),
    "D6": ("Acronyms expanded", "clear, no unexplained jargon", "deterministic",
           "Every acronym (RAG, LLM ...) is written in full at least once."),
    "D7": ("Enough examples", "teaches by example", "deterministic",
           f"An Example section exists and at least {config.MIN_EXAMPLES} examples/analogies are used."),
    "D8": ("Length in range", "covers the key points", "deterministic",
           f"Between {config.MIN_WORDS} and {config.MAX_WORDS} words."),
    "D9": ("Self-check quiz", "coherent teaching flow", "deterministic",
           f"At least {config.MIN_QUIZ_QUESTIONS} questions, each with an answer."),
    "J1": ("Factually accurate and grounded", "accurate & grounded", "llm",
           "No claim contradicts the source facts or matches a known misconception."),
    "J2": ("Covers all key points", "covers the key points", "llm",
           "Every must-cover key point (K1..K7) is clearly taught."),
    "J3": ("Teaches through concrete examples", "teaches by example", "llm",
           "A relatable running example walks through the actual steps, plus an analogy."),
    "J4": ("Coherent teaching flow", "coherent teaching flow", "llm",
           "Ideas build in order; nothing is used before it is explained; no contradictions."),
    "J5": ("Beginner learner understands it", "beginner-friendly language", "llm",
           "A simulated 12th-pass, non-English-medium learner finds no blocking confusion."),
}

# Words a learner with limited English vocabulary is likely to struggle with.
HARD_WORDS = [
    "utilize", "utilise", "leverage", "paradigm", "facilitate", "furthermore", "moreover",
    "consequently", "aforementioned", "plethora", "myriad", "robust", "seamless", "seamlessly",
    "subsequently", "thereby", "henceforth", "notwithstanding", "albeit", "ubiquitous",
    "holistic", "synergy", "endeavor", "endeavour", "commence", "ascertain", "pertaining",
    "elucidate", "delve", "intricate", "nuanced", "comprehensive", "methodology", "paramount",
    "multifaceted", "encompass", "augmentative", "cognizant", "efficacy", "pivotal", "manageable",
]

# Advanced terms: too deep for a first lesson. The writer is told to AVOID them;
# if they still appear they must be defined (D5) and usually trip J5 too.
ADVANCED_TERMS = {"cosine similarity", "HNSW", "dense retrieval", "token", "weights", "context window"}

# Technical terms that must be defined in the Key Words section if they are used.
# canonical -> regex that detects use in the lesson body
JARGON = {
    "large language model": r"\blarge language models?\b|\bLLMs?\b",
    "retrieval": r"\bretriev(?:al|e|es|ed|ing)\b",
    "generation": r"\bgenerat(?:ion|e|es|ed|ing)\b",
    "augmented": r"\baugment(?:ed|ation|s|ing)?\b",
    "embedding": r"\bembeddings?\b",
    "vector": r"\bvectors?\b",
    "vector database": r"\bvector (?:database|db|store)s?\b",
    "chunk": r"\bchunk(?:s|ing|ed)?\b",
    "prompt": r"\bprompts?\b",
    "hallucination": r"\bhallucinat(?:ion|ions|e|es|ing)\b",
    "knowledge cutoff": r"\bknowledge cut-?off\b|\bcut-?off date\b",
    "semantic search": r"\bsemantic(?:ally)?\b",
    "context window": r"\bcontext window\b",
    "fine-tuning": r"\bfine-?tun(?:e|ed|ing)\b",
    "token": r"\btokens?\b",
    "indexing": r"\bindex(?:ing|ed)?\b",
    "weights": r"\b(?:model )?weights\b|\bparameters\b",
    "cosine similarity": r"\bcosine\b",
    "HNSW": r"\bHNSW\b",
    "dense retrieval": r"\bdense (?:retrieval|index|vectors?)\b",
    "knowledge base": r"\bknowledge (?:base|source)s?\b",
    "query": r"\bquer(?:y|ies)\b",
}

ACRONYM_ALLOW = {"AI", "OK", "I", "A", "PDF", "PDFs", "UP", "MCQ", "Q", "A1", "A2", "A3", "FAQ", "FAQs"}

SECTION_PATTERNS = {
    "What is": r"^#{1,3}\s.*\bwhat is\b",
    "Why it matters": r"^#{1,3}\s.*\bwhy\b",
    "How it works": r"^#{1,3}\s.*\bhow\b",
    "Example": r"^#{1,3}\s.*\bexample\b",
    "Key Words": r"^#{1,3}\s.*\b(key words|glossary|new words)\b",
    "Recap": r"^#{1,3}\s.*\b(recap|summary)\b",
    "Check Yourself": r"^#{1,3}\s.*\b(check yourself|quiz|test yourself)\b",
}


# ---------------------------------------------------------------- helpers ---
def count_syllables(word: str) -> int:
    """Standard vowel-group heuristic (same family as textstat's fallback)."""
    w = word.lower().strip("'")
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def flesch_reading_ease(text: str) -> float:
    """Flesch Reading Ease = 206.835 - 1.015*(words/sentences) - 84.6*(syllables/words)."""
    ws = words(text)
    ss = sentences(text) or [text]
    if not ws:
        return 0.0
    syl = sum(count_syllables(w) for w in ws)
    return round(206.835 - 1.015 * (len(ws) / len(ss)) - 84.6 * (syl / len(ws)), 1)


def split_sections(md: str) -> dict[str, str]:
    """{heading_line_lower: body} for every markdown heading."""
    out, cur, buf = {}, "__intro__", []
    for line in md.splitlines():
        if re.match(r"^#{1,3}\s", line):
            out[cur] = "\n".join(buf)
            cur, buf = line.strip().lower(), []
        else:
            buf.append(line)
    out[cur] = "\n".join(buf)
    return out


def find_section(md: str, key: str) -> str:
    pat = re.compile(SECTION_PATTERNS[key], re.I)
    for head, body in split_sections(md).items():
        if pat.search(head):
            return body
    return ""


def plain_text(md: str, drop_sections: tuple[str, ...] = ()) -> str:
    """Strip markdown so readability is measured on what the learner reads."""
    if drop_sections:
        keep = []
        for head, body in split_sections(md).items():
            if any(re.search(SECTION_PATTERNS[s], head, re.I) for s in drop_sections):
                continue
            keep.append(body)
        md = "\n".join(keep)
    t = re.sub(r"```.*?```", " ", md, flags=re.S)
    t = re.sub(r"^#{1,6}\s.*$", " ", t, flags=re.M)
    t = re.sub(r"!\[.*?\]\(.*?\)|\[(.*?)\]\(.*?\)", r"\1", t)
    t = re.sub(r"[*_`>|#]", "", t)
    t = re.sub(r"^\s*[-+]\s+", "", t, flags=re.M)
    t = re.sub(r"^\s*\d+[.)]\s+", "", t, flags=re.M)
    t = re.sub(r"^\s*-{3,}\s*$", " ", t, flags=re.M)
    return t


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n{1,}", text)
    return [p.strip() for p in parts if len(p.strip().split()) >= 3]


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'-]*", text)


# ----------------------------------------------------- deterministic checks ---
def _r(cid, passed, reason, evidence=None, fix=""):
    name, dim, kind, _ = RUBRIC[cid]
    return CheckResult(cid, name, dim, kind, passed, reason, evidence or [], fix)


def check_sections(md):
    missing = [k for k, p in SECTION_PATTERNS.items() if not re.search(p, md, re.I | re.M)]
    h2 = [h.strip().lower() for h in re.findall(r"^##\s+(.+)$", md, re.M)]
    dups = sorted({h for h in h2 if h2.count(h) > 1})
    if dups:
        return _r("D1", False, f"Duplicate section headings: {', '.join(dups)}", dups,
                  "Each '## ' section must appear exactly once.")
    if missing:
        return _r("D1", False, f"Missing sections: {', '.join(missing)}", missing,
                  "Add the missing sections as '## ' headings in the required order.")
    return _r("D1", True, "All 7 required sections present.")


def check_readability(md):
    body = plain_text(md, drop_sections=("Check Yourself",))
    score = flesch_reading_ease(body)
    if score < config.MIN_FLESCH_READING_EASE:
        return _r("D2", False, f"Flesch Reading Ease = {score:.1f} (need >= {config.MIN_FLESCH_READING_EASE}).",
                  [f"score={score:.1f}"],
                  "Use shorter sentences and shorter, everyday words (1-2 syllables). Split long sentences.")
    return _r("D2", True, f"Flesch Reading Ease = {score:.1f}.", [f"score={score:.1f}"])


def check_sentence_length(md):
    sents = sentences(plain_text(md))
    if not sents:
        return _r("D3", False, "No sentences found.")
    lens = [len(s.split()) for s in sents]
    avg = sum(lens) / len(lens)
    long = [s for s in sents if len(s.split()) > config.MAX_SENTENCE_WORDS]
    if avg > config.MAX_AVG_SENTENCE_WORDS or long:
        ev = [f"avg={avg:.1f} words"] + [f"({len(s.split())} words) {s[:160]}" for s in long[:5]]
        return _r("D3", False, f"Average sentence {avg:.1f} words; {len(long)} sentence(s) over {config.MAX_SENTENCE_WORDS} words.",
                  ev, "Split every long sentence into two or three short ones.")
    return _r("D3", True, f"Average sentence {avg:.1f} words; none too long.", [f"avg={avg:.1f}"])


def check_hard_words(md):
    text = plain_text(md).lower()
    found = sorted({w for w in HARD_WORDS if re.search(rf"\b{w}\b", text)})
    if found:
        return _r("D4", False, f"Hard words used: {', '.join(found)}", found,
                  "Replace these with simple everyday words (e.g. 'use' not 'utilize').")
    return _r("D4", True, "No banned hard words.")


def glossary_text(md) -> str:
    return find_section(md, "Key Words").lower()


def check_jargon_defined(md):
    gloss = glossary_text(md)
    body = plain_text(md, drop_sections=("Key Words",))
    missing = []
    for term, pat in JARGON.items():
        if re.search(pat, body, re.I):
            # defined if the canonical term or any matching form appears in the glossary
            if term.lower() in gloss or re.search(pat, gloss, re.I):
                continue
            missing.append(term)
    if not gloss.strip():
        return _r("D5", False, "No Key Words section, so no term is defined.", list(JARGON)[:5],
                  "Add a '## Key Words' section defining every technical word in one simple sentence.")
    if missing:
        return _r("D5", False, f"Technical terms used but not defined in Key Words: {', '.join(missing)}",
                  missing, "Add each missing term to Key Words with a one-line simple definition, "
                  "or remove the term if it is not needed.")
    return _r("D5", True, "Every technical term used is defined in Key Words.")


def check_acronyms(md):
    text = plain_text(md)
    acrs = sorted({a for a in re.findall(r"\b[A-Z]{2,6}s?\b", text)} - ACRONYM_ALLOW)  # letters only: skips codes like CS101
    missing = []
    for a in acrs:
        base = a[:-1] if a.endswith("s") and a[:-1].isupper() else a
        if base in ACRONYM_ALLOW:
            continue
        # expanded if "(RAG)" follows words, or "RAG (" / "RAG stands for" / "RAG means"
        suffix = r"(?:-\d+)?"  # e.g. COVID-19
        expanded = (re.search(rf"\(\s*{base}s?{suffix}\s*\)", md)
                    or re.search(rf"\b{base}s?{suffix}\b\s*(\(|stands for|means|is short for|:)", md))
        if not expanded:
            missing.append(base)
    missing = sorted(set(missing))
    if missing:
        return _r("D6", False, f"Acronyms never written in full: {', '.join(missing)}", missing,
                  "Write each acronym in full the first time, e.g. 'Large Language Model (LLM)'.")
    return _r("D6", True, "All acronyms are expanded.")


def check_examples(md):
    has_section = bool(re.search(SECTION_PATTERNS["Example"], md, re.I | re.M))
    markers = len(re.findall(r"\bfor example\b|\bfor instance\b|\bimagine\b|\bthink of\b|\bjust like\b|\bexample\b|\bsuppose\b|\blet'?s say\b", md, re.I))
    if not has_section or markers < config.MIN_EXAMPLES:
        return _r("D7", False, f"Example section present: {has_section}; example markers: {markers}.",
                  [f"markers={markers}"], "Add a full worked example section and at least one everyday analogy.")
    return _r("D7", True, f"Example section present; {markers} example/analogy markers.")


def check_length(md):
    n = len(words(plain_text(md)))
    if not (config.MIN_WORDS <= n <= config.MAX_WORDS):
        fix = "Add more explanation and examples." if n < config.MIN_WORDS else "Cut repetition; keep each idea once."
        return _r("D8", False, f"{n} words (need {config.MIN_WORDS}-{config.MAX_WORDS}).", [f"words={n}"], fix)
    return _r("D8", True, f"{n} words.", [f"words={n}"])


def check_quiz(md):
    quiz = find_section(md, "Check Yourself")
    qs = len(re.findall(r"\?", quiz))
    ans = len(re.findall(r"\banswer\b", quiz, re.I))
    if qs < config.MIN_QUIZ_QUESTIONS or ans < config.MIN_QUIZ_QUESTIONS:
        return _r("D9", False, f"Quiz has {qs} questions and {ans} answers (need {config.MIN_QUIZ_QUESTIONS} each).",
                  [f"questions={qs}", f"answers={ans}"],
                  "Add at least 3 simple questions in 'Check Yourself', each followed by 'Answer: ...'.")
    return _r("D9", True, f"Quiz has {qs} questions with answers.")


DETERMINISTIC_CHECKS = [check_sections, check_readability, check_sentence_length, check_hard_words,
                        check_jargon_defined, check_acronyms, check_examples, check_length, check_quiz]


_UNICODE_FIX = str.maketrans({"\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "-",
                               "\u2212": "-", "\u00a0": " ", "\u202f": " ", "\u2018": "'", "\u2019": "'",
                               "\u201c": '"', "\u201d": '"'})


def normalize(md: str) -> str:
    """LLMs often emit non-breaking hyphens/spaces and curly quotes. Normalise
    them so regex checks do not produce false failures (found in a real run:
    'COVID\u201119' was not recognised as an expanded acronym)."""
    return md.translate(_UNICODE_FIX)


def run_deterministic(md: str) -> list[CheckResult]:
    md = normalize(md)
    return [fn(md) for fn in DETERMINISTIC_CHECKS]


def lesson_stats(md: str) -> dict:
    md = normalize(md)
    body = plain_text(md)
    sents = sentences(body)
    return {
        "words": len(words(body)),
        "flesch_reading_ease": round(flesch_reading_ease(plain_text(md, ("Check Yourself",))), 1),
        "avg_sentence_words": round(sum(len(s.split()) for s in sents) / max(1, len(sents)), 1),
    }


def preflight_checklist() -> str:
    """The deterministic rubric, shown to the WRITER before it writes ("shift left"):
    cheaper to prevent a failure than to catch it and spend a retry."""
    core = ", ".join(t for t in JARGON if t not in ADVANCED_TERMS)
    avoid = ", ".join(sorted(ADVANCED_TERMS))
    return (
        "PRE-FLIGHT CHECKLIST (an automatic checker will verify every item; a single miss rejects the lesson):\n"
        f"- Length: at least {config.MIN_WORDS + 200} words and at most {config.MAX_WORDS - 500} words. Count before you finish.\n"
        f"- Core words: if you use any of these (or their forms), it MUST appear in '## Key Words' with a simple meaning: {core}.\n"
        f"- Do NOT use these advanced words at all in a first lesson (they are not needed): {avoid}. "
        "Do not explain the math behind embeddings or similarity; a simple analogy is enough.\n"
        "- Every acronym (RAG, LLM, HR, ...) written in full the first time: 'Large Language Model (LLM)'. "
        "Avoid acronyms that are not needed.\n"
        f"- Never use: {', '.join(HARD_WORDS[:20])}.\n"
        f"- Average sentence under {int(config.MAX_AVG_SENTENCE_WORDS) - 3} words; no sentence over {config.MAX_SENTENCE_WORDS - 7} words.\n"
        "- Sections exactly as in the template, including '## A Full Example' and '## Check Yourself' "
        f"with at least {config.MIN_QUIZ_QUESTIONS} questions, each followed by 'Answer: ...'.\n"
    )


def looks_degenerate(md: str) -> str | None:
    """Detect broken model output (repetition loops, word-salad bolding).
    This is an infrastructure failure, not a content failure, so the graph
    re-samples instead of spending a content retry."""
    md = normalize(md)
    h2 = [h.strip().lower() for h in re.findall(r"^##\s+(.+)$", md, re.M)]
    if any(h2.count(h) > 2 for h in h2):
        return "same heading repeated 3+ times"
    paras = [p.strip() for p in re.split(r"\n\s*\n", md) if len(p.strip()) > 40]
    if paras and len(paras) - len(set(paras)) >= 3:
        return "paragraphs repeated"
    ws = words(plain_text(md))
    bold = len(re.findall(r"\*\*[^*]+\*\*", md))
    if ws and bold / len(ws) > 0.15:
        return f"too much bold ({bold} bold spans / {len(ws)} words)"
    if len(ws) < 300:
        return f"too short ({len(ws)} words), likely truncated"
    return None
