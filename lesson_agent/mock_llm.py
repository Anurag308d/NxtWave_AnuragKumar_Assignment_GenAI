"""Offline mock LLM so the whole graph can be tested without an API key.

Behaviour is scripted to exercise the loop: the first draft has real
problems (an undefined term, a hard word, a missing key point), the judge
reports them, and the revision fixes them. With injection on, the judge
catches the planted misconception.
"""
from __future__ import annotations

import json
import re

from .llm import Usage

_GOOD = """# Introduction to RAG: How AI Finds Facts Before It Answers

## Before We Start
In this lesson you will learn what RAG is. You will see why it is useful. You will also see how it works, step by step.
Many AI jobs today use RAG. So this is a great first topic for your AI career.

## What Is RAG?
RAG stands for **Retrieval-Augmented Generation (RAG)**. Let us break the name into three parts.
**Retrieval** means finding and bringing back useful information. **Augmented** means added to or made stronger.
**Generation** means writing or creating an answer.

So RAG means this: first find useful information, then add it to the question, then write the answer.

Think of an exam. In a closed-book exam, you write only from memory. You may forget things. You may even guess.
In an open-book exam, you first open the book and find the right page. Then you write your answer. RAG is the open-book exam for AI.

## Why Does It Matter?
AI chat tools like ChatGPT run on a **Large Language Model (LLM)**. An LLM is a computer program that has read a huge amount of text. It can understand questions and write answers like a human.

But an LLM has three big problems.
- It learned from data up to a certain date. This date is called its **knowledge cutoff**. It does not know about things that happened after that.
- It does not know your private documents. For example, it has never read your college rulebook.
- Sometimes it gives an answer that sounds sure but is wrong or made up. This is called **hallucination**.

RAG helps with all three. It gives the model real and fresh text to read before it answers.
- The answers can use new or private information.
- There are fewer made-up answers. RAG reduces mistakes, but it does not remove them fully.
- There is no need to train the model again. You only add or change documents.
- The system can show which document the answer came from. So you can check it.

## How Does It Work?
Let us use one example. Your college has a 200-page rulebook. A student asks a chatbot: "How many days can I be absent before I miss the exam?"

RAG works in two phases. The first phase happens once, before any question. The second phase happens every time someone asks.

### Phase 1: Getting the documents ready (indexing)
**Indexing** means preparing the documents so they are easy to search later.
1. **Collect** the documents. Here, it is the college rulebook PDF.
2. **Chunking.** The long rulebook is cut into small pieces called **chunks**. Each chunk is a few paragraphs. Small pieces are easier to search.
3. **Embedding.** Each chunk is turned into a list of numbers called an **embedding**. Another name for this list is a **vector**. Chunks with similar meaning get similar numbers.
4. **Storing.** All the embeddings are saved in a **vector database**. This is a special database that can search by meaning.

### Phase 2: Answering the question
5. **Retrieve.** The student's question, or **query**, is also turned into an embedding. The system finds the chunks with the closest numbers. This is **semantic search**, which means search by meaning, not only by exact words. It finds the chunk about "attendance rules".
6. **Augment.** The best chunks are added to the **prompt**. A prompt is the text we give to the LLM. It now says: "Use this rule text to answer the question."
7. **Generate.** The LLM reads the question and the rule text. Then it writes: "You need at least 75% attendance to sit for the exam."

Only the top few chunks are given to the model, not the whole rulebook. The model can read only a limited amount of text at one time. This limit is called the **context window**.

One important point: the model itself does not change. RAG does not train the model again. It only changes what we give the model to read.

## A Full Example
Imagine a railway enquiry chatbot. A passenger asks: "Is my train to Lucknow late today?"
- The LLM alone cannot know today's train status. Its knowledge stopped at its cutoff date.
- With RAG, the system first searches today's train status page.
- It finds the chunk: "Train 12230 is running 40 minutes late."
- It adds this chunk to the prompt with the question.
- The LLM writes: "Yes, your train is running about 40 minutes late."

The model did not learn anything new. It simply read the right information at the right time.

## Where Is It Used?
- Customer support chatbots that answer from a company's help pages.
- College or office chatbots that answer from their own documents.
- Search tools that answer from the latest news.
- Helpers for doctors and lawyers that answer from their reference books.

RAG also has limits. If the search finds the wrong chunk, the answer can still be wrong.
If the documents are old or wrong, the answers will be wrong too. RAG also adds extra steps, so it can be a little slower.

## Key Words
- **Retrieval**: Finding and bringing back useful information.
- **Augmented**: Added to or made stronger.
- **Generation**: Writing or creating an answer.
- **Large Language Model (LLM)**: A computer program that has read a lot of text and can write answers.
- **Knowledge cutoff**: The date after which the model knows nothing new.
- **Hallucination**: When AI gives a confident answer that is false.
- **Indexing**: Preparing documents so they are easy to search.
- **Chunk**: A small piece of a long document.
- **Embedding**: A list of numbers that stores the meaning of a text.
- **Vector**: Another name for this list of numbers.
- **Vector database**: A database that stores embeddings and searches by meaning.
- **Query**: The question a user asks.
- **Semantic search**: Searching by meaning, not only by exact words.
- **Prompt**: The text input we give to an LLM.
- **Context window**: The limit on how much text a model can read at one time.
- **Weights**: The numbers inside a model that store what it learned in training.
- **Fine-tuning**: Training a model more on new data, which changes its weights.

## Quick Recap
- RAG means: find useful information first, then write the answer.
- It is like an open-book exam for AI.
- It helps with old knowledge, private documents and made-up answers.
- First, documents are cut into chunks, turned into embeddings and stored.
- Then, for each question, the best chunks are found and added to the prompt.
- The model is not trained again. Only its input changes.
- If the search finds wrong chunks, the answer can still be wrong.

## Check Yourself
1. What do the three letters in RAG stand for?
Answer: Retrieval, Augmented, Generation.
2. Does RAG train the model again on your documents?
Answer: No. The model stays the same. RAG only adds useful text to the prompt.
3. Why are documents cut into chunks?
Answer: Small pieces are easier to search and fit in the model's context window.
4. Can RAG still give a wrong answer?
Answer: Yes. If it finds the wrong chunk or the documents are wrong, the answer can be wrong.
"""

_BAD_FIRST = _GOOD.replace(
    "- **Context window**: The limit on how much text a model can read at one time.\n", "").replace(
    "So this is a great first topic", "Furthermore, this is a pivotal first topic")


class MockLLM:
    def __init__(self):
        self.usage = Usage()
        self.gen_calls = 0

    def chat(self, system, user, *, model, temperature=0.3, json_mode=False, max_tokens=4096, role="llm"):
        self.usage.add(role, len(user) // 4, 500)
        if role == "generator":
            self.gen_calls += 1
            return _BAD_FIRST if self.gen_calls == 1 else _GOOD
        return json.dumps(self._json(role, user))

    def chat_json(self, system, user, **kw):
        return json.loads(self.chat(system, user, json_mode=True, **kw))

    def _json(self, role, user):
        if role == "planner":
            return {"title": "Introduction to RAG", "analogy": "open-book exam",
                    "running_example": "college rulebook chatbot",
                    "sections": [{"title": t, "goal": "", "points": []} for t in
                                 ["Before We Start", "What Is RAG?", "Why Does It Matter?", "How Does It Work?",
                                  "A Full Example", "Where Is It Used?", "Key Words", "Quick Recap", "Check Yourself"]],
                    "terms_to_define": ["LLM", "embedding"]}
        if role == "judge":
            lesson = user.split("LESSON:", 1)[-1]
            ok = {"pass": True, "evidence": [], "reason": "OK", "fix": ""}
            j1 = dict(ok)
            m = re.search(r"RAG works by retraining[^.]*\.", lesson)
            if m:
                j1 = {"pass": False, "evidence": [f"{m.group(0)} (conflicts with F21, M01)"],
                      "reason": "States that RAG retrains the model, a known misconception.",
                      "fix": "Remove the claim; say the model is not changed, only its input."}
            return {"J1": j1, "J2": ok, "J3": ok, "J4": ok}
        if role == "learner":
            return {"confusions": [], "ravi_explains_it": "RAG first finds the right page, then answers.",
                    "understood_main_idea": True}
        if role == "distiller":
            return {"rule": "Before finishing, re-read every bold term in the lesson and make sure it is listed in Key Words."}
        return {}
