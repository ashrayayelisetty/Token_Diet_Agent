import os
from dotenv import load_dotenv
from app.services.router import ModelRouter
from app.services.pruner import SemanticPruner
from app.services.judge import ResponseJudge
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

class TokenDietAgent:
    def __init__(self):
        self.router = ModelRouter()
        self.pruner = SemanticPruner()
        self.judge = ResponseJudge()
        self.api_key = os.getenv("GROQ_API_KEY")

    def run(self, user_query: str):
        print(f"\nStarting Agent for: '{user_query}'")

        # 1. Route: Decide which model to use
        model_name = self.router.select_model(user_query)
        print(f"📡 Routing to model: {model_name}")

        # 2. Prune: Get only relevant info from DB
        context = self.pruner.get_relevant_context(user_query, k=2)
        print(f"✂️ Context Pruned. Sending minimal tokens to AI...")

        # 3. Generate: Call the LLM
        llm = ChatGroq(api_key=self.api_key, model_name=model_name)
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"Answer based ONLY on this context:\n{context}"),
            ("human", user_query)
        ])
        
        response = (prompt | llm).invoke({}).content
        print(f"🤖 AI Response: {response}")

        # 4. Judge: Self-Correction Loop
        is_good = self.judge.evaluate_response(user_query, response)
        
        if is_good:
            print("✅ Judge Result: PASS")
            return response
        else:
            print("❌ Judge Result: FAIL. (In a full graph, we would loop back here!)")
            return "I need more information to answer that accurately."

if __name__ == "__main__":
    agent = TokenDietAgent()
    # Test it with something that should be in your DB from Day 5/6 tests
    agent.run("How does the agent save money?")