from typing import Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel

from app.recommender import Recommender
from app.settings import APP_ENV
from app.storage import write_prediction_log


app = FastAPI(
    title="Política de la Felicidad - MLOps Recommender",
    version="1.0.0"
)

recommender = Recommender()


class PredictionRequest(BaseModel):
    text: str


@app.get("/")
def root() -> Dict[str, Any]:
    return {
        "service": "Política de la Felicidad - MLOps Recommender",
        "status": "running",
        "environment": APP_ENV
    }


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "environment": APP_ENV,
        "model_ready": recommender.model_ready,
        "model_type": "onnx" if recommender.model_ready else "fallback-local"
    }


@app.post("/predict")
def predict(request: PredictionRequest) -> Dict[str, Any]:
    result = recommender.predict(request.text)

    result["environment"] = APP_ENV

    write_prediction_log(result)

    return result


@app.post("/predict-dev")
def predict_dev(request: PredictionRequest) -> Dict[str, Any]:
    return predict(request)


@app.post("/predict-prod")
def predict_prod(request: PredictionRequest) -> Dict[str, Any]:
    return predict(request)
