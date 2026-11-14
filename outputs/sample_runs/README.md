# Sample runs (real Groq runs, kept as evidence)

Each folder is a complete run: `rejection_log.md` (start here), `lesson_final.md`, every draft in
`attempts/`, and `run.json` (full trace). They show the loop working AND how the evaluator itself was
debugged from real logs.

| Folder | Result | What it shows |
|---|---|---|
| `01_evaluator_false_positive_unicode_hyphen` | Not shipped | Writer fixed every real issue, but D6 kept failing on "Coronavirus Disease 2019 (COVID‑19)". Root cause: a non-breaking hyphen (U+2011) in my regex check. Fixed with Unicode normalisation + a regression test. |
| `02_learner_judge_too_strict` | Not shipped | Real catches on draft 1 (J1: "RAG fixes these issues" conflicts with F08). Then the simulated learner (J5) failed every new word even when explained in the same sentence. Fixed by recalibrating the persona, verifying quotes and adding comprehension questions. |
| `03_writer_model_degenerated` | Not shipped | Qwen as writer fell into repetition loops and bolded every word. The system correctly refused to ship. Fixed with an output guard and by moving Qwen to the learner role. Also: judge caught "It does not guess" against misconception M08, added from human feedback. |
| `04_shipped_with_j4_overturn` | Shipped, attempt 3 | The judge failed J4 for terms defined inline in the same sentence; the code overturned it because every quoted sentence defined its term. |
| `05_final_shipped_lesson` | **Shipped, attempt 2** | The submitted lesson. Draft 1 failed only D6 (COVID not expanded); retry passed all 14 checks with 5 learned rules applied. |

The submitted lesson document = run 05 plus one human review edit (example organisation renamed to an
imaginary one), see `final_lesson/`.
