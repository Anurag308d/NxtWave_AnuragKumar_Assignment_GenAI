# Intro to Retrieval‑Augmented Generation

## Before We Start
In this lesson you will learn what Retrieval‑Augmented Generation (RAG) is.  
You will see why RAG helps AI give correct and recent answers.  
Understanding RAG is a good first step toward building AI products.

## What Is Retrieval‑Augmented Generation?
Retrieval‑Augmented Generation (RAG) is a method that first **retrieves** (finds) useful information, then **generates** (writes) an answer using that information.  
Think of a school librarian. The librarian first fetches the right books, then tells you the answer based on those books.  
RAG works the same way for a computer program.

## Why Does It Matter?
Large Language Models (LLMs) learn only up to a certain date. This date is called the **knowledge cutoff**.  
After that date the model cannot see new facts, such as the latest COVID‑19 rules.  
LLMs also cannot read private documents like a college’s internal notice board unless you give them those files.  
Sometimes LLMs make up information. This is called a **hallucination**.  
RAG lets the model answer using fresh or private documents without changing the model itself.  
Because the answer is built from real sources, users can check where the answer came from, reducing hallucinations.

## How Does It Work?
RAG has two phases: **indexing** and **query**.

1. **Indexing phase** – done before any question is asked.  
   - First we collect documents (PDFs, web pages, notes). This is the **knowledge base**.  
   - Next we split each document into small pieces called **chunks**. A chunk may be a paragraph or two.  
   - Each chunk is turned into a list of numbers called an **embedding**. The numbers act like a meaning address. Similar meanings get nearby addresses.  
   - All embeddings and their chunks are stored in a **vector database**. The database can quickly find chunks whose addresses are close to a query address.

2. **Query phase** – runs every time a user asks something.  
   - The user’s question is also turned into an embedding.  
   - The system performs **semantic search**: it looks in the vector database for chunks whose embeddings are most similar to the question embedding. This step is called **retrieval**.  
   - The top few chunks are added to a **prompt** together with the original question. The prompt also tells the LLM to answer only using the given chunks.  
   - The LLM reads the prompt and **generates** a concise answer. It can also add a citation for each chunk it used.

Running example: A student asks, “What are the latest COVID‑19 guidelines in India?”  
During indexing, a government health PDF, a May‑2024 news article, and a state health notice are turned into chunks and stored.  
During query, the question is embedded, the three most relevant chunks are retrieved, added to the prompt, and the LLM writes an up‑to‑date answer citing each source.

## A Full Example
Let’s walk through the whole flow for the COVID‑19 question.

1. **Embed the question** – The sentence “What are the latest COVID‑19 guidelines in India?” becomes a numeric list (embedding).  
2. **Retrieve top 3 chunks** – The vector database returns:  
   - Chunk A: a paragraph from the government health PDF about mask rules.  
   - Chunk B: a news article paragraph about booster dose recommendations.  
   - Chunk C: a state notice about travel restrictions.  
3. **Create the prompt** – The system builds a text like:  

   ```
   Answer the question using only the following information. Cite each source.

   [Chunk A]  
   [Chunk B]  
   [Chunk C]

   Question: What are the latest COVID‑19 guidelines in India?
   ```  

4. **Generate the answer** – The LLM reads the prompt and writes:  

   “As of May 2024, the Indian health ministry advises wearing masks in indoor public places (source: government PDF). A booster dose is recommended for everyone over 18 years (source: news article). Travelers from states with high case counts must present a negative test before boarding (source: state notice).”

The answer is short, recent, and each fact points to its source.

## Where Is It Used?
- **Customer support bots** that answer from a company’s help manuals.  
- **Legal assistants** that search contracts and case law to give advice.  
- **Study helpers** that pull facts from textbooks and lecture notes.  
- **Medical aides** that look up the latest guidelines from trusted health bulletins.

One honest limit: if the stored documents are wrong or outdated, RAG can still give a wrong answer. The system can only be as accurate as the knowledge base it searches.

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
- **Retrieving**: another word for the retrieval step.  
- **Source citation**: mentioning which document each fact came from.  
- **Retraining**: same as fine‑tuning; changing the model’s internal weights (not used in RAG).  

## Quick Recap
- RAG = retrieve then generate.  
- It helps LLMs give up‑to‑date, private, and sourced answers.  
- Two phases: indexing (chunk‑embed‑store) and query (embed‑retrieve‑prompt‑generate).  
- The model itself does not change; only the retrieved text influences the answer.  
- Good documents give good answers; bad documents can cause errors.  
- RAG reduces but does not completely remove hallucinations.  

## Check Yourself
1. **What does RAG stand for?**  
   Answer: Retrieval‑Augmented Generation.  

2. **Why can a plain LLM give wrong answers about recent events?**  
   Answer: It has a knowledge cutoff and cannot see new documents.  

3. **Name the two main phases of RAG.**  
   Answer: Indexing phase and Query phase.  

4. **In the running example, what types of documents were retrieved?**  
   Answer: A government health PDF, a recent news article, and a state health notice.  

5. **Give one limitation of RAG.**  
   Answer: It can only be as accurate as the documents it retrieves; wrong sources lead to wrong answers.