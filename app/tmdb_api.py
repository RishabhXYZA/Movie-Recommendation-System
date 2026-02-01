import os
import requests
import logging
from functools import lru_cache

# Set up logging for production visibility
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("TMDB_API_KEY")
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
FALLBACK_POSTER = "https://via.placeholder.com/300x450?text=No+Poster"

if not API_KEY:
    logger.error("CRITICAL: TMDB_API_KEY not found in environment variables!")
    # We don't raise ValueError here to allow the app to build, 
    # but features will return 'None' safely.

# Create a session to reuse connections (faster performance)
http = requests.Session()

@lru_cache(maxsize=500)
def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:
        response = http.get(url, timeout=7)
        response.raise_for_status() # Raises error for 4xx or 5xx
        data = response.json()
        
        return {
            "id": movie_id,
            "title": data.get("title", "Unknown Title"),
            "overview": data.get("overview", "No description available."),
            "runtime": data.get("runtime", 0),
            "release_year": data.get("release_date", "")[:4],
            "genres": ", ".join([g["name"] for g in data.get("genres", [])]),
            "vote_average": round(data.get("vote_average", 0), 1),
            "stars": round(data.get("vote_average", 0) / 2, 1),
            "poster": (IMAGE_BASE_URL + data["poster_path"]) if data.get("poster_path") else FALLBACK_POSTER,
        }
    except requests.exceptions.RequestException as e:
        logger.warning(f"TMDB Fetch Failed for ID {movie_id}: {e}")
        return None

@lru_cache(maxsize=500)
def get_movie_credits(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"

    try:
        response = http.get(url, timeout=7)
        response.raise_for_status()
        data = response.json()

        cast = ", ".join([c["name"] for c in data.get("cast", [])[:5]])
        director = next((c["name"] for c in data.get("crew", []) if c["job"] == "Director"), "N/A")
        return cast, director
        
    except requests.exceptions.RequestException:
        return "N/A", "N/A"
