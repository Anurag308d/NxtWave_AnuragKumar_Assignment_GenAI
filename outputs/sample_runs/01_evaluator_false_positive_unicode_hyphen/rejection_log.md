# Rejection Log: Introduction to RAG (Retrieval-Augmented Generation)

- Run ID: `20261113-141307-9716`
- Final status: **NOT SHIPPED (flagged for human review)**
- Attempts: 3 (max 3)
- Deliberate error injection: off
- Learned rules applied from memory: 0

## Summary across attempts

| Check | Dimension | Attempt 1 | Attempt 2 | Attempt 3 |
|---|---|---|---|---|
| D1 Required sections present | coherent teaching flow | PASS | PASS | PASS |
| D2 Readability (Flesch >= 60) | beginner-friendly language | PASS | PASS | PASS |
| D3 Short sentences | beginner-friendly language | PASS | PASS | PASS |
| D4 No hard / fancy words | beginner-friendly language | PASS | PASS | PASS |
| D5 Every technical term is in Key Words | clear, no unexplained jargon | **FAIL** | PASS | PASS |
| D6 Acronyms expanded | clear, no unexplained jargon | **FAIL** | **FAIL** | **FAIL** |
| D7 Enough examples | teaches by example | PASS | PASS | PASS |
| D8 Length in range | covers the key points | PASS | PASS | PASS |
| D9 Self-check quiz | coherent teaching flow | PASS | PASS | PASS |
| J1 Factually accurate and grounded | accurate & grounded | PASS | PASS | PASS |
| J2 Covers all key points | covers the key points | **FAIL** | PASS | PASS |
| J3 Teaches through concrete examples | teaches by example | PASS | PASS | PASS |
| J4 Coherent teaching flow | coherent teaching flow | **FAIL** | PASS | PASS |
| J5 Beginner learner understands it | beginner-friendly language | PASS | PASS | PASS |

## Attempt 1: REJECT

Stats: 1008 words, Flesch 62.7, avg sentence 12.6 words.

### D5 Every technical term is in Key Words: FAILED
- Why: Technical terms used but not defined in Key Words: prompt, indexing, query
- Evidence: prompt
- Evidence: indexing
- Evidence: query
- Fix requested: Add each missing term to Key Words with a one-line simple definition, or remove the term if it is not needed.

### D6 Acronyms expanded: FAILED
- Why: Acronyms never written in full: COVID
- Evidence: COVID
- Fix requested: Write each acronym in full the first time, e.g. 'Large Language Model (LLM)'.

### J2 Covers all key points: FAILED
- Why: Missing key point K3: RAG can show the sources (documents) used for an answer, allowing users to verify the information.
- Evidence: "RAG helps solve these problems: It lets the model answer questions about recent or private data without changing the model itself."
- Fix requested: Add a sentence such as "RAG systems can also display the exact documents or passages that were used to generate the answer, so users can check the source."

### J4 Coherent teaching flow: FAILED
- Why: The term LLM is used before it is defined, which may confuse beginners. Also the term "vector database" is introduced before its definition.
- Evidence: "Large language models (LLMs) only know what they learned before a certain date."
- Fix requested: Move the definition of LLM (e.g., "An LLM is a computer program trained on vast amounts of text…") to immediately after the first mention of LLM, and similarly introduce "vector database" before it is used in the indexing section.

## Attempt 2: REJECT

Stats: 1059 words, Flesch 62.5, avg sentence 12.8 words.

### D6 Acronyms expanded: FAILED
- Why: Acronyms never written in full: COVID
- Evidence: COVID
- Fix requested: Write each acronym in full the first time, e.g. 'Large Language Model (LLM)'.

### What changed on this retry
- Fixed checks: D5, J2, J4
- Still failing: D6
- Newly failing (regressions): none
- Lines added / removed: 42 / 37
- Stats before -> after: {'words': 1008, 'flesch_reading_ease': 62.7, 'avg_sentence_words': 12.6} -> {'words': 1059, 'flesch_reading_ease': 62.5, 'avg_sentence_words': 12.8}
- Offending text from J2: "RAG helps solve these problems: It lets the model answer questions about recent or private data without changing the model itself." -> removed/rewritten
- Offending text from J4: "Large language models (LLMs) only know what they learned before a certain date." -> removed/rewritten

## Attempt 3: REJECT

Stats: 1083 words, Flesch 61.9, avg sentence 12.8 words.

### D6 Acronyms expanded: FAILED
- Why: Acronyms never written in full: COVID
- Evidence: COVID
- Fix requested: Write each acronym in full the first time, e.g. 'Large Language Model (LLM)'.

### What changed on this retry
- Fixed checks: none
- Still failing: D6
- Newly failing (regressions): none
- Lines added / removed: 8 / 5
- Stats before -> after: {'words': 1059, 'flesch_reading_ease': 62.5, 'avg_sentence_words': 12.8} -> {'words': 1083, 'flesch_reading_ease': 61.9, 'avg_sentence_words': 12.8}

## New rules learned after this run
- (D6) Ensure each acronym is spelled out in full on its first appearance, e.g., COVID-19 (Coronavirus Disease 2019).

## Event trace
```
14:13:07 [memory] 0 learned rule(s) loaded for the generator; 0 past failure example(s) loaded for the evaluator
14:13:12 [plan] 'Intro to Retrieval‑Augmented Generation (RAG)' with 4 sections; analogy: Like going to a library (or a neighbour) to fetch the exact page you need before
14:13:12 [retrieve] 21 distinct source facts retrieved across 4 sections (BM25)
14:13:17 [generate] attempt 1: 1008 words
14:14:08 [evaluate] attempt 1: 10/14 checks passed -> REJECTED (D5, D6, J2, J4)
14:14:14 [regenerate (retry 1/2)] attempt 2: 1059 words
14:15:53 [evaluate] attempt 2: 13/14 checks passed -> REJECTED (D6)
14:15:59 [regenerate (retry 2/2)] attempt 3: 1083 words
14:17:38 [evaluate] attempt 3: 13/14 checks passed -> REJECTED (D6)
14:17:38 [human_review] retries exhausted; best = attempt 3 -> NOT shipped, flagged for a human
14:17:39 [learn] 1 new rule(s) learned from repeated failures
      + (D6) Ensure each acronym is spelled out in full on its first appearance, e.g., COVID-19 (Coronavirus Disease 2019).
```