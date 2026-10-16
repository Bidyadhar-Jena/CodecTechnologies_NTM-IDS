from collections import defaultdict, deque
from time import time
from threading import Lock


class IntrusionDetector:
    def __init__(
        self,
        time_window=10,
        port_threshold=15
    ):
        self.time_window = time_window
        self.port_threshold = port_threshold

        # Source IP -> recent (timestamp, destination port) events
        self.connections = defaultdict(deque)

        # Avoid repeatedly reporting the same source in every packet
        self.reported_sources = set()

        self.lock = Lock()

    def analyze(self, record):
        """
        Return an alert if a source contacts many different
        destination ports within the configured time window.
        """

        source_ip = record.get("source_ip")
        destination_port = record.get("destination_port")

        if not source_ip or destination_port is None:
            return None

        current_time = time()

        with self.lock:
            events = self.connections[source_ip]

            events.append((current_time, destination_port))

            # Remove expired events
            while (
                events
                and current_time - events[0][0] > self.time_window
            ):
                events.popleft()

            # Count unique destination ports
            unique_ports = {
                port for _, port in events
            }

            if (
                len(unique_ports) >= self.port_threshold
                and source_ip not in self.reported_sources
            ):
                self.reported_sources.add(source_ip)

                return {
                    "type": "Possible Port Scan",
                    "source_ip": source_ip,
                    "unique_ports": len(unique_ports),
                    "time_window_seconds": self.time_window,
                    "message": (
                        f"Source {source_ip} contacted "
                        f"{len(unique_ports)} different destination "
                        f"ports within {self.time_window} seconds."
                    )
                }

        return None