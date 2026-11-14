# Intro to Retrieval‑Augmented Generation (RAG)

## Before We Start
You will learn how a computer can look up fresh facts before writing an answer.  
This skill lets you build AI tools that give reliable, up‑to‑date information.  

## What Is Retrieval‑Augmented Generation?
**Retrieval‑Augmented Generation (RAG)** is a method where the system first **retrieves** (finds) useful text, then **generates** (writes) an answer using that text.  

Think of a student in an open‑book exam. The student first opens the textbook, finds the right page, and then writes the answer. Without the book, the student would have to rely only on memory.  

## Why Does It Matter?
Large language models (LLMs) only know what they learned before a certain date. They cannot see new documents unless they are given those documents. This can cause two problems:

* The model may give outdated or missing information.  
* It may create answers that sound true but are actually false – a problem called **hallucination**.

RAG helps solve these problems:

* It lets the model answer questions about recent or private data without changing the model itself.  
* By giving real text to the model, it reduces hallucination, though it does not erase it completely.  
* Updating knowledge is as easy as adding, changing, or removing documents; the model does not need expensive retraining.  

## How Does It Work?
RAG works in two phases: **indexing** (done once) and **query** (done for every question). We will follow the running example:  

> *A student asks, “What are the latest COVID‑19 guidelines for schools in Delhi?”*  

### 1. Indexing Phase (pre‑setup)

1. **Collect documents** – Gather PDFs, web pages, and school notices that contain the guidelines.  
2. **Chunking** – Break each long document into small pieces (chunks) of a few paragraphs each. Smaller pieces are easier to search and fit inside the model’s input limit.  
3. **Embedding** – Turn every chunk into a list of numbers called an **embedding**. Chunks with similar meaning get similar numbers.  
4. **Store in a vector database** – Save all embeddings and their original text in a special search system that can compare numbers quickly. This system is called a **vector database**.  

All these steps happen before any user asks a question.

### 2. Query Phase (answering)

1. **Convert the question to an embedding** – The student’s question is also turned into a list of numbers.  
2. **Semantic search** – The system looks in the vector database for chunks whose embeddings are closest to the question’s embedding. It picks the top few most relevant chunks.  
3. **Augmentation** – The chosen chunks are attached to the prompt that will be sent to the LLM. The prompt often includes an instruction like “Answer only using the information below.”  
4. **Generation** – The LLM reads the prompt (question + retrieved chunks) and writes the final answer in natural language.  

The result is an answer that is based on real, recent documents, not only on the model’s memory.

## A Full Example
Let’s see the whole flow with a fresh question:

> *“What is the new mask rule for students in Delhi schools after March 2024?”*

1. **Document collection** – The system already has a government circular (PDF), a news article, and the school’s own notice board text.  
2. **Chunking & embedding** – Each document was split into 200‑word chunks and turned into embeddings during indexing.  
3. **User question** – The question is entered on a chat interface.  
4. **Question embedding** – The system creates an embedding for the question.  
5. **Semantic search** – The vector database returns three chunks:  
   * a paragraph from the government circular stating “Masks are mandatory for students above class 5 from 1 March 2024,”  
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
* **Healthcare** – A system fetches recent medical guidelines to help doctors with up‑to‑date treatment advice.  
* **Education** – A study assistant pulls the newest syllabus or exam notice before explaining a topic.  
* **Legal help** – A tool searches the latest court rulings to give a lawyer a quick summary.  

**Limits**  
* If the stored documents are wrong or old, the system can give wrong answers.  
* The extra search step makes the response a little slower and needs a vector database to work.  

## Key Words
- **Retrieval‑Augmented Generation (RAG)**: A method that first finds relevant text, then lets a language model write an answer.  
- **Large Language Model (LLM)**: A computer program trained on huge text data that can understand questions and write human‑like text.  
- **Embedding**: A list of numbers that represents the meaning of a piece of text. Similar meanings have similar numbers.  
- **Chunk**: A small piece of a larger document, usually a few paragraphs long.  
- **Vector database**: A special storage that keeps embeddings and can quickly find those that are close in meaning.  
- **Semantic search**: Searching by meaning, not just by exact words.  
- **Hallucination**: When an AI gives an answer that sounds confident but is actually false.  
- **Knowledge cutoff**: The latest date up to which a language model was trained on data.  

## Quick Recap
- RAG = Retrieval + Generation.  
- It works in two phases: indexing (prepare documents) and query (answer a question).  
- Indexing splits documents, makes embeddings, and stores them in a vector database.  
- Query turns the question into an embedding, finds similar chunks, and adds them to the prompt.  
- The LLM writes the final answer using the retrieved text.  
- RAG reduces hallucination and lets AI use fresh or private data without retraining.  
- Updating knowledge only needs new or changed documents, not a new model.  
- Limits: slower response, depends on quality of stored documents.  

## Check Yourself
1. **What does RAG stand for?**  
   *Answer: Retrieval‑Augmented Generation.*  

2. **Why do we split documents into chunks?**  
   *Answer: Smaller pieces are easier to search and fit inside the model’s input limit.*  

3. **What is an embedding?**  
   *Answer: A list of numbers that captures the meaning of a text piece.*  

4. **How does RAG help with outdated information?**  
   *Answer: It lets the system fetch the latest documents, so the answer uses current facts.*  

5. **Name one limitation of RAG.**  
   *Answer: If the stored documents are wrong, the system can give wrong answers.*