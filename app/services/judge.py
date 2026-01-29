import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

class ResponseJudge:
    def __init__(self):
        # We use the 70B model because it's better at 'judging' logic
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )

    def evaluate_response(self, query: str, response: str) -> bool:
        """
        Analyzes the response to see if it actually answered the question.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Senior QA Engineer. If the AI answer provides the requested information, reply 'PASS'. If the AI says 'I don't know', 'not mentioned', or gives an empty excuse, reply 'FAIL'."),
            ("human", f"User Question: {query}\nAI Response: {response}")
        ])
        
        chain = prompt | self.llm
        result = chain.invoke({}).content
        
        return "PASS" in result.upper()

if __name__ == "__main__":
    judge = ResponseJudge()
    
    # Test 1: A failure case
    print(f"Test 1 (Failure): {judge.evaluate_response('Who is the CEO?', 'The text does not mention the CEO.')}")
    
    # Test 2: A success case
    print(f"Test 2 (Success): {judge.evaluate_response('What is 10+10?', '10 + 10 is 20.')}")