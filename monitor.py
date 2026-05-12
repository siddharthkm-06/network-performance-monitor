import json
import time
from datetime import datetime

# Import our own files — this is why we built them separately
from pinger import ping_host
from alerter import check_and_alert
from reporter import init_report, log_result

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

HOSTS = config["hosts"]
INTERVAL = config["settings"]["interval_seconds"]
PINGS_PER_HOST = config["settings"]["pings_per_host"]


def run_monitor():
    """
    Main monitoring loop. Runs forever until you press Ctrl+C.
    Each cycle: pings all hosts, checks alerts, logs to CSV.
    """
    print("=" * 55)
    print("   Python Network Performance Monitor")
    print("   Press Ctrl+C to stop")
    print("=" * 55)

    # Create today's CSV file before the loop starts
    init_report()

    cycle = 1

    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[Cycle {cycle}] — {timestamp}")
        print("-" * 55)

        all_clear = True

        for host in HOSTS:
            name = host["name"]
            ip = host["ip"]

            # 1. Ping the host
            result = ping_host(ip, count=PINGS_PER_HOST)

            latency = result["avg_latency_ms"]
            loss = result["packet_loss_percent"]

            # 2. Display result on screen
            latency_display = f"{latency}ms" if latency is not None else "N/A"
            print(f"  {name:<20} {ip:<18} Latency: {latency_display:<10} Loss: {loss}%")

            # 3. Check thresholds and alert if needed
            alert_triggered = check_and_alert(name, result)

            if alert_triggered:
                all_clear = False

            # 4. Save this result to today's CSV
            log_result(name, result, alert_triggered)

        # Summary line at end of each cycle
        if all_clear:
            print(f"\n  ✓ All hosts healthy — next check in {INTERVAL}s")
        else:
            print(f"\n  ⚠ Alerts triggered — check logs/alerts.log")

        cycle += 1

        # Wait for next cycle (Ctrl+C during this is caught below)
        time.sleep(INTERVAL)


# --- Run it ---
if __name__ == "__main__":
    try:
        run_monitor()
    except KeyboardInterrupt:
        print("\n\nMonitor stopped. Goodbye!")