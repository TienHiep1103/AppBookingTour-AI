from requests import Session
from app.utils import vietnamese_tokenizer, VIETNAMESE_STOPWORDS as VI_STOPWORDS
from ..models.ai_model import ai_model
from .accommodation_service import get_accommodations_by_city_id, get_accommodations_other_by_city_id
from ..models.accommodation import Accommodation
from app import db
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack
import numpy as np

def predictComment(comment: str) -> int:
    return ai_model.classify(comment)

# def recommend_accommodations(db: Session, item_id: int, top_k: int) -> list[int]:
#     accommodation =  db.query(Accommodation).filter(Accommodation.id == item_id).first()
#     if not accommodation:
#         return []
#     city_id = accommodation.city_id
#     accommodation_same_city = get_accommodations_by_city_id(db, city_id)
#     accommodation_other_city = get_accommodations_other_by_city_id(db, city_id)
#     recommendations = []
#     if len(accommodation_same_city) > top_k:
#         recommendations = accommodation_same_city
#     else:
#         recommendations = accommodation_same_city + accommodation_other_city
#     similarity_matrix = build_similarity_matrix(recommendations)
#     if similarity_matrix is None:
#         return []
#     # Find index by comparing IDs since recommendations are AccommodationResponse objects
#     item_index = next((i for i, acc in enumerate(recommendations) if acc.id == item_id), None)
#     if item_index is None:
#         return []
#     similarity_scores = similarity_matrix[item_index]
#     similar_indices = np.argsort(-similarity_scores)
#     recommended_ids = []
#     for idx in similar_indices:
#         if recommendations[idx].id != item_id:
#             recommended_ids.append(recommendations[idx].id)
#         if len(recommended_ids) >= top_k:
#             break
#     return recommended_ids    
        
# Caculate similarity scores
# def build_similarity_matrix(accommodations: list[Accommodation]):
#     if len(accommodations) < 2:
#         return None
#     # 1. TEXT VECTOR (TF-IDF)
#     texts = [f"{acc.name or ''} {acc.description or ''}"for acc in accommodations]

#     tfidf = TfidfVectorizer(
#         tokenizer=vietnamese_tokenizer,
#         stop_words=VI_STOPWORDS,
#         max_features=500,
#         ngram_range=(1, 2)
#     )

#     text_vectors = tfidf.fit_transform(texts)  # (N, T)

#     # 2. NUMERIC VECTOR
#     numeric_data = np.array([
#         [acc.star_rating or 0, acc.rating or 0, acc.num_of_rooms or 0, acc.avg_price or 0]
#         for acc in accommodations
#     ])

#     scaler = MinMaxScaler()
#     numeric_vectors = scaler.fit_transform(numeric_data)  # (N, K)

#     # 3. WEIGHTS
#     TEXT_WEIGHT = 0.5
#     NUMERIC_WEIGHT = 0.5

#     # 4. FINAL VECTOR
#     final_vectors = hstack([text_vectors * TEXT_WEIGHT, numeric_vectors * NUMERIC_WEIGHT])  # (N, T+K)
    
#     # 5. COSINE SIMILARITY
#     similarity_matrix = cosine_similarity(final_vectors)

#     return similarity_matrix
