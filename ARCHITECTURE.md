\# Architecture



\## Overview

This project implements a production-ready semantic search system for news articles.

The system ingests news from RSS feeds, preprocesses text, generates dense embeddings,

retrieves relevant documents using cosine similarity, and optionally applies a large

language model (LLM) to summarize the retrieved results.



The LLM component is intentionally designed as a post-retrieval enhancement rather

than part of the core search pipeline to preserve interpretability and robustness.



---



\## System Pipeline



RSS Feeds

↓

Ingestion (src/ingest.py)



Parse RSS feeds



Fetch article HTML



Extract paragraph text

↓

Raw Articles (JSONL)

↓

Preprocessing (src/preprocess.py)



Normalize whitespace



Remove boilerplate text



Filter short or low-information articles

↓

Processed Documents (JSONL)

↓

Embedding \& Indexing (src/embed.py)



SentenceTransformer (all-MiniLM-L6-v2)



Normalize embeddings



Save embeddings and metadata

↓

Semantic Search (src/search.py)



Embed user query



Cosine similarity search



Top-K document retrieval

↓

LLM Enhancement (src/llm.py)



Summarize retrieved documents



Graceful fallback if LLM fails





---



\## Core Components



\### Ingestion

\- Implemented in `src/ingest.py`

\- Uses RSS feeds as a reproducible data source

\- Fetches article web pages and extracts paragraph text

\- Stores raw articles in JSONL format

\- Skips failed or blocked pages without crashing



\### Preprocessing

\- Implemented in `src/preprocess.py`

\- Cleans and normalizes text content

\- Removes boilerplate and excessive whitespace

\- Filters documents that are too short to be meaningful

\- Produces a clean corpus suitable for embedding



\### Embedding and Indexing

\- Implemented in `src/embed.py`

\- Uses Sentence Transformers (`all-MiniLM-L6-v2`)

\- Embeddings are normalized to unit length

\- Outputs:

&nbsp; - Dense float32 embedding matrix

&nbsp; - Aligned document metadata



\### Semantic Search

\- Implemented in `src/search.py`

\- Query text is embedded using the same model as documents

\- Cosine similarity is computed as a dot product on normalized vectors

\- Returns the top-K most semantically similar documents



\### LLM Enhancement

\- Implemented in `src/llm.py`

\- Applied only after document retrieval

\- Summarizes the top-K retrieved documents

\- Includes a fallback summarizer to ensure robustness if the LLM fails

\- Designed as an optional augmentation rather than a core dependency



---



\## Interfaces



\### Command-Line Interface

\- Implemented in `src/cli.py`

\- Supports ingestion, preprocessing, index construction, search, and summarization

\- Enables reproducible execution of the full pipeline



\### Streamlit Interface

\- Implemented in `streamlit\_app.py`

\- Provides an interactive UI for querying, viewing results, and generating summaries



---



\## Error Handling and Robustness

\- Ingestion failures do not interrupt the pipeline

\- Search validates index existence before execution

\- LLM calls are wrapped in exception handling with a safe fallback

\- Generated data artifacts and caches are excluded from version control



---



\## Design Rationale

\- Embeddings capture semantic similarity beyond keyword matching

\- Cosine similarity is scale-invariant and well-suited for normalized vectors

\- Separating retrieval from LLM generation reduces hallucination risk

\- Modular design enables future extensions such as approximate nearest neighbor search



---



\## Reproducibility

All raw data, processed documents, and embeddings are generated via documented CLI

commands and are intentionally excluded from version control. The full system can be

reproduced by running the pipeline described in the README.



