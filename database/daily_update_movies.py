import requests
import pandas as pd
import time
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed
import psycopg2
from psycopg2.extras import execute_values
import os

API_KEY = os.getenv("TMDB_API_KEY")
# API_KEY = "TMDB_API_KEY"

base_url = "https://api.themoviedb.org/3/discover/movie"

languages = {
    "Hindi": ("hi", 5),
    "Tamil": ("ta", 5),
    "Telugu": ("te", 5),
    "Kannada": ("kn", 5),
    "Malayalam": ("ml", 5),
    "Bengali": ("bn", 5),
    "Marathi": ("mr", 5)
}

all_movies = []

for lang_name, (lang_code, total_pages) in languages.items():

    print(f"Fetching {lang_name} movies...")

    for page in range(1, total_pages + 1):

        params = {
            "api_key": API_KEY,
            "with_original_language": lang_code,
            "page": page,
            "sort_by": "primary_release_date.desc",
            "primary_release_date.gte": "2025-01-01"
        }

        max_retries = 10

        for attempt in range(max_retries):

            try:
                response = requests.get(base_url, params=params, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    break

                else:
                    print("API error:", response.status_code)

            except Exception:
                print(f"Retrying {lang_name} page {page} attempt {attempt+1}")
                time.sleep(1)

        else:
            print(f"Failed page {page}")
            continue

        movies = data.get("results", [])

        for movie in movies:

            poster_path = movie.get("poster_path")

            poster_url = None
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"

            movie_data = {
                "movie_id": movie.get("id"),
                "title": movie.get("title"),
                "release_date": movie.get("release_date"),
                "popularity": movie.get("popularity"),
                "overview": movie.get("overview"),
                "genre_ids": movie.get("genre_ids"),
                "poster_path": poster_url
            }

            all_movies.append(movie_data)

        print(f"{lang_name} Page {page}/{total_pages}")

        time.sleep(0.5)

print("All movies fetched!")

df = pd.DataFrame(all_movies)

# pickle.dump(df, open(r'D:\movie_recommender_system\database\df1.pkl','wb'))

# Fetch Genre Mapping
# url = "https://api.themoviedb.org/3/genre/movie/list"
# params = {"api_key": API_KEY}

# for attempt in range(max_retries):
#     try:
#         response = requests.get(url, params=params, timeout=10)

#         if response.status_code == 200:
#             genres = response.json()["genres"]
#             break

#     except Exception:
#         print("Retrying genre request...", attempt+1)
#         time.sleep(1)

# else:
#     raise Exception("Failed to fetch genres after retries")

# genre_map = {g["id"]: g["name"] for g in genres}

# pickle.dump(genre_map,open(r"D:\movie_recommender_system\database\genre_map.pkl","wb"))



# df = pickle.load(open(r"D:\movie_recommender_system\database\df1.pkl",'rb'))
genre_map = pickle.load(open('database/genre_map.pkl','rb'))

# # print(df.info())
# # print(df.head())



df["genres"] = df["genre_ids"].apply(
    lambda ids: [genre_map.get(i) for i in ids if i in genre_map] if isinstance(ids,list) else []
)

df["genres"] = df["genres"].apply(lambda x: " ".join(x))

df.drop("genre_ids", axis=1, inplace=True)

# print(df.head())

# print(max(df['popularity']))

df['release_date'] = pd.to_datetime(df['release_date'])

# print(df.info())
# print(df.head())

# pickle.dump(df, open(r'D:\movie_recommender_system\database\df1.pkl','wb'))




# df = pickle.load(open(r"D:\movie_recommender_system\database\df1.pkl",'rb'))

#Script to Fetch Extra Columns
def fetch_movie_details(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": API_KEY,
        "append_to_response": "credits,keywords"
    }

    for attempt in range(10):   # retry 10 times
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
            else:
                print("API error:", response.status_code)
                return None

            cast = [c["name"] for c in data.get("credits", {}).get("cast", [])[:5]]

            director = [
                c["name"]
                for c in data.get("credits", {}).get("crew", [])
                if c["job"] == "Director"
            ]

            keywords = [
                k["name"]
                for k in data.get("keywords", {}).get("keywords", [])
            ]

            return {
                "movie_id": movie_id,
                "cast": cast,
                "director": director,
                "keywords": keywords
            }

        except Exception as e:
            time.sleep(1)
            print(f"failed attempt {attempt+1}")
    else:
        return {
                    "movie_id": movie_id,
                    "cast": [],
                    "director": [],
                    "keywords": []
                }

#Run Parallel Requests
movie_ids = df["movie_id"].tolist()

results = []

with ThreadPoolExecutor(max_workers=8) as executor:

    futures = [executor.submit(fetch_movie_details, mid) for mid in movie_ids]

    # This is where you add the progress monitoring code
    for i, future in enumerate(as_completed(futures)):
        results.append(future.result())

        total = len(movie_ids)

        if (i+1) % 500 == 0:
            print(f"{i+1}/{total} movies processed")

extra_df = pd.DataFrame(results)

#Merging With our Dataset
df = pd.merge(df,extra_df, on="movie_id",how="left")

# print(df.head())
# print(df.info())

# pickle.dump(df,open(r'D:\movie_recommender_system\database\df1.pkl','wb'))

# df = pickle.load(open(r"D:\movie_recommender_system\database\df1.pkl",'rb'))
# # print(df['cast'])

df['cast'] = df['cast'].apply(lambda x:[s.replace(" ","") for s in x])
df['cast'] = df['cast'].apply(lambda x:" ".join(x))

df['director'] = df['director'].apply(lambda x:[s.replace(" ","") for s in x])
df['director'] = df['director'].apply(lambda x:" ".join(x))

df['keywords'] = df['keywords'].apply(lambda x:[s.replace(" ","") for s in x])
df['keywords'] = df['keywords'].apply(lambda x:" ".join(x))

# Create the Tags Column
df["tags"] = (
    df["genres"].astype(str) + " " +
    df["cast"].astype(str) + " " +
    df["director"].astype(str) + " " +
    df["keywords"].astype(str) + " " +
    df["overview"].astype(str)
)

df['tags'] = df['tags'].str.lower()

#creating semantic embeddings 
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

df["semantic_embedding"] = df["tags"].apply(
    lambda x: model.encode(x).tolist()
)

df = df.rename(columns={'movie_id':'tmdb_id'})

df["release_date"] = df["release_date"].apply(
    lambda x: x.date() if pd.notnull(x) else None
)

# # print(df.info())
# pickle.dump(df,open(r'D:\movie_recommender_system\database\df1.pkl','wb'))


# df = pickle.load(open(r"D:\movie_recommender_system\database\df1.pkl",'rb'))

df = df.where(pd.notnull(df), None)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

# Ensure column order matches the SQL query
records = [tuple(row) for row in df[
    [
        "tmdb_id",
        "title",
        "overview",
        "genres",
        "tags",
        "semantic_embedding",
        "popularity",
        "release_date",
        "poster_path"
    ]
].values]

# SQL Query
query = """
INSERT INTO movies
(tmdb_id, title, overview, genres, tags, semantic_embedding, popularity, release_date, poster_path)
VALUES %s
ON CONFLICT (tmdb_id)
DO NOTHING
"""

# Execute bulk insert
execute_values(cursor, query, records)

# Commit changes
conn.commit()

print("Movies inserted/updated successfully!")

cursor.close()
conn.close()
