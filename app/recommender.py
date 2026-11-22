import joblib
import numpy as np
import pandas as pd

from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "movie_recommender_artifacts.joblib"


# Load trained artifacts
artifacts = joblib.load(MODEL_PATH)

movies = artifacts["movies"]
genre_features = artifacts["genre_features"]

user_movie_matrix = artifacts["user_movie_matrix"]
user_means = artifacts["user_means"]

weighted_deviations = artifacts["weighted_deviations"]
similarity_weights = artifacts["similarity_weights"]

best_alpha = artifacts["best_alpha"]


def recommend_movies(user_id, top_n=10):

    if user_id not in user_movie_matrix.index:
        raise ValueError("User ID not found.")

    user_ratings = user_movie_matrix.loc[user_id]

    liked_movie_ids = user_ratings[
        user_ratings >= 4
    ].dropna().index

    if len(liked_movie_ids) == 0:
        return pd.DataFrame()

    available_movies = genre_features.index.intersection(
        liked_movie_ids
    )

    if len(available_movies) == 0:
        return pd.DataFrame()

    user_profile = genre_features.loc[
        available_movies
    ].mean(axis=0)

    content_scores = cosine_similarity(
        user_profile.values.reshape(1, -1),
        genre_features
    )[0]

    content_scores = pd.Series(
        content_scores,
        index=genre_features.index
    )

    user_index = user_movie_matrix.index.get_loc(user_id)

    numerator = weighted_deviations.getrow(
        user_index
    ).toarray().ravel()

    denominator = similarity_weights.getrow(
        user_index
    ).toarray().ravel()

    valid_mask = denominator > 0

    predicted_ratings = np.full(
        len(user_movie_matrix.columns),
        np.nan
    )

    predicted_ratings[valid_mask] = (
        user_means.loc[user_id]
        + numerator[valid_mask] / denominator[valid_mask]
    )

    predicted_ratings = np.clip(
        predicted_ratings,
        1,
        5
    )

    collaborative_scores = pd.Series(
        predicted_ratings,
        index=user_movie_matrix.columns
    )

    collaborative_scores = (
        (collaborative_scores - 1) / 4
    )

    common_ids = content_scores.index.intersection(
        collaborative_scores.dropna().index
    )

    results = pd.DataFrame({
        "MovieID": common_ids,
        "ContentScore": content_scores.loc[common_ids].values,
        "CollaborativeScore": collaborative_scores.loc[common_ids].values
    })

    results["HybridScore"] = (
        best_alpha * results["ContentScore"]
        + (1 - best_alpha) * results["CollaborativeScore"]
    )

    watched_movie_ids = set(
        user_ratings.dropna().index
    )

    results = results[
        ~results["MovieID"].isin(watched_movie_ids)
    ]

    results = results.merge(
        movies[["MovieID", "Title", "Genres"]],
        on="MovieID",
        how="left"
    )

    return results.sort_values(
        "HybridScore",
        ascending=False
    ).head(top_n).reset_index(drop=True)