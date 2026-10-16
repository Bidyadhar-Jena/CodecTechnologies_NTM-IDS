import time
from datetime import datetime
from pathlib import Path
from collections import defaultdict, deque

from scapy.all import sniff, IP, TCP, UDP

from database.db_manager import initialize_database, save_alert
from detection.ml_detector import NetworkAnomalyDetector


# Project configuration
PROJECT_DIR = Path(__file__).resolve().parent
ALERTS_FILE = PROJECT_DIR / "logs" / "alerts.json"

traffic_data = deque(maxlen=200)
alerts = deque(maxlen=100)

# Track packet rates by source IP
packet_timestamps = defaultdict(deque)

# Avoid repeating the same anomaly alert too frequently
last_alert_time = {}
ALERT_COOLDOWN_SECONDS = 30

detector = NetworkAnomalyDetector()
ml_enabled = False


def initialize_monitor():
    """Initialize the database and load the trained ML model."""
    global ml_enabled

    initialize_database()

    try:
        detector.load()
        ml_enabled = True
        print("[ML] Anomaly detector enabled.")
    except Exception as error:
        ml_enabled = False
        print(f"[ML] Detector unavailable: {error}")
        print("[ML] Packet monitoring will continue without ML detection.")


def save_alert_file():
    """Save recent alerts to the JSON file."""
    import json

    ALERTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with ALERTS_FILE.open("w", encoding="utf-8") as file:
        import json
        json.dump(list(alerts), file, indent=4)


def process_packet(packet):
    """Extract packet information and check for potential anomalies."""
    if IP not in packet:
        return

    now = time.time()
    ip_layer = packet[IP]

    source_ip = ip_layer.src
    destination_ip = ip_layer.dst
    packet_size = len(packet)

    destination_port = 0
    protocol = "OTHER"

    if TCP in packet:
        destination_port = int(packet[TCP].dport)
        protocol = "TCP"
    elif UDP in packet:
        destination_port = int(packet[UDP].dport)
        protocol = "UDP"

    # Calculate the recent packet rate for this source.
    timestamps = packet_timestamps[source_ip]
    timestamps.append(now)

    while timestamps and now - timestamps[0] > 1:
        timestamps.popleft()

    packets_per_second = len(timestamps)

    packet_info = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_ip": source_ip,
        "destination_ip": destination_ip,
        "protocol": protocol,
        "source_port": (
            int(packet[TCP].sport) if TCP in packet
            else int(packet[UDP].sport) if UDP in packet
            else None
        ),
        "destination_port": destination_port or None,
        "size": packet_size,
    }

    traffic_data.append(packet_info)

    # Use the trained model to check for potential anomalies.
    if ml_enabled:
        try:
            result = detector.predict(
                packet_size=packet_size,
                packets_per_second=packets_per_second,
                destination_port=destination_port,
            )

            if result["is_anomaly"]:
                cooldown_key = (source_ip, destination_ip, destination_port)
                previous_alert = last_alert_time.get(cooldown_key, 0)

                if now - previous_alert >= ALERT_COOLDOWN_SECONDS:
                    last_alert_time[cooldown_key] = now

                    alert = {
                        "time": packet_info["time"],
                        "type": "ML Anomaly",
                        "source_ip": source_ip,
                        "destination_ip": destination_ip,
                        "severity": "WARNING",
                        "message": (
                            "Potential unusual network traffic detected "
                            f"(port {destination_port}, "
                            f"anomaly score {result['anomaly_score']:.4f})."
                        ),
                    }

                    alerts.appendleft(alert)

                    try:
                        save_alert(alert)
                        save_alert_file()
                    except Exception as error:
                        print(f"[DB] Could not save alert: {error}")

                    print("[ALERT]", alert["message"])

        except Exception as error:
            print(f"[ML] Prediction error: {error}")


def start_monitor(interface=None):
    """Start capturing packets."""
    initialize_monitor()

    print("[MONITOR] Starting packet capture...")

    try:
        sniff(
            iface=interface,
            prn=process_packet,
            store=False,
        )
    except PermissionError:
        print(
            "[MONITOR] Permission denied. "
            "Try running VS Code as Administrator."
        )
    except Exception as error:
        print(f"[MONITOR] Packet capture error: {error}")


if __name__ == "__main__":
    start_monitor()