import numpy as np

from detection.ml_detector import NetworkAnomalyDetector


def generate_demo_training_data(samples=500):
    """
    Generate SYNTHETIC normal-like traffic features
    for testing the model-training pipeline.

    Columns:
    1. Packet size in bytes
    2. Packets per second
    3. Destination port

    This is demonstration data, not a real traffic dataset.
    """

    rng = np.random.default_rng(42)

    packet_sizes = rng.integers(64, 1400, size=samples)
    packet_rates = rng.uniform(1, 50, size=samples)

    common_ports = np.array([
        53, 80, 123, 443, 443, 443,
        8080, 8443, 53, 80
    ])

    destination_ports = rng.choice(
        common_ports,
        size=samples
    )

    return np.column_stack((
        packet_sizes,
        packet_rates,
        destination_ports
    ))


def main():
    print("[1/3] Preparing demonstration data...")

    training_data = generate_demo_training_data()

    print(f"[2/3] Training with {len(training_data)} samples...")

    detector = NetworkAnomalyDetector()
    detector.train(training_data)

    print("[3/3] Testing the saved model...")

    detector.load()

    result = detector.predict(
        packet_size=1200,
        packets_per_second=20,
        destination_port=443
    )

    print("\nDemo prediction:")
    print(result)

    print("\nTraining pipeline completed successfully.")
    print("NOTE: This does not validate real-world detection accuracy.")


if __name__ == "__main__":
    main()