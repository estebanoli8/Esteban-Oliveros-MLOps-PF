import json
from datetime import datetime, timezone
from typing import Dict, Any

from google.cloud import storage

from app.settings import GCP_BUCKET, get_prediction_log_path


def write_prediction_log(payload: Dict[str, Any]) -> None:
    """
    Guarda cada predicción como una línea JSON dentro del archivo TXT del ambiente.
    Para el demo se usa lectura + escritura del archivo completo.
    Esto es suficiente para baja concurrencia académica.
    """

    if not GCP_BUCKET:
        return

    client = storage.Client()
    bucket = client.bucket(GCP_BUCKET)

    log_path = get_prediction_log_path()
    blob = bucket.blob(log_path)

    line = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        **payload
    }

    new_line = json.dumps(line, ensure_ascii=False)

    try:
        current_text = blob.download_as_text()
    except Exception:
        current_text = ""

    updated_text = current_text + new_line + "\n"

    blob.upload_from_string(
        updated_text,
        content_type="text/plain; charset=utf-8"
    )
