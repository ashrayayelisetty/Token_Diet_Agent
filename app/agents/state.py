from typing import TypedDict, Optional

class AgentState(TypedDict):
    # 1. Input Data
    prompt: str             # The user's original query
    context: Optional[str]  # Any large text provided (e.g., a PDF content)
    
    # 2. Processing Data
    optimized_prompt: str   # The prompt after pruning filler words
    chosen_model: str       # "gpt-4o-mini" or "gpt-4o"
    
    # 3. Output Data
    response: str           # The AI's generated answer
    quality_score: int      # 1 to 10 score from the Judge
    
    # 4. Metrics (The "Value" of your project)
    original_token_count: int
    final_token_count: int
    money_saved: float      # Calculated as (Original Cost - New Cost)
    
    # 5. Control Flow
    iteration_count: int    # To prevent infinite loops (Self-correction count)