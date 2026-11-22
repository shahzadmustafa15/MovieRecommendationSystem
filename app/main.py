import streamlit as st
import pandas as pd
import requests
import re
import html

from recommender import (
    recommend_movies,
    user_movie_matrix,
    movies,
    best_alpha
)


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MovieMind | Discover Movies",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 2. TMDB CONFIGURATION
# ============================================================

try:
    TMDB_API_KEY = st.secrets.get("TMDB_API_KEY", "")
except Exception:
    TMDB_API_KEY = ""

TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/"
TMDB_POSTER_SIZE = "w500"
TMDB_BACKDROP_SIZE = "w1280"


# ============================================================
# 3. GLOBAL STYLING
# ============================================================

st.html("""
<style>

.stApp {
    background: #141414;
    color: #FFFFFF;
}

.block-container {
    max-width: 1600px;
    padding: 1.5rem 3.5rem 3rem 3.5rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu,
footer {
    visibility: hidden;
}

h1, h2, h3, h4 {
    color: #FFFFFF !important;
}

p {
    color: #D0D0D0;
}

hr {
    border-color: #303030;
}

/* NAVIGATION */

.brand {
    font-size: 30px;
    font-weight: 950;
    letter-spacing: -1.5px;
    color: #FFFFFF;
}

.brand-red {
    color: #E50914;
}

.brand-subtitle {
    font-size: 10px;
    color: #888888;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: -4px;
}

.nav-caption {
    font-size: 11px;
    color: #888888;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

/* HERO */

.hero-container {
    position: relative;
    width: 100%;
    min-height: 440px;
    border-radius: 13px;
    overflow: hidden;
    margin-top: 22px;
    margin-bottom: 35px;
    background-color: #252525;
    background-position: center 25%;
    background-size: cover;
    display: flex;
    align-items: flex-end;
    box-shadow: 0 12px 35px rgba(0,0,0,0.35);
}

.hero-overlay {
    position: absolute;
    inset: 0;
    background:
        linear-gradient(
            90deg,
            rgba(0,0,0,0.94) 0%,
            rgba(0,0,0,0.70) 42%,
            rgba(0,0,0,0.08) 100%
        ),
        linear-gradient(
            0deg,
            rgba(20,20,20,1) 0%,
            rgba(20,20,20,0.1) 65%,
            rgba(20,20,20,0.05) 100%
        );
}

.hero-content {
    position: relative;
    z-index: 2;
    padding: 45px;
    max-width: 650px;
}

.hero-eyebrow {
    display: inline-block;
    color: #FFFFFF;
    background: #E50914;
    font-size: 10px;
    font-weight: 850;
    letter-spacing: 1.5px;
    padding: 7px 11px;
    border-radius: 3px;
    margin-bottom: 17px;
}

.hero-title {
    font-size: clamp(30px, 4vw, 54px);
    font-weight: 950;
    line-height: 1.08;
    letter-spacing: -1.5px;
    color: #FFFFFF;
    margin-bottom: 15px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.5);
}

.hero-description {
    color: #D5D5D5;
    font-size: 14px;
    line-height: 1.75;
    max-width: 550px;
    margin-bottom: 18px;
}

.hero-meta {
    color: #D0D0D0;
    font-size: 12px;
    margin-top: 15px;
    letter-spacing: 0.5px;
}

.hero-score {
    color: #46D369;
    font-weight: 850;
}

/* SECTION HEADINGS */

.section-heading {
    font-size: 22px;
    font-weight: 850;
    letter-spacing: -0.4px;
    color: #FFFFFF;
    margin-top: 25px;
    margin-bottom: 4px;
}

.section-subheading {
    color: #929292;
    font-size: 12px;
    margin-bottom: 17px;
}

.section-accent {
    color: #E50914;
}

/* MOVIE CARDS */

.movie-card {
    position: relative;
    background: #1E1E1E;
    border: 1px solid #292929;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 5px;
    transition:
        transform 0.28s ease,
        box-shadow 0.28s ease,
        border-color 0.28s ease;
}

.movie-card:hover {
    transform: translateY(-7px) scale(1.025);
    border-color: #E50914;
    box-shadow: 0 14px 28px rgba(0,0,0,0.55);
    z-index: 5;
}

.movie-poster {
    width: 100%;
    height: 280px;
    object-fit: cover;
    object-position: center;
    display: block;
    background: #303030;
    transition: transform 0.35s ease;
}

.movie-card:hover .movie-poster {
    transform: scale(1.035);
}

.poster-placeholder {
    height: 280px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, #303030, #151515);
    font-size: 42px;
}

.movie-card-content {
    padding: 12px 12px 14px 12px;
}

.movie-title {
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 800;
    line-height: 1.45;
    min-height: 37px;
    margin-bottom: 5px;
}

.movie-genres {
    color: #969696;
    font-size: 10px;
    line-height: 1.5;
    min-height: 29px;
}

.movie-rating {
    color: #46D369;
    font-size: 11px;
    font-weight: 800;
    margin-top: 9px;
}

.movie-score {
    color: #E50914;
    font-size: 11px;
    font-weight: 800;
    margin-top: 5px;
}

.movie-rank {
    position: absolute;
    top: 9px;
    left: 9px;
    background: rgba(15,15,15,0.88);
    color: #FFFFFF;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 5px 8px;
    font-size: 10px;
    font-weight: 850;
    z-index: 2;
}

/* BUTTONS */

.stButton > button {
    background: #E50914;
    color: #FFFFFF;
    border: 1px solid #E50914;
    border-radius: 5px;
    font-size: 12px;
    font-weight: 800;
    min-height: 38px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #B20710;
    color: #FFFFFF;
    border-color: #B20710;
    transform: translateY(-1px);
}

.stButton > button:focus {
    color: #FFFFFF;
    border-color: #E50914;
    box-shadow: 0 0 0 2px rgba(229,9,20,0.25);
}

/* NAVIGATION RADIO */

div[role="radiogroup"] {
    gap: 8px;
}

div[role="radiogroup"] label {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 5px;
    padding: 6px 12px;
    transition: 0.2s ease;
}

div[role="radiogroup"] label:hover {
    background: #252525;
}

div[role="radiogroup"] label p {
    color: #C5C5C5;
    font-size: 12px;
    font-weight: 700;
}

div[role="radiogroup"] label:has(input:checked) {
    background: #292929;
    border-bottom: 2px solid #E50914;
}

div[role="radiogroup"] label:has(input:checked) p {
    color: #FFFFFF;
}

/* INPUTS */

[data-baseweb="select"] > div,
[data-baseweb="input"] > div {
    background: #202020;
    border-color: #383838;
    border-radius: 5px;
}

[data-baseweb="select"] *,
[data-baseweb="input"] input {
    color: #FFFFFF !important;
}

[data-testid="stTextInput"] input {
    background: #202020;
    color: #FFFFFF;
    border-color: #383838;
}

[data-testid="stSelectbox"] label,
[data-testid="stTextInput"] label {
    color: #AFAFAF;
    font-size: 11px;
}

/* METRICS */

[data-testid="stMetric"] {
    background: #202020;
    border: 1px solid #303030;
    padding: 13px 17px;
    border-radius: 7px;
}

[data-testid="stMetricLabel"] {
    color: #A0A0A0 !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

/* DETAIL PANEL */

.detail-panel {
    background: #202020;
    border: 1px solid #353535;
    border-radius: 10px;
    padding: 22px;
    margin-top: 15px;
    margin-bottom: 25px;
}

.detail-title {
    color: #FFFFFF;
    font-size: 30px;
    font-weight: 900;
    line-height: 1.2;
    margin-bottom: 12px;
}

.detail-overview {
    color: #C1C1C1;
    font-size: 13px;
    line-height: 1.8;
}

.detail-label {
    color: #858585;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.detail-value {
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 700;
    margin-top: 4px;
}

/* EMPTY STATES / FOOTER */

.empty-state {
    background: #202020;
    border: 1px dashed #414141;
    border-radius: 9px;
    padding: 35px;
    text-align: center;
    color: #A0A0A0;
}

.footer {
    border-top: 1px solid #303030;
    margin-top: 55px;
    padding-top: 22px;
    text-align: center;
    color: #777777;
    font-size: 11px;
    line-height: 1.8;
}

.tmdb-note {
    color: #858585;
    font-size: 10px;
    text-align: center;
    margin-top: 10px;
}

/* ANIMATIONS */

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.hero-container,
.movie-card,
.detail-panel {
    animation: fadeIn 0.45s ease both;
}

/* RESPONSIVE */

@media (max-width: 900px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero-container {
        min-height: 360px;
    }

    .hero-content {
        padding: 25px;
    }

    .hero-title {
        font-size: 32px;
    }

    .movie-poster,
    .poster-placeholder {
        height: 220px;
    }
}

@media (max-width: 600px) {

    .hero-container {
        min-height: 300px;
    }

    .hero-content {
        padding: 20px;
    }

    .hero-title {
        font-size: 26px;
    }

    .movie-poster,
    .poster-placeholder {
        height: 180px;
    }
}

</style>
""")


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def safe_text(value):

    if pd.isna(value):
        return ""

    return html.escape(str(value))


def get_genres(value):

    if pd.isna(value) or not value:
        return []

    return str(value).split("|")


def safe_score(value):

    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def get_release_year(title):

    match = re.search(r"\((\d{4})\)\s*$", str(title))

    return match.group(1) if match else None


def section_heading(title, subtitle=""):

    st.html(
        f"""
        <div class="section-heading">
            {title}
        </div>

        <div class="section-subheading">
            {subtitle}
        </div>
        """
    )


def normalize_title(value):

    return str(value).strip().casefold()


# ============================================================
# 5. TMDB SEARCH
# ============================================================

@st.cache_data(ttl=86400, show_spinner=False)
def get_tmdb_movie(movie_title, api_key):

    if not api_key:
        return None

    title = str(movie_title)
    year = get_release_year(title)

    search_title = title

    if year:

        search_title = re.sub(
            r"\s*\(\d{4}\)\s*$",
            "",
            title
        ).strip()

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": api_key,
        "query": search_title,
        "include_adult": False
    }

    if year:
        params["year"] = year

    try:

        response = requests.get(
            url,
            params=params,
            timeout=8
        )

        response.raise_for_status()

        results = response.json().get("results", [])

        if not results:
            return None

        if year:

            exact_matches = [
                item for item in results
                if item.get("release_date", "").startswith(year)
            ]

            if exact_matches:
                results = exact_matches

        result = results[0]

        return {
            "id": result.get("id"),
            "title": result.get("title"),
            "overview": result.get("overview", ""),
            "release_date": result.get("release_date", ""),
            "vote_average": result.get("vote_average"),
            "poster_path": result.get("poster_path"),
            "backdrop_path": result.get("backdrop_path")
        }

    except (
        requests.RequestException,
        ValueError,
        TypeError,
        KeyError
    ):

        return None


def poster_url(metadata):

    if metadata and metadata.get("poster_path"):

        return (
            TMDB_IMAGE_BASE
            + TMDB_POSTER_SIZE
            + metadata["poster_path"]
        )

    return None


def backdrop_url(metadata):

    if metadata and metadata.get("backdrop_path"):

        return (
            TMDB_IMAGE_BASE
            + TMDB_BACKDROP_SIZE
            + metadata["backdrop_path"]
        )

    return None


# ============================================================
# 6. CATALOGUE PREPARATION
# ============================================================

# Discover uses the complete MovieLens catalogue.
# This is intentionally NOT the recommendation dataframe.

catalogue = movies.copy()

catalogue["Title"] = catalogue["Title"].astype(str)

catalogue["Genres"] = catalogue["Genres"].fillna("Unknown")

catalogue = catalogue.drop_duplicates(
    subset=["MovieID"]
).reset_index(drop=True)


# ============================================================
# 7. AVAILABLE USERS
# ============================================================

available_users = sorted(
    int(user_id)
    for user_id in user_movie_matrix.index
)

if not available_users:

    st.error(
        "No users are available in the recommendation dataset."
    )

    st.stop()


# ============================================================
# 8. TOP NAVIGATION
# ============================================================

nav_left, nav_middle, nav_right = st.columns(
    [1.5, 3.5, 1.5],
    vertical_alignment="center"
)

with nav_left:

    st.html("""
    <div class="brand">
        MOVIE<span class="brand-red">MIND</span>
    </div>

    <div class="brand-subtitle">
        Movie discovery
    </div>
    """)

with nav_middle:

    page = st.radio(
        "Navigation",
        ["Home", "Discover", "My Recommendations"],
        horizontal=True,
        label_visibility="collapsed",
        key="navigation"
    )

with nav_right:

    selected_user = st.selectbox(
        "Profile",
        options=available_users,
        index=0,
        format_func=lambda value: f"User {value}",
        key="selected_profile"
    )


# ============================================================
# 9. RECOMMENDATION LOADING
# ============================================================

if (
    "recommendations" not in st.session_state
    or st.session_state.get("loaded_user") != selected_user
):

    try:

        with st.spinner(
            "Preparing your personalized movie collection..."
        ):

            result = recommend_movies(
                user_id=selected_user,
                top_n=1000
            )

            st.session_state.recommendations = result
            st.session_state.loaded_user = selected_user

    except Exception as error:

        st.error(
            f"Recommendation error: {error}"
        )

        st.stop()


recommendations = st.session_state.recommendations.copy()


# ============================================================
# 10. RECOMMENDATION LOOKUP
# ============================================================

# Create a lookup table of recommendation scores.
# Catalogue movies do not receive fabricated recommendation scores.

recommendation_lookup = {}

if not recommendations.empty:

    for _, row in recommendations.iterrows():

        recommendation_lookup[
            int(row["MovieID"])
        ] = {
            "ContentScore": safe_score(row.get("ContentScore", 0)),
            "CollaborativeScore": safe_score(
                row.get("CollaborativeScore", 0)
            ),
            "HybridScore": safe_score(
                row.get("HybridScore", 0)
            )
        }


# ============================================================
# 11. MOVIE DETAIL STATE
# ============================================================

if "selected_movie_title" not in st.session_state:

    st.session_state.selected_movie_title = None


# ============================================================
# 12. MOVIE CARD COMPONENT
# ============================================================

def render_movie_card(
    movie,
    rank,
    card_key,
    show_model_score=False
):

    title = str(movie["Title"])

    genres = safe_text(movie.get("Genres", "Unknown"))

    movie_id = int(movie["MovieID"])

    metadata = get_tmdb_movie(
        title,
        TMDB_API_KEY
    )

    image = poster_url(metadata)

    if image:

        poster_html = f"""
        <img
            class="movie-poster"
            src="{html.escape(image, quote=True)}"
            alt="{safe_text(title)} poster"
            loading="lazy"
        >
        """

    else:

        poster_html = """
        <div class="poster-placeholder">
            🎬
        </div>
        """

    rating_html = ""

    if metadata and metadata.get("vote_average"):

        rating_html = (
            '<div class="movie-rating">'
            f'★ {float(metadata["vote_average"]):.1f}/10 TMDB'
            '</div>'
        )

    score_html = ""

    if show_model_score:

        score_html = (
            '<div class="movie-score">'
            f'Match Score: '
            f'{safe_score(movie.get("HybridScore", 0)):.3f}'
            '</div>'
        )

    rank_html = ""

    if rank is not None:

        rank_html = (
            '<div class="movie-rank">'
            f'#{rank}'
            '</div>'
        )

    card_html = f"""
    <div class="movie-card">

        {rank_html}

        {poster_html}

        <div class="movie-card-content">

            <div class="movie-title">
                {safe_text(title)}
            </div>

            <div class="movie-genres">
                {genres}
            </div>

            {rating_html}

            {score_html}

        </div>

    </div>
    """

    st.html(card_html)

    if st.button(
        "More Information",
        key=f"details_{card_key}",
        use_container_width=True
    ):

        st.session_state.selected_movie_title = title

        st.rerun()


# ============================================================
# 13. MOVIE DETAIL VIEW
# ============================================================

def render_movie_details(title):

    # Look up movie from the FULL catalogue.
    # No longer dependent on recommendations.

    movie_rows = catalogue[
        catalogue["Title"] == title
    ]

    if movie_rows.empty:

        st.warning(
            "The selected movie could not be found in the catalogue."
        )

        return

    movie = movie_rows.iloc[0]

    movie_id = int(movie["MovieID"])

    metadata = get_tmdb_movie(
        title,
        TMDB_API_KEY
    )

    st.divider()

    left, right = st.columns(
        [1, 2.5],
        gap="large"
    )

    with left:

        image = poster_url(metadata)

        if image:

            st.image(
                image,
                use_container_width=True
            )

        else:

            st.html("""
            <div class="poster-placeholder">
                🎬
            </div>
            """)

    with right:

        overview = (
            metadata.get("overview", "")
            if metadata else
            ""
        )

        if not overview:

            overview = (
                "An overview is not available from TMDB "
                "for this movie."
            )

        st.html(
            f"""
            <div class="detail-panel">

                <div class="detail-title">
                    {safe_text(title)}
                </div>

                <div class="detail-overview">
                    {safe_text(overview)}
                </div>

            </div>
            """
        )

        year = (
            metadata.get("release_date", "")[:4]
            if metadata and metadata.get("release_date")
            else get_release_year(title) or "Unknown"
        )

        tmdb_rating = (
            f'{float(metadata["vote_average"]):.1f}/10'
            if metadata and metadata.get("vote_average")
            else "Not available"
        )

        detail1, detail2 = st.columns(2)

        detail1.metric(
            "Release Year",
            year
        )

        detail2.metric(
            "TMDB Rating",
            tmdb_rating
        )

        genre_text = str(
            movie["Genres"]
        ).replace("|", " • ")

        st.markdown("**Genres**")

        st.write(genre_text)

        # Only display model scores if this movie is actually
        # present in the model's recommendation results.

        if movie_id in recommendation_lookup:

            scores = recommendation_lookup[movie_id]

            st.divider()

            score1, score2, score3 = st.columns(3)

            score1.metric(
                "Content Score",
                f'{scores["ContentScore"]:.3f}'
            )

            score2.metric(
                "Collaborative Score",
                f'{scores["CollaborativeScore"]:.3f}'
            )

            score3.metric(
                "Hybrid Score",
                f'{scores["HybridScore"]:.3f}'
            )

            st.caption(
                "These scores are from the recommendation model "
                "for the selected profile."
            )

        else:

            st.caption(
                "This movie is in the catalogue but is not "
                "currently included in this profile's "
                "recommendation results."
            )

    if st.button(
        "← Back to Movies",
        key="back_to_movies"
    ):

        st.session_state.selected_movie_title = None

        st.rerun()


# ============================================================
# 14. HERO DATA
# ============================================================

if not recommendations.empty:

    hero_movie = recommendations.iloc[0]

    hero_title = str(hero_movie["Title"])

    hero_metadata = get_tmdb_movie(
        hero_title,
        TMDB_API_KEY
    )

    hero_background = backdrop_url(hero_metadata)

    if hero_background:

        hero_background_css = (
            "background-image: url('"
            + html.escape(hero_background, quote=True)
            + "');"
        )

    else:

        hero_background_css = """
        background-image:
            linear-gradient(120deg, #303030, #141414);
        """

    hero_overview = (
        hero_metadata.get("overview", "")
        if hero_metadata else
        "A personalized movie selection generated "
        "by your hybrid recommendation model."
    )

    if len(hero_overview) > 260:

        hero_overview = (
            hero_overview[:257].rsplit(" ", 1)[0]
            + "..."
        )

    hero_year = (
        hero_metadata.get("release_date", "")[:4]
        if hero_metadata and hero_metadata.get("release_date")
        else get_release_year(hero_title) or ""
    )

    hero_rating = (
        f'★ {float(hero_metadata["vote_average"]):.1f}/10'
        if hero_metadata and hero_metadata.get("vote_average")
        else "Personalized Pick"
    )

    hero_score = safe_score(
        hero_movie["HybridScore"]
    )

else:

    hero_title = None


# ============================================================
# 15. HOME PAGE
# ============================================================

if page == "Home":

    if recommendations.empty:

        st.info(
            "No personalized recommendations are currently available."
        )

    else:

        st.html(
            f"""
            <div class="hero-container"
                style="{hero_background_css}">

                <div class="hero-overlay"></div>

                <div class="hero-content">

                    <div class="hero-eyebrow">
                        YOUR PERSONALIZED PICK
                    </div>

                    <div class="hero-title">
                        {safe_text(hero_title)}
                    </div>

                    <div class="hero-description">
                        {safe_text(hero_overview)}
                    </div>

                    <div class="hero-meta">
                        {safe_text(hero_year)}
                        &nbsp;&nbsp; • &nbsp;&nbsp;
                        {safe_text(hero_rating)}
                        &nbsp;&nbsp; • &nbsp;&nbsp;
                        <span class="hero-score">
                            {hero_score:.3f} Match
                        </span>
                    </div>

                </div>

            </div>
            """
        )

        hero_button1, hero_button2 = st.columns(
            [1, 5]
        )

        with hero_button1:

            if st.button(
                "View Movie",
                key="hero_movie_details",
                use_container_width=True
            ):

                st.session_state.selected_movie_title = hero_title

                st.rerun()

        with hero_button2:

            st.caption(
                "Selected using your Content-Based and "
                "Collaborative Filtering preferences."
            )

        section_heading(
            '<span class="section-accent">Top Picks</span> For You',
            "Personalized recommendations generated by MovieMind."
        )

        top_movies = recommendations.head(10)

        card_rows = [
            top_movies.iloc[i:i + 5]
            for i in range(0, len(top_movies), 5)
        ]

        for row_index, movie_row in enumerate(card_rows):

            columns = st.columns(5, gap="medium")

            for column_index, (_, movie) in enumerate(
                movie_row.iterrows()
            ):

                with columns[column_index]:

                    rank = row_index * 5 + column_index + 1

                    render_movie_card(
                        movie,
                        rank,
                        f"home_{rank}",
                        show_model_score=True
                    )

        st.divider()

        section_heading(
            'More <span class="section-accent">To Explore</span>',
            "Continue discovering movies selected for your profile."
        )

        more_movies = recommendations.iloc[10:20]

        if not more_movies.empty:

            columns = st.columns(5, gap="medium")

            for index, (_, movie) in enumerate(
                more_movies.iterrows()
            ):

                with columns[index % 5]:

                    render_movie_card(
                        movie,
                        index + 11,
                        f"home_more_{index}",
                        show_model_score=True
                    )


# ============================================================
# 16. DISCOVER PAGE
# ============================================================

elif page == "Discover":

    section_heading(
        'Discover <span class="section-accent">Movies</span>',
        "Explore the complete MovieLens movie catalogue."
    )

    st.caption(
        "Browse movies independently of your personalized "
        "recommendation rankings."
    )

    all_genres = set()

    for genre_string in catalogue["Genres"].dropna():

        all_genres.update(
            get_genres(genre_string)
        )

    genre_options = [
        "All Genres"
    ] + sorted(all_genres)

    filter1, filter2 = st.columns(
        [2, 1]
    )

    with filter1:

        search_query = st.text_input(
            "Search movie titles",
            placeholder="Search Titanic, Toy Story, Batman...",
            key="discover_search"
        )

    with filter2:

        selected_genre = st.selectbox(
            "Select genre",
            genre_options,
            key="discover_genre"
        )

    # --------------------------------------------------------
    # SEARCH THE FULL CATALOGUE
    # --------------------------------------------------------

    filtered = catalogue.copy()

    if search_query.strip():

        filtered = filtered[
            filtered["Title"].str.contains(
                search_query.strip(),
                case=False,
                na=False,
                regex=False
            )
        ]

    if selected_genre != "All Genres":

        filtered = filtered[
            filtered["Genres"].apply(
                lambda value:
                    selected_genre in get_genres(value)
            )
        ]

    filtered = filtered.reset_index(drop=True)

    # --------------------------------------------------------
    # OPTIONAL MODEL SCORES
    # --------------------------------------------------------

    filtered["HybridScore"] = filtered["MovieID"].map(
        lambda movie_id:
            recommendation_lookup.get(
                int(movie_id),
                {}
            ).get("HybridScore", None)
    )

    st.caption(
        f"{len(filtered):,} movies found in the catalogue"
    )

    if filtered.empty:

        st.html("""
        <div class="empty-state">

            <h3>No movies found</h3>

            <p>
                Try another search or choose a different genre.
            </p>

        </div>
        """)

    else:

        display_count = st.selectbox(
            "Movies per page",
            [10, 20, 30, 50],
            index=1,
            key="discover_display_count"
        )

        # Reset pagination whenever search or genre changes.

        filter_signature = (
            search_query.strip().casefold(),
            selected_genre,
            display_count
        )

        if (
            st.session_state.get("discover_filter_signature")
            != filter_signature
        ):

            st.session_state.discover_page = 0

            st.session_state.discover_filter_signature = (
                filter_signature
            )

        if "discover_page" not in st.session_state:

            st.session_state.discover_page = 0

        total_pages = max(
            1,
            (len(filtered) + display_count - 1)
            // display_count
        )

        st.session_state.discover_page = max(
            0,
            min(
                st.session_state.discover_page,
                total_pages - 1
            )
        )

        nav1, nav2, nav3 = st.columns(
            [1, 3, 1]
        )

        with nav1:

            if st.button(
                "← Previous",
                disabled=(
                    st.session_state.discover_page == 0
                ),
                key="discover_previous"
            ):

                st.session_state.discover_page -= 1

                st.rerun()

        with nav2:

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    color:#999;
                    padding-top:8px;
                ">
                    Page {st.session_state.discover_page + 1}
                    of {total_pages}
                </div>
                """,
                unsafe_allow_html=True
            )

        with nav3:

            if st.button(
                "Next →",
                disabled=(
                    st.session_state.discover_page
                    >= total_pages - 1
                ),
                key="discover_next"
            ):

                st.session_state.discover_page += 1

                st.rerun()

        start = (
            st.session_state.discover_page
            * display_count
        )

        page_movies = filtered.iloc[
            start:start + display_count
        ]

        rows = [
            page_movies.iloc[i:i + 5]
            for i in range(0, len(page_movies), 5)
        ]

        for row_index, movie_row in enumerate(rows):

            columns = st.columns(
                5,
                gap="medium"
            )

            for column_index, (_, movie) in enumerate(
                movie_row.iterrows()
            ):

                with columns[column_index]:

                    rank = (
                        start
                        + row_index * 5
                        + column_index
                        + 1
                    )

                    # Discover cards do NOT display fabricated
                    # recommendation match scores.

                    render_movie_card(
                        movie,
                        rank,
                        f"discover_{rank}",
                        show_model_score=False
                    )


# ============================================================
# 17. MY RECOMMENDATIONS PAGE
# ============================================================

elif page == "My Recommendations":

    section_heading(
        'My <span class="section-accent">Recommendations</span>',
        "Your personalized movie collection, ranked by the hybrid model."
    )

    if recommendations.empty:

        st.info(
            "No recommendations are available for this profile."
        )

    else:

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric(
            "Selected User",
            selected_user
        )

        metric2.metric(
            "Recommendations",
            len(recommendations)
        )

        metric3.metric(
            "Content Weight",
            f"{float(best_alpha):.0%}"
        )

        st.caption(
            "The hybrid model combines Content-Based and "
            "Collaborative Filtering scores."
        )

        display_count = st.selectbox(
            "Number of movies to display",
            [10, 20, 30, 50],
            index=1,
            key="my_recommendation_count"
        )

        selected_movies = recommendations.head(
            display_count
        )

        rows = [
            selected_movies.iloc[i:i + 5]
            for i in range(0, len(selected_movies), 5)
        ]

        for row_index, movie_row in enumerate(rows):

            columns = st.columns(
                5,
                gap="medium"
            )

            for column_index, (_, movie) in enumerate(
                movie_row.iterrows()
            ):

                with columns[column_index]:

                    rank = (
                        row_index * 5
                        + column_index
                        + 1
                    )

                    render_movie_card(
                        movie,
                        rank,
                        f"personal_{rank}",
                        show_model_score=True
                    )


# ============================================================
# 18. SELECTED MOVIE DETAILS
# ============================================================

if st.session_state.selected_movie_title:

    render_movie_details(
        st.session_state.selected_movie_title
    )


# ============================================================
# 19. FOOTER
# ============================================================

st.html("""
<div class="footer">

    <div style="
        font-size:20px;
        font-weight:900;
        letter-spacing:-1px;
        color:#FFFFFF;
        margin-bottom:8px;
    ">
        MOVIE<span style="color:#E50914;">MIND</span>
    </div>

    Personalized Movie Recommendation System

    <br>

    Powered by Content-Based Filtering,
    Collaborative Filtering and Hybrid Recommendation.

    <br><br>

    This product uses the TMDB API but is not endorsed
    or certified by TMDB.

    <br>

    MovieMind is an independent academic project.

</div>
""")