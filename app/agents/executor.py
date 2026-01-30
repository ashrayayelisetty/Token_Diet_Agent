import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.agents.state import AgentState

load_dotenv()

class ExecutionerNode:
    def __init__(self):
        # We'll use the versatile model as our default powerhouse
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )

    def execute(self, state: AgentState) -> dict:
        """
        The main logic for the Executor. It takes the state,
        generates an answer, and returns the updated fields.
        """
        print(f"--- EXECUTOR: Generating response for model {state.get('chosen_model')} ---")
        
        # 1. Prepare the Prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer based ONLY on the provided context."),
            ("human", f"Context: {state['context']}\n\nQuestion: {state['prompt']}")
        ])

        # 2. Call the LLM (Using the model chosen by our router earlier)
        chain = prompt | self.llm
        response = chain.invoke({})

        # 3. Update the Scorecard (State)
        # Note: In LangGraph, we return only the keys we want to update
        return {
            "response": response.content,
            "iteration_count": state.get("iteration_count", 0) + 1
        }