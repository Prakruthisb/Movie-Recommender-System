import streamlit as st
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity
import os

# -----------------------------
# Database Connection
# -----------------------------
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    connect_args={"sslmode": "require"},
    pool_pre_ping=True
)

# -----------------------------
# Load Movies (Cached)
# -----------------------------
@st.cache_data
def load_movies():
    query = "SELECT * FROM public.movies;"
    df = pd.read_sql(query, engine)

    # Convert embeddings to numpy arrays
    df['semantic_embedding'] = df['semantic_embedding'].apply(lambda x: np.array(x))

    return df


movies = load_movies()

# Stack embeddings into matrix
embeddings_matrix = np.stack(movies['semantic_embedding'].values)


# -----------------------------
# Recommendation Function
# -----------------------------
def recommend(movie_title):

    movie_index = movies[movies['title'] == movie_title].index[0]

    selected_embedding = embeddings_matrix[movie_index]

    similarities = cosine_similarity(
        [selected_embedding],
        embeddings_matrix
    )[0]

    movie_list = sorted(
        list(enumerate(similarities)),
        key=lambda x: x[1],
        reverse=True
    )[1:11]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:

        title = movies.iloc[i[0]]['title']
        poster = movies.iloc[i[0]]['poster_path']

        recommended_movies.append(title)

        if pd.notna(poster) and poster != "":
            recommended_posters.append(poster)
        else:
            recommended_posters.append(None)

    return recommended_movies, recommended_posters


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

# -----------------------------
# Recommend Button
# -----------------------------
if st.button("Recommend"):

    selected_movie_row = movies[movies['title'] == selected_movie].iloc[0]

    selected_movie_poster = selected_movie_row['poster_path']
    overview = selected_movie_row['overview']
    genres = selected_movie_row['genres']

    st.markdown(
        f"<h2 style='text-align:center'>{selected_movie}</h2>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        if pd.notna(selected_movie_poster) and selected_movie_poster != "":
            st.image(selected_movie_poster)
        else:
            st.write("Poster not available")

    with col2:
        st.write("### 🎬 Title")
        st.write(selected_movie)

        st.write("### 📝 Overview")
        st.write(overview)

        st.write("### 🎭 Genres")
        st.write(genres)

    st.header("✨ Recommended Movies")

    movies_name, movies_poster = recommend(selected_movie)

    for i in range(0, len(movies_name), 5):

        cols = st.columns(5)

        for j, col in enumerate(cols):

            if i + j < len(movies_name):

                col.caption(movies_name[i + j])

                if movies_poster[i + j]:
                    col.image(movies_poster[i + j])
                else:
                    col.write("Poster not available")