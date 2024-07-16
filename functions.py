from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Final
import environ
env = environ.Env()
environ.Env.read_env()
import pyrebase


TOKEN: Final = env("TOKEN")
BOT_USERNAME: Final = env("BOT_USERNAME")

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
all_movies = db.child("movies").get()

movies_info = []
current_page = 0


def format_movie_response(movies, start_index=0, limit=10):
    response = ""
    end_index = start_index + limit
    for movie in movies[start_index:end_index]:
        response += f"Name: {movie['Title']}\n"
        response += f"Year: {movie['Year']}\n"
        response += f"Genre: {movie['Genre']}\n"
        response += f"Rate: {movie['Rate']}\n\n"

    return response


def create_pagination_buttons(current_page, total_movies, limit=10):
    buttons = []
    if current_page > 0:
        buttons.append(InlineKeyboardButton("Previous", callback_data=f"page_{current_page-1}"))
    if (current_page + 1) * limit < total_movies:
        buttons.append(InlineKeyboardButton("Next", callback_data=f"page_{current_page+1}"))
    return InlineKeyboardMarkup([buttons])


def get_movie_info_by_name(movie_name):
    matching_movies = []
    for movie in all_movies.each():
        if movie_name.lower() in movie.val()["Title"].lower():
            matching_movies.append(movie.val())
    return matching_movies

def parse_movie_rate(input_str):
    try:
        if '-' in input_str:
            start, end = map(int, input_str.split('-'))
            return [start, end]
        else:
            rate = int(input_str)
            return [rate, rate]
    except ValueError:
        print("Invalid input format. Please enter a valid number or range like '1-10' or '5'.")
        return None

def get_movie_info_by_rate(movie_rate):
    parsed_movie_rate = parse_movie_rate(movie_rate)

    if parsed_movie_rate is None:
        return 'no rate'

    list_of_movies = []
    for movie in all_movies.each():
        rate = movie.val()['Rate']
        print(f"rate is {rate}")
        if parsed_movie_rate[0] <= abs(rate) <= parsed_movie_rate[-1]:
            list_of_movies.append(movie.val())
            print(len(list_of_movies))
    return list_of_movies
