# agents/llm_decision_agent.py
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

def llm_decision(state):
    print("[🤖] LLM Agent deciding whether to deploy...")

    trivy_ok = state.get("trivy_passed", False)
    smoke_ok = state.get("smoke_test_passed", False)

    if not trivy_ok or not smoke_ok:
        print("❌ Pre-check failed. LLM will automatically decline deploy.")
        state["llm_decision"] = False
        return state

    prompt = f"""
    You are a DevOps assistant. Decide if deployment should proceed based on tests.

    Trivy scan passed: {trivy_ok}
    Smoke test passed: {smoke_ok}

    Should we proceed with deployment? Answer 'YES' or 'NO' only.
    """

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    response = llm([HumanMessage(content=prompt)])
    decision_text = response.content.strip().lower()

    decision = "yes" in decision_text
    state["llm_decision"] = decision
    return state

