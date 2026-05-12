import csv
import os
from datetime import datetime

# CSV file will be named by today's date e.g. report_2026-05-11.csv
today = datetime.now().strftime("%Y-%m-%d")
REPORT_FILE = f"logs/report_{today}.csv"

# These are the column headers in our CSV
HEADERS = ["timestamp", "host_name", "ip", "avg_latency_ms", "packet_loss_percent", "status"]


def init_report():
    """
    Creates the CSV file with headers if it doesn't exist yet.
    Called once when the monitor starts up.
    """
    if not os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)
        print(f"Report file created: {REPORT_FILE}")
    else:
        print(f"Report file already exists: {REPORT_FILE}")


def log_result(host_name, ping_result, alert_triggered):
    """
    Appends one row to the CSV for this host's ping result.
    Called after every single host is pinged.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    latency = ping_result["avg_latency_ms"]
    loss = ping_result["packet_loss_percent"]

    # Status is either OK or ALERT — easy to filter in Excel later
    status = "ALERT" if alert_triggered else "OK"

    # If latency is None (unreachable), write "N/A" instead of blank
    latency_display = latency if latency is not None else "N/A"

    row = [timestamp, host_name, ping_result["ip"], latency_display, loss, status]

    with open(REPORT_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)


# --- Quick test ---
if __name__ == "__main__":
    print("Testing reporter...")
    init_report()

    # Simulate logging 3 results
    log_result("Google DNS", {"ip": "8.8.8.8", "avg_latency_ms": 38, "packet_loss_percent": 0}, False)
    log_result("Cloudflare DNS", {"ip": "1.1.1.1", "avg_latency_ms": 150, "packet_loss_percent": 0}, True)
    log_result("Broken Host", {"ip": "192.168.99.99", "avg_latency_ms": None, "packet_loss_percent": 100}, True)

    print(f"Done! Open logs/report_{today}.csv to see the results.")