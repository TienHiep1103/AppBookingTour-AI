from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from ...utils import vietnamese_tokenizer, VIETNAMESE_STOPWORDS as VI_STOPWORDS

# Cache feature theo city_id, chỉ rebuild khi dữ liệu thay đổi.

_feature_cache = {}

def build_city_features(city_id: int, accommodations: list):
    texts = [
        f"{a.name or ''} {a.description or ''}"
        for a in accommodations
    ]

    tfidf = TfidfVectorizer(
        tokenizer=vietnamese_tokenizer,
        stop_words=VI_STOPWORDS,
        max_features=500,
        ngram_range=(1, 2)
    )

    text_vec = tfidf.fit_transform(texts)
    
    _feature_cache[city_id] = {
        "vectors": text_vec,
        "ids": [a.id for a in accommodations],
        "tfidf": tfidf
    }

def get_city_features(city_id: int):
    return _feature_cache.get(city_id)

def clear_city_features(city_id: int):
    _feature_cache.pop(city_id, None)

def build_tour_features(tours: list):
    texts = [
        f"{t.name or ''} {t.description or ''} "
        for t in tours
    ]

    tfidf = TfidfVectorizer(
        tokenizer=vietnamese_tokenizer,
        stop_words=VI_STOPWORDS,
        max_features=500,
        ngram_range=(1, 2)
    )

    text_vec = tfidf.fit_transform(texts)
    
    _feature_cache["tour"] = {
        "vectors": text_vec,
        "ids": [t.id for t in tours],
        "tfidf": tfidf
    }
    
def get_tour_features():
    return _feature_cache.get("tour")

def build_combo_features(combos: list):
    texts = [
        f"{c.name or ''} {c.short_description or ''}"
        for c in combos
    ]

    tfidf = TfidfVectorizer(
        tokenizer=vietnamese_tokenizer,
        stop_words=VI_STOPWORDS,
        max_features=500,
        ngram_range=(1, 2)
    )

    text_vec = tfidf.fit_transform(texts)

    _feature_cache["combo"] = {
        "vectors": text_vec,
        "ids": [c.id for c in combos],
        "tfidf": tfidf
    }

def get_combo_features():
    return _feature_cache.get("combo")