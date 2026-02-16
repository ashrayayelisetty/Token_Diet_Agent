import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
from chromadb.config import Settings
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

        # ChromaDB setup with newer API
        self.client = chromadb.PersistentClient(path="./db")
        
        # Get or create collection (reuse if exists)
        self.collection = self.client.get_or_create_collection(
            name="token_diet_context"
        )
    def ingest_document(self, document_text: str, chunk_size: int = 800):
        """
        Ingests a document by splitting it into chunks and adding to vector DB.
        Larger chunks (800) to keep related information together.
        Clears existing data first to avoid mixing documents.
        """
        # Clear existing data before ingesting new document
        try:
            self.client.delete_collection(name="token_diet_context")
            self.collection = self.client.create_collection(name="token_diet_context")
            print("🗑️ Cleared previous document data")
        except:
            pass
        
        chunks = []
        start = 0

        while start < len(document_text):
            end = start + chunk_size
            chunk = document_text[start:end]
            chunks.append(chunk)
            start = end

        # Add to ChromaDB with embeddings
        embeddings_list = self.embeddings.embed_documents(chunks)
        
        self.collection.add(
            documents=chunks,
            embeddings=embeddings_list,
            ids=[f"doc_{i}" for i in range(len(chunks))]
        )
        print(f"📚 Ingested {len(chunks)} chunks into vector DB.")


    def add_context(self, text_chunks: list[str]):
        """
        Adds chunks to vector store (knowledge base).
        """
        embeddings_list = self.embeddings.embed_documents(text_chunks)
        
        self.collection.add(
            documents=text_chunks,
            embeddings=embeddings_list,
            ids=[f"chunk_{i}" for i in range(len(text_chunks))]
        )
        print(f"✅ Added {len(text_chunks)} chunks to vector DB.")

    def get_relevant_context(
        self,
        query: str,
        original_context: str,
        k: int = 6
    ) -> str:
        """
        Returns semantically relevant context WITHOUT increasing token count.
        Falls back to original context if pruning is not beneficial.
        """

        # Token count BEFORE pruning
        original_tokens = count_tokens(original_context)

        # Refresh collection reference (in case it was recreated)
        try:
            self.collection = self.client.get_collection(name="token_diet_context")
            
            # Embed query and search
            query_embedding = self.embeddings.embed_query(query)
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k
            )
            
            # Extract documents from results
            retrieved_context = "\n".join(
                results['documents'][0] if results['documents'] else []
            )

            # Token count AFTER retrieval
            retrieved_tokens = count_tokens(retrieved_context)

            # Safety rule: never increase tokens
            if retrieved_tokens >= original_tokens or not retrieved_context:
                return original_context

            return retrieved_context
            
        except Exception as e:
            # Collection doesn't exist or query failed, return original context
            print(f"⚠️ Pruner fallback: {str(e)}")
            return original_context


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
