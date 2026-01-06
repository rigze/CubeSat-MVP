import datetime
import os
import json

LOG_FILE = "logs/comm.log"


def log_event(component, event_type, details, level="INFO"):
    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = (
        f"\n[{timestamp}]\n"
        f"Level     : {level}\n"
        f"Component : {component}\n"
        f"Event     : {event_type}\n"
        f"Details   : {json.dumps(details)}\n"
        f"{'-'*50}\n"
    )

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
