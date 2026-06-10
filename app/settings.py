import os


APP_ENV = os.getenv("APP_ENV", "local")

GCP_BUCKET = os.getenv("GCP_BUCKET", "")
MODEL_PREFIX = os.getenv("MODEL_PREFIX", "models/minilm")
LOCAL_MODEL_DIR = os.getenv("LOCAL_MODEL_DIR", "/tmp/mlops-pf-model")

PREDICTIONS_DEV_FILE = "logs/predicciones_dev.txt"
PREDICTIONS_PROD_FILE = "logs/predicciones_prod.txt"


def get_prediction_log_path() -> str:
    if APP_ENV == "prod":
        return PREDICTIONS_PROD_FILE

    return PREDICTIONS_DEV_FILE
