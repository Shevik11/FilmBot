from database_connected import db
import random

all_movies = db.child("movies").get()

movies_info = []
current_page = 0


def get_movie_info_by_name(movie_name):
    matching_movies = []
    for movie in all_movies.each():
        if movie_name.lower() in movie.val()["Title"].lower():
            matching_movies.append(movie.val())
    return matching_movies

def get_movie_info_by_rate(movie_rate):
    matching_movies = []
    try:
        first_num, last_num = map(float, movie_rate.split('-'))
        for movie in all_movies.each():
            rate = float(movie.val()['Rate'])
            if first_num <= rate <= last_num:
                matching_movies.append(movie.val())
        if matching_movies:
            return random.choice(matching_movies)
        else:
            return None
    except ValueError:
        return None


def get_movie_info_by_year(movie_year):
    matching_movies = []
    movie_year = movie_year.strip()

    # Check if the input is a single year or a range
    if '-' in movie_year:
        # It's a range
        year_range = movie_year.split('-')
        if len(year_range) != 2:
            print("Invalid input format for year range. Please provide a range in the format 'YYYY-YYYY'.")
            return None

        # Get the first and last year
        first_num, last_num = year_range

        # Ensure both parts are exactly 4 digits long and are valid integers
        if not (first_num.isdigit() and len(first_num) == 4 and last_num.isdigit() and len(last_num) == 4):
            print("Invalid year format in range. Please ensure both years are in 'YYYY' format.")
            return None

        # Convert first_num and last_num to integers
        first_year = int(first_num)
        last_year = int(last_num)
    else:
        # It's a single year
        if not (movie_year.isdigit() and len(movie_year) == 4):
            print("Invalid year format. Please provide a year in 'YYYY' format.")
            return None

        # Convert to integer
        first_year = last_year = int(movie_year)

    # Print for debugging
    print(first_year)
    print(last_year)

    # Iterate over movies and find matches
    for movie in all_movies.each():
        year_str = movie.val().get('Year', '')
        if not year_str.isdigit():
            print(f"Skipping invalid year: {year_str}")
            continue

        year = int(year_str)
        if first_year <= year <= last_year:
            matching_movies.append(movie.val())

    print(f" that's {matching_movies}")
    if matching_movies:
        return random.choice(matching_movies)
    else:
        print("No matching movies found.")
        return None






def get_movie_info_by_genre(movie_genre):
    matching_movies = []

    # Convert user input genres to lowercase and strip whitespace
    user_genres = [genre.strip().lower() for genre in movie_genre.split(',')]

    for movie in all_movies.each():
        # Convert movie genres to lowercase and strip whitespace
        movie_genres = [genre.strip().lower() for genre in movie.val().get('Genre', '').split(',')]

        # Check if any of the user's genres are in the movie's genres
        if all(user_genre in movie_genres for user_genre in user_genres):
            matching_movies.append(movie.val())

    if matching_movies:
        return random.choice(matching_movies)
    else:
        return None
