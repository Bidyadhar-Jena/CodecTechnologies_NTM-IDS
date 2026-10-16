import sqlite3
from pathlib import Path

# Store the database inside the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_DIR / "network_security.db"


def get_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the alerts table if it doesn't exist."""

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                source_ip TEXT,
                destination_ip TEXT,
                severity TEXT NOT NULL DEFAULT 'INFO',
                message TEXT NOT NULL
            )
            """
        )

    print("[DB] Database initialized successfully.")


def save_alert(alert):
    """Save a security alert to the database."""

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO alerts (
                timestamp,
                alert_type,
                source_ip,
                destination_ip,
                severity,
                message
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                alert.get("time", ""),
                alert.get("type", "Unknown"),
                alert.get("source_ip"),
                alert.get("destination_ip"),
                alert.get("severity", "INFO"),
                alert.get("message", "")
            )
        )


def get_recent_alerts(limit=50):
    """Retrieve recent alerts from the database."""

    limit = max(1, min(int(limit), 500))

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM alerts
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

    return [dict(row) for row in rows]

def get_alert_count():
    with get_connection() as connection:
        row = connection.execute(
            "SELECT COUNT(*) AS total FROM alerts"
        ).fetchone()
    return row["total"]

if __name__ == "__main__":
    initialize_database()

    print("Recent alerts:")
    print(get_recent_alerts())