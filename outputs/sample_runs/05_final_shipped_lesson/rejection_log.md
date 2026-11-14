# Rejection Log: Introduction to RAG (Retrieval-Augmented Generation)

- Run ID: `20261114-101613-d823`
- Final status: **SHIPPED**
- Attempts: 2 (max 3)
- Deliberate error injection: off
- Learned rules applied from memory: 5

## Rules applied from memory (self-evolving prompt)
- (J1, human, v2) In examples, use clearly fictional documents and organisations (for example 'Sunrise College rulebook'), never real institutions' rules or numbers, so the lesson never states false real-world facts.
- (J4, auto, v1) Define each new term before using it, with a brief example.
- (D6, auto, v2) Ensure each acronym appears in full form at least once, e.g., write 'Database (DB)' before using the abbreviation.
- (D8, auto, v1) Write a lesson between 900 and 2300 words.
- (J1, human, v1) Never claim the model cannot make things up when the documents lack the answer. Say it may still guess, so good documents and good search matter.

## Summary across attempts

| Check | Dimension | Attempt 1 | Attempt 2 |
|---|---|---|---|
| D1 Required sections present | coherent teaching flow | PASS | PASS |
| D2 Readability (Flesch >= 60) | beginner-friendly language | PASS | PASS |
| D3 Short sentences | beginner-friendly language | PASS | PASS |
| D4 No hard / fancy words | beginner-friendly language | PASS | PASS |
| D5 Every technical term is in Key Words | clear, no unexplained jargon | PASS | PASS |
| D6 Acronyms expanded | clear, no unexplained jargon | **FAIL** | PASS |
| D7 Enough examples | teaches by example | PASS | PASS |
| D8 Length in range | covers the key points | PASS | PASS |
| D9 Self-check quiz | coherent teaching flow | PASS | PASS |
| J1 Factually accurate and grounded | accurate & grounded | PASS | PASS |
| J2 Covers all key points | covers the key points | PASS | PASS |
| J3 Teaches through concrete examples | teaches by example | PASS | PASS |
| J4 Coherent teaching flow | coherent teaching flow | PASS | PASS |
| J5 Beginner learner understands it | beginner-friendly language | PASS | PASS |

## Attempt 1: REJECT

Stats: 1002 words, Flesch 64.8, avg sentence 11.2 words.

### D6 Acronyms expanded: FAILED
- Why: Acronyms never written in full: COVID
- Evidence: COVID
- Fix requested: Write each acronym in full the first time, e.g. 'Large Language Model (LLM)'.

## Attempt 2: PASS

Stats: 1147 words, Flesch 62.4, avg sentence 11.5 words.

All checks passed.

### What changed on this retry
- Fixed checks: D6
- Still failing: none
- Newly failing (regressions): none
- Lines added / removed: 74 / 50
- Stats before -> after: {'words': 1002, 'flesch_reading_ease': 64.8, 'avg_sentence_words': 11.2} -> {'words': 1147, 'flesch_reading_ease': 62.4, 'avg_sentence_words': 11.5}

## New rules learned after this run
- (D6) Always write the full form of each acronym before using its abbreviation.
- (J5) Explain step-by-step how words become numbers, using simple analogies (e.g., letters as numbered positions) to show how meaning is captured.

## Event trace
```
10:16:13 [memory] 5 learned rule(s) loaded for the generator; 7 past failure example(s) loaded for the evaluator
10:16:17 [plan] 'Intro to Retrieval‑Augmented Generation' with 9 sections; analogy: Like a librarian who first fetches the right books before answering your questio
10:16:17 [retrieve] 26 distinct source facts retrieved across 9 sections (BM25)
10:16:28 [generate] attempt 1: 1002 words
10:16:32 [evaluate] attempt 1: 13/14 checks passed -> REJECTED (D6)
10:17:21 [regenerate (retry 1/2)] attempt 2: 1147 words
10:17:55 [evaluate] attempt 2: 14/14 checks passed -> PASSED
10:17:55 [ship] lesson passed all 14 checks on attempt 2
10:18:20 [learn] 2 new rule(s) learned from repeated failures
      + (D6) Always write the full form of each acronym before using its abbreviation.
      + (J5) Explain step-by-step how words become numbers, using simple analogies (e.g., letters as numbered positions) to show how meaning is captured.
```