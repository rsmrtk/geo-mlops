"""
Train location classifier and register it in MLflow Model Registry.

Usage:
    python -m training.train
"""

import logging
import os

import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

from training.data import fetch_training_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "location-classifier")
EXPERIMENT_NAME = "geo-mlops"


def train() -> None:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    logger.info("fetching training data...")
    samples = fetch_training_data(limit_per_class=200)

    if len(samples) < 50:
        raise RuntimeError(f"not enough training data: {len(samples)} samples")

    X = np.array([[s.lat, s.lng] for s in samples])
    raw_labels = [s.label for s in samples]

    encoder = LabelEncoder()
    y = encoder.fit_transform(raw_labels)
    classes = list(encoder.classes_)
    logger.info("classes: %s", classes)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    with mlflow.start_run():
        params = {"n_estimators": 100, "max_depth": 8, "random_state": 42}
        clf = RandomForestClassifier(**params)
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=classes)

        mlflow.log_params(params)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_text(report, "classification_report.txt")
        mlflow.log_param("classes", ",".join(classes))
        mlflow.log_param("train_samples", len(X_train))
        mlflow.log_param("test_samples", len(X_test))

        logger.info("accuracy: %.3f", accuracy)
        logger.info("\n%s", report)

        # Wrap classifier to return (label_str, confidence) pairs
        class LocationClassifierWrapper(mlflow.pyfunc.PythonModel):
            def __init__(self, clf, encoder):
                self.clf = clf
                self.encoder = encoder

            def predict(self, context, model_input):
                proba = self.clf.predict_proba(model_input)
                idx = proba.argmax(axis=1)
                labels = self.encoder.inverse_transform(idx)
                confidences = proba.max(axis=1)
                # Return flat array: [label0, conf0, label1, conf1, ...]
                result = []
                for label, conf in zip(labels, confidences):
                    result.extend([label, round(float(conf), 4)])
                return result

        wrapper = LocationClassifierWrapper(clf, encoder)

        mlflow.pyfunc.log_model(
            artifact_path="model",
            python_model=wrapper,
            registered_model_name=MODEL_NAME,
        )
        logger.info("model registered as '%s' (Staging)", MODEL_NAME)


if __name__ == "__main__":
    train()
