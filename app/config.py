import os
import torch

MODEL_NAME = os.getenv("MODEL_NAME", "5CD-AI/Vietnamese-Sentiment-visobert")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_NEW_TOKENS = 100
