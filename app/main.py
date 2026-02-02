# from app.agents.state import AgentState
# from app.agents.executor import ExecutionerNode
# from app.agents.graph import decide_next_step

# def run_agent(user_query: str):
#     # 1. Initialize our Scorecard (The State)
#     # We are filling in the starting info
#     state: AgentState = {
#         "prompt": user_query,
#         "context": "The agent saves money by pruning tokens and routing to cheaper models.", # Simulating the pruner for now
#         "response": "",
#         "quality_score": 0,
#         "iteration_count": 0,
#         "chosen_model": "llama-3.3-70b-versatile"
#     }

#     # 2. Run the Executioner Node
#     executor = ExecutionerNode()
#     result = executor.execute(state)
    
#     # 3. Update the state with the result
#     state.update(result)

#     # 4. Use the Decision Logic (Day 8/9 Logic)
#     next_step = decide_next_step(state)
    
#     print(f"\n--- FINAL RESULT ---")
#     print(f"AI Response: {state['response']}")
#     print(f"Next Step Decided: {next_step}")

# if __name__ == "__main__":
#     query = "How does this agent save me money?"
#     run_agent(query)

from app.agents.graph import build_agent_graph

agent = build_agent_graph()

initial_state = {
    "prompt": "How does the agent save money?",
    "context": "The agent saves money by pruning tokens and routing to cheaper models.",
    "response": "",
    "quality_score": 0,
    "iteration_count": 0,
    "chosen_model": "",
    "original_token_count": 0,
    "final_token_count": 0,
    "money_saved": 0.0
}

final_state = agent.invoke(initial_state)

print("\n🎯 FINAL STATE:")
print(final_state)
