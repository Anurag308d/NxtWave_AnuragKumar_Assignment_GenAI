# Rejection Log: Introduction to RAG (Retrieval-Augmented Generation)

- Run ID: `20261113-142327-36d5`
- Final status: **NOT SHIPPED (flagged for human review)**
- Attempts: 3 (max 3)
- Deliberate error injection: off
- Learned rules applied from memory: 0

## Summary across attempts

| Check | Dimension | Attempt 1 | Attempt 2 | Attempt 3 |
|---|---|---|---|---|
| D1 Required sections present | coherent teaching flow | **FAIL** | PASS | PASS |
| D2 Readability (Flesch >= 60) | beginner-friendly language | PASS | PASS | PASS |
| D3 Short sentences | beginner-friendly language | PASS | PASS | PASS |
| D4 No hard / fancy words | beginner-friendly language | PASS | PASS | PASS |
| D5 Every technical term is in Key Words | clear, no unexplained jargon | **FAIL** | PASS | PASS |
| D6 Acronyms expanded | clear, no unexplained jargon | **FAIL** | PASS | PASS |
| D7 Enough examples | teaches by example | **FAIL** | PASS | PASS |
| D8 Length in range | covers the key points | PASS | PASS | **FAIL** |
| D9 Self-check quiz | coherent teaching flow | PASS | PASS | PASS |
| J1 Factually accurate and grounded | accurate & grounded | **FAIL** | PASS | PASS |
| J2 Covers all key points | covers the key points | PASS | PASS | PASS |
| J3 Teaches through concrete examples | teaches by example | PASS | PASS | PASS |
| J4 Coherent teaching flow | coherent teaching flow | PASS | PASS | PASS |
| J5 Beginner learner understands it | beginner-friendly language | **FAIL** | **FAIL** | **FAIL** |

## Attempt 1: REJECT

Stats: 916 words, Flesch 78.6, avg sentence 8.1 words.

### D1 Required sections present: FAILED
- Why: Missing sections: Example
- Evidence: Example
- Fix requested: Add the missing sections as '## ' headings in the required order.

### D5 Every technical term is in Key Words: FAILED
- Why: Technical terms used but not defined in Key Words: augmented, semantic search
- Evidence: augmented
- Evidence: semantic search
- Fix requested: Add each missing term to Key Words with a one-line simple definition, or remove the term if it is not needed.

### D6 Acronyms expanded: FAILED
- Why: Acronyms never written in full: RAG
- Evidence: RAG
- Fix requested: Write each acronym in full the first time, e.g. 'Large Language Model (LLM)'.

### D7 Enough examples: FAILED
- Why: Example section present: False; example markers: 5.
- Evidence: markers=5
- Fix requested: Add a full worked example section and at least one everyday analogy.

### J1 Factually accurate and grounded: FAILED
- Why: The lesson overstates RAG's capabilities, claiming it completely fixes hallucination and always yields true data, which is inaccurate.
- Evidence: "RAG fixes these issues." (conflicts with F08, which states RAG reduces hallucination but does not remove it completely)
- Evidence: "The answer is based on true data." (conflicts with F26 and F27, which note that if retrieval returns wrong or outdated documents, the answer can be wrong)
- Fix requested: Change the sentences to say that RAG *reduces* hallucination and can improve answer accuracy, but it does not guarantee correctness; the quality of the answer depends on the relevance and correctness of the retrieved documents.

### J5 Beginner learner understands it: FAILED
- Why: Simulated learner got stuck 17 time(s) (blocking). Main idea understood: True.
- Evidence: "RAG stands for Retrieval-Augmented Generation." -> Ravi does not know the acronym RAG or the meaning of 'Retrieval-Augmented Generation'.
- Evidence: "Retrieval means finding the right text." -> The word 'Retrieval' is unfamiliar to Ravi.
- Evidence: "Generation means writing the answer." -> The word 'Generation' is unfamiliar to Ravi.
- Evidence: "This is called the knowledge cutoff." -> The phrase 'knowledge cutoff' is not explained and is unknown to Ravi.
- Evidence: "This is called hallucination." -> The term 'hallucination' is technical and unknown to Ravi.
- Evidence: "RAG has two phases: Indexing and Query." -> The words 'phases', 'Indexing', and 'Query' are new concepts for Ravi.
- Fix requested: Rewrite each quoted sentence in simpler words and explain the missing idea before using it.

## Attempt 2: REJECT

Stats: 1099 words, Flesch 77.2, avg sentence 8.3 words.

### J5 Beginner learner understands it: FAILED
- Why: Simulated learner got stuck 16 time(s) (blocking). Main idea understood: False.
- Evidence: "# Intro to Retrieval-Augmented Generation (RAG)" -> The term "Retrieval-Augmented Generation (RAG)" contains three technical words Ravi has never seen, so he cannot grasp what the lesson is about
- Evidence: "## What Is Retrieval-Augmented Generation (RAG)?" -> Repeats the same unknown acronym; Ravi still has no idea what it means
- Evidence: "**Retrieval-Augmented Generation** is a method for AI." -> Uses the phrase "Retrieval-Augmented Generation" without simple explanation; Ravi is lost
- Evidence: "Without RAG, the student writes from memory." -> Mentions "RAG" again; Ravi cannot connect it to the previous sentence
- Evidence: "With RAG, the student opens their book." -> Again uses the unknown term "RAG"; Ravi cannot follow the comparison
- Evidence: "RAG helps reduce this problem." -> Refers to "RAG" again without clarification; Ravi still does not know what it is
- Fix requested: Rewrite each quoted sentence in simpler words and explain the missing idea before using it.

### What changed on this retry
- Fixed checks: D1, D5, D6, D7, J1
- Still failing: J5
- Newly failing (regressions): none
- Lines added / removed: 50 / 43
- Stats before -> after: {'words': 916, 'flesch_reading_ease': 78.6, 'avg_sentence_words': 8.1} -> {'words': 1099, 'flesch_reading_ease': 77.2, 'avg_sentence_words': 8.3}
- Offending text from J1: "RAG fixes these issues." -> removed/rewritten
- Offending text from J1: "The answer is based on true data." -> removed/rewritten
- Offending text from J5: "RAG stands for Retrieval-Augmented Generation." -> removed/rewritten
- Offending text from J5: "Retrieval means finding the right text." -> removed/rewritten
- Offending text from J5: "Generation means writing the answer." -> removed/rewritten
- Offending text from J5: "This is called the knowledge cutoff." -> removed/rewritten

## Attempt 3: REJECT

Stats: 781 words, Flesch 70.8, avg sentence 12.1 words.

### D8 Length in range: FAILED
- Why: 781 words (need 900-2300).
- Evidence: words=781
- Fix requested: Add more explanation and examples.

### J5 Beginner learner understands it: FAILED
- Why: Simulated learner got stuck 11 time(s) (blocking). Main idea understood: True.
- Evidence: "Retrieval-Augmented Generation (RAG) is a way for a computer to find useful text and then write an answer from it." -> Term "Retrieval-Augmented Generation (RAG)" is completely new
- Evidence: "They do not know new events after a certain date, called the knowledge cutoff." -> Phrase "knowledge cutoff" is not explained
- Evidence: "Sometimes AI makes up facts that are not true; this is called hallucination." -> Word "hallucination" is unfamiliar
- Evidence: "RAG has two main parts: indexing and query." -> Terms "indexing" and "query" are new concepts
- Evidence: "During indexing, you collect documents, split them into small pieces called chunks, turn each chunk into a list of numbers called an embedding, and store these embeddings in a special database." -> Multiple new terms: documents, chunks, embedding, database
- Evidence: "Large Language Model (LLM): a computer program that can understand questions and write human‑like text." -> Acronym "LLM" and phrase "Large Language Model" are not explained
- Fix requested: Rewrite each quoted sentence in simpler words and explain the missing idea before using it.

### What changed on this retry
- Fixed checks: none
- Still failing: J5
- Newly failing (regressions): D8
- Lines added / removed: 64 / 86
- Stats before -> after: {'words': 1099, 'flesch_reading_ease': 77.2, 'avg_sentence_words': 8.3} -> {'words': 781, 'flesch_reading_ease': 70.8, 'avg_sentence_words': 12.1}
- Offending text from J5: "Intro to Retrieval-Augmented Generation (RAG)" -> STILL PRESENT
- Offending text from J5: "What Is Retrieval-Augmented Generation (RAG)?" -> STILL PRESENT
- Offending text from J5: "Retrieval-Augmented Generation** is a method for AI." -> removed/rewritten
- Offending text from J5: "Without RAG, the student writes from memory." -> removed/rewritten

## New rules learned after this run
- (J5) Introduce each new term or acronym with a simple definition and everyday example before using it.

## Event trace
```
14:23:27 [memory] 0 learned rule(s) loaded for the generator; 0 past failure example(s) loaded for the evaluator
14:23:30 [plan] 'How AI Finds Answers in Your Files: Intro to RAG' with 9 sections; analogy: Imagine you are a student in a library. You do not memorize every book. Instead,
14:23:30 [retrieve] 23 distinct source facts retrieved across 9 sections (BM25)
14:23:48 [generate] attempt 1: 916 words
14:23:59 [evaluate] attempt 1: 8/14 checks passed -> REJECTED (D1, D5, D6, D7, J1, J5)
14:24:21 [regenerate (retry 1/2)] attempt 2: 1099 words
14:25:08 [evaluate] attempt 2: 13/14 checks passed -> REJECTED (J5)
14:26:29 [regenerate (retry 2/2)] attempt 3: 781 words
14:26:57 [evaluate] attempt 3: 12/14 checks passed -> REJECTED (D8, J5)
14:26:57 [human_review] retries exhausted; best = attempt 2 -> NOT shipped, flagged for a human
14:26:58 [learn] 1 new rule(s) learned from repeated failures
      + (J5) Introduce each new term or acronym with a simple definition and everyday example before using it.
```