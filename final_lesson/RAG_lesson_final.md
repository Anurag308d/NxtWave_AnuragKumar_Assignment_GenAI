> Final submitted lesson. Source: run `20261114-101613-d823` (shipped, 14/14 checks, attempt 2) plus one human review edit: the example's real railway company was renamed to an imaginary one (Sunrise Railways) and a note added that example documents are imaginary. That gap is now an automatic J1 check.

# Introduction to Retrieval-Augmented Generation (RAG)

## Before We Start
In this lesson you will learn what Retrieval‑Augmented Generation (RAG) is.  
You will see how RAG helps an AI system give answers that are recent, private and trustworthy.  
Knowing RAG is a solid first step for a career in Artificial Intelligence (AI).

## What Is Retrieval‑Augmented Generation (RAG)?
Retrieval‑Augmented Generation (RAG) is a method that first **retrieves** (finds) useful information, then **generates** (writes) an answer using that information.  
Think of a student who opens a textbook, finds the right page, and then writes the answer. The textbook page is the retrieved part, the writing is the generation part.

## Why Does It Matter?
Large Language Models (LLM) learn only up to a certain date. This date is called the **knowledge cutoff**.  
After that date the model cannot see new facts, such as the latest **Coronavirus disease 2019 (COVID‑19)** rules.  
LLMs also cannot read private papers, like a college’s internal notice board, unless you give them those files.  
Sometimes LLMs make up information. This is called a **hallucination**.  
RAG lets the model answer using fresh or private documents without changing the model itself.  
Because the answer is built from real sources, users can check where the answer came from, reducing hallucinations.

## How Does It Work?
RAG works in two big phases: **indexing** and **query**. We will follow one running example: a student asks a railway enquiry chatbot, “What are the latest COVID‑19 travel rules for trains in India?”

### Indexing Phase (done before any question)
1. **Loading** – Collect documents that may contain the answer.  
   *Examples*: a PDF from Sunrise Railways (an imaginary railway company), a recent news article, a state health notice.  
   These documents together form the **knowledge base**.
2. **Chunking** – Break each document into small pieces called **chunks**.  
   A chunk can be one paragraph or a few sentences. Smaller pieces are easier to search.
3. **Embedding** – Run each chunk through a special model that creates an **embedding**.  
   An embedding is a list of numbers that works like a meaning address. Texts about similar topics get nearby addresses.
4. **Storing** – Save all embeddings and their chunks in a **vector database**.  
   The vector database can quickly find chunks whose meaning addresses are close to a query address.

### Query Phase (runs every time a user asks)
1. **Question embedding** – Convert the user’s question into an embedding, just like the chunks.
2. **Retrieval** – Perform **semantic search** in the vector database. The system finds the top few chunks whose embeddings are most similar to the question embedding.  
   This step is called **retrieval**.
3. **Augmentation** – Add the retrieved chunks to a **prompt** together with the original question. The prompt also tells the LLM to answer only using the given chunks.
4. **Generation** – The LLM reads the prompt and **generates** a concise answer. It can also add a citation for each chunk it used.

#### Running example in detail
*Note: all documents and rules in this lesson's examples are imaginary. They are made up only to show how RAG works.*
*Question*: “What are the latest Coronavirus disease 2019 (COVID‑19) travel rules for trains in India?”  

- **Embedding**: The question becomes a numeric list.  
- **Retrieval**: The vector database returns three chunks:  
  1. Chunk A – a paragraph from the Sunrise Railways PDF saying masks are mandatory on all trains.  
  2. Chunk B – a news article stating that a negative test is required for travelers from high‑risk states.  
  3. Chunk C – a state health notice that vaccination proof is needed for passengers over 60.  
- **Prompt**:  

  ```
  Answer the question using only the following information. Cite each source.

  [Chunk A]
  [Chunk B]
  [Chunk C]

  Question: What are the latest Coronavirus disease 2019 (COVID‑19) travel rules for trains in India?
  ```  

- **Generation**: The LLM writes:  

  “Masks are mandatory on all Sunrise Railways trains (source: Sunrise Railways PDF). Travelers from high‑risk states must show a negative COVID‑19 test (source: news article). Passengers over 60 need to present vaccination proof (source: state health notice).”

The answer is short, up‑to‑date, and each fact points to its source.

## A Full Example
Let’s walk through the whole flow for a fresh question: “How many points does a team get for a win in the Ranji Trophy?”

1. **Load documents** – Gather the latest Ranji Trophy rulebook, a sports news summary, and a cricket board announcement.  
2. **Chunk** – Split each document into paragraphs.  
3. **Embed** – Create embeddings for every paragraph.  
4. **Store** – Save them in a vector database.

When the student asks the question:

1. **Embed the question** – “How many points does a team get for a win in the Ranji Trophy?” becomes a numeric list.  
2. **Retrieve top 3 chunks** –  
   - Chunk X: rulebook paragraph saying a win gives 6 points.  
   - Chunk Y: news article confirming the 6‑point rule for the 2024 season.  
   - Chunk Z: board announcement that a tie gives 3 points (included for context).  
3. **Create prompt** – Combine the three chunks with the question and an instruction to use only the given information.  
4. **Generate answer** – The LLM replies:  

   “A team earns 6 points for a win in the Ranji Trophy (source: rulebook). The 2024 season follows the same rule (source: news article).”

The system has answered correctly without needing to retrain the model.

## Where Is It Used?
- **Customer support bots** that answer from a company’s help manuals.  
- **Legal assistants** that search contracts and case law to give advice.  
- **Study helpers** that pull facts from textbooks and lecture notes.  
- **Medical aides** that look up the latest health guidelines from trusted bulletins.  

**Honest limits**:  
- If the stored documents are wrong or outdated, RAG can still give a wrong answer.  
- Retrieval adds extra time, so answers may be a little slower than a plain LLM.

## Key Words
- **Retrieval‑Augmented Generation (RAG)**: first find information, then write an answer using it.  
- **Large Language Model (LLM)**: a computer program that can read text and write human‑like answers.  
- **Knowledge cutoff**: the date after which the model has no new facts.  
- **Hallucination**: when the model makes up information that is not true.  
- **Chunk**: a small piece of a larger document, like a paragraph.  
- **Embedding**: a list of numbers that represents the meaning of a text piece.  
- **Vector**: the numeric list (embedding) that can be compared with other vectors.  
- **Vector database**: a storage that can quickly find vectors that are close in meaning.  
- **Prompt**: the text given to the LLM telling it what to do.  
- **Retrieval**: the step of finding the most relevant chunks for a question.  
- **Generation**: the step where the LLM writes the final answer.  
- **Semantic search**: searching by meaning, not by exact words.  
- **Fine‑tuning**: training the model again on new data; different from RAG, which does not change the model.  
- **Indexing**: the preparation work of chunking, embedding, and storing documents.  
- **Knowledge base**: the collection of documents that RAG can search.  
- **Query**: the user’s question that starts the retrieval‑generation cycle.  
- **Augmented**: added with extra information from the knowledge base.  

## Quick Recap
- RAG = retrieve then generate.  
- It helps LLMs give up‑to‑date, private, and sourced answers.  
- Two phases: indexing (chunk‑embed‑store) and query (embed‑retrieve‑prompt‑generate).  
- The model itself does not change; only the retrieved text influences the answer.  
- Good documents give good answers; bad documents can cause errors.  
- RAG reduces but does not completely remove hallucinations.  
- Retrieval happens at question time, not during training.  

## Check Yourself
1. **What does RAG stand for?**  
   Answer: Retrieval‑Augmented Generation.  

2. **Why can a plain LLM give wrong answers about recent events?**  
   Answer: It has a knowledge cutoff and cannot see new documents.  

3. **Name the two main phases of RAG.**  
   Answer: Indexing phase and Query phase.  

4. **In the railway example, what types of documents were retrieved?**  
   Answer: A Sunrise Railways PDF, a recent news article, and a state health notice.  

5. **Give one limitation of RAG.**  
   Answer: If the stored documents are wrong or outdated, the answer can be wrong.