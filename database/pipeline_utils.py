def build_poster_url(poster_path):
    return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

def map_genres(genre_ids, genre_map):
    if not isinstance(genre_ids, list):
        return ""
    return " ".join(genre_map[i] for i in genre_ids if i in genre_map)

def squash_names(names):
    return " ".join(n.replace(" ", "") for n in names)

def build_tags(genres, cast, director, keywords, overview):
    return f"{genres} {cast} {director} {keywords} {overview or ''}".lower()