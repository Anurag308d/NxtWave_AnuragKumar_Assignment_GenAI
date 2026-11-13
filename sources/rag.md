# Source pack: Retrieval-Augmented Generation (RAG)

Curated, verified facts used to GROUND the lesson. The generator may only teach claims that
are consistent with these facts, and the evaluator checks the lesson against them.
Each fact has an ID so the evaluator can point to the exact fact a lesson contradicts.

References used to write this pack:
- Lewis et al., 2020, "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (NeurIPS 2020), arXiv:2005.11401
- Gao et al., 2023, "Retrieval-Augmented Generation for Large Language Models: A Survey", arXiv:2312.10997
- Public documentation from LangChain, LlamaIndex and major cloud providers describing RAG pipelines

## Facts

F01 | basics | RAG stands for Retrieval-Augmented Generation.
F02 | basics | RAG is a technique where a system first finds (retrieves) relevant information from an outside source, then gives that information to a language model so it can write (generate) a better answer.
F03 | basics | The term RAG was introduced in a 2020 research paper by Patrick Lewis and colleagues at Facebook AI Research (now Meta AI), University College London and New York University.
F04 | llm | A large language model (LLM) is a computer program trained on a very large amount of text so that it can understand questions and write human-like text. ChatGPT, Gemini, Claude and Llama are examples of LLMs or products built on them.
F05 | llm | An LLM learns from data collected up to a certain date. It does not automatically know about events or documents after that date. This date is called the knowledge cutoff.
F06 | llm | An LLM does not know a company's or person's private documents (for example a college's internal rulebook) unless that information is given to it.
F07 | llm | LLMs can sometimes produce answers that sound confident but are false or made up. This is called hallucination.
F08 | why | RAG helps reduce hallucination by giving the model real, relevant text to base its answer on. It reduces hallucination but does not remove it completely.
F09 | why | RAG lets a model answer questions about new or private information without retraining the model.
F10 | why | With RAG, updating knowledge is as simple as adding, changing or removing documents in the knowledge source. The model itself does not change.
F11 | why | RAG systems can show the sources (documents) used for an answer, so users can check where the answer came from.
F12 | why | Retraining or fine-tuning a model on new data is usually slower and more expensive than updating the documents used by a RAG system.
F13 | how | A RAG system has two main phases: an indexing phase (preparing the documents, done before questions are asked) and a query phase (answering a question, done every time a user asks).
F14 | how | Indexing step 1, loading: documents such as PDFs, web pages or notes are collected.
F15 | how | Indexing step 2, chunking: long documents are split into smaller pieces called chunks, for example a few paragraphs each. Smaller pieces are easier to search and fit inside the model's input.
F16 | how | Indexing step 3, embedding: each chunk is converted into a list of numbers called an embedding (or vector). Texts with similar meaning get similar numbers.
F17 | how | Indexing step 4, storing: the embeddings and their chunks are saved in a special database built for searching by meaning, called a vector database (examples: FAISS, Chroma, Pinecone, Weaviate).
F18 | how | Query step 1, retrieval: the user's question is also converted into an embedding, and the system finds the chunks whose embeddings are most similar to the question. This is called semantic search (search by meaning, not just exact words).
F19 | how | Query step 2, augmentation: the retrieved chunks are added to the prompt together with the user's question, often with an instruction like "answer using only this information".
F20 | how | Query step 3, generation: the LLM reads the question plus the retrieved chunks and writes the answer.
F21 | how | In RAG, the model's internal knowledge (its weights or parameters) is NOT changed when documents are added or when questions are asked. Only the input given to the model changes.
F22 | how | Retrieval happens at question time (when the user asks), not only once during training.
F23 | how | Usually only the top few most relevant chunks (for example the top 3 to 5) are given to the model, because the model's input has a size limit called the context window.
F24 | how | A prompt is the text input given to an LLM, such as a question or an instruction.
F25 | how | Retrieval can also use keyword search, or a mix of keyword search and semantic search (called hybrid search). Semantic search with embeddings is the most common way to explain basic RAG.
F26 | limits | If the retrieval step finds the wrong or irrelevant chunks, the answer can still be wrong. The quality of a RAG answer depends a lot on the quality of retrieval.
F27 | limits | If the knowledge source has wrong or outdated documents, a RAG system can give wrong answers based on them.
F28 | limits | RAG adds extra steps (searching before answering), so it can be a little slower and needs extra setup such as a vector database.
F29 | uses | Common uses of RAG: customer support chatbots that answer from company help pages, chatbots that answer questions about a college or company's own documents, search assistants that answer from latest news or web pages, and assistants for doctors, lawyers or engineers that answer from their reference documents.
F30 | compare | RAG is different from fine-tuning. Fine-tuning changes the model's weights by training it more on new data. RAG keeps the model the same and gives it relevant information at the time of the question. They can also be used together.
F31 | analogy | A common analogy: an LLM without RAG is like a student writing a closed-book exam from memory; an LLM with RAG is like a student in an open-book exam who first looks up the right page in the book and then writes the answer.

## Common misconceptions (the evaluator treats these as factual errors)

M01 | RAG trains or retrains the model on your documents. (False: see F21, F30)
M02 | RAG permanently changes what the model knows / changes the model's weights. (False: see F21)
M03 | RAG completely eliminates hallucination / RAG answers are always correct. (False: see F08, F26, F27)
M04 | RAG searches the whole internet by default. (False: it searches whatever knowledge source the builder connects; this may or may not include the web.)
M05 | The vector database itself writes the answer. (False: the LLM writes the answer; the database only stores and finds chunks, see F17, F20)
M06 | Embeddings are encrypted text / embeddings are the same as keywords. (False: embeddings are lists of numbers that capture meaning, see F16)
M07 | The whole document collection is always given to the model at once. (False: only the top relevant chunks are given, see F23)

## Must-cover key points (the evaluator checks coverage of each)

K1 | What RAG is: retrieve relevant information first, then generate an answer using it. (F02)
K2 | The problem it solves: LLMs have a knowledge cutoff, do not know private documents, and can hallucinate. (F05, F06, F07)
K3 | Why it matters: up-to-date / private answers without retraining, fewer hallucinations, sources can be shown. (F08-F12)
K4 | Indexing phase: chunking, embedding, storing in a vector database. (F15-F17)
K5 | Query phase: retrieve similar chunks, add them to the prompt, LLM generates the answer. (F18-F20)
K6 | The model itself is not retrained or changed. (F21)
K7 | At least one limitation of RAG. (F26-F28)
