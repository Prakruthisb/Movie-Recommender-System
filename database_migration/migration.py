import psycopg2
import pandas as pd
from psycopg2.extras import execute_values
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# load_dotenv() #for local development

# LOCAL DATABASE CONNECTION
local_conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=os.getenv("DB_PORT")
)

# SUPABASE DATABASE CONNECTION
cloud_conn = psycopg2.connect(
    host=os.getenv("CLOUD_DB_HOST"),
    database=os.getenv("CLOUD_DB_NAME"),
    user=os.getenv("CLOUD_DB_USER"),
    password=os.getenv("CLOUD_DB_PASSWORD"),
    port=os.getenv("CLOUD_DB_PORT")
)

print("Connected to cloud database successfully")

# -------------------------
# Fetch data from local DB
# -------------------------

query = "SELECT * FROM movies"

engine = create_engine(
    "postgresql+psycopg2://postgres:psql%402026@localhost/movie_recommender"
)
df = pd.read_sql(query, engine)

print("Rows fetched from local:", len(df))

# -------------------------
# Insert into cloud DB
# -------------------------

cursor = cloud_conn.cursor()

records = df[
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
].values.tolist()

query = """
INSERT INTO movies (
    tmdb_id,
    title,
    overview,
    genres,
    tags,
    semantic_embedding,
    popularity,
    release_date,
    poster_path
)
VALUES %s
ON CONFLICT (tmdb_id) DO NOTHING
"""

execute_values(cursor, query, records)

cloud_conn.commit()

print("Data successfully migrated to cloud!")

cursor.close()
local_conn.close()
cloud_conn.close()