import os
import subprocess

def trigger_git_push(state):
    print("[📦] Committing and pushing code to GitHub...")

    try:
        # Add all changes
        subprocess.run(["git", "add", "."], check=True)

        # Commit with message
        subprocess.run(["git", "commit", "-m", "🤖 Agent commit: updated code"], check=True)

        # Push to origin/main
        subprocess.run(["git", "push", "origin", "main"], check=True)

        print("✅ Git push successful.")
        state["git_pushed"] = True

    except subprocess.CalledProcessError as e:
        print("❌ Git push failed:", e)
        state["git_pushed"] = False

    return state

