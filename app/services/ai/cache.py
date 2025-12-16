# services/ai/cache.py

feature_cache = {}

def get_features(item_type: str):
    return feature_cache.get(item_type)

def clear_features(item_type: str):
    feature_cache.pop(item_type, None)
