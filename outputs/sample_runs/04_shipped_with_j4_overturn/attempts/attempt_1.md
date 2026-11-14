# Introduction to Retrieval‑Augmented Generation (RAG)

## Before We Start
You will learn what **RAG** means and how it works step by step.  
You will see why it helps give fresh, private, and correct answers.  
Knowing RAG opens many AI jobs that need reliable information.

## What Is Retrieval‑Augmented Generation?
**Retrieval‑Augmented Generation (RAG)** is a method that first **retrieves** useful text and then lets a **Large Language Model (LLM)** **generate** the answer.  
Think of a school library: you ask the librarian for a book, read the needed pages, and then write a short summary for your teacher. The librarian does not have to learn every book; you only bring the right pages to the exam.

## Why Does It Matter?
An LLM learns only from data that existed before a certain date. This date is called the **knowledge cutoff**. After that date the model does not know new facts.  
The model also cannot see your private documents unless you give them.  
Sometimes the model makes up facts. This is called a **hallucination**.  
RAG lets the model use fresh public data or private files without changing its internal weights.  
Answers become more accurate, up‑to‑date, and can show which documents were used.

## How Does It Work?
RAG has two main phases: **indexing** and **query**.

1. **Indexing phase** (done once before any question)  
   * **Chunking** – split each long document into small pieces called **chunks**. A chunk may be a few paragraphs.  
   * **Embedding** – a special AI model reads each chunk and creates a list of numbers, called an **embedding**. Think of it as a “meaning address”. Similar chunks get nearby addresses.  
   * **Storing** – the embeddings and their chunks are saved in a **vector database**. This database can quickly find pieces whose meaning matches a query.

2. **Query phase** (done every time a user asks)  
   * **Embedding the question** – the user’s question is turned into an embedding.  
   * **Retrieval** – the system looks in the vector database for chunks whose embeddings are close to the question embedding. This is **semantic search** (search by meaning, not just exact words).  
   * **Augmentation** – the found chunks are attached to the original question inside a **prompt**. The prompt may say, “Answer only using the information below.”  
   * **Generation** – the LLM reads the prompt and writes the final answer.

The LLM itself never changes; only the prompt changes.

### Running Example (IIT admission rules)
A student asks: “What are the latest IIT admission rules for 2025?”  

* **Chunking** – the official IIT PDF, a news article, and an FAQ page are each broken into small chunks.  
* **Embedding** – each chunk gets a meaning address and is stored.  
* **Question embedding** – the query “latest IIT admission rules 2025” becomes a meaning address.  
* **Retrieval** – the vector database returns three chunks: one from the PDF, one from the news article, and one from the FAQ that best match the query.  
* **Prompt** – the system builds a prompt:  
  ```
  Use the following documents to answer the question.
  Document 1: …
  Document 2: …
  Document 3: …
  Question: What are the latest IIT admission rules for 2025?
  ```  
* **Generation** – the LLM writes a concise answer and lists the three source titles.

## A Full Example
Let’s see the whole flow with a fresh question.

1. **Question** – “What are the latest IIT admission rules for 2025?”  
2. **Embedding** – the question is turned into a list of numbers.  
3. **Retrieval** – the vector database finds the three most similar chunks from the prepared documents.  
4. **Prompt creation** – the system adds those chunks to the prompt with an instruction like “Answer only using this information.”  
5. **Answer generation** – the LLM reads the prompt and writes:  
   *“For 2025, IITs will use the JEE Main score, require a minimum 75 % in Class 12, and allow two attempts. See the official PDF (page 5), the news article (line 3), and the FAQ (section 2).”*  

The answer includes the source titles so the student can verify the information.

## Where Is It Used?
* **Customer‑support bots** – they pull the latest policy PDFs and answer user questions.  
* **Enterprise search** – employees ask about internal reports and get answers from the company’s knowledge base.  
* **Educational tools** – students ask about the newest syllabus and receive answers from updated textbooks.  

**Limits** – If the retrieved chunks are irrelevant or outdated, the answer can still be wrong. The system also shows sources, so users can check the information.

## Key Words
- **Retrieval**: finding useful pieces of text from a collection.  
- **Generation**: writing an answer using a language model.  
- **Augmented**: added with extra information before answering.  
- **Large Language Model (LLM)**: a big AI that can write text in many styles.  
- **Knowledge cutoff**: the date after which the model has no new training data.  
- **Hallucination**: when the model makes up facts that are not true.  
- **Chunk**: a small piece of a longer document, like a few paragraphs.  
- **Embedding**: a list of numbers that represents the meaning of a text piece.  
- **Vector**: another word for an embedding; a “meaning address”.  
- **Vector database**: a storage that can quickly find vectors that are close in meaning.  
- **Prompt**: the text given to the LLM that tells it what to do.  
- **Fine‑tuning**: training the model again on new data to change its internal weights.  
- **Indexing**: the preparation steps (chunking, embedding, storing) done before any question.  
- **Knowledge base**: the collection of documents that the system can search.  
- **Query**: the user’s question that starts the retrieval‑generation process.  
- **Semantic search**: looking for text that means the same thing, not just matching words.

## Quick Recap
- RAG = retrieve then generate.  
- It helps LLMs give up‑to‑date, private, and sourced answers.  
- Two phases: **indexing** (chunk → embed → store) and **query** (search → prompt → generate).  
- The LLM itself is unchanged; only the prompt changes.  
- Good retrieval is essential; wrong chunks lead to wrong answers.  
- RAG does not remove hallucinations completely, but it reduces them.  

## Check Yourself
1. **What does RAG stand for?**  
   Answer: Retrieval‑Augmented Generation.  

2. **Why do we need RAG for recent facts?**  
   Answer: Because LLMs stop learning after their knowledge cutoff.  

3. **Name one step in the indexing phase.**  
   Answer: Chunking the documents.  

4. **What is a hallucination in AI?**  
   Answer: When the model invents information that isn’t true.  

5. **Give one real‑world use of RAG.**  
   Answer: A customer‑support bot that uses the latest policy documents.