import subprocess
import re

def ping_host(ip, count=4):
    """
    Pings an IP address 'count' times using Windows ping command.
    Returns a dictionary with latency (ms) and packet loss (%).
    """

    # Build the ping command: ping -n 4 8.8.8.8
    command = ["ping", "-n", str(count), ip]

    # Run the command and capture its output as text
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    output = result.stdout

    # --- Parse packet loss ---
    # Windows ping prints something like: "Packets: Sent = 4, Received = 3, Lost = 1 (25% loss)"
    loss_match = re.search(r"(\d+)% loss", output)
    if loss_match:
        packet_loss = int(loss_match.group(1))
    else:
        packet_loss = 100  # If we can't parse it, assume total loss

    # --- Parse average latency ---
    # Windows ping prints something like: "Average = 14ms"
    latency_match = re.search(r"Average = (\d+)ms", output)
    if latency_match:
        avg_latency = int(latency_match.group(1))
    else:
        avg_latency = None  # None means host was unreachable

    return {
        "ip": ip,
        "avg_latency_ms": avg_latency,
        "packet_loss_percent": packet_loss
    }


# --- Quick test (only runs when you run THIS file directly) ---
if __name__ == "__main__":
    test_ip = "8.8.8.8"
    print(f"Testing ping to {test_ip}...")
    result = ping_host(test_ip)
    print(result)