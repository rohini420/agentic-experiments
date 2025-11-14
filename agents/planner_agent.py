import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from langgraph.graph import StateGraph
from dotenv import load_dotenv
load_dotenv()
# Step functions
from agents.llm_decision_agent import llm_decision
from agents.git_trigger_agent import trigger_git_push        
from agents.github_dispatch_agent import trigger_github_action 
from utils.logger import log_state

def trivy_scan_step(state):
    print("[🛡️] Running Trivy scan...")
    result = os.system("./agents/trivy_agent.sh")
    passed = (result == 0)
    state["trivy_passed"] = passed
    log_state("trivy_scan", "passed" if passed else "failed")
    return state

def smoke_test_step(state):
    print("[🔥] Running smoke test...")
    result = os.system("bash smoke_test.sh")
    passed = (result == 0)
    state["smoke_test_passed"] = passed
    log_state("smoke_test", "passed" if passed else "failed")
    return state

def deploy_step(state):
    print("[🚀] Deploying to ECS via deploy_agent...")
    os.system("python3 agents/deploy_agent.py")
    state["deployed"] = True
    log_state("deploy", "started")
    return state

def stop_step(state):
    print("[⛔] Halting deployment due to failed checks or LLM decision.")
    state["deployed"] = False
    log_state("deployment", "stopped")
    return state

#  LangGraph pipeline
def build_graph():
    builder = StateGraph(dict)

    # Add nodes
    builder.add_node("start", lambda state: state)
    builder.add_node("git_push", trigger_git_push)
    builder.add_node("github_dispatch", trigger_github_action)
    builder.add_node("trivy", trivy_scan_step)
    builder.add_node("smoke", smoke_test_step)
    builder.add_node("llm_decide", llm_decision)
    builder.add_node("deploy", deploy_step)
    builder.add_node("stop", stop_step)

    # Define flow
    builder.set_entry_point("start")
    builder.add_edge("start", "git_push")
    builder.add_edge("git_push", "github_dispatch")
    builder.add_edge("github_dispatch", "trivy")
    builder.add_edge("trivy", "smoke")

    builder.add_conditional_edges(
        "smoke",
        lambda state: "pass" if state.get("smoke_test_passed") else "fail",
        {
            "pass": "llm_decide",
            "fail": "stop"
        }
    )

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

#  Entry point
def main():
    state = {"trigger": "deploy"}
    graph = build_graph()
    final_state = graph.invoke(state)
    print("=========================================")
    print("✅ FINAL STATE:", final_state)
    print("=========================================")

if __name__ == "__main__":
    main()
