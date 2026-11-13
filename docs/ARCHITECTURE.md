# Architecture and Design Decisions

## The problem, restated

The job is not "write a good prompt". It is to own a system that produces learning content
**and decides on its own whether that content is good enough to ship**. So most of the design
goes into the evaluator and the loop around it.

## Why an explicit LangGraph state machine

- The loop is a real cycle with a branch (pass / retry / give up). LangGraph makes that cycle
  explicit and inspectable: every node is a pure function `state -> update`. You can see in the trace
  exactly which node ran and why the router went where it did.
- Termination is guaranteed by the router (`attempt >= 1 + MAX_RETRIES -> human_review`), not by
  hoping the model behaves.
- Each node is swappable: a better retriever or a new judge is a one-node change.
- Alternative considered: a single "write and self-critique" prompt. Rejected because one model
  grading itself in the same context shares its own blind spots and gives no audit trail.

## Components and why each exists

| Node | Why |
|---|---|
| **load_memory** | Pulls learned rules (for the writer) and past failure examples (for the judge) before any work starts. |
| **plan** | Separates *what to teach* from *how to write it*. A plan with one analogy and one running example gives the lesson a spine and makes J3/J4 easier to pass. Falls back to a default outline if the planner fails, so planning can never kill a run. |
| **retrieve** | Grounding. A curated source pack (`sources/rag.md`: 31 facts, 7 misconceptions, 7 key points, each with an ID) is searched with BM25 per section. Facts with IDs let the judge say *"this sentence conflicts with F21"*, which is far more useful than *"seems wrong"*. BM25 instead of a vector DB because the pack is ~40 short facts; a vector DB would add setup with no gain at this size. |
| **generate / regenerate** | First draft from plan + facts. Retries are **targeted revisions**: the writer receives the previous lesson plus the exact failed checks, evidence quotes and a fix instruction, and is told to keep what passed. This converges faster than regenerating from scratch, which tends to fix one thing and break another. |
| **inject_error** | Planted, known mistakes (misconception, unexplained jargon, hard vocabulary) prove the evaluator works. It runs only on draft 1, only when asked. |
| **evaluate** | The rubric (below). |
| **ship / human_review** | If all checks pass it ships. If retries run out, the best attempt (fewest failures) is saved with a NOT SHIPPED banner. The system never silently ships a failing lesson. |
| **learn** | Updates memory and distils new rules from repeated failures. |

## The evaluator: hybrid by design

**Principle: measure what can be measured in code; use an LLM only for what needs a reader.**

- **Deterministic checks (D1–D9)** cover structure, readability, sentence length, hard words, jargon
  defined, acronyms, examples, length and quiz. They are free, instant and 100% repeatable, and
  they cannot be talked out of a fail. For a learner with limited English, readability and jargon are
  the most important dimensions, so making them hard numeric gates matters.
- **LLM judge (J1–J4)** covers what code cannot: factual accuracy against the source facts, key-point
  coverage, quality of examples, and teaching flow.
- **Simulated learner (J5)** is a different persona prompt: "Ravi", an 18-year-old Hindi-medium
  12th-pass student, reads the lesson and lists every sentence where he would get stuck. This checks
  comprehension from the learner's side, not the expert's side.

Further choices:

- **Hard pass/fail, no scores.** A score of 7.4/10 does not tell the writer what to fix. A failed check
  with a quote and a fix instruction does.
- **Different model for judging** (`openai/gpt-oss-120b` judges `llama-3.3-70b` output). This reduces
  self-preference bias. Both are configurable.
- **Evidence or it did not happen.** An LLM fail without a quoted sentence is overturned and logged.
  This stops the loop wasting retries on vague or invented complaints.
- **Temperature 0 for judging**, 0.6 for writing.
- **All checks run every time** (no early exit), so a retry gets the complete list of problems at once.

## Memory and self-evolution

SQLite, one file, zero setup, survives across runs.

1. Every check result of every attempt is stored (`check_events`).
2. **Prompt evolution:** when a check has failed ≥ `RULE_PROMOTION_THRESHOLD` times across runs, an
   LLM distils one short, specific rule from the real failure reasons. Active rules go into every
   future generation prompt. The system tracks failures after each rule was created; if a rule is not
   working it is rewritten (v2, v3). Rules are capped at 12 so the prompt does not grow forever.
3. **Rubric sharpening:** concrete past failures with evidence are shown to the judge as
   "problems like these must fail", which makes judging more consistent across runs.
4. **Human feedback** becomes a rule the same way (`main.py feedback`).
5. **Demo runs do not pollute learning:** injected-error attempts are logged but excluded.

## Trade-offs I made knowingly

| Choice | Gain | Cost |
|---|---|---|
| Curated source pack | Real grounding, fact-level evidence | Needs a pack per topic; other topics run ungrounded (flagged) |
| BM25, not embeddings | Zero setup, transparent | Weaker on synonyms (fine for 40 facts) |
| One judge call for J1–J4 | Fits Groq free-tier token limits | Checks are not fully independent; mitigated by per-check evidence and a separate learner call |
| Flesch formula | Objective, standard | Built for native English; used as a floor, not the only language check (D3, D4, D5, J5 also apply) |
| Max 2 retries | Bounded cost and time | A hard lesson may go to human review; that is the safe outcome |
| Targeted revision | Faster convergence | Can keep a weak structure from draft 1; the planner reduces this risk |

## What I would add with more time

- A small **golden set** of lessons with known defects to measure the judge's precision and recall,
  and run it on every rubric change (regression tests for the evaluator itself).
- Multiple judge samples with majority vote on borderline checks.
- Hindi or Hinglish glossary support and a translation pass.
- Automatic source-pack building (retrieve from trusted docs, then human approval).
- A/B testing of learned rules: keep a rule only if first-attempt pass rate improves.
