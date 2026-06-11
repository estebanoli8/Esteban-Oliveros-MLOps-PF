import os
from pathlib import Path

from google.cloud import storage


GCP_BUCKET = os.getenv("GCP_BUCKET", "")
MODEL_PREFIX = os.getenv("MODEL_PREFIX", "models/minilm")
LOCAL_MODEL_DIR = Path(os.getenv("LOCAL_MODEL_DIR", "runtime_artifacts/minilm"))

TEST_DATA_OBJECT = os.getenv(
    "TEST_DATA_OBJECT",
    "test_data/test_messages.json"
)

LOCAL_TEST_DATA = Path(
    os.getenv(
        "LOCAL_TEST_DATA",
        "runtime_artifacts/test_messages.json"
    )
)


def download_blob(bucket_name: str, source_blob_name: str, destination_path: Path) -> None:
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    print(f"Descargando gs://{bucket_name}/{source_blob_name}")
    print(f"Destino local: {destination_path}")

    blob.download_to_filename(destination_path)


def download_model_files() -> None:
    model_files = [
        "config.json",
        "model.onnx",
        "special_tokens_map.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "vocab.txt",
    ]

    for file_name in model_files:
        source_blob = f"{MODEL_PREFIX}/{file_name}"
        destination = LOCAL_MODEL_DIR / file_name

        download_blob(GCP_BUCKET, source_blob, destination)


def download_test_data() -> None:
    download_blob(
        GCP_BUCKET,
        TEST_DATA_OBJECT,
        LOCAL_TEST_DATA
    )


def main() -> None:
    if not GCP_BUCKET:
        raise ValueError("La variable de entorno GCP_BUCKET no está configurada.")

    download_model_files()
    download_test_data()

    print("Artefactos descargados correctamente.")


if __name__ == "__main__":
    main()
