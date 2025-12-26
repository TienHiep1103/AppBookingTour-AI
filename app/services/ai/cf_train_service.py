# app/services/cf_train_service.py
import pandas as pd
from sqlalchemy.orm import Session
from app.models.ai.mf_trainer import MatrixFactorization
from app.models.user_favourite import UserFavourite
from app.enums import ItemType

MODEL_PATH = "app/models/ai/saved"

def train_cf_models(db: Session):
    user_favourites = db.query(UserFavourite).all()
    
    rows = [
        (uf.user_id, uf.item_id, uf.item_type, float(uf.rating) if uf.rating is not None else 0.0)
        for uf in user_favourites
    ]

    df = pd.DataFrame(rows, columns=["userId", "itemId", "itemType", "rating"])

    for item_type, file_name in {
        ItemType.TOUR: "cf_tour.pkl",
        ItemType.ACCOMMODATION: "cf_accommodation.pkl",
        ItemType.COMBO: "cf_combo.pkl"
    }.items():

        sub_df = df[df["itemType"] == item_type][["userId", "itemId", "rating"]]
        if sub_df.empty:
            continue

        user2idx = {u: i for i, u in enumerate(sub_df.userId.unique())}
        item2idx = {i: j for j, i in enumerate(sub_df.itemId.unique())}

        ratings = [
            (user2idx[u], item2idx[i], r)
            for u, i, r in sub_df.itertuples(index=False)
        ]

        mf = MatrixFactorization(
            n_users=len(user2idx),
            n_items=len(item2idx)
        )
        mf.train(ratings)
        mf.save(f"{MODEL_PATH}/{file_name}", user2idx, item2idx)
