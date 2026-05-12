import csv
from datetime import datetime
from collections import defaultdict

# Find today's report
today = datetime.now().strftime("%Y-%m-%d")
REPORT_FILE = f"logs/report_{today}.csv"

def analyse():
    # Store per-host data
    stats = defaultdict(lambda: {
        "latencies": [],
        "losses": [],
        "alerts": 0,
        "total": 0
    })

    with open(REPORT_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["host_name"]
            stats[name]["total"] += 1

            if row["avg_latency_ms"] != "N/A":
                stats[name]["latencies"].append(int(row["avg_latency_ms"]))

            stats[name]["losses"].append(float(row["packet_loss_percent"]))

            if row["status"] == "ALERT":
                stats[name]["alerts"] += 1

    # Print report
    print("=" * 60)
    print(f"  Network Monitor Summary — {today}")
    print(f"  Report: {REPORT_FILE}")
    print("=" * 60)

    for host, data in stats.items():
        latencies = data["latencies"]
        losses = data["losses"]
        total = data["total"]
        alerts = data["alerts"]
        uptime = ((total - alerts) / total) * 100

        print(f"\n  Host      : {host}")
        print(f"  Cycles    : {total}")
        print(f"  Latency   : min={min(latencies)}ms  "
              f"max={max(latencies)}ms  "
              f"avg={round(sum(latencies)/len(latencies))}ms")
        print(f"  Avg Loss  : {round(sum(losses)/len(losses), 2)}%")
        print(f"  Uptime    : {round(uptime, 1)}%")
        print(f"  Alerts    : {alerts}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    analyse()