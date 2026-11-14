# Rejection Log: Introduction to RAG (Retrieval-Augmented Generation)

- Run ID: `20261114-101121-715e`
- Final status: **SHIPPED**
- Attempts: 3 (max 3)
- Deliberate error injection: off
- Learned rules applied from memory: 4

## Rules applied from memory (self-evolving prompt)
- (J4, auto, v1) Define each new term before using it, with a brief example.
- (D6, auto, v2) Ensure each acronym appears in full form at least once, e.g., write 'Database (DB)' before using the abbreviation.
- (D8, auto, v1) Write a lesson between 900 and 2300 words.
- (J1, human, v1) Never claim the model cannot make things up when the documents lack the answer. Say it may still guess, so good documents and good search matter.

## Summary across attempts

| Check | Dimension | Attempt 1 | Attempt 2 | Attempt 3 |
|---|---|---|---|---|
| D1 Required sections present | coherent teaching flow | PASS | PASS | PASS |
| D2 Readability (Flesch >= 60) | beginner-friendly language | PASS | PASS | PASS |
| D3 Short sentences | beginner-friendly language | PASS | PASS | PASS |
| D4 No hard / fancy words | beginner-friendly language | PASS | PASS | PASS |
| D5 Every technical term is in Key Words | clear, no unexplained jargon | PASS | PASS | PASS |
| D6 Acronyms expanded | clear, no unexplained jargon | **FAIL** | PASS | PASS |
| D7 Enough examples | teaches by example | PASS | PASS | PASS |
| D8 Length in range | covers the key points | PASS | PASS | PASS |
| D9 Self-check quiz | coherent teaching flow | PASS | PASS | PASS |
| J1 Factually accurate and grounded | accurate & grounded | PASS | PASS | PASS |
| J2 Covers all key points | covers the key points | PASS | PASS | PASS |
| J3 Teaches through concrete examples | teaches by example | PASS | PASS | PASS |
| J4 Coherent teaching flow | coherent teaching flow | PASS | PASS | PASS |
| J5 Beginner learner understands it | beginner-friendly language | **FAIL** | **FAIL** | PASS |

## Attempt 1: REJECT

Stats: 932 words, Flesch 66.7, avg sentence 11.5 words.

### D6 Acronyms expanded: FAILED
- Why: Acronyms never written in full: IIT, JEE
- Evidence: IIT
- Evidence: JEE
- Fix requested: Write each acronym in full the first time, e.g. 'Large Language Model (LLM)'.

### J5 Beginner learner understands it: FAILED
- Why: Simulated learner got stuck 1 time(s) (blocking). Main idea understood: True.
- Evidence: "a special AI model reads each chunk and creates a list of numbers, called an embedding. Think of it as a “meaning address”. Similar chunks get nearby addresses." -> Ravi does not know how a piece of text becomes a list of numbers. It feels like magic. He does not understand the process of turning meaning into numbers, so he is stuck on how the computer 'knows' the meaning.
- Fix requested: Rewrite each quoted sentence in simpler words and explain the missing idea before using it.

## Attempt 2: REJECT

Stats: 968 words, Flesch 65.4, avg sentence 11.7 words.

### J5 Beginner learner understands it: FAILED
- Why: Simulated learner got stuck 1 time(s) (blocking). Main idea understood: True.
- Evidence: "a small AI model looks at the words in a chunk and turns them into a list of numbers." -> Ravi does not know how a computer turns words into numbers. It feels like magic. He understands that it is a 'meaning code' but not how the code is made, so he is stuck on the process.
- Fix requested: Rewrite each quoted sentence in simpler words and explain the missing idea before using it.

### What changed on this retry
- Fixed checks: D6
- Still failing: J5
- Newly failing (regressions): none
- Lines added / removed: 54 / 46
- Stats before -> after: {'words': 932, 'flesch_reading_ease': 66.7, 'avg_sentence_words': 11.5} -> {'words': 968, 'flesch_reading_ease': 65.4, 'avg_sentence_words': 11.7}
- Offending text from J5: "a special AI model reads each chunk and creates a list of numbers, called an embedding. Think of it as a “meaning address”. Similar chunks get nearby addresses." -> removed/rewritten

## Attempt 3: PASS

Stats: 983 words, Flesch 64.3, avg sentence 11.8 words.

All checks passed.

### What changed on this retry
- Fixed checks: J5
- Still failing: none
- Newly failing (regressions): none
- Lines added / removed: 20 / 18
- Stats before -> after: {'words': 968, 'flesch_reading_ease': 65.4, 'avg_sentence_words': 11.7} -> {'words': 983, 'flesch_reading_ease': 64.3, 'avg_sentence_words': 11.8}
- Offending text from J5: "a small AI model looks at the words in a chunk and turns them into a list of numbers." -> removed/rewritten

## New rules learned after this run
- (J5) Explain the word-to-number conversion step-by-step, using a simple analogy (e.g., mapping words to coordinates on a grid) and avoid abstract terms like 'embedding' without context.

## Event trace
```
10:11:21 [memory] 4 learned rule(s) loaded for the generator; 7 past failure example(s) loaded for the evaluator
10:11:25 [plan] 'Introduction to Retrieval‑Augmented Generation (RAG)' with 9 sections; analogy: Like going to a librarian (search) to fetch the right book (information) and the
10:11:25 [retrieve] 24 distinct source facts retrieved across 9 sections (BM25)
10:11:30 [generate] attempt 1: 932 words
10:11:34 [evaluate] attempt 1: 12/14 checks passed -> REJECTED (D6, J5)
10:12:23 [regenerate (retry 1/2)] attempt 2: 968 words
10:12:27 [evaluate] attempt 2: 13/14 checks passed -> REJECTED (J5)
10:13:17 [regenerate (retry 2/2)] attempt 3: 983 words
10:13:22 [evaluate] attempt 3: 14/14 checks passed -> PASSED
10:13:22 [ship] lesson passed all 14 checks on attempt 3
10:13:34 [learn] 1 new rule(s) learned from repeated failures
      + (J5) Explain the word-to-number conversion step-by-step, using a simple analogy (e.g., mapping words to coordinates on a grid) and avoid abstract terms like 'embedding' without context.
```