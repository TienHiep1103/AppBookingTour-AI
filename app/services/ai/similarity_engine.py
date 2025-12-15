from sklearn.metrics.pairwise import cosine_similarity

def top_k_similar(vectors, item_index: int, top_k: int):
    scores = cosine_similarity(
        vectors[item_index],
        vectors
    ).flatten()

    indices = scores.argsort()[::-1]
    return indices[1: top_k + 1]
