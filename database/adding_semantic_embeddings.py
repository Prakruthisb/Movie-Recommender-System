import pandas as pd #Used to read CSV files and work with tables
import psycopg2 #Used to connect Python with PostgreSQL database
import ast

movies = pd.read_csv(r"D:\movie_recommender_system\database\semantic_movies.csv")

movies['semantic_embedding'] = movies['semantic_embedding'].apply(ast.literal_eval)

# print(type(movies['embedding'][0]))

movies = movies.drop_duplicates(subset=['tmdb_id'], keep='first')

# Connect to DB
conn = psycopg2.connect(
    host="localhost",
    database="movie_recommender",
    user="postgres",
    password="psql@2026"
)

cur = conn.cursor() #A pen to write SQL commands. Without cursor → we cannot execute queries.

for _, row in movies.iterrows():
    cur.execute("""
        UPDATE movies
        SET semantic_embedding = %s
        WHERE tmdb_id = %s
    """, (row["semantic_embedding"], row["tmdb_id"]))

conn.commit()
cur.close()
conn.close()

print("Data inserted successfully!")