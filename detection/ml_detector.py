from pathlib import Path

import joblib
import numpy as np

from sklearn.ensemble import IsolationForest
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


PROJECT_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_DIR / "models"
MODEL_PATH = MODEL_DIR / "anomaly_model.joblib"

FEATURE_NAMES = [
    "packet_size",
    "packets_per_second",
    "destination_port"
]


class NetworkAnomalyDetector:
    def __init__(self):
        self.model = None

    def train(self, training_data):
        """
        Train using representative NORMAL network traffic.

        training_data must be a numeric array with three columns:
        packet size, packets per second, destination port.
        """

        data = np.asarray(training_data, dtype=float)

        if data.ndim != 2 or data.shape[1] != len(FEATURE_NAMES):
            raise ValueError(
                "Training data must contain exactly three features."
            )

        if data.shape[0] < 20:
            raise ValueError(
                "Provide at least 20 representative training samples."
            )

        if not np.isfinite(data).all():
            raise ValueError("Training data contains invalid values.")

        if (data < 0).any():
            raise ValueError("Training features cannot be negative.")

        self.model = make_pipeline(
            StandardScaler(),
            IsolationForest(
                n_estimators=100,
                contamination=0.05,
                random_state=42
            )
        )

        self.model.fit(data)

        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)

        print("[ML] Model trained and saved successfully.")

    def load(self):
        """Load a previously trained model."""

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "Trained model not found. Train the model first."
            )

        self.model = joblib.load(MODEL_PATH)

        print("[ML] Model loaded successfully.")

    def predict(self, packet_size, packets_per_second, destination_port):
        """
        Return a basic anomaly assessment.

        -1 indicates an anomaly according to the model.
         1 indicates an observation classified as normal.
        """

        if self.model is None:
            raise RuntimeError(
                "Model is not loaded. Train or load it first."
            )

        features = np.array([[
            packet_size,
            packets_per_second,
            destination_port
        ]], dtype=float)

        if not np.isfinite(features).all():
            raise ValueError("Prediction features must be finite.")

        if (features < 0).any():
            raise ValueError("Prediction features cannot be negative.")

        prediction = int(self.model.predict(features)[0])
        score = float(self.model.decision_function(features)[0])

        return {
            "is_anomaly": prediction == -1,
            "prediction": prediction,
            "anomaly_score": score,
            "features": dict(zip(FEATURE_NAMES, features[0].tolist()))
        }


if __name__ == "__main__":
    print("Network Anomaly Detector")
    print("Features:", ", ".join(FEATURE_NAMES))
    print("Model path:", MODEL_PATH)
    print("Train the model using representative normal traffic.")