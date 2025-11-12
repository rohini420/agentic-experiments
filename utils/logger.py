import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("pipeline_state.json")

def log_state(step_name, status, extras=None):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "step": step_name,
        "status": status
    }
    if extras:
        log_entry.update(extras)

    if LOG_PATH.exists():
        with LOG_PATH.open("r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_entry)

    with LOG_PATH.open("w") as f:
        json.dump(logs, f, indent=2)

