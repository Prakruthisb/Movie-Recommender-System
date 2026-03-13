import pandas as pd #Used to read CSV files and work with tables
import psycopg2 #Used to connect Python with PostgreSQL database
import ast
import os

movies = pd.read_csv(r"D:\movie_recommender_system\database\movies.csv")

movies['embedding'] = movies['embedding'].apply(ast.literal_eval)

# print(type(movies['embedding'][0]))

movies = movies.drop_duplicates(subset=['tmdb_id'], keep='first')

# Connect to DB
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor() #A pen to write SQL commands. Without cursor → we cannot execute queries.

for index, row in movies.iterrows():
    cur.execute("""
        INSERT INTO movies (tmdb_id, title, overview, genres, tags, embedding, popularity, release_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row['tmdb_id'],
        row['title'],
        row['overview'],
        row['genres'],
        row['tags'],
        row['embedding'],
        row['popularity'],
        row['release_date']

    ))

conn.commit()
cur.close()
conn.close()

print("Data inserted successfully!")