# How AI Finds Answers in Your Files: Intro to RAG

## Before We Start

In this lesson, you will learn how AI reads your private files. It helps it give correct answers. This skill is very important for AI jobs. Companies need AI that knows their own data. You do not need to code today. We will only talk about ideas.

## What Is RAG?

**RAG** stands for **Retrieval-Augmented Generation**. It is a two-step process. First, the system finds information. Then, it writes an answer.

Think of a student in an exam. Without RAG, the student writes from memory. This is like a "closed-book" exam. With RAG, the student opens the book. They find the right page first. Then they write the answer. This is like an "open-book" exam.

**Retrieval** means finding the right text. **Generation** means writing the answer. The AI looks up facts before it speaks. This makes the answer better.

## Why Does It Matter?

AI models have limits. They learn from data up to a specific date. This is called the **knowledge cutoff**. They do not know news from last week. They also do not know your private company rules.

Sometimes, AI makes up false facts. This is called **hallucination**. It sounds confident but is wrong. RAG fixes these issues. It shows the AI real, new, and private text. The answer is based on true data. You can even see the source. This builds your **trust** in the AI.

## How It Works?

We will use one running example. Imagine you have a file called `HR_Handbook.pdf`. You ask: "What is the leave policy for sick days?".

RAG has two phases: **Indexing** and **Query**.

### Phase 1: The Setup (Indexing)

This is done once before you ask questions.

1.  **Chunking**: The AI cuts the long `HR_Handbook.pdf` into small, readable **chunks**. Think of cutting a book into single paragraphs. Small chunks are easy to read.
2.  **Embeddings**: The AI converts each text **chunk** into a list of numbers. This list is called a **vector**. These numbers represent the *meaning* of the text. Similar meanings get similar numbers.
3.  **Vector Storage**: These number vectors are sent to a special database. This is called a **Vector database**. It is fast and good at comparing meanings.

### Phase 2: The Question (Query)

This is done every time you type a question.

1.  **Question Vector**: The AI converts your question into numbers too.
2.  **Semantic Retrieval**: The system searches the **Vector database**. It finds the text chunks that are "closest" in number to your question. It does not just look for exact words. It understands the **meaning**.
3.  **Augmentation**: The system takes the top 3-5 best-matching chunks. It pastes them into the **prompt** (the message sent to the AI).
4.  **Generation**: The AI reads your question and the pasted chunks. It writes the answer. It does not change its own "brain". It just uses the provided **notes**.

## A Fresh, Concrete Question

Imagine you have a file called `Product_Manual.pdf`. You ask: "How do I reset the Wi-Fi password?".

1.  **Search**: The system looks for chunks related to "reset" and "Wi-Fi".
2.  **Find**: It finds a chunk from page 45. It says: "To reset Wi-Fi, hold the button for 10 seconds."
3.  **Answer**: The AI reads this text. It writes: "To reset the Wi-Fi password, please hold the button for 10 seconds. This is from page 45 of the manual."
4.  **Result**: The answer is correct. It cites the source. You can check page 45 yourself.

## Where Is It Used?

RAG is used in many real jobs.

*   **Customer Support**: Bots read company help pages. They answer user queries correctly.
*   **Legal AI**: Lawyers use it to search thousands of case files. It finds relevant laws quickly.
*   **Personal Assistants**: They remember your personal notes and emails. They answer based on your own data.

However, RAG has limits. If the document is not in the database, the AI cannot answer. If the search finds the wrong page, the answer will be wrong. RAG reduces **hallucination**, but it does not remove it completely.

## Key Words

*   **RAG**: A method where AI looks up facts before answering.
*   **Retrieval**: The act of finding the right information.
*   **Generation**: The act of writing the answer.
*   **Knowledge Cutoff**: The date after which the AI does not know new facts.
*   **Hallucination**: When AI makes up a fact that is not true.
*   **Chunking**: Cutting long text into small pieces.
*   **Embedding**: Turning text into numbers so computers can compare meanings.
*   **Vector**: A list of numbers that represents the meaning of text.
*   **Vector Database**: A special storage place for these number lists.
*   **Prompt**: The instruction and context given to the AI model.
*   **Indexing**: The one-time setup where documents are prepared.
*   **Query**: The step where the user asks a question.

## Quick Recap

*   **RAG** = Retrieve first, then Generate.
*   It solves the problem of AI not knowing private or new data.
*   Documents are cut into **chunks**.
*   Chunks are turned into numbers called **embeddings**.
*   These numbers are stored in a **Vector database**.
*   When you ask a question, the AI finds similar numbers.
*   The AI reads the matching text and writes the answer.
*   The AI model itself is not retrained or changed.

## Check Yourself

**Q1: Does RAG change the brain of the AI model?**
Answer: No, the model stays the same. It just reads extra notes provided during the query.

**Q2: What is 'chunking'?**
Answer: It is the process of cutting a long document into small, readable pieces.

**Q3: Why do we use a Vector Database?**
Answer: To store the number lists (embeddings) so we can find similar texts quickly by meaning.

**Q4: What is a 'hallucination'?**
Answer: It is when the AI makes up a false fact that is not in the source documents.

**Q5: If I ask a question about a file I did not upload, can RAG answer it?**
Answer: No, it can only use the files it has indexed in its database.