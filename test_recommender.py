from app.recommender import recommend_movies, best_alpha

print("Selected hybrid alpha:", best_alpha)

recommendations = recommend_movies(
    user_id=1,
    top_n=10
)

print("\nRecommendations for User 1:")
print(
    recommendations[
        ["Title", "ContentScore", "CollaborativeScore", "HybridScore"]
    ].to_string(index=False)
)