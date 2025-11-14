import os
import requests
from utils.logger import log_state

def trigger_github_action(state):
    print("[🚀] Triggering GitHub Actions workflow...")

    # Environment Variables (you MUST set these securely)
    token = os.getenv("GITHUB_TOKEN")  # GitHub Personal Access Token (classic or fine-grained with workflow scope)
    repo = os.getenv("GITHUB_REPO")    # Format: username/repo (e.g., rbhatlapenumarthi/agentic-poc)
    workflow = os.getenv("GITHUB_WORKFLOW", "deploy.yml")  # Default to deploy.yml
    ref = os.getenv("GITHUB_REF", "main")                  # Default branch

    if not all([token, repo]):
        print("[❌] Missing GITHUB_TOKEN or GITHUB_REPO env variables.")
        state["gh_dispatch"] = False
        log_state("github_dispatch", "failed - missing env")
        return state

    url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow}/dispatches"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    data = {
        "ref": ref
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 204:
        print("[✅] GitHub Actions triggered successfully.")
        state["gh_dispatch"] = True
        log_state("github_dispatch", "triggered")
    else:
        print(f"[❌] Failed to trigger GitHub Actions: {response.status_code}, {response.text}")
        state["gh_dispatch"] = False
        log_state("github_dispatch", "failed")

    return state

