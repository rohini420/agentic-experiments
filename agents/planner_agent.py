import os
from langgraph.graph import StateGraph
from agents.llm_decision_agent import llm_decision
from utils.logger import log_state  # ✅ NEW: import logger

# Step functions
def trivy_scan_step(state):
    print("[🛡️] Running Trivy scan...")
    result = os.system("./agents/trivy_agent.sh")
    passed = (result == 0)
    state["trivy_passed"] = passed
    log_state("trivy_scan", "passed" if passed else "failed")  # ✅ Log result
    return state

def smoke_test_step(state):
    print("[🔥] Running smoke test...")
    result = os.system("bash smoke_test.sh")
    passed = (result == 0)
    state["smoke_test_passed"] = passed
    log_state("smoke_test", "passed" if passed else "failed")  # ✅ Log result
    return state

def deploy_step(state):
    print("[🚀] Deploying to ECS via deploy_agent...")
    os.system("python3 agents/deploy_agent.py")
    state["deployed"] = True
    log_state("deploy", "started")  # ✅ Log deployment trigger
    return state

def stop_step(state):
    print("[⛔] Halting deployment due to failed checks or LLM decision.")
    state["deployed"] = False
    log_state("deployment", "stopped")  # ✅ Log halt reason
    return state

# Build LangGraph planner
def build_graph():
    builder = StateGraph(dict)

    # Add nodes
    builder.add_node("start", lambda state: state)
    builder.add_node("trivy", trivy_scan_step)
    builder.add_node("smoke", smoke_test_step)
    builder.add_node("llm_decide", llm_decision)
    builder.add_node("deploy", deploy_step)
    builder.add_node("stop", stop_step)

    # Define flow
    builder.set_entry_point("start")
    builder.add_edge("start", "trivy")
    builder.add_edge("trivy", "smoke")

    # After smoke test, branch based on result
    builder.add_conditional_edges(
        "smoke",
        lambda state: "pass" if state.get("smoke_test_passed") else "fail",
        {
            "pass": "llm_decide",
            "fail": "stop"
        }
    )

    # LLM decision branch
    builder.add_conditional_edges(
        "llm_decide",
        lambda state: "proceed" if state.get("llm_decision") else "halt",
        {
            "proceed": "deploy",
            "halt": "stop"
        }
    )

    builder.set_finish_point("deploy")
    builder.set_finish_point("stop")

    return builder.compile()

# Run it
def main():
    state = {"trigger": "deploy"}
    graph = build_graph()
    final_state = graph.invoke(state)
    print("✅ Final state:", final_state)

if __name__ == "__main__":
    main()

