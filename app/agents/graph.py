from app.agents.state import AgentState

def decide_next_step(state: AgentState):
    """
    This is the logic for the 'Conditional Edge' on Day 8.
    It looks at the scorecard and decides the path.
    """
    # 1. Check if the Judge is happy (Score >= 7)
    if state["quality_score"] >= 7:
        print("--- DECISION: QUALITY MET ---")
        return "end"

    # 2. Check if we've tried too many times (Prevent Infinite Loops - Day 10 prep)
    if state["iteration_count"] >= 3:
        print("--- DECISION: MAX RETRIES REACHED ---")
        return "end"

    # 3. Otherwise, try again!
    print(f"--- DECISION: RE-TRYING (Current iteration: {state['iteration_count']}) ---")
    return "prune"