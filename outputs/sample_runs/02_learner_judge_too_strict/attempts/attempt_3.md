# Intro to Retrieval-Augmented Generation (RAG)

## Before We Start
In this lesson you will learn how a computer can look up information before answering a question.  
This skill makes AI smarter and more useful.  
It is a good start if you want a job in AI.  
You do not need to write code now. We will use simple ideas.

## What Is Retrieval-Augmented Generation (RAG)?
Retrieval-Augmented Generation (RAG) is a way for a computer to find useful text and then write an answer from it.  
Think of a student who first opens a book to find the right page, then writes the answer.  
With RAG, the computer first searches for the right text, then uses that text to answer.

## Why Does It Matter?
AI models remember only what they were trained on.  
They do not know new events after a certain date, called the knowledge cutoff.  
Sometimes AI makes up facts that are not true; this is called hallucination.  
RAG reduces hallucination by giving the computer real text to read.  
If the text is wrong, the answer can still be wrong.  
RAG lets the computer answer new or private questions without retraining.

## How Does It Work?
RAG has two main parts: **indexing** and **query**.  
During indexing, you collect documents, split them into small pieces called **chunks**, turn each chunk into a list of numbers called an **embedding**, and store these embeddings in a special database.  
During query, the computer turns your question into an embedding, finds the most similar chunks, adds those chunks to the question, and then writes the answer.  
Only the top few chunks are used because the computer can handle only a limited amount of text at once.

### Running Example
Suppose you have a PDF of your college notice board.  
You want to know the rule for late return of library books.  
The system first prepares the PDF (indexing).  
When you ask the question, the system searches for the most relevant chunks and writes the answer.

## A Full Example
1. **Prepare the PDF** – the system loads the notice board file, splits it into small paragraphs, creates embeddings for each paragraph, and stores them.  
2. **Ask a question** – you type, “What is the rule for returning books late?”  
3. **Search** – the system turns the question into numbers and finds the paragraph that talks about late returns.  
4. **Answer** – the system reads that paragraph and writes, “Books must be returned within 5 days. A fine of ₹10 per day is charged.”  
5. **Check** – you can look at the paragraph in the PDF to confirm.

## Where Is It Used?
* Customer support bots that read company help pages.  
* Chatbots that answer questions about a college’s own documents.  
* Search assistants that pull the latest news from a set of web pages.  
* Helpers for doctors or lawyers that use their own reference books.  

**Limits** – If a needed document is missing, the system cannot answer.  
If the stored document is wrong, the answer will be wrong.  
RAG adds a search step, so it can be a little slower.

## Key Words
* **Retrieval-Augmented Generation (RAG)**: a method where a computer first finds useful text and then writes an answer from it.  
* **Retrieval**: finding the right text from a collection.  
* **Augmented**: adding extra information to help the answer.  
* **Generation**: writing the final answer.  
* **Large Language Model (LLM)**: a computer program that can understand questions and write human‑like text.  
* **Knowledge cutoff**: the last date up to which the model was trained.  
* **Hallucination**: when the model says something that is not true.  
* **Chunk**: a small part of a long document, like a paragraph.  
* **Embedding**: a list of numbers that represents the meaning of a chunk.  
* **Vector database**: a place that stores embeddings and lets the computer find similar ones quickly.  
* **Semantic search**: searching by meaning, not just by exact words.  
* **Prompt**: the text given to the computer, including the question and the retrieved chunks.  
* **Indexing**: the one‑time step of preparing and storing documents.  
* **Query**: the step of answering a question.  

## Quick Recap
* RAG lets a computer look up text before answering.  
* It helps answer new or private questions without retraining.  
* Documents are split into small **chunks**.  
* Each chunk becomes an **embedding** and is stored in a **vector database**.  
* When a question arrives, the system finds similar chunks and uses them to write the answer.  
* The computer’s internal knowledge does not change.  

## Check Yourself
**Q1:** Does RAG change what the computer knows inside?  
Answer: No, it only adds new text for the computer to read when answering.  

**Q2:** What is a **chunk**?  
Answer: A small piece of a long document, like a paragraph.  

**Q3:** Why do we use a **vector database**?  
Answer: To store embeddings so the computer can quickly find the most similar text.  

**Q4:** What does **hallucination** mean?  
Answer: When the computer says something that is not true.  

**Q5:** If the source document has a mistake, will RAG still give a correct answer?  
Answer: No, the answer will follow the mistake in the document.