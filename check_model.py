from detection.ml_detector import NetworkAnomalyDetector

detector = NetworkAnomalyDetector()

try:
    detector.load()
    print("SUCCESS: Model loaded correctly.")

    result = detector.predict(
        packet_size=1200,
        packets_per_second=20,
        destination_port=443
    )

    print("\nTest prediction:")
    print(result)

except FileNotFoundError:
    print("ERROR: Model file was not found.")
    print("Run: python train_model.py")

except Exception as error:
    print("ERROR:", error)