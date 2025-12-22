# from requests import Session
# from app.utils import vietnamese_tokenizer, VIETNAMESE_STOPWORDS as VI_STOPWORDS
# from ..models.ai_model import ai_model
# from .accommodation_service import get_accommodations_by_city_id, get_accommodations_other_by_city_id
# from ..models.accommodation import Accommodation
# from app import db
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.metrics.pairwise import cosine_similarity
# from scipy.sparse import hstack
# import numpy as np

# def predictComment(comment: str) -> int:
#     return ai_model.classify(comment)