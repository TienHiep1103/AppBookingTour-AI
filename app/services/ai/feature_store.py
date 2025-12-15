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
        "ids": [a.id for a in accommodations]
    }

def get_city_features(city_id: int):
    return _feature_cache.get(city_id)

def clear_city_features(city_id: int):
    _feature_cache.pop(city_id, None)
