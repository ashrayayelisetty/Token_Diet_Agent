from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.services.pruner import SemanticPruner
from app.services.router import ModelRouter
from app.services.judge import ResponseJudge
from app.agents.executor import ExecutionerNode
from app.utils import count_tokens


# --- Initialize Services ---
pruner = SemanticPruner()
router = ModelRouter()
judge = ResponseJudge()
executor = ExecutionerNode()


# --- Graph Nodes ---

from app.utils import count_tokens, calculate_cost

def prune_node(state: AgentState) -> dict:
    print("\n✂️ PRUNER NODE")

    original_context = state["context"]

    # Token count BEFORE pruning
    original_tokens = count_tokens(original_context)

    # Semantic pruning
    pruned_context = pruner.get_relevant_context(state["prompt"])

    # Token count AFTER pruning
    final_tokens = count_tokens(pruned_context)

    # Cost calculation (simulated but valid)
    original_cost = calculate_cost(original_tokens, "gpt-4o")
    optimized_cost = calculate_cost(final_tokens, "gpt-4o-mini")

    money_saved = round(original_cost - optimized_cost, 6)

    print(f"💰 Money Saved: ${money_saved}")

    return {
        "context": pruned_context,
        "original_token_count": original_tokens,
        "final_token_count": final_tokens,
        "money_saved": money_saved
    }


def route_node(state: AgentState) -> dict:
    print("\n📡 ROUTER NODE")

    chosen_model = router.select_model(state["prompt"])

    return {
        "chosen_model": chosen_model
    }


def execute_node(state: AgentState) -> dict:
    print("\n🤖 EXECUTOR NODE")
    return executor.execute(state)


def judge_node(state: AgentState) -> dict:
    print("\n🧪 JUDGE NODE")

    score = judge.evaluate_response(
        state["prompt"],
        state["response"]
    )

    return {
        "quality_score": score
    }


# --- Conditional Logic ---

def decide_next_step(state: AgentState):
    print("\n🧠 DECISION NODE")

    if state["quality_score"] >= 7:
        print("✅ Quality acceptable. Ending.")
        return END

    if state["iteration_count"] >= 3:
        print("⚠️ Max retries reached. Ending.")
        return END

    print("🔁 Retrying with improved context/model...")
    return "prune"


# --- Build LangGraph ---

def build_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("prune", prune_node)
    graph.add_node("route", route_node)
    graph.add_node("execute", execute_node)
    graph.add_node("judge", judge_node)

    graph.set_entry_point("prune")

    graph.add_edge("prune", "route")
    graph.add_edge("route", "execute")
    graph.add_edge("execute", "judge")

    graph.add_conditional_edges(
        "judge",
        decide_next_step,
        {
            "prune": "prune",
            END: END
        }
    )

    return graph.compile()
