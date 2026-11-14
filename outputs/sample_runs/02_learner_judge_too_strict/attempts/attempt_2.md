# Intro to Retrieval-Augmented Generation (RAG)

## Before We Start

In this lesson, you will learn how AI uses your files to answer questions. This makes AI more helpful and accurate. This skill is very useful for AI jobs. Companies want AI that knows their own data. You do not need to code today. We will only talk about simple ideas.

## What Is Retrieval-Augmented Generation (RAG)?

**Retrieval-Augmented Generation** is a method for AI. It has two main parts. First, the AI finds relevant information. Second, it writes an answer using that information.

Think of a student in an exam. Without RAG, the student writes from memory. This is like a "closed-book" exam. They might forget things. With RAG, the student opens their book. They find the right page first. Then they write the answer. This is like an "open-book" exam.

**Retrieval** means finding the right text from a source. **Augmented** means adding helpful extra information. **Generation** means writing the final answer. The AI looks up facts before it speaks. This helps it give better answers.

## Why Does It Matter?

AI models have limits. They learn from data up to a specific date. This date is called the **knowledge cutoff**. They do not know news from last week. They also do not know your private company rules.

Sometimes, AI makes up false facts. This is called **hallucination**. The AI sounds confident, but the fact is wrong. RAG helps reduce this problem. It gives the AI real, relevant text to look at. This makes the answer more accurate. However, it does not remove errors completely. If the source text is wrong, the answer can still be wrong.

You can also see the source of the answer. This builds your **trust** in the AI. You can check the original document yourself.

## How Does It Work?

We will use one running example. Imagine you have a file called `HR_Handbook.pdf`. You ask: "What is the leave policy for sick days?".

RAG has two main stages. We call them **Indexing** and **Query**.

### Stage 1: Preparing the Files (Indexing)

This is done once before you ask questions. It is like organizing a library.

1.  **Loading**: The system collects documents. For us, this is the `HR_Handbook.pdf`.
2.  **Chunking**: The system cuts the long document into small pieces. We call these **chunks**. Think of cutting a book into single paragraphs. Small chunks are easier to search.
3.  **Embedding**: The system turns each chunk into a list of numbers. This list is called an **embedding**. These numbers represent the *meaning* of the text. Texts with similar meanings get similar numbers.
4.  **Storing**: The system saves these number lists in a special database. This is called a **vector database**. It is built for searching by meaning.

### Stage 2: Answering the Question (Query)

This is done every time you type a question.

1.  **Question Embedding**: The system turns your question into numbers too.
2.  **Semantic Search**: The system looks in the database. It finds the chunks whose numbers are most similar to your question. This is called **semantic search**. It searches by meaning, not just exact words.
3.  **Augmentation**: The system takes the top few best-matching chunks. It adds them to your question. This creates a new input message called a **prompt**.
4.  **Generation**: The AI reads the question and the added chunks. It writes the answer. The AI model itself does not change. It just reads the notes you gave it.

## A Full Example

Let us look at a fresh, concrete question.

Imagine you have a file called `Product_Manual.pdf`. You ask: "How do I reset the Wi-Fi password?".

1.  **Search**: The system turns your question into numbers. It searches the database. It finds chunks related to "reset" and "Wi-Fi".
2.  **Find**: It finds a chunk from page 45. The text says: "To reset Wi-Fi, hold the button for 10 seconds."
3.  **Answer**: The AI reads this specific text. It writes: "To reset the Wi-Fi password, please hold the button for 10 seconds. This is from page 45 of the manual."
4.  **Result**: The answer is based on the document. It cites the source. You can check page 45 yourself. If the manual was wrong, the answer would be wrong too. So, the quality of the answer depends on the quality of the documents.

## Where Is It Used?

RAG is used in many real jobs.

*   **Customer Support**: Bots read company help pages. They answer user questions correctly based on those pages.
*   **Legal AI**: Lawyers use it to search large case files. It finds relevant laws quickly.
*   **Personal Assistants**: They use your personal notes and emails. They answer based on your own data.

However, RAG has limits. If the document is not in the database, the AI cannot answer. If the search finds the wrong page, the answer will be wrong. RAG reduces **hallucination**, but it does not remove it completely.

## Key Words

*   **Retrieval-Augmented Generation (RAG)**: A method where AI finds information first, then writes an answer using it.
*   **Retrieval**: The act of finding the right information from a source.
*   **Augmented**: Adding helpful extra information to help the AI answer.
*   **Generation**: The act of writing the final answer.
*   **Knowledge Cutoff**: The date after which the AI does not know new facts.
*   **Hallucination**: When AI makes up a fact that is not true.
*   **Chunking**: Cutting long text into small pieces.
*   **Embedding**: Turning text into a list of numbers so computers can compare meanings.
*   **Vector**: A list of numbers that represents the meaning of text.
*   **Vector Database**: A special storage place for these number lists.
*   **Semantic Search**: Searching by meaning, not just exact words.
*   **Prompt**: The full text input given to the AI, including the question and added notes.
*   **Indexing**: The one-time setup where documents are prepared and stored.
*   **Query**: The step where the user asks a question and the system finds answers.

## Quick Recap

*   **RAG** means find information first, then write the answer.
*   It helps AI answer questions about private or new data.
*   Documents are cut into small **chunks**.
*   Chunks are turned into numbers called **embeddings**.
*   These numbers are stored in a **vector database**.
*   When you ask a question, the AI finds similar numbers.
*   The AI reads the matching text and writes the answer.
*   The AI model itself is not changed or retrained.

## Check Yourself

**Q1: Does RAG change the brain of the AI model?**
Answer: No, the model stays the same. It just reads extra notes provided during the question.

**Q2: What is 'chunking'?**
Answer: It is the process of cutting a long document into small, readable pieces.

**Q3: Why do we use a Vector Database?**
Answer: To store the number lists (embeddings) so we can find similar texts quickly by meaning.

**Q4: What is a 'hallucination'?**
Answer: It is when the AI makes up a false fact that is not in the source documents.

**Q5: If the source document has a mistake, will RAG be correct?**
Answer: No, if the source document is wrong or outdated, the RAG answer can also be wrong.