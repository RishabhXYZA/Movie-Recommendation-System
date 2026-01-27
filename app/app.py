from flask import Flask, render_template, request, redirect, url_for,jsonify
import random
from tmdb_api import get_movie_details, get_movie_credits
from recommender import get_recommendations
import pickle
import pandas as pd
import os

app = Flask(__name__)

# LOAD MOVIES FOR HOME PAGE
movie_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movie_dict)


# -------------------------------
# HOME PAGE (15 RANDOM MOVIES)
# -------------------------------
@app.route("/")
def home():
    random_movies = movies.sample(15)

    movie_cards = []
    for _, row in random_movies.iterrows():
        details = get_movie_details(int(row["movie_id"]))
        if details:
            movie_cards.append({
                "id": details["id"],
                "title": details["title"],
                "poster": details["poster"]
            })

    return render_template("home.html", movies=movie_cards)


# -------------------------------
# MOVIE DETAILS PAGE
# -------------------------------
@app.route("/movie/<int:movie_id>")
def movie_page(movie_id):

    movie = get_movie_details(movie_id)
    cast, director = get_movie_credits(movie_id)

    movie["cast"] = cast
    movie["director"] = director

    recommended_ids = get_recommendations(movie_id)

    recommendations = []
    for rid in recommended_ids:
        rec = get_movie_details(rid)
        if rec:
            recommendations.append(rec)

    return render_template(
        "movie.html",
        movie=movie,
        recommendations=recommendations
    )

# -------------------------------
# ABOUT SECTION
# -------------------------------
@app.route("/about")
def about():
    return render_template("about.html")


# -------------------------------
# AUTOCOMPLETE SEARCH
# -------------------------------
@app.route("/autocomplete")
def autocomplete():
    query = request.args.get("q", "").strip().lower()

    if len(query) < 2:
        return jsonify([])

    results = movies[
        movies["title"].str.lower().str.contains(query)
    ].head(8)

    suggestions = [
        {
            "id": int(row["movie_id"]),
            "title": row["title"]
        }
        for _, row in results.iterrows()
    ]

    return jsonify(suggestions)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
