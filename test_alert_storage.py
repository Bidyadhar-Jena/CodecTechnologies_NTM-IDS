from database.db_manager import (
    initialize_database,
    save_alert,
    get_recent_alerts,
    get_alert_count
)
from datetime import datetime

def main():
    print("=" * 45)
    print("SENTINEL - DATABASE TEST")
    print("=" * 45)

    initialize_database()

    test_alert = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "Test Alert",
        "source_ip": "192.0.2.10",
        "destination_ip": "192.0.2.20",
        "severity": "WARNING",
        "message": "This is a simulated alert for database testing."
    }

    save_alert(test_alert)
    print("\nTest alert saved.")

    recent_alerts = get_recent_alerts(limit=5)

    print("\nRecent alerts:")
    for alert in recent_alerts:
        print(alert)

    print("\nTotal stored alerts:", get_alert_count())
    print("\nDatabase test completed.")

if __name__ == "__main__":
    main()