# Introduction to Retrieval‑Augmented Generation (RAG)

## Before We Start
You will learn how a computer can look up fresh facts before writing an answer.  
This skill helps you build AI tools that give reliable, up‑to‑date information.  

## What Is Retrieval‑Augmented Generation?
**Retrieval‑Augmented Generation (RAG)** is a method that first **retrieves** (finds) useful text and then **generates** (writes) an answer using that text.  

Think of a student in an open‑book exam. The student first opens the textbook, finds the right page, and then writes the answer.  

A **Large Language Model (LLM)** is a computer program trained on huge amounts of text so it can understand questions and write human‑like replies.  

A **vector database** is a special storage that keeps text embeddings and can quickly find those that are close in meaning.

## Why Does It Matter?
LLMs only know what they learned before a certain date. They cannot see new documents unless those documents are given to them. This causes two problems:

* The model may give outdated or missing information.  
* It may produce answers that sound true but are actually false – this is called **hallucination**.

RAG helps with these problems:

* It lets the model answer questions about recent or private data without changing the model itself.  
* By giving real text to the model, it reduces hallucination, though it does not erase it completely.  
* Updating knowledge is as easy as adding, changing, or removing documents; the model itself does not need retraining.  
* RAG can also show the exact documents that were used, so users can verify the answer.

## How Does It Work?
RAG works in two phases: **indexing** (done once) and **query** (done for every question). We will follow one running example:

> *A student asks, “What are the latest Coronavirus Disease 2019 (COVID‑19) guidelines for schools in Delhi?”*

### 1. Indexing Phase (pre‑setup)

1. **Collect documents** – Gather PDFs, web pages, and school notices that contain the guidelines.  
2. **Chunking** – Break each long document into small pieces called **chunks**, each a few paragraphs long. Smaller pieces are easier to search and fit inside the model’s input limit.  
3. **Embedding** – Turn every chunk into a list of numbers called an **embedding**. Chunks with similar meaning get similar numbers.  
4. **Store in a vector database** – Save all embeddings and their original chunks in the vector database so they can be found quickly later.

### 2. Query Phase (answering)

1. **Question embedding** – Convert the user’s question into an embedding.  
2. **Semantic search** – Look in the vector database for chunks whose embeddings are closest to the question’s embedding. This finds the most relevant pieces of text.  
3. **Augmentation** – Attach the retrieved chunks to a **prompt** (the text sent to the LLM). The prompt often includes an instruction like “Answer only using the information below.”  
4. **Generation** – The LLM reads the prompt (question + retrieved chunks) and writes the final answer.

## A Full Example
Let’s see the whole flow with a fresh question:

> *“What is the new mask rule for students in Delhi schools after March 2024?”*

1. **Document collection** – The system already has a government circular (PDF), a news article, and the school’s notice board text.  
2. **Chunking & embedding** – Each document was split into small chunks and turned into embeddings during indexing.  
3. **User question** – The question is typed into a chat interface.  
4. **Question embedding** – The system creates an embedding for the question.  
5. **Semantic search** – The vector database returns three chunks:  
   * a paragraph from the government circular stating “Masks are mandatory for students above class 5 from 1 March 2024,”  
   * a news snippet confirming the rule,  
   * the school notice that says “Follow the government mask rule.”  
6. **Prompt creation** – The system builds a prompt:  

   ```
   Use only the information below to answer the question.
   Question: What is the new mask rule for students in Delhi schools after March 2024?
   Information:
   1. Masks are mandatory for students above class 5 from 1 March 2024. (Govt circular)
   2. News article confirms the rule. (Date: 2 March 2024)
   3. School notice: Follow the government mask rule.
   ```  

7. **Generation** – The LLM reads the prompt and writes:  

   *“From 1 March 2024, students in Delhi schools who are in class 5 or higher must wear masks inside the classroom. All schools should follow this government rule.”*  

The answer is short, accurate, and cites the latest sources.

## Where Is It Used?
* **Customer support** – A bot looks up the latest policy PDF before answering a user’s query.  
* **Healthcare** – A system fetches recent medical guidelines to help doctors with up‑to‑date advice.  
* **Education** – A study assistant pulls the newest syllabus or exam notice before explaining a topic.  
* **Legal help** – A tool searches the latest court rulings to give a lawyer a quick summary.  

**Limits**  
* If the stored documents are wrong or old, the system can give wrong answers.  
* The extra search step makes the response a little slower and needs a vector database to work.

## Key Words
- **Retrieval‑Augmented Generation (RAG)**: First find relevant text, then let a language model write an answer.  
- **Large Language Model (LLM)**: A program trained on huge text data that can understand questions and write human‑like text.  
- **Embedding**: A list of numbers that represents the meaning of a piece of text. Similar meanings have similar numbers.  
- **Chunk**: A small piece of a larger document, usually a few paragraphs long.  
- **Vector database**: A storage that keeps embeddings and can quickly find those that are close in meaning.  
- **Semantic search**: Searching by meaning, not just by exact words.  
- **Hallucination**: When an AI gives an answer that sounds confident but is actually false.  
- **Knowledge cutoff**: The latest date up to which a language model was trained on data.  
- **Prompt**: The text input sent to an LLM, such as a question plus any extra instructions.  
- **Indexing**: The preparation step where documents are turned into chunks and embeddings and stored.  
- **Query**: The step that happens each time a user asks a question, involving retrieval and generation.  

## Quick Recap
- RAG = Retrieval + Generation.  
- It works in two phases: indexing (prepare documents) and query (answer a question).  
- Indexing splits documents, makes embeddings, and stores them in a vector database.  
- Query turns the question into an embedding, finds similar chunks, and adds them to a prompt.  
- The LLM writes the final answer using the retrieved text.  
- RAG reduces hallucination and lets AI use fresh or private data without retraining.  
- Updating knowledge only needs new or changed documents, not a new model.  
- RAG can show the source documents so users can verify the answer.  
- Limits: slower response and depends on quality of stored documents.  

## Check Yourself
1. **What does RAG stand for?**  
   Answer: Retrieval‑Augmented Generation.  

2. **Why do we split documents into chunks?**  
   Answer: Smaller pieces are easier to search and fit inside the model’s input limit.  

3. **What is an embedding?**  
   Answer: A list of numbers that captures the meaning of a text piece.  

4. **How does RAG help with outdated information?**  
   Answer: It lets the system fetch the latest documents, so the answer uses current facts.  

5. **Name one limitation of RAG.**  
   Answer: If the stored documents are wrong, the system can give wrong answers.