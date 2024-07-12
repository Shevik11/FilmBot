import pyrebase
import requests
import time

import environ

env = environ.Env()
environ.Env.read_env()

# Firebase configuration
config = {
    "apiKey": env("API_KEY"),
    "authDomain": env("AUTH_DOMAIN"),
    "databaseURL": env("DATABASE_URL"),
    "projectId": env("PROJECT_ID"),
    "storageBucket": env("STORAGE_BUCKET"),
    "messagingSenderId": env("MESSAGING_SENDER_ID"),
    "appId": env("APP_ID"),
    "measurementId": env("MEASUREMENT_ID"),
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# API ключ TMDB
tmdb_api_key = env("TMDB_API_KEY")


def get_movie_data(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}&language=uk"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_popular_movies(page=1):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={tmdb_api_key}&language=uk&page={page}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Collect all accessible films
page = 1
total_movies = 0

while True:
    print(f"check page {page}")
    result = get_popular_movies(page)

    if not result or "results" not in result or not result["results"]:
        print("No more films. End.")
        break

    movies = result["results"]

    for movie in movies:
        movie_data = get_movie_data(movie["id"])
        if movie_data:
            movie_entry = {
                "Title": movie_data["title"],
                "Year": (
                    movie_data["release_date"][:4]
                    if movie_data["release_date"]
                    else "undefined"
                ),
                "Genre": ", ".join([genre["name"] for genre in movie_data["genres"]]),
                "Rate": movie_data["vote_average"],
            }
            db.child("movies").push(movie_entry)
            print(f"Додано фільм: {movie_entry['Title']}")
            total_movies += 1

    page += 1

    # stop time
    time.sleep(1)

    # check if list end
    if "total_pages" in result and page > result["total_pages"]:
        print("End of list.")
        break

print(f"Total number: {total_movies} films to Firebase!")
