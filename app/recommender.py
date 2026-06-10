import os
import re
from typing import Dict, Any, List, Tuple

import numpy as np

from app.categories import CATEGORIES
from app.settings import LOCAL_MODEL_DIR


class Recommender:
    def __init__(self) -> None:
        self.use_fake_model = os.getenv("USE_FAKE_MODEL", "false").lower() == "true"
        self.model_ready = False

        self.tokenizer = None
        self.session = None

        if not self.use_fake_model:
            self._try_load_onnx_model()

    def _try_load_onnx_model(self) -> None:
        try:
            import onnxruntime as ort
            from transformers import AutoTokenizer

            model_path = os.path.join(LOCAL_MODEL_DIR, "model.onnx")

            if not os.path.exists(model_path):
                self.model_ready = False
                return

            self.tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_DIR)
            self.session = ort.InferenceSession(model_path)
            self.model_ready = True

        except Exception:
            self.model_ready = False

    def _normalize_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-záéíóúñü0-9 ]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _fake_embedding(self, text: str) -> np.ndarray:
        """
        Embedding simple para pruebas locales.
        No reemplaza al modelo ONNX de producción.
        """

        text = self._normalize_text(text)
        tokens = text.split()

        vocabulary = [
            "ayudar", "voluntario", "comunidad", "obra", "contrato",
            "corrupción", "escuela", "liderazgo", "comunicación",
            "redes", "estado", "secop", "equipo", "campaña",
            "servicios", "propuesta", "valor", "ciudadana"
        ]

        vector = np.zeros(len(vocabulary), dtype=np.float32)

        for i, word in enumerate(vocabulary):
            if word in tokens or word in text:
                vector[i] = 1.0

        norm = np.linalg.norm(vector)

        if norm == 0:
            return vector

        return vector / norm

    def _onnx_embedding(self, text: str) -> np.ndarray:
        encoded = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="np"
        )

        model_inputs = {
            "input_ids": encoded["input_ids"],
            "attention_mask": encoded["attention_mask"]
        }

        if "token_type_ids" in encoded:
            model_inputs["token_type_ids"] = encoded["token_type_ids"]

        outputs = self.session.run(None, model_inputs)

        token_embeddings = outputs[0]
        attention_mask = encoded["attention_mask"]

        expanded_mask = np.expand_dims(attention_mask, axis=-1)
        masked_embeddings = token_embeddings * expanded_mask

        summed = masked_embeddings.sum(axis=1)
        counts = np.clip(expanded_mask.sum(axis=1), a_min=1e-9, a_max=None)

        sentence_embedding = summed / counts
        sentence_embedding = sentence_embedding[0]

        norm = np.linalg.norm(sentence_embedding)

        if norm == 0:
            return sentence_embedding

        return sentence_embedding / norm

    def embed(self, text: str) -> np.ndarray:
        if self.model_ready:
            return self._onnx_embedding(text)

        return self._fake_embedding(text)

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        denominator = np.linalg.norm(a) * np.linalg.norm(b)

        if denominator == 0:
            return 0.0

        return float(np.dot(a, b) / denominator)

    def predict(self, text: str) -> Dict[str, Any]:
        input_embedding = self.embed(text)

        results: List[Tuple[str, float]] = []

        for category_name, category_info in CATEGORIES.items():
            reference_scores = []

            for reference_text in category_info["reference_texts"]:
                reference_embedding = self.embed(reference_text)
                score = self.cosine_similarity(input_embedding, reference_embedding)
                reference_scores.append(score)

            category_score = max(reference_scores)
            results.append((category_name, category_score))

        results.sort(key=lambda item: item[1], reverse=True)

        best_category, best_score = results[0]
        category_info = CATEGORIES[best_category]

        return {
            "input_text": text,
            "category": best_category,
            "score": round(best_score, 4),
            "recommendation": category_info["recommendation"],
            "route": category_info["route"],
            "model_type": "onnx" if self.model_ready else "fallback-local",
            "top_categories": [
                {
                    "category": category,
                    "score": round(score, 4)
                }
                for category, score in results[:3]
            ]
        }
