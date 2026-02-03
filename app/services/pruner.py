import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.utils import count_tokens

load_dotenv()


class SemanticPruner:
    """
    Semantic Pruner that ensures token reduction.
    It will NEVER return more tokens than the original context.
    """

    def __init__(self):
        # Free local embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        # ChromaDB setup
        self.vector_db = Chroma(
            collection_name="token_diet_context",
            embedding_function=self.embeddings,
            persist_directory="./db"
        )

    def add_context(self, text_chunks: list[str]):
        """
        Adds chunks to vector store (knowledge base).
        """
        self.vector_db.add_texts(text_chunks)
        print(f"✅ Added {len(text_chunks)} chunks to vector DB.")

    def get_relevant_context(
        self,
        query: str,
        original_context: str,
        k: int = 2
    ) -> str:
        """
        Returns semantically relevant context WITHOUT increasing token count.
        Falls back to original context if pruning is not beneficial.
        """

        # Token count BEFORE pruning
        original_tokens = count_tokens(original_context)

        # Retrieve relevant chunks
        results = self.vector_db.similarity_search(query, k=k)
        retrieved_context = "\n".join(
            doc.page_content for doc in results
        )

        # Token count AFTER retrieval
        retrieved_tokens = count_tokens(retrieved_context)

        # Safety rule: never increase tokens
        if retrieved_tokens >= original_tokens:
            return original_context

        return retrieved_context


# -------------------------
# Local Test (Optional)
# -------------------------
if __name__ == "__main__":
    pruner = SemanticPruner()

    knowledge_base = [
        "The agent saves money by pruning unnecessary tokens before sending prompts to the LLM.",
        "It routes simple queries to cheaper models and complex ones to powerful models.",
        "Semantic pruning significantly reduces token usage and API costs."
    ]

    pruner.add_context(knowledge_base)

    query = "How does the agent save money?"
    original_context = (
        "This document explains many things about AI systems, models, "
        "infrastructure, deployment strategies, monitoring, scaling, and cost control."
    )

    pruned = pruner.get_relevant_context(
        query=query,
        original_context=original_context
    )

    print("\n--- PRUNER TEST ---")
    print("Original tokens:", count_tokens(original_context))
    print("Final tokens:", count_tokens(pruned))
    print("Final context:\n", pruned)
