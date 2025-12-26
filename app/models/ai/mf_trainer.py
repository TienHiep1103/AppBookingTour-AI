# app/models/ai/mf_trainer.py
import numpy as np
import pickle

class MatrixFactorization:
    def __init__(self, n_users, n_items, k=20, lr=0.01, reg=0.01):
        self.k = k
        self.lr = lr
        self.reg = reg
        self.P = np.random.normal(0, .1, (n_users, k))
        self.Q = np.random.normal(0, .1, (n_items, k))

    def train(self, ratings, epochs=20):
        for _ in range(epochs):
            for u, i, r in ratings:
                pred = np.dot(self.P[u], self.Q[i])
                err = r - pred

                self.P[u] += self.lr * (err * self.Q[i] - self.reg * self.P[u])
                self.Q[i] += self.lr * (err * self.P[u] - self.reg * self.Q[i])

    def save(self, path, user2idx, item2idx):
        with open(path, "wb") as f:
            pickle.dump({
                "P": self.P,
                "Q": self.Q,
                "user2idx": user2idx,
                "item2idx": item2idx
            }, f)
