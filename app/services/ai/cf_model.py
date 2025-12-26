# app/services/cf_model.py
import pickle
import numpy as np
from app.enums import ItemType

MODEL_FILES = {
    ItemType.TOUR: "app/models/ai/saved/cf_tour.pkl",
    ItemType.ACCOMMODATION: "app/models/ai/saved/cf_accommodation.pkl",
    ItemType.COMBO: "app/models/ai/saved/cf_combo.pkl",
}

class CFModel:
    def __init__(self, item_type: int):
        with open(MODEL_FILES[item_type], "rb") as f:
            data = pickle.load(f)

        self.P = data["P"]
        self.Q = data["Q"]
        self.user2idx = data["user2idx"]
        self.item2idx = data["item2idx"]
        self.idx2item = {v: k for k, v in self.item2idx.items()}

    def recommend(self, user_id: int, top_n=5):
        if user_id not in self.user2idx:
            return []

        u_idx = self.user2idx[user_id]
        scores = self.P[u_idx] @ self.Q.T
        top_idx = scores.argsort()[::-1][:top_n]

        return [
            {"item_id": self.idx2item[i], "score": float(scores[i])}
            for i in top_idx
        ]
