import os
import requests
from functools import lru_cache
# ===============================
# TMDB CONFIG (DEPLOYMENT SAFE)
# ===============================

API_KEY = os.getenv("TMDB_API_KEY")

IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
FALLBACK_POSTER = "https://via.placeholder.com/300x450?text=No+Poster"

if not API_KEY:
    raise ValueError("TMDB_API_KEY not found in environment variables")


# ===============================
# FETCH MOVIE DETAILS
# ===============================
@lru_cache(maxsize=500)
def get_movie_details(movie_id):

    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}"
        f"?api_key={API_KEY}&language=en-US"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

    except Exception as e:
        print(f"TMDB ERROR (details) → {movie_id}: {e}")
        return None

    return {
        "id": movie_id,
        "title": data.get("title"),
        "overview": data.get("overview"),
        "runtime": data.get("runtime"),
        "release_year": data.get("release_date", "")[:4],
        "genres": ", ".join(
            [g["name"] for g in data.get("genres", [])]
        ),
        "vote_average": round(data.get("vote_average", 0), 1),
        "stars": round(data.get("vote_average", 0) / 2, 1),
        "poster": (
            IMAGE_BASE_URL + data["poster_path"]
            if data.get("poster_path")
            else FALLBACK_POSTER
        ),
    }


# ===============================
# FETCH CAST & CREW
# ===============================
@lru_cache(maxsize=500)
def get_movie_credits(movie_id):

    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
        f"?api_key={API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

    except Exception as e:
        print(f"TMDB ERROR (credits) → {movie_id}: {e}")
        return "N/A", "N/A"

    cast = ", ".join(
        [c["name"] for c in data.get("cast", [])[:5]]
    )

    director = next(
        (c["name"] for c in data.get("crew", [])
         if c["job"] == "Director"),
        "N/A"
    )

    return cast, director
