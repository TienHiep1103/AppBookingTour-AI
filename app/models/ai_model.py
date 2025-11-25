import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig
from app.config import MODEL_NAME, DEVICE

# Mapping cho model 5CD-AI: 0-Negative, 1-Positive, 2-Neutral (nhãn gốc của model)
LABEL_MAP = {"NEG": 0, "POS": 1, "NEU": 2}

class AIModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.config = AutoConfig.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to(DEVICE)
        self.model.eval()

    def classify(self, comment: str) -> int:
        inputs = self.tokenizer(comment, return_tensors='pt', truncation=True, max_length=256).to(DEVICE)
        with torch.no_grad():
            out = self.model(**inputs)
            scores = torch.softmax(out.logits, dim=1)[0]
            label_id = scores.argmax().item()
            # Chuẩn hóa trả ra 0 (NEG), 1 (POS), 2 (NEU)
            label = self.config.id2label[label_id]
            return LABEL_MAP[label]

ai_model = AIModel()
