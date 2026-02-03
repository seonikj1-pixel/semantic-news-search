\# Semantic News Search



This project is a production-ready semantic search application for news articles.

It retrieves semantically relevant articles using dense embeddings and cosine

similarity, and optionally applies a large language model (LLM) to summarize the

retrieved results.



The system is designed to be modular, reproducible, and robust, with a clear

separation between retrieval and generation.



---



\## Features

\- Domain: News articles (RSS ingestion)

\- Corpus: 100+ news articles

\- Embeddings: Sentence Transformers (all-MiniLM-L6-v2)

\- Search: Cosine similarity with top-K retrieval

\- LLM Enhancement: Optional summarization of retrieved results

\- Interfaces:

&nbsp; - Command-line interface (CLI)

&nbsp; - Streamlit web interface



---



\## Project Structure



semantic-news-search/

├── src/

├── streamlit\_app.py

├── README.md

├── ARCHITECTURE.md

├── TEAM\_CONTRIBUTIONS.md

├── requirements.txt

└── .gitignore



Generated data (raw articles, processed data, embeddings) is intentionally excluded

from version control and produced via CLI commands.



---



\## Setup



Create and activate environment:

conda create -n semantic-news python=3.10 -y

conda activate semantic-news



Install dependencies:

pip install -r requirements.txt



(Optional) Enable LLM summarization:

set OPENAI\_API\_KEY=YOUR\_API\_KEY



---



\## Usage (CLI)



Ingest news articles:

python -m src.cli ingest --limit 200



Preprocess articles:

python -m src.cli preprocess



Build embedding index:

python -m src.cli build-index



Semantic search:

python -m src.cli search --query "AI regulation" --top\_k 5



Semantic search with summarization:

python -m src.cli search --query "AI regulation" --top\_k 5 --summarize



---



\## Streamlit Interface (Bonus)



streamlit run streamlit\_app.py



---



For technical details, see ARCHITECTURE.md.





