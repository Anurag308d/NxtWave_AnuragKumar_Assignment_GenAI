# Rejection Log: Introduction to RAG (Retrieval-Augmented Generation)

- Run ID: `20261113-143944-abcc`
- Final status: **NOT SHIPPED (flagged for human review)**
- Attempts: 3 (max 3)
- Deliberate error injection: off
- Learned rules applied from memory: 5

## Rules applied from memory (self-evolving prompt)
- (J1, human, v2) Never claim the model cannot make things up when the documents lack the answer. Say it may still guess, so good documents and good search matter.
- (J1, auto, v1) Accurately define LLM as Large Language Model, avoid claiming RAG fully eliminates hallucinations, and do not introduce undefined acronyms like LTM.
- (D8, auto, v1) Ensure the lesson contains at least 900 words by expanding each section with examples and explanations.
- (D6, auto, v1) When first using any acronym, write its full term followed by the abbreviation in parentheses.
- (D5, auto, v1) Include every technical term used in the lesson in the Key Words section, providing a concise definition for each.

## Summary across attempts

| Check | Dimension | Attempt 1 | Attempt 2 | Attempt 3 |
|---|---|---|---|---|
| D1 Required sections present | coherent teaching flow | PASS | **FAIL** | **FAIL** |
| D2 Readability (Flesch >= 60) | beginner-friendly language | PASS | PASS | PASS |
| D3 Short sentences | beginner-friendly language | PASS | PASS | PASS |
| D4 No hard / fancy words | beginner-friendly language | PASS | PASS | PASS |
| D5 Every technical term is in Key Words | clear, no unexplained jargon | **FAIL** | **FAIL** | **FAIL** |
| D6 Acronyms expanded | clear, no unexplained jargon | **FAIL** | PASS | **FAIL** |
| D7 Enough examples | teaches by example | PASS | **FAIL** | PASS |
| D8 Length in range | covers the key points | PASS | **FAIL** | PASS |
| D9 Self-check quiz | coherent teaching flow | PASS | **FAIL** | **FAIL** |
| J1 Factually accurate and grounded | accurate & grounded | **FAIL** | **FAIL** | **FAIL** |
| J2 Covers all key points | covers the key points | PASS | PASS | **FAIL** |
| J3 Teaches through concrete examples | teaches by example | PASS | **FAIL** | PASS |
| J4 Coherent teaching flow | coherent teaching flow | PASS | **FAIL** | **FAIL** |
| J5 Beginner learner understands it | beginner-friendly language | PASS | **FAIL** | PASS |

## Attempt 1: REJECT

Stats: 1159 words, Flesch 80.4, avg sentence 6.6 words.

### D5 Every technical term is in Key Words: FAILED
- Why: Technical terms used but not defined in Key Words: knowledge base, query
- Evidence: knowledge base
- Evidence: query
- Fix requested: Add each missing term to Key Words with a one-line simple definition, or remove the term if it is not needed.

### D6 Acronyms expanded: FAILED
- Why: Acronyms never written in full: COVID, LLM, WHO
- Evidence: COVID
- Evidence: LLM
- Evidence: WHO
- Fix requested: Write each acronym in full the first time, e.g. 'Large Language Model (LLM)'.

### J1 Factually accurate and grounded: FAILED
- Why: The lesson claims the AI never guesses, which is a known misconception about RAG.
- Evidence: "The AI reads this. It writes the answer based on the facts. It does not guess." (conflicts with M08: RAG does not guarantee the AI never guesses; the model may still hallucinate when retrieval fails)
- Fix requested: Replace the sentence with something like: "The AI reads the prompt and tries to answer using the provided facts, but if the retrieved chunks are insufficient it may still generate or hallucinate an answer."

## Attempt 2: REJECT

Stats: 425 words, Flesch 88.1, avg sentence 5.7 words.

### D1 Required sections present: FAILED
- Why: Missing sections: Why it matters, How it works, Example, Key Words, Recap, Check Yourself
- Evidence: Why it matters
- Evidence: How it works
- Evidence: Example
- Evidence: Key Words
- Evidence: Recap
- Evidence: Check Yourself
- Fix requested: Add the missing sections as '## ' headings in the required order.

### D5 Every technical term is in Key Words: FAILED
- Why: No Key Words section, so no term is defined.
- Evidence: large language model
- Evidence: retrieval
- Evidence: generation
- Evidence: augmented
- Evidence: embedding
- Fix requested: Add a '## Key Words' section defining every technical word in one simple sentence.

### D7 Enough examples: FAILED
- Why: Example section present: False; example markers: 4.
- Evidence: markers=4
- Fix requested: Add a full worked example section and at least one everyday analogy.

### D8 Length in range: FAILED
- Why: 425 words (need 900-2300).
- Evidence: words=425
- Fix requested: Add more explanation and examples.

### D9 Self-check quiz: FAILED
- Why: Quiz has 0 questions and 0 answers (need 3 each).
- Evidence: questions=0
- Evidence: answers=0
- Fix requested: Add at least 3 simple questions in 'Check Yourself', each followed by 'Answer: ...'.

### J1 Factually accurate and grounded: FAILED
- Why: The lesson misdefines the acronym LLM, calling it "Large Model" instead of "Large Language Model".
- Evidence: "RAG is a method for making **Large** **Model** (LLM) **answers** **better**." (conflicts with F04: LLM stands for Large Language Model)
- Fix requested: Replace "Large Model (LLM)" with "Large Language Model (LLM)" and ensure the definition matches F04.

### J3 Teaches through concrete examples: FAILED
- Why: No concrete running example is present, and the only analogy is generic; it does not meet the requirement for a detailed Indian‑relevant example.
- Evidence: The lesson provides only an open‑book exam analogy and repeats headings; it does not walk through a concrete step‑by‑step example of loading a document, chunking, embedding, retrieving a chunk, augmenting the prompt and generating an answer.
- Fix requested: Insert a concrete example, e.g., loading a Hindi‑language college handbook PDF, chunking it into paragraph‑sized pieces, embedding them, storing in a vector DB, then querying "What is the deadline for scholarship applications?" showing retrieval of the relevant chunk, augmentation in the prompt, and the LLM generating the answer.

### J4 Coherent teaching flow: FAILED
- Why: The lesson is disorganized, repeats the same content, introduces terms incorrectly before definition, and uses fragmented wording, making it hard for a beginner to follow.
- Evidence: Repeated sections titled "## What Is RAG?" appear four times with identical content, causing disjointed flow.
- Evidence: "RAG is a method for making **Large** **Model** (LLM) **answers** **better**." defines LLM incorrectly before any explanation of LLMs.
- Evidence: Broken words such as "Retri val" and "Aug mented" interrupt readability.
- Fix requested: Rewrite the lesson in a linear structure: (1) introduce LLMs correctly, (2) define RAG and its two phases, (3) explain indexing steps, (4) explain query steps, (5) give analogy, (6) provide concrete example, (7) list benefits and limitations. Remove duplicate sections and fix broken word splits.

### J5 Beginner learner understands it: FAILED
- Why: Simulated learner got stuck 2 time(s) (blocking). Main idea understood: True.
- Evidence: "Large Model (LLM)" -> The abbreviation LLM is used without a simple explanation, so Ravi does not know what it means
- Evidence: "adds the text to the prompt" -> The word prompt is used without a simple explanation, so Ravi cannot follow how the text is used
- Fix requested: Rewrite each quoted sentence in simpler words and explain the missing idea before using it.

### What changed on this retry
- Fixed checks: D6
- Still failing: D5, J1
- Newly failing (regressions): D1, D7, D8, D9, J3, J4, J5
- Lines added / removed: 29 / 137
- Stats before -> after: {'words': 1159, 'flesch_reading_ease': 80.4, 'avg_sentence_words': 6.6} -> {'words': 425, 'flesch_reading_ease': 88.1, 'avg_sentence_words': 5.7}
- Offending text from J1: "The AI reads this. It writes the answer based on the facts. It does not guess." -> removed/rewritten

## Attempt 3: REJECT

Stats: 1842 words, Flesch 81.1, avg sentence 6.5 words.

### D1 Required sections present: FAILED
- Why: Missing sections: Key Words, Recap, Check Yourself
- Evidence: Key Words
- Evidence: Recap
- Evidence: Check Yourself
- Fix requested: Add the missing sections as '## ' headings in the required order.

### D5 Every technical term is in Key Words: FAILED
- Why: No Key Words section, so no term is defined.
- Evidence: large language model
- Evidence: retrieval
- Evidence: generation
- Evidence: augmented
- Evidence: embedding
- Fix requested: Add a '## Key Words' section defining every technical word in one simple sentence.

### D6 Acronyms expanded: FAILED
- Why: Acronyms never written in full: HR, LLS
- Evidence: HR
- Evidence: LLS
- Fix requested: Write each acronym in full the first time, e.g. 'Large Language Model (LLM)'.

### D9 Self-check quiz: FAILED
- Why: Quiz has 0 questions and 0 answers (need 3 each).
- Evidence: questions=0
- Evidence: answers=0
- Fix requested: Add at least 3 simple questions in 'Check Yourself', each followed by 'Answer: ...'.

### J1 Factually accurate and grounded: FAILED
- Why: The lesson misdefines LLM and incorrectly claims the model does not use its prior knowledge, which are factual errors.
- Evidence: "The Large Model (LLM) receives this prompt. It is a Large Model trained on huge text data." (conflicts with F04: LLM stands for Large Language Model)
- Evidence: "It does not use its old memory. It only reads the note." (conflicts with F21: the model's internal knowledge remains and can still influence the answer)
- Fix requested: Correct the definition to "Large Language Model (LLM)" and state that the model still retains its trained knowledge but the retrieved text guides its answer.

### J2 Covers all key points: FAILED
- Why: Key point K3 (ability to show sources) is not covered.
- Evidence: Missing point: the lesson never mentions that RAG can show the sources (documents) used for an answer, which is required by K3.
- Fix requested: Add a sentence explaining that RAG systems can display the retrieved chunks or document references alongside the answer so users can verify the source.

### J4 Coherent teaching flow: FAILED
- Why: The lesson jumps between many repetitive example sections and introduces undefined terms, making the teaching sequence incoherent for beginners.
- Evidence: Repeated "## A full example" sections cause disjointed flow and confuse the reader.
- Evidence: The term "LLL" (Large Model) appears without definition, after many uses of "LLM", breaking logical order.
- Fix requested: Organize the content into a single clear example section, remove redundant repeats, and ensure all acronyms (LLM) are defined before use; avoid introducing new terms like "LLL" without explanation.

### What changed on this retry
- Fixed checks: D7, D8, J3, J5
- Still failing: D1, D5, D9, J1, J4
- Newly failing (regressions): D6, J2
- Lines added / removed: 286 / 59
- Stats before -> after: {'words': 425, 'flesch_reading_ease': 88.1, 'avg_sentence_words': 5.7} -> {'words': 1842, 'flesch_reading_ease': 81.1, 'avg_sentence_words': 6.5}
- Offending text from J1: "RAG is a method for making **Large** **Model**" -> removed/rewritten
- Offending text from J3: "The lesson provides only an open‑book exam analogy and repeats headings; it does not walk through a concrete step‑by‑step example of loading a document, chunkin" -> removed/rewritten
- Offending text from J4: "Repeated sections titled "## What Is RAG?" appear four times with identical content, causing disjointed flow." -> removed/rewritten
- Offending text from J4: "RAG is a method for making **Large** **Model** (LLM) **answers** **better**." defines LLM incorrectly before any explanation of LLMs." -> removed/rewritten
- Offending text from J4: "Broken words such as "Retri val" and "Aug mented" interrupt readability." -> removed/rewritten
- Offending text from J5: "adds the text to the prompt" -> removed/rewritten

## New rules learned after this run
- (D1) Include a final checklist ensuring each required section appears, using exact headings: What is, Why it matters, How it works, Example, Key Words, Recap, Check Yourself.
- (D5) Include a "Key Words" section listing and defining every technical term used in the lesson.
- (D6) When first using any acronym, write its full form followed by the abbreviation in parentheses.
- (D7) Include an "Example" section containing at least two distinct examples or analogies that illustrate the concept.
- (D9) Include a self‑check quiz with at least three distinct questions, each followed by its correct answer.
- (J1) Always define LLM as “Large Language Model”, note RAG only reduces hallucination and the model may still guess when retrieval fails.
- (J4) Introduce each new term before its first use and include only one concise example section to maintain clear, sequential flow.
- (J5) When introducing technical terms (e.g., LLM, prompt), include a brief plain-language definition in parentheses for non‑English‑medium learners.

## Event trace
```
14:39:44 [memory] 5 learned rule(s) loaded for the generator; 4 past failure example(s) loaded for the evaluator
14:41:04 [plan] 'Intro to Retrieval-Augmented Generation (RAG)' with 9 sections; analogy: Like a student who first looks up the right chapter in a book and then asks the 
14:41:04 [retrieve] 25 distinct source facts retrieved across 9 sections (BM25)
14:41:40 [generate] attempt 1: 1159 words
14:41:50 [evaluate] attempt 1: 11/14 checks passed -> REJECTED (D5, D6, J1)
14:42:16 [regenerate (retry 1/2)] attempt 2: 425 words
14:42:52 [evaluate] attempt 2: 5/14 checks passed -> REJECTED (D1, D5, D7, D8, D9, J1, J3, J4, J5)
14:42:59 [regenerate (retry 2/2)] attempt 3: 1842 words
14:44:19 [evaluate] attempt 3: 7/14 checks passed -> REJECTED (D1, D5, D6, D9, J1, J2, J4)
14:44:19 [human_review] retries exhausted; best = attempt 1 -> NOT shipped, flagged for a human
14:45:01 [learn] 8 new rule(s) learned from repeated failures
      + (D1) Include a final checklist ensuring each required section appears, using exact headings: What is, Why it matters, How it works, Example, Key Words, Recap, Check Yourself.
      + (D5) Include a "Key Words" section listing and defining every technical term used in the lesson.
      + (D6) When first using any acronym, write its full form followed by the abbreviation in parentheses.
      + (D7) Include an "Example" section containing at least two distinct examples or analogies that illustrate the concept.
      + (D9) Include a self‑check quiz with at least three distinct questions, each followed by its correct answer.
      + (J1) Always define LLM as “Large Language Model”, note RAG only reduces hallucination and the model may still guess when retrieval fails.
      + (J4) Introduce each new term before its first use and include only one concise example section to maintain clear, sequential flow.
      + (J5) When introducing technical terms (e.g., LLM, prompt), include a brief plain-language definition in parentheses for non‑English‑medium learners.
```