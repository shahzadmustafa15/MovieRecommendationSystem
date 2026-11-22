
import streamlit as st


def load_css():

    st.markdown("""
    <style>
        /* Main application */
        .stApp {
            background: #09090B;
            color: #FAFAFA;
        }

        /* Main content spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1500px;
        }

        /* Headings */
        h1, h2, h3 {
            color: #FAFAFA;
            letter-spacing: -0.5px;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: #111114;
            border-right: 1px solid #27272A;
        }

        /* Buttons */
        .stButton > button {
            background: #8B5CF6;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.55rem 1.2rem;
        }

        .stButton > button:hover {
            background: #7C3AED;
            color: white;
            border: none;
        }

        /* Movie cards */
        .movie-card {
            background: #18181B;
            border: 1px solid #27272A;
            border-radius: 12px;
            padding: 14px;
            height: 100%;
        }

        .movie-title {
            color: #FAFAFA;
            font-size: 16px;
            font-weight: 650;
            margin-top: 10px;
            min-height: 42px;
        }

        .movie-genre {
            color: #A1A1AA;
            font-size: 12px;
            margin-top: 5px;
        }

        .movie-score {
            color: #A78BFA;
            font-weight: 600;
            font-size: 13px;
            margin-top: 12px;
        }

        /* Subtle divider */
        hr {
            border-color: #27272A;
        }
    </style>
    """, unsafe_allow_html=True)
