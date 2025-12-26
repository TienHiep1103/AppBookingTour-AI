from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import numpy as np

def top_k_similar(vectors, item_index: int, top_k: int = 5):
    vectors = normalize(vectors)

    scores = cosine_similarity(
        vectors[item_index],
        vectors
    ).flatten()

    # loại chính nó
    scores[item_index] = -1

    # sắp xếp giảm dần
    sorted_idx = np.argsort(scores)[::-1]

    results = [
        (i, scores[i]) for i in sorted_idx if scores[i] > 0
    ]

    return results[:top_k]