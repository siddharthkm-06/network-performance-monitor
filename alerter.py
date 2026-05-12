import json
import os
from datetime import datetime

# Load thresholds from config.json
with open("config.json", "r") as f:
    config = json.load(f)

LATENCY_THRESHOLD = config["settings"]["latency_threshold_ms"]
LOSS_THRESHOLD = config["settings"]["packet_loss_threshold_percent"]

LOG_FILE = "logs/alerts.log"


def write_alert(message):
    """
    Writes a timestamped alert message to the log file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] ALERT: {message}"

    # Print to screen so you can see it live
    print(full_message)

    # Also save it to the log file
    with open(LOG_FILE, "a") as log:
        log.write(full_message + "\n")


def check_and_alert(host_name, ping_result):
    """
    Receives a host name and ping result dict.
    Checks both latency and packet loss against thresholds.
    Returns True if any alert was triggered, False if all clear.
    """
    alert_triggered = False
    latency = ping_result["avg_latency_ms"]
    loss = ping_result["packet_loss_percent"]

    # Check if host is completely unreachable
    if latency is None:
        write_alert(f"{host_name} ({ping_result['ip']}) is UNREACHABLE — 100% packet loss")
        alert_triggered = True
        return alert_triggered

    # Check latency threshold
    if latency > LATENCY_THRESHOLD:
        write_alert(
            f"{host_name} ({ping_result['ip']}) — high latency: {latency}ms "
            f"(threshold: {LATENCY_THRESHOLD}ms)"
        )
        alert_triggered = True

    # Check packet loss threshold
    if loss > LOSS_THRESHOLD:
        write_alert(
            f"{host_name} ({ping_result['ip']}) — packet loss: {loss}% "
            f"(threshold: {LOSS_THRESHOLD}%)"
        )
        alert_triggered = True

    return alert_triggered


# --- Quick test ---
if __name__ == "__main__":
    # Simulate a bad result to test alerting
    fake_result = {
        "ip": "8.8.8.8",
        "avg_latency_ms": 150,
        "packet_loss_percent": 10
    }
    print("Testing alerter with a simulated bad result...")
    check_and_alert("Google DNS", fake_result)
    print("\nCheck your logs/alerts.log file to see the saved alert!")