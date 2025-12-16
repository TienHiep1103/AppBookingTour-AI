from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse import hstack
import numpy as np
from app.utils import vietnamese_tokenizer, VIETNAMESE_STOPWORDS as VI_STOPWORDS

# Cache feature theo city_id, chỉ rebuild khi dữ liệu thay đổi.

_feature_cache = {}

def build_city_features(city_id: int, accommodations: list):
    texts = [f"{a.name or ''} {a.description or ''}" for a in accommodations]

    tfidf = TfidfVectorizer(
        tokenizer=vietnamese_tokenizer,
        stop_words=VI_STOPWORDS,
        max_features=500,
        ngram_range=(1, 2)
    )

    text_vec = tfidf.fit_transform(texts)

    numeric = np.array([
        [a.star_rating or 0, a.rating or 0, a.num_of_rooms or 0, a.avg_price or 0]
        for a in accommodations
    ])

    scaler = MinMaxScaler()
    numeric_vec = scaler.fit_transform(numeric)

    final_vec = hstack([text_vec * 0.5, numeric_vec * 0.5]).tocsr()

    _feature_cache[city_id] = {
        "vectors": final_vec,
        "ids": [...],
        "tfidf": tfidf,
        "scaler": scaler
    }

def get_city_features(city_id: int):
    return _feature_cache.get(city_id)

def clear_city_features(city_id: int):
    _feature_cache.pop(city_id, None)

def build_tour_features(tours: list):
    texts = [f"{t.name or ''} {t.description or ''}"for t in tours]

    tfidf = TfidfVectorizer(
        tokenizer=vietnamese_tokenizer,
        stop_words=VI_STOPWORDS,
        max_features=500,
        ngram_range=(1, 2)
    )

    text_vec = tfidf.fit_transform(texts)

    numeric = np.array([
        [
            t.duration_nights or 0,
            t.duration_days or 0,
            np.log1p(t.base_price_adult or 0),
            np.log1p(t.base_price_child or 0)
        ]
        for t in tours
    ])

    scaler = MinMaxScaler()
    numeric_vec = scaler.fit_transform(numeric)

    final_vec = hstack([
        text_vec * 0.6,
        numeric_vec * 0.4
    ]).tocsr()

    _feature_cache["tour"] = {
        "vectors": final_vec,
        "ids": [t.id for t in tours],
        "tfidf": tfidf,
        "scaler": scaler
    }