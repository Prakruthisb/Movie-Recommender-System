from database.pipeline_utils import build_poster_url, map_genres, squash_names, build_tags

GENRES = {28: "Action", 18: "Drama"}

def test_poster_url_built():
    assert build_poster_url("/abc.jpg") == "https://image.tmdb.org/t/p/w500/abc.jpg"

def test_poster_url_missing():
    assert build_poster_url(None) is None

def test_map_genres_skips_unknown_ids():
    assert map_genres([28, 999, 18], GENRES) == "Action Drama"

def test_map_genres_handles_bad_input():
    assert map_genres(None, GENRES) == ""

def test_squash_names_removes_spaces():
    assert squash_names(["Allu Arjun", "Rashmika Mandanna"]) == "AlluArjun RashmikaMandanna"

def test_build_tags_is_lowercase():
    tags = build_tags("Action", "AlluArjun", "Sukumar", "heist", "A Big Story")
    assert tags == tags.lower() and "sukumar" in tags

def test_build_tags_handles_missing_overview():
    assert "none" not in build_tags("Action", "", "", "", None)