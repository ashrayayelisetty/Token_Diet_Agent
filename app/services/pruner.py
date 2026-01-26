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

if __name__ == "__main__":
    pruner = SemanticPruner()
    pruner.add_context(["The capital of France is Paris."])