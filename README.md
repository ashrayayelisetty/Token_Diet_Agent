# 🤖 Token-Diet Agent

A cost-efficient, Agentic RAG system built to minimize LLM token usage without sacrificing accuracy.

## 🚀 The Problem
Standard RAG (Retrieval-Augmented Generation) often sends massive blocks of text to an LLM, leading to:
1. High API costs.
2. Latency issues.
3. "Lost in the Middle" syndrome where the AI ignores the most important facts.

## 💡 The Solution: The "Token Diet"
This agent uses a multi-stage pipeline to ensure we only pay for the tokens we actually need:

1. **Model Router:** Dynamically selects between high-reasoning (Llama-3.3-70B) and fast/cheap models based on query complexity.
2. **Semantic Pruner:** Uses a local vector database (ChromaDB) to filter out 80% of "noise" and only send the most relevant context.
3. **Self-Correction Judge:** A dedicated "Quality Control" node that reviews the AI's response. If the answer is insufficient, the agent automatically expands its search radius and retries.

## 🛠️ Tech Stack
**Orchestration:** LangGraph (Agentic Control Flow)
- **LLM Provider:** Groq (Llama-3 models)
- **Vector DB:** ChromaDB (Local persistence)
- **Embeddings:** HuggingFace (all-MiniLM-L6-v2) - *Runs 100% free locally*
- **Environment:** Python 3.10+, Dotenv

## 🚦 Getting Started
1. Clone the repo.
2. Create a `.env` file with your `GROQ_API_KEY`.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
