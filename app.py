# ============================================
# 🎬 Movie Recommendation System - Streamlit App
# ============================================

# ---------- IMPORT LIBRARIES ----------
import streamlit as st
import pandas as pd
import pickle


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Recommendation System")
st.write(
    "Select a movie and get similar movie recommendations instantly!"
)


# ============================================
# LOAD SAVED FILES (FROM NOTEBOOK)
# ============================================

@st.cache_data
def load_data():

    # Load processed dataset
    data = pd.read_csv("processed_data.csv")

    # Load similarity matrix (pickle)
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)

    return data, similarity


data, movie_similarity_df = load_data()


# ============================================
# GET MOVIE LIST
# ============================================

movie_list = data['title'].unique()
movie_list = sorted(movie_list)


# ============================================
# RECOMMENDATION FUNCTION
# ============================================

def recommend_movies(movie_name, n=10):

    # Check movie exists
    if movie_name not in movie_similarity_df.index:
        return ["Movie not found in dataset"]

    # Fetch similarity scores
    similarity_scores = movie_similarity_df[movie_name]

    # Sort movies based on similarity
    similar_movies = similarity_scores \
        .sort_values(ascending=False)[1:n+1]

    return similar_movies.index.tolist()


# ============================================
# USER INPUT UI
# ============================================

selected_movie = st.selectbox(
    "🎥 Select a Movie",
    movie_list
)


# ============================================
# BUTTON ACTION
# ============================================

if st.button("🔍 Recommend"):

    with st.spinner("Finding best movies for you... 🎬"):

        recommendations = recommend_movies(
            selected_movie, 10
        )

    st.subheader(
        f"Top Recommendations for '{selected_movie}'"
    )

    for i, movie in enumerate(recommendations, 1):
        st.write(f"{i}. {movie}")
