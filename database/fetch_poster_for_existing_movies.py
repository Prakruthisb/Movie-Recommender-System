import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from sqlalchemy import create_engine, text

# ----------------------------
# Config
# ----------------------------
API_KEY = "TMDB_API_KEY"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"  # TMDB poster URL base
MAX_WORKERS = 20      # parallel threads
BATCH_SIZE = 19000    # fetch half of movies at a time
THROTTLE_TIME = 0.25  # seconds between requests to avoid TMDB rate limit

# ----------------------------
# Create SQLAlchemy engine
# ----------------------------
engine = create_engine("postgresql+psycopg2://postgres:psql%402026@localhost/movie_recommender")

# ----------------------------
# Fetch movies that don't have poster yet
# ----------------------------
query = text(f"""
SELECT * FROM movies
WHERE poster_path IS NULL
LIMIT {BATCH_SIZE};
""")

movies_to_fetch = pd.read_sql(query, engine)
print(f"Fetching posters for {len(movies_to_fetch)} movies...")

# ----------------------------
# Function to fetch poster path
# ----------------------------
def fetch_poster(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    params = {"api_key": API_KEY}
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return TMDB_IMAGE_BASE + poster_path
        else:
            return None
    except Exception as e:
        print(f"Error fetching movie {tmdb_id}: {e}")
        return None
    finally:
        time.sleep(THROTTLE_TIME)  # throttle to avoid rate limit

# ----------------------------
# Run in parallel
# ----------------------------
results = []
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(fetch_poster, tmdb_id): tmdb_id for tmdb_id in movies_to_fetch['tmdb_id']}
    
    for i, future in enumerate(as_completed(futures), start=1):
        tmdb_id = futures[future]
        poster = future.result()
        results.append((tmdb_id, poster))
        
        # Constant progress update
        if i % 100 == 0 or i == len(futures):
            print(f"{i}/{len(futures)} movies processed...")

# ----------------------------
# Update database directly
# ----------------------------
with engine.connect() as conn:
    for tmdb_id, poster_path in results:
        if poster_path:  # only update if poster is found
            conn.execute(
                text("UPDATE movies SET poster_path = :poster WHERE tmdb_id = :tmdb_id"),
                {"poster": poster_path, "tmdb_id": tmdb_id}
            )
    conn.commit()

print("Posters updated in database successfully!")