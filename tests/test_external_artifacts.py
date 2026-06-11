import json
import os
from pathlib import Path


def test_external_test_data_file_exists():
    path = Path(
        os.getenv(
            "LOCAL_TEST_DATA",
            "runtime_artifacts/test_messages.json"
        )
    )

    assert path.exists(), "No se encontró el archivo externo de datos de prueba."

    data = json.loads(path.read_text(encoding="utf-8"))

    assert isinstance(data, list)
    assert len(data) >= 3

    first_item = data[0]

    assert "text" in first_item
    assert "expected_category" in first_item


def test_external_model_file_exists():
    model_dir = Path(
        os.getenv(
            "LOCAL_MODEL_DIR",
            "runtime_artifacts/minilm"
        )
    )

    model_path = model_dir / "model.onnx"

    assert model_path.exists(), "No se encontró el modelo ONNX externo."

    assert model_path.stat().st_size > 1_000_000
