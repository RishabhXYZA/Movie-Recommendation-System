import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# LOAD DATA
movie_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movie_dict)

# BUILD SIMILARITY
cv = CountVectorizer(max_features=5000, stop_words="english")
vectors = cv.fit_transform(movies["tag"]).toarray()
similarity = cosine_similarity(vectors)


def get_recommendations(movie_id, top_n=5):
    """
    Returns list of TMDB movie IDs
    """
    index = movies[movies["movie_id"] == movie_id].index

    if len(index) == 0:
        return []

    idx = index[0]
    distances = similarity[idx]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1 : top_n + 1]

    recommended_ids = [
        int(movies.iloc[i[0]]["movie_id"]) for i in movie_list
    ]

    return recommended_ids
