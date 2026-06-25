import os
import logging
from contextlib import asynccontextmanager

import mlflow.pyfunc
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

logger = logging.getLogger(__name__)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "location-classifier")
MODEL_STAGE = os.getenv("MODEL_STAGE", "Production")

model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    model_uri = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
    logger.info("loading model from %s", model_uri)
    try:
        model = mlflow.pyfunc.load_model(model_uri)
        logger.info("model loaded")
    except Exception as e:
        # Service starts even without a model — returns "unknown" until model is available
        logger.warning("could not load model: %s", e)
    yield


app = FastAPI(title="ml-svc", lifespan=lifespan)


class ClassifyRequest(BaseModel):
    lat: float
    lng: float

    @field_validator("lat")
    @classmethod
    def validate_lat(cls, v: float) -> float:
        if not -90 <= v <= 90:
            raise ValueError("lat must be in [-90, 90]")
        return v

    @field_validator("lng")
    @classmethod
    def validate_lng(cls, v: float) -> float:
        if not -180 <= v <= 180:
            raise ValueError("lng must be in [-180, 180]")
        return v


class ClassifyResponse(BaseModel):
    location_type: str
    confidence: float


LOCATION_TYPES = [
    "residential",
    "commercial",
    "industrial",
    "park",
    "transport",
    "education",
    "healthcare",
    "religious",
    "unknown",
]


@app.post("/classify", response_model=ClassifyResponse)
def classify(req: ClassifyRequest) -> ClassifyResponse:
    if model is None:
        return ClassifyResponse(location_type="unknown", confidence=0.0)

    features = np.array([[req.lat, req.lng]])
    try:
        result = model.predict(features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    loc_type = str(result[0])
    # MLflow pyfunc returns raw prediction; confidence comes from predict_proba wrapper
    confidence = float(result[1]) if len(result) > 1 else 0.0

    return ClassifyResponse(location_type=loc_type, confidence=confidence)


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}
