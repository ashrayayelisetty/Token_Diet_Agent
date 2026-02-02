import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.agents.state import AgentState

load_dotenv()


class ExecutionerNode:
    """
    Executes the LLM call using the model selected by the router.
    This node is COST-AWARE and respects dynamic routing.
    """

    def execute(self, state: AgentState) -> dict:
        print(f"--- EXECUTOR: Using model → {state['chosen_model']} ---")

        # Create LLM dynamically based on routing decision
        llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name=state["chosen_model"]
        )

        # Build prompt using PRUNED context only
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a precise assistant. Answer ONLY using the provided context. "
                "If the answer is not present, say 'Information not available.'"
            ),
            (
                "human",
                f"Context:\n{state['context']}\n\nQuestion:\n{state['prompt']}"
            )
        ])

        chain = prompt | llm
        response = chain.invoke({})

        # Update only relevant state fields (LangGraph-style)
        return {
            "response": response.content,
            "iteration_count": state.get("iteration_count", 0) + 1
        }
