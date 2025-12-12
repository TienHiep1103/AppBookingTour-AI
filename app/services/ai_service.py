from ..models.ai_model import ai_model

def predictComment(comment: str) -> int:
    return ai_model.classify(comment)
