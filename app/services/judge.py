import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


class ResponseJudge:
    """
    Evaluates the quality of an AI response.
    Returns a numeric score (1–10) for LangGraph decisions.
    """

    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )

    def evaluate_response(self, query: str, response: str) -> int:
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a strict QA evaluator.\n"
                "Score the AI answer from 1 to 10.\n"
                "Score 8–10 if the answer directly addresses the question.\n"
                "Score 1–4 if it avoids, deflects, or lacks information.\n"
                "Reply with ONLY the number."
            ),
            (
                "human",
                f"User Question:\n{query}\n\nAI Response:\n{response}"
            )
        ])

        chain = prompt | self.llm
        result = chain.invoke({}).content.strip()

        # Defensive parsing (LLMs sometimes misbehave)
        try:
            score = int(result)
        except ValueError:
            score = 3  # default fail-safe

        print(f"🧪 JUDGE SCORE: {score}/10")
        return score
