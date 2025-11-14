import os
import subprocess
from utils.logger import log_state

def git_trigger(state):
    print("[📤] Committing and pushing code to GitHub...")

    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "🚀 Automated commit from AI agent"], check=True)
        subprocess.run(["git", "push"], check=True)
        state["git_push"] = True
        log_state("git", "pushed")
    except subprocess.CalledProcessError as e:
        print(f"[❌] Git operation failed: {e}")
        state["git_push"] = False
        log_state("git", "failed")

    return state

