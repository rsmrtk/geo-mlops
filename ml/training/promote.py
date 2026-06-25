"""
Promote the latest Staging model version to Production in MLflow Model Registry.

Usage:
    python -m training.promote
    python -m training.promote --version 3   # promote specific version
"""

import argparse
import logging
import os

import mlflow
from mlflow import MlflowClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "location-classifier")


def promote(version: int | None = None) -> None:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient()

    if version is None:
        staging = client.get_latest_versions(MODEL_NAME, stages=["Staging"])
        if not staging:
            raise RuntimeError(f"no Staging version found for '{MODEL_NAME}'")
        version = int(staging[0].version)
        logger.info("latest Staging version: %d", version)

    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=str(version),
        stage="Production",
        archive_existing_versions=True,
    )
    logger.info("version %d promoted to Production", version)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", type=int, default=None)
    args = parser.parse_args()
    promote(args.version)
