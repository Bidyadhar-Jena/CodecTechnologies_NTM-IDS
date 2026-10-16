from detection.ml_detector import NetworkAnomalyDetector

def main():
    detector = NetworkAnomalyDetector()

    print("=" * 50)
    print("SENTINEL - ML DETECTOR TEST")
    print("=" * 50)

    try:
        detector.load()
    except Exception as error:
        print("ERROR: Could not load the model:", error)
        return

    test_cases = [
        {
            "name": "Ordinary web traffic example",
            "packet_size": 512,
            "packets_per_second": 10,
            "destination_port": 443,
        },
        {
            "name": "Large packet example",
            "packet_size": 60000,
            "packets_per_second": 10,
            "destination_port": 443,
        },
        {
            "name": "High packet-rate example",
            "packet_size": 512,
            "packets_per_second": 10000,
            "destination_port": 443,
        },
    ]

    for case in test_cases:
        result = detector.predict(
            packet_size=case["packet_size"],
            packets_per_second=case["packets_per_second"],
            destination_port=case["destination_port"],
        )

        status = (
            "POTENTIAL ANOMALY"
            if result["is_anomaly"]
            else "NORMAL"
        )

        print(f"\nTest: {case['name']}")
        print(f"Result: {status}")
        print(f"Anomaly score: {result['anomaly_score']:.4f}")
        print(f"Features: {result['features']}")

    print("\nDetector test completed.")

if __name__ == "__main__":
    main()