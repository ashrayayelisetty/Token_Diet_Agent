import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

class SemanticPruner:
    def __init__(self):
        # 1. Use a FREE local model (all-MiniLM-L6-v2)
        # This downloads a small file to your PC and runs for free
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # 2. Setup ChromaDB
        self.vector_db = Chroma(
            collection_name="token_diet_context",
            embedding_function=self.embeddings,
            persist_directory="./db"
        )

    def add_context(self, text_chunks: list[str]):
        self.vector_db.add_texts(text_chunks)
        print(f"✅ Successfully added {len(text_chunks)} chunks to FREE storage.")
    def get_relevant_context(self, query: str, k: int = 2) -> str:
        """
        Finds the top 'k' most relevant pieces of information for a query.
        This is what reduces the token count by filtering out noise.
        """
        # Similarity search against the local vector database
        results = self.vector_db.similarity_search(query, k=k)
        
        # Combine the results into a single clean string
        pruned_context = "\n".join([doc.page_content for doc in results])
        return pruned_context

if __name__ == "__main__":
    pruner = SemanticPruner()
    
    # 1. Add 'Noisy' data (Stuff the AI shouldn't see for every question)
    knowledge_base = [
        "The Token-Diet Agent is designed to save money on API calls.",
        "The weather today is cloudy with a chance of rain.",
        "LangGraph is a library for building stateful, multi-agent applications.",
        "A typical healthy breakfast includes oatmeal and fruits."
    ]
    pruner.add_context(knowledge_base)
    
    # 2. Ask a specific question about the project
    query = "How does the agent save money?"
    
    print(f"\n--- Day 5 Test ---")
    print(f"User Query: {query}")
    
    # Retrieve only relevant info
    context = pruner.get_relevant_context(query)
    
    print(f"Context Found:\n{context}")