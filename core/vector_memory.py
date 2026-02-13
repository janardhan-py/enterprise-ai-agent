import json
import os
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


VECTOR_DB_PATH = "data/vector_memory.json"


class VectorMemory:
    """
    Lightweight semantic memory store.
    Local-only storage (GDPR-safe).
    """

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        os.makedirs("data", exist_ok=True)

    def _load_db(self):
        if not os.path.exists(VECTOR_DB_PATH):
            return []

        with open(VECTOR_DB_PATH, "r") as f:
            return json.load(f)

    def _save_db(self, data):
        with open(VECTOR_DB_PATH, "w") as f:
            json.dump(data, f)

    def store(self, text: str):
        if not text:
            return

        db = self._load_db()
        embedding = self.model.encode(text).tolist()

        db.append({
            "text": text,
            "embedding": embedding
        })

        self._save_db(db)

    def retrieve(self, query: str, top_k: int = 1) -> List[str]:
        db = self._load_db()
        if not db:
            return []

        query_embedding = self.model.encode(query).reshape(1, -1)

        similarities = []
        for item in db:
            emb = np.array(item["embedding"]).reshape(1, -1)
            score = cosine_similarity(query_embedding, emb)[0][0]
            similarities.append((score, item["text"]))

        similarities.sort(reverse=True, key=lambda x: x[0])
        return [text for _, text in similarities[:top_k]]
