# Python Network Performance Monitor

A Python-based network monitoring tool that continuously polls multiple hosts
via ICMP, detects latency and packet loss anomalies, triggers timestamped alerts,
and generates structured CSV reports for trend analysis.

Built to simulate real-world NOC (Network Operations Center) workflows.

---

## What Problem Does This Solve?

In production networks, engineers need continuous visibility into host reachability
and performance. Manual checking is not scalable. This tool automates that process —
polling 5 hosts every 60 seconds, flagging degraded performance instantly, and
building a historical record for pattern analysis.

---

## Features

- Polls multiple hosts via ICMP ping on a configurable interval
- Measures average round-trip latency (ms) and packet loss (%) per host
- Threshold-based alerting — triggers when latency > 100ms or loss > 5%
- Writes timestamped alerts to `logs/alerts.log`
- Generates daily CSV reports (`logs/report_YYYY-MM-DD.csv`) for trend tracking
- Summary analyser calculates min/max/avg latency and uptime % per host
- All thresholds and hosts configurable via `config.json` — no code changes needed

---

## Project Structure

network_monitor/
├── config.json      # Hosts to monitor and alert thresholds
├── pinger.py        # ICMP ping engine — returns latency and packet loss
├── alerter.py       # Threshold checker — writes alerts to log file
├── reporter.py      # CSV logger — one row per host per cycle
├── monitor.py       # Main loop — orchestrates all modules every 60s
├── analyser.py      # Post-run statistics — min/max/avg/uptime per host
└── logs/
├── alerts.log
└── report_YYYY-MM-DD.csv

---

## Sample Output

### Live Monitor

<img width="886" height="368" alt="image" src="https://github.com/user-attachments/assets/6fd10e5d-b6fd-4141-80cd-b9c413cee0c6" />

### Summary Analysis 

<img width="685" height="862" alt="image" src="https://github.com/user-attachments/assets/939bcb95-79b1-4803-bba9-fd25847237c5" />

---

## How to Run

**Requirements:** Python 3.8+ — no external libraries needed (uses stdlib only)

```bash
# Clone the repo
git clone https://github.com/siddharthkm-06/network-performance-monitor.git
cd network-performance-monitor

# Start monitoring
python monitor.py

# After running, analyse results
python analyser.py
```

---

## Configuration

Edit `config.json` to change hosts or thresholds — no code changes needed:

```json
{
  "hosts": [
    {"name": "Google DNS", "ip": "8.8.8.8"}
  ],
  "settings": {
    "interval_seconds": 60,
    "pings_per_host": 4,
    "latency_threshold_ms": 100,
    "packet_loss_threshold_percent": 5
  }
}
```

---

## Key Technical Concepts Demonstrated

- **ICMP protocol** — understanding of ping as a network diagnostic tool
- **Subprocess management** — spawning OS-level commands from Python
- **Regex parsing** — extracting structured data from raw command output
- **Threshold-based alerting** — core pattern in network monitoring systems
- **CSV report generation** — structured data logging for trend analysis
- **Modular code design** — each component independently testable

---

## Real-World Relevance

This tool mirrors workflows used in production NOC environments:
- Continuous host polling → matches network availability monitoring
- Threshold alerting → matches PagerDuty/Nagios alert logic
- CSV trend reports → matches capacity planning data pipelines
