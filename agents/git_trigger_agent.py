import os
import subprocess
from utils.logger import log_state

def trigger_git_push(state):
    print("[📦] Committing and pushing code to GitHub...")

    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "agentic commit 🚀"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)

        print("[✅] Code pushed to GitHub.")
        state["git_commit"] = True
        log_state("git_push", "success")
    except subprocess.CalledProcessError as e:
        print(f"[❌] Git push failed: {e}")
        state["git_commit"] = False
        log_state("git_push", "failure")

    return state

