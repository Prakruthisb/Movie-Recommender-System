import streamlit as st
import numpy as np
import requests

from sqlalchemy import create_engine
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

# Create SQLAlchemy engine
engine = create_engine("postgresql+psycopg2://postgres:psql%402026@localhost/movie_recommender")

# Use pandas with the engine
query = "SELECT * FROM movies;"
movies = pd.read_sql(query, engine)

# print(type(movies['embedding'][0]))

# Convert embeddings from list (or string) to np.array
movies['semantic_embedding'] = movies['semantic_embedding'].apply(lambda x: np.array(x))


# Stack embeddings into a 2D array
embeddings_matrix = np.stack(movies['semantic_embedding'].values)

# Compute cosine similarity
similarity_matrix = cosine_similarity(embeddings_matrix)

def fetch_poster(movie_name):
    url =  f"http://www.omdbapi.com/?t={movie_name}&apikey=f4d089de" 

    response = requests.get(url) 
    data = response.json() 

    if data['Response'] == 'True':
        return data['Poster']
    else:
        return 'No'

def recommend(movie):
    # Find the index of the selected movie
    movie_index = movies[movies['title'] == movie].index[0]
    
    # Get similarity scores for that movie
    distances = similarity_matrix[movie_index]
    
    # Sort movies by similarity score (exclude the selected movie itself)
    movie_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:11]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]]['title'])
        poster = fetch_poster(movies.iloc[i[0]]['title'])
        if poster != 'No':
            recommended_movies_poster.append(poster)
        else:
            recommended_movies_poster.append('Movie poster not found!!!')

    return recommended_movies, recommended_movies_poster

st.title("Movies Recommendation System")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    selected_movie_poster = fetch_poster(selected_movie)
    st.markdown("<h2 style='text-align: center;'>"+selected_movie+"</h2>", unsafe_allow_html=True)

    col1,col2 = st.columns([1,2]) 

    with col1:
        if selected_movie_poster != 'No':
            st.image(selected_movie_poster) 
        else:
            st.write("Movies Poster Not Found!!!") 

    with col2:
        st.write(":rainbow[TITLE] :  "+selected_movie) 

        st.write(":rainbow[OVERVIEW] : ")
        overview = movies[movies['title']==selected_movie]['overview'].values[0] 
        st.write(overview)  

        # st.write(":rainbow[GENERE] :  " + " , ".join(movies[movies['title']==selected_movie]['genres'].tolist()[0]))   
        st.write(":rainbow[GENERE] :  " + movies[movies['title']==selected_movie]['genres'].values[0]) 
             

    st.header(":rainbow[_RECOMMENDED MOVIES FOR YOU_]") 
    movies_name,movies_poster = recommend(selected_movie)

    for i in range(0, len(movies_name), 5):
            cols = st.columns(5)
            for j, col in enumerate(cols):
                if i + j < len(movies_name):
                    if movies_poster[i+j] != 'Movie poster not found!!!': 
                        col.caption(movies_name[i+j]) 
                        col.image(movies_poster[i + j])
                    else:
                        continue 