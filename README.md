# Movie Recommendation System

A hybrid movie recommendation system built using **Content-Based Filtering** and **User-Based Collaborative Filtering**. The project uses the MovieLens 1M dataset and combines both recommendation approaches to generate personalized movie suggestions through an interactive Streamlit application.

## Project Overview

The system recommends movies based on two sources of information:

- **Content-Based Filtering:** Identifies movies with similar genres to those a user has previously rated positively.
- **Collaborative Filtering:** Identifies users with similar rating patterns and uses their preferences to suggest movies.

A hybrid recommendation approach combines both methods using a weighted scoring formula.

## Key Features

- Movie recommendations personalized by user ID
- Content-based movie similarity using cosine similarity
- User-based collaborative filtering
- Hybrid recommendation scoring
- Adjustable content and collaborative filtering weights during experimentation
- Movie discovery through search and genre filters
- Movie details and poster information through TMDB integration
- Interactive Streamlit interface
- Model evaluation using ranking and rating-prediction metrics

## Dataset

**MovieLens 1M Dataset** by GroupLens Research.

Dataset: https://grouplens.org/datasets/movielens/1m/

The dataset contains approximately:

- 1 million movie ratings
- 6,040 users
- 3,900 movies

Files include movie information, user ratings, and demographic information.

The dataset is not included in this repository. Download MovieLens 1M and extract its files into the project's `data/` directory before running the notebooks.

## Recommendation Methodology

### 1. Content-Based Filtering

Movie genres are transformed into multi-hot encoded feature vectors. Cosine similarity measures how closely movies match one another.

### 2. User-Based Collaborative Filtering

A user-item rating matrix represents interactions between users and movies. Ratings are mean-centered, and cosine similarity identifies users with similar preferences. Recommendations are generated using similarity-weighted rating deviations.

### 3. Hybrid Recommendation

The two recommendation scores are combined:

\[
HybridScore = \alpha(ContentScore) + (1-\alpha)(CollaborativeScore)
\]

The selected hybrid weight is **α = 0.7**, based on the project's model-comparison experiment.

## Model Evaluation

The project evaluates recommendation quality using:

- Precision@10
- Recall@10
- RMSE
- MAE

Content-Based, Collaborative, and Hybrid recommendation approaches are compared using a shared candidate movie catalogue for ranking evaluation.

## Technology Stack

- Python
- Pandas and NumPy
- SciPy
- Scikit-learn
- Matplotlib and Seaborn
- Plotly
- Streamlit
- Joblib
- TMDB API

## Project Structure

```text
MovieRecommendationSystem/
│
├── app/
│   ├── main.py
│   └── recommender.py
│
├── data/
│   └── (download MovieLens 1M here)
│
├── models/
│   └── movie_recommender_artifacts.joblib
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_data_preprocessing.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_content_based_recommender.ipynb
│   ├── 06_collaborative_filtering.ipynb
│   ├── 07_model_evaluation.ipynb
│   ├── 08_hybrid_recommender.ipynb
│   ├── 09_hybrid_model_evaluation.ipynb
│   └── 10_model_preparation.ipynb
│
├── reports/
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd MovieRecommendationSystem
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure TMDB API

Create `.streamlit/secrets.toml` and add your TMDB API key:

```toml
TMDB_API_KEY = "YOUR_TMDB_API_KEY"
```

Keep this file private. Never commit your API key to GitHub.

### 5. Run the application

```bash
streamlit run app/main.py
```

## Limitations

- Movie recommendations are based on the MovieLens 1M dataset and its available movie genres and ratings.
- New users without rating history may not receive personalized recommendations.
- The dataset is relatively old and does not represent current movie popularity.
- Movie posters and additional movie metadata depend on the availability of TMDB information.

## Future Improvements

- Incorporate richer movie metadata.
- Improve recommendations