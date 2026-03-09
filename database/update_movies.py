#getting the number of movies and pages we have in each language we are using

# import requests

# API_KEY = "89e257699ba82af50858fc341569a96f"

# url = "https://api.themoviedb.org/3/discover/movie"

# languages = [
#     "hi",  # Hindi
#     "ta",  # Tamil
#     "te",  # Telugu
#     "kn",  # Kannada
#     "ml",  # Malayalam
#     "bn",  # Bengali
#     "mr"   # Marathi
# ]

# for lang in languages:

#     params = {
#         "api_key": API_KEY,
#         "with_original_language": lang,
#         "page": 1
#     }

#     response = requests.get(url, params=params)

#     data = response.json()

#     print("Language:", lang)
#     print("Total Movies:", data["total_results"])
#     print("Total Pages:", data["total_pages"])
#     print("----------------------")


#fetching the hindi movies into a dataframe

# import requests
# import pandas as pd
# import time

# API_KEY = "89e257699ba82af50858fc341569a96f"

# base_url = "https://api.themoviedb.org/3/discover/movie"

# languages = {
#     "Hindi": ("hi", 487),
#     # "Tamil": ("ta", 279),
#     # "Telugu": ("te", 181),
#     # "Kannada": ("kn", 109),
#     # "Malayalam": ("ml", 236),
#     # "Bengali": ("bn", 200),
#     # "Marathi": ("mr", 77)
# }

# all_movies = []

# for lang_name, (lang_code, total_pages) in languages.items():

#     print(f"Fetching {lang_name} movies...")

#     for page in range(1, total_pages + 1):

#         params = {
#             "api_key": API_KEY,
#             "with_original_language": lang_code,
#             "page": page,
#             "sort_by": "primary_release_date.asc"
#         }

#         response = requests.get(base_url, params=params)
#         data = response.json()

#         movies = data["results"]

#         for movie in movies:

#             movie_data = {
#                 "movie_id": movie["id"],
#                 "title": movie["title"],
#                 # "language": lang_name,
#                 # "original_language": movie["original_language"],
#                 "release_date": movie["release_date"],
#                 "popularity": movie["popularity"],
#                 # "vote_average": movie["vote_average"],
#                 # "vote_count": movie["vote_count"],
#                 "overview": movie["overview"],
#                 "genre_ids": movie["genre_ids"] 
#             }

#             all_movies.append(movie_data)

#         print(f"{lang_name} Page {page}/{total_pages}")

#         time.sleep(0.2)  # avoid API rate limits

# print("All movies fetched!")

# df = pd.DataFrame(all_movies)

import pickle 
# pickle.dump(df,open(r'D:\movie_recommender_system\database\df.pkl','wb'))

# df = pickle.load(open(r'D:\movie_recommender_system\database\df.pkl','rb'))
# print(df.head())


#fetching the tamil and telgu movies into a dataframe

# import requests
# import pandas as pd
# import time

# API_KEY = "89e257699ba82af50858fc341569a96f"

# base_url = "https://api.themoviedb.org/3/discover/movie"

# languages = {
#     # "Hindi": ("hi", 487),
#     "Tamil": ("ta", 279),
#     "Telugu": ("te", 181)
#     # "Kannada": ("kn", 109),
#     # "Malayalam": ("ml", 236),
#     # "Bengali": ("bn", 200),
#     # "Marathi": ("mr", 77)
# }

# all_movies = []

# for lang_name, (lang_code, total_pages) in languages.items():

#     print(f"Fetching {lang_name} movies...")

#     for page in range(1, total_pages + 1):

#         params = {
#             "api_key": API_KEY,
#             "with_original_language": lang_code,
#             "page": page,
#             "sort_by": "primary_release_date.asc"
#         }

#         response = requests.get(base_url, params=params)
#         data = response.json()

#         movies = data["results"]

#         for movie in movies:

#             movie_data = {
#                 "movie_id": movie["id"],
#                 "title": movie["title"],
#                 # "language": lang_name,
#                 # "original_language": movie["original_language"],
#                 "release_date": movie["release_date"],
#                 "popularity": movie["popularity"],
#                 # "vote_average": movie["vote_average"],
#                 # "vote_count": movie["vote_count"],
#                 "overview": movie["overview"],
#                 "genre_ids": movie["genre_ids"] 
#             }

#             all_movies.append(movie_data)

#         print(f"{lang_name} Page {page}/{total_pages}")

#         time.sleep(0.2)  # avoid API rate limits

# print("All movies fetched!")

# df = pd.concat([df, pd.DataFrame(all_movies)], ignore_index=True)
# pickle.dump(df,open(r'D:\movie_recommender_system\database\df.pkl','wb')) 

# print(len(df)) 


# df = pickle.load(open(r'D:\movie_recommender_system\database\df.pkl','rb'))

#fetching the kannada and malyalam movies into a dataframe

# import requests
# import pandas as pd
# import time

# API_KEY = "89e257699ba82af50858fc341569a96f"

# base_url = "https://api.themoviedb.org/3/discover/movie"

# languages = {
#     # "Hindi": ("hi", 487),
#     # "Tamil": ("ta", 279),
#     # "Telugu": ("te", 181)
#     "Kannada": ("kn", 109),
#     "Malayalam": ("ml", 236)
#     # "Bengali": ("bn", 200),
#     # "Marathi": ("mr", 77)
# }

# all_movies = []

# for lang_name, (lang_code, total_pages) in languages.items():

#     print(f"Fetching {lang_name} movies...")

#     for page in range(1, total_pages + 1):

#         params = {
#             "api_key": API_KEY,
#             "with_original_language": lang_code,
#             "page": page,
#             "sort_by": "primary_release_date.asc"
#         }

#         response = requests.get(base_url, params=params)
#         data = response.json()

#         # movies = data["results"]
#         movies = data.get("results", [])

#         for movie in movies:

#             movie_data = {
#                 "movie_id": movie["id"],
#                 "title": movie["title"],
#                 # "language": lang_name,
#                 # "original_language": movie["original_language"],
#                 "release_date": movie["release_date"],
#                 "popularity": movie["popularity"],
#                 # "vote_average": movie["vote_average"],
#                 # "vote_count": movie["vote_count"],
#                 "overview": movie["overview"],
#                 "genre_ids": movie["genre_ids"] 
#             }

#             all_movies.append(movie_data)

#         print(f"{lang_name} Page {page}/{total_pages}")

#         time.sleep(0.2)  # avoid API rate limits

# print("All movies fetched!")

# df = pd.concat([df, pd.DataFrame(all_movies)], ignore_index=True)
# pickle.dump(df,open(r'D:\movie_recommender_system\database\df.pkl','wb'))

# df = pickle.load(open(r'D:\movie_recommender_system\database\df.pkl','rb'))
# print(len(df))
# print(df.tail())


# fetching the Bengali and Marathi movies into a dataframe

# import requests
# import pandas as pd
# import time

# API_KEY = "89e257699ba82af50858fc341569a96f"

# base_url = "https://api.themoviedb.org/3/discover/movie"

# languages = {
#     # "Hindi": ("hi", 487),
#     # "Tamil": ("ta", 279),
#     # "Telugu": ("te", 181)
#     # "Kannada": ("kn", 109),
#     # "Malayalam": ("ml", 236)
#     "Bengali": ("bn", 200),
#     "Marathi": ("mr", 77)
# }

# all_movies = []

# for lang_name, (lang_code, total_pages) in languages.items():

#     print(f"Fetching {lang_name} movies...")

#     for page in range(1, total_pages + 1):

#         params = {
#             "api_key": API_KEY,
#             "with_original_language": lang_code,
#             "page": page,
#             "sort_by": "primary_release_date.asc"
#         }

#         response = requests.get(base_url, params=params)
#         data = response.json()

#         # movies = data["results"]
#         movies = data.get("results", [])

#         for movie in movies:

#             movie_data = {
#                 "movie_id": movie["id"],
#                 "title": movie["title"],
#                 # "language": lang_name,
#                 # "original_language": movie["original_language"],
#                 "release_date": movie["release_date"],
#                 "popularity": movie["popularity"],
#                 # "vote_average": movie["vote_average"],
#                 # "vote_count": movie["vote_count"],
#                 "overview": movie["overview"],
#                 "genre_ids": movie["genre_ids"] 
#             }

#             all_movies.append(movie_data)

#         print(f"{lang_name} Page {page}/{total_pages}")

#         time.sleep(0.2)  # avoid API rate limits

# print("All movies fetched!")

# df = pd.concat([df, pd.DataFrame(all_movies)], ignore_index=True)
# pickle.dump(df,open(r'D:\movie_recommender_system\database\df.pkl','wb'))
# print(len(df))


# df = pickle.load(open(r'D:\movie_recommender_system\database\df.pkl','rb'))
# print(len(df))

# print(df.head())



#converting genre_ids to genre

#Fetch Genre Mapping
# import requests

# API_KEY = "89e257699ba82af50858fc341569a96f"

# url = "https://api.themoviedb.org/3/genre/movie/list"

# params = {
#     "api_key": API_KEY
# }

# response = requests.get(url, params=params)
# genres = response.json()["genres"]

# print(genres)

# #Create Genre Dictionary
# genre_map = {g["id"]: g["name"] for g in genres}
# print(genre_map)

# #Converting genre_ids in our DataFrame
# df["genres"] = df["genre_ids"].apply(
#     lambda ids: [genre_map[i] for i in ids if i in genre_map]
# )

# #Convert to Text
# df["genres"] = df["genres"].apply(lambda x: " ".join(x))

# #Remove Old Column
# df.drop("genre_ids", axis=1, inplace=True) 

# print(df.head())

# pickle.dump(df,open(r'D:\movie_recommender_system\database\df.pkl','wb'))





# df = pickle.load(open(r'D:\movie_recommender_system\database\df.pkl','rb'))
# # print(df.head())

# df['popularity'] = df['popularity']*100
# # print(df.head())

# # print(df.info())

# import pandas as pd
# df['release_date'] = pd.to_datetime(df['release_date'])
# # print(df.info())

# # print(len(df))
# df.drop(columns=['tags','keywords','director','cast'],axis=1,inplace=True)

# # print(df.info())

# pickle.dump(df,open(r'D:\movie_recommender_system\database\df.pkl','wb'))







# df = pickle.load(open(r'D:\movie_recommender_system\database\df.pkl','rb'))
# #Script to Fetch Extra Columns
# import requests
# import pandas as pd
# from concurrent.futures import ThreadPoolExecutor, as_completed

# API_KEY = "89e257699ba82af50858fc341569a96f"

# def fetch_movie_details(movie_id):

#     url = f"https://api.themoviedb.org/3/movie/{movie_id}"

#     params = {
#         "api_key": API_KEY,
#         "append_to_response": "credits,keywords"
#     }

#     try:
#         response = requests.get(url, params=params, timeout=10)
#         data = response.json()

#         cast = [c["name"] for c in data["credits"]["cast"][:5]]

#         director = [
#             c["name"]
#             for c in data["credits"]["crew"]
#             if c["job"] == "Director"
#         ]

#         keywords = [
#             k["name"]
#             for k in data["keywords"]["keywords"]
#         ]

#         return {
#             "movie_id": movie_id,
#             "cast": cast,
#             "director": director,
#             "keywords": keywords
#         }

#     except Exception as e:
#         print(f"Error for movie {movie_id}: {e}")
#         return {
#             "movie_id": movie_id,
#             "cast": [],
#             "director": [],
#             "keywords": []
#         }

# #Run Parallel Requests
# movie_ids = df["movie_id"].tolist()

# results = []

# with ThreadPoolExecutor(max_workers=40) as executor:

#     futures = [executor.submit(fetch_movie_details, mid) for mid in movie_ids]

#     # This is where you add the progress monitoring code
#     for i, future in enumerate(as_completed(futures)):
#         results.append(future.result())

#         if i % 500 == 0:  # Print progress every 500 movies
#             print(f"{i} movies processed")

# extra_df = pd.DataFrame(results)

# #Merging With our Dataset
# df = df.merge(extra_df, on="movie_id")

# #Create the Tags Column
# # df["tags"] = (
# #     df["genres"].astype(str) + " " +
# #     df["cast"].astype(str) + " " +
# #     df["director"].astype(str) + " " +
# #     df["keywords"].astype(str) + " " +
# #     df["overview"].astype(str)
# # )

# print(df.head())

# pickle.dump(df,open(r'D:\movie_recommender_system\database\df.pkl','wb'))







# df = pickle.load(open(r'D:\movie_recommender_system\database\df.pkl','rb'))
# # print(df.info())

# df['cast'] = df['cast'].apply(lambda x:[s.replace(" ","") for s in x])
# df['cast'] = df['cast'].apply(lambda x:" ".join(x))
# # print(df['cast'])

# # print(df['director'])
# df['director'] = df['director'].apply(lambda x:[s.replace(" ","") for s in x])
# df['director'] = df['director'].apply(lambda x:" ".join(x))
# # print(df['director'])

# df['keywords'] = df['keywords'].apply(lambda x:[s.replace(" ","") for s in x])
# df['keywords'] = df['keywords'].apply(lambda x:" ".join(x))
# # print(df['keywords'])

# # Create the Tags Column
# df["tags"] = (
#     df["genres"].astype(str) + " " +
#     df["cast"].astype(str) + " " +
#     df["director"].astype(str) + " " +
#     df["keywords"].astype(str) + " " +
#     df["overview"].astype(str)
# )

# df['tags'] = df['tags'].str.lower()
# # print(df['tags'])

# #creating semantic embeddings 
# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer("all-MiniLM-L6-v2")

# df["semantic_embedding"] = df["tags"].apply(
#     lambda x: model.encode(x).tolist()
# )
# pickle.dump(df,open(r'D:\movie_recommender_system\database\df.pkl','wb'))




# df = pickle.load(open(r'D:\movie_recommender_system\database\df.pkl','rb'))
# # print(df.info())
# # print(df['semantic_embedding'])

# df = df.rename(columns={'movie_id':'tmdb_id'})
# # print(df.info())
# pickle.dump(df,open(r'D:\movie_recommender_system\database\df.pkl','wb'))




df = pickle.load(open(r'D:\movie_recommender_system\database\df.pkl','rb'))
# print(df.isnull().sum())

#replacing NaT values in release_date with None
import pandas as pd
df["release_date"] = df["release_date"].apply(
    lambda x: x.date() if pd.notnull(x) else None
)

#tried to convert numpy datatypes into python datatypes but it is not working 
# for col in df.columns:
#     print(f"{col} = {type(df[col][0])}")

# Convert numpy types to native python types
# df["tmdb_id"] = df["tmdb_id"].astype(int)
# df["popularity"] = df["popularity"].astype(float)

# for col in df.columns:
#     print(f"{col} = {type(df[col][0])}")

import psycopg2
from psycopg2.extras import execute_values

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="movie_recommender",
    user="postgres",
    password="psql@2026",
    port="5432"
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
        "release_date"
    ]
].values]

# SQL Query
query = """
INSERT INTO movies
(tmdb_id, title, overview, genres, tags, semantic_embedding, popularity, release_date)
VALUES %s
ON CONFLICT (tmdb_id)
DO UPDATE SET
title = EXCLUDED.title,
overview = EXCLUDED.overview,
genres = EXCLUDED.genres,
tags = EXCLUDED.tags,
semantic_embedding = EXCLUDED.semantic_embedding,
popularity = EXCLUDED.popularity,
release_date = EXCLUDED.release_date
"""

# Execute bulk insert
execute_values(cursor, query, records)

# Commit changes
conn.commit()

print("Movies inserted/updated successfully!")

cursor.close()
conn.close()






