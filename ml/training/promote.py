"""
Promote the latest model version to Production in MLflow Model Registry.

Uses aliases (champion) instead of deprecated stages.

Usage:
    python -m training.promote
    python -m training.promote --version 3
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
        versions = client.search_model_versions(f"name='{MODEL_NAME}'")
        if not versions:
            raise RuntimeError(f"no versions found for '{MODEL_NAME}'")
        # get latest version by version number
        version = max(int(v.version) for v in versions)
        logger.info("latest version: %d", version)

    client.set_registered_model_alias(
        name=MODEL_NAME,
        alias="champion",
        version=str(version),
    )
    logger.info("version %d set as alias 'champion' (Production)", version)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", type=int, default=None)
    args = parser.parse_args()
    promote(args.version)
