import os
from langgraph.graph import StateGraph
from agents.llm_decision_agent import llm_decision
from agents.build_and_deploy_agent import main as build_and_deploy
from utils.logger import log_state


# ---------------------------------------------------------
# STEP 1 — SECURITY SCAN (TRIVY)
# ---------------------------------------------------------
def trivy_scan_step(state):
    print("[🛡️] Running Trivy scan...")

    result = os.system("./agents/trivy_agent.sh")
    passed = (result == 0)

    state["trivy_passed"] = passed
    log_state("trivy_scan", "passed" if passed else "failed")

    return state


# ---------------------------------------------------------
# STEP 2 — SMOKE TEST
# ---------------------------------------------------------
def smoke_test_step(state):
    print("[🔥] Running smoke test...")

    result = os.system("bash smoke_test.sh")
    passed = (result == 0)

    state["smoke_test_passed"] = passed
    log_state("smoke_test", "passed" if passed else "failed")

    return state


# ---------------------------------------------------------
# STEP 3 — LLM DECISION (PROCEED / HALT)
# ---------------------------------------------------------
def llm_decision_step(state):
    print("[🤖] LLM Agent deciding whether to deploy...")

    decision = llm_decision(state)
    state["llm_decision"] = decision

    log_state("llm_decision", "proceed" if decision else "halt")

    return state


# ---------------------------------------------------------
# STEP 4 — BUILD + PUSH DOCKER → ECR + DEPLOY TO ECS
# ---------------------------------------------------------
def deploy_step(state):
    print("[🚀] Running Build + ECR Push + ECS Deployment Agent...")

    # This calls the Build-and-Deploy agent
    build_and_deploy()

    state["deployed"] = True
    log_state("deploy", "started")

    return state


# ---------------------------------------------------------
# STEP 5 — FAILURE HANDLER
# ---------------------------------------------------------
def stop_step(state):
    print("[⛔] Halting deployment due to failed checks or LLM decision.")
    state["deployed"] = False
    log_state("deployment", "stopped")
    return state


# =========================================================
# BUILD LANGGRAPH WORKFLOW
# =========================================================
def build_graph():
    builder = StateGraph(dict)

    builder.add_node("start", lambda state: state)
    builder.add_node("trivy", trivy_scan_step)
    builder.add_node("smoke", smoke_test_step)
    builder.add_node("llm_decide", llm_decision_step)
    builder.add_node("deploy", deploy_step)
    builder.add_node("stop", stop_step)

    # Entry → Trivy
    builder.set_entry_point("start")
    builder.add_edge("start", "trivy")
    builder.add_edge("trivy", "smoke")

    # Smoke → (pass / fail)
    builder.add_conditional_edges(
        "smoke",
        lambda state: "pass" if state.get("smoke_test_passed") else "fail",
        {"pass": "llm_decide", "fail": "stop"},
    )

    # LLM → (proceed / halt)
    builder.add_conditional_edges(
        "llm_decide",
        lambda state: "proceed" if state.get("llm_decision") else "halt",
        {"proceed": "deploy", "halt": "stop"},
    )

    builder.set_finish_point("deploy")
    builder.set_finish_point("stop")

    return builder.compile()


# =========================================================
# MAIN ENTRY
# =========================================================
def main():
    state = {"trigger": "deploy"}
    graph = build_graph()
    final_state = graph.invoke(state)

    print("=========================================")
    print("✅ FINAL STATE:", final_state)
    print("=========================================")


if __name__ == "__main__":
    main()
