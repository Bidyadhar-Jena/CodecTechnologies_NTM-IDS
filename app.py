from flask import Flask, render_template, jsonify
from threading import Thread

from packet_monitor import traffic_data, alerts, start_monitor
from database.db_manager import get_recent_alerts, get_alert_count

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/traffic")
def get_traffic():
    return jsonify(list(traffic_data)[-100:])


@app.route("/api/alerts")
def get_alerts():
    return jsonify(list(alerts)[:50])


@app.route("/api/alerts/history")
def get_alert_history():
    try:
        history = get_recent_alerts(limit=50)
        return jsonify(history)
    except Exception as error:
        app.logger.exception("Could not retrieve alert history")
        return jsonify({
            "error": "Unable to retrieve alert history."
        }), 500


@app.route("/api/stats")
def get_stats():
    try:
        return jsonify({
            "traffic_packets": len(traffic_data),
            "live_alerts": len(alerts),
            "stored_alerts": get_alert_count()
        })
    except Exception:
        app.logger.exception("Could not retrieve dashboard statistics")
        return jsonify({
            "error": "Unable to retrieve dashboard statistics."
        }), 500


if __name__ == "__main__":
    monitor_thread = Thread(
        target=start_monitor,
        kwargs={"interface": None},
        daemon=True
    )
    monitor_thread.start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )