# Introduction to Retrieval‑Augmented Generation (RAG)

## Before We Start
In this lesson you will learn what Retrieval‑Augmented Generation (RAG) means.  
You will see how RAG helps an AI give recent and trustworthy answers.  
Understanding RAG opens entry‑level AI jobs that need reliable information.

## What Is Retrieval‑Augmented Generation?
Retrieval‑Augmented Generation (RAG) is a way for a computer to first **retrieve** useful text and then **generate** an answer.  
Think of a student who can open a school textbook during an exam. The student first finds the right page, then writes the answer. The textbook is the outside source, and the student’s writing is the generation.

## Why Does It Matter?
A **Large Language Model (LLM)** learns only from data that existed before a certain date.  
That date is called the **knowledge cutoff**. After the cutoff the model does not know new facts.  
The model also cannot see private papers unless we give them.  
Sometimes the model makes up facts. This is called a **hallucination**.  
RAG lets the model use fresh public data or private files without changing its internal knowledge.  
The result is more accurate, recent, and source‑visible answers.

## How Does It Work?
RAG works in two phases: **indexing** (once) and **query** (every time you ask).

### Indexing Phase  
1. **Loading** – collect documents such as PDFs, web pages, or notes.  
2. **Chunking** – split each long document into small pieces called **chunks**. A chunk can be a few paragraphs.  
3. **Embedding** – a small AI model reads the words in a chunk and creates a **meaning code**.  
   *A meaning code is simply a list of numbers that represents the idea in the text.*  
   *Texts about similar ideas get similar codes.*  
   *We call this list an **embedding**.*  
4. **Storing** – save each embedding together with its chunk in a **vector database**.  
   *A vector database can quickly find codes that are close in meaning.*

### Query Phase  
1. **Embedding the question** – the user’s question is also turned into a meaning code (an embedding).  
2. **Retrieval** – the system looks in the vector database for chunks whose codes are close to the question code. This is called **semantic search** (search by meaning).  
3. **Augmentation** – the found chunks are added to the user’s question inside a **prompt**. The prompt may say, “Answer only using this information.”  
4. **Generation** – the LLM reads the prompt and writes the final answer.

The LLM itself never changes; only the prompt changes.

### Running Example (IIT admission rules)
Imagine a student asks: “What are the latest Indian Institute of Technology (IIT) admission rules for 2025?”  

* **Loading** – we collect the official IIT admission PDF, a recent news article, and an FAQ page.  
* **Chunking** – each source is broken into small chunks of a few paragraphs.  
* **Embedding** – each chunk receives a meaning code (embedding) and is stored.  
* **Question embedding** – the query “latest IIT admission rules 2025” becomes a meaning code.  
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
Now we walk through a fresh question step by step.

1. **Question** – “What are the latest Joint Entrance Examination (JEE) score requirements for IITs in 2025?”  
2. **Embedding** – the question is turned into a meaning code (embedding).  
3. **Retrieval** – the vector database finds the three most similar chunks from the prepared documents.  
4. **Prompt creation** – the system adds those chunks to the prompt with the instruction “Answer only using this information.”  
5. **Answer generation** – the LLM reads the prompt and writes:  

   *“For 2025, IITs will use the Joint Entrance Examination (JEE) Main score, require at least 75 % marks in Class 12, and allow two attempts. See the official PDF (page 5), the news article (line 3), and the FAQ (section 2).”*  

The answer also shows the source titles so the student can verify the data.

## Where Is It Used?
* **Customer‑support bots** – they pull the latest policy PDFs and answer user questions.  
* **Enterprise search tools** – employees ask about internal reports and receive answers from the company’s knowledge base.  
* **Educational assistants** – students ask about the newest syllabus and get answers from updated textbooks.  

**Limits** – If the retrieved chunks are irrelevant or outdated, the answer can still be wrong. The system also shows sources, so users can check the information. RAG reduces hallucinations but does not remove them completely.

## Key Words
- **Large Language Model (LLM)**: a big AI that can write text in many styles.  
- **Retrieval**: finding useful pieces of text from a collection.  
- **Generation**: writing an answer using a language model.  
- **Augmented**: added with extra information before answering.  
- **Embedding**: a list of numbers that acts as a meaning code for a text piece.  
- **Vector**: another word for an embedding; a “meaning address”.  
- **Vector database**: a storage that can quickly find vectors that are close in meaning.  
- **Chunk**: a small piece of a longer document, like a few paragraphs.  
- **Prompt**: the text given to the LLM that tells it what to do.  
- **Hallucination**: when the model makes up facts that are not true.  
- **Knowledge cutoff**: the date after which the model has no new training data.  
- **Semantic search**: looking for text that means the same thing, not just matching words.  
- **Fine‑tuning**: training the model again on new data to change its internal knowledge.  
- **Indexing**: the preparation steps (chunking, embedding, storing) done before any question.  
- **Knowledge base**: the collection of documents that the system can search.  
- **Query**: the user’s question that starts the retrieval‑generation process.  

## Quick Recap
- RAG = retrieve then generate.  
- It helps LLMs give recent, private, and sourced answers.  
- Two phases: **indexing** (load → chunk → embed → store) and **query** (embed question → retrieve → prompt → generate).  
- The LLM itself stays the same; only the prompt changes.  
- Good retrieval is essential; wrong chunks lead to wrong answers.  
- RAG reduces but does not remove hallucinations completely.  

## Check Yourself
1. **What does RAG stand for?**  
   Answer: Retrieval‑Augmented Generation.  

2. **Why do we need RAG for recent facts?**  
   Answer: Because an LLM stops learning after its knowledge cutoff date.  

3. **Name one step in the indexing phase.**  
   Answer: Chunking the documents into smaller pieces.  

4. **What is a hallucination in AI?**  
   Answer: When the model invents information that isn’t true.  

5. **Give one real‑world use of RAG.**  
   Answer: A customer‑support bot that uses the latest policy documents.