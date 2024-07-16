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


# lister=0
# for x in all_movies:
#     lister += 1
#     print(lister)

# def remove_duplicates(collection_name, field_name):
#     # Отримуємо всі дані з вказаної колекції
#     data = db.child(collection_name).get().val()
#
#     if data:
#         unique_values = set()
#         duplicate_keys = []
#
#         for key, value in data.items():
#             field_value = value.get(field_name)
#
#             if field_value in unique_values:
#                 duplicate_keys.append(key)
#             else:
#                 unique_values.add(field_value)
#
#         for key in duplicate_keys:
#             db.child(collection_name).child(key).remove()
#             print(f"Deleted duplicate record with {field_name}: {key}")
#     else:
#         print("No data found in the collection.")
#
# # Приклад виклику функції для колекції 'movies' і поля 'title'
# remove_duplicates('movies', 'Title')