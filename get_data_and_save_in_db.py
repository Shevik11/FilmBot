import pyrebase
import requests
import time

# Конфігурація Firebase
config = {
    'apiKey': "AIzaSyBeNxsdVMVXIDyrw_geVSYohwAlMyTVxXU",
    'authDomain': "filmbot-6a5ad.firebaseapp.com",
    'databaseURL': "https://filmbot-6a5ad-default-rtdb.firebaseio.com",
    'projectId': "filmbot-6a5ad",
    'storageBucket': "filmbot-6a5ad.appspot.com",
    'messagingSenderId': "1052576779841",
    'appId': "1:1052576779841:web:56a4e5c0df9a9d68da40c0",
    'measurementId': "G-4FX5J8KGWQ"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# API ключ TMDB
tmdb_api_key = '464988569c44e84ca184b0038c4ba74c'


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


# Збираємо всі доступні фільми
page = 1
total_movies = 0

while True:
    print(f"Обробка сторінки {page}")
    result = get_popular_movies(page)

    if not result or 'results' not in result or not result['results']:
        print("Більше фільмів не знайдено. Завершення.")
        break

    movies = result['results']

    for movie in movies:
        movie_data = get_movie_data(movie['id'])
        if movie_data:
            movie_entry = {
                'Title': movie_data['title'],
                'Year': movie_data['release_date'][:4] if movie_data['release_date'] else 'Невідомо',
                'Genre': ', '.join([genre['name'] for genre in movie_data['genres']]),
                'Rate': movie_data['vote_average']
            }
            db.child('movies').push(movie_entry)
            print(f"Додано фільм: {movie_entry['Title']}")
            total_movies += 1

    page += 1

    # Затримка, щоб не перевищити ліміт запитів до API
    time.sleep(1)

    # Перевірка, чи досягнуто кінця списку фільмів
    if 'total_pages' in result and page > result['total_pages']:
        print("Досягнуто кінця списку фільмів.")
        break

print(f'Всього додано {total_movies} фільмів до Firebase!')