import requests
import json
from dotenv import load_dotenv
import os
import urllib
import re

# Load environment variables from .env file
load_dotenv()
# TMDb API key (replace with your own API key)
API_KEY = os.getenv("TMDB_API_KEY")
TMDB_TOKEN = os.getenv("TMDB_TOKEN")
DIRECTORY = "tools_set/13_movie_recommendations"
class TMDBApiClient(object):
    """
    Client for api calls
    """
    def __init__(self):
        self.headers = {"Content-Type": "application/json;charset=utf-8",
                         "Authorization": f"Bearer {TMDB_TOKEN}"
                        }
        self.base_url = "https://api.themoviedb.org/3/"

    
    def _make_url(self, path):
        try:
            url = urllib.parse.urljoin(self.base_url, path) 
            return url       
        except Exception as ex:
            print(f'Error creating url {self.base_url} {path} {ex}')

    def get(self, path, params=None):
        """
        Executes the get request with the given path and params returns json response
        """
        url = self._make_url(path)
        try:
            r = requests.get(url, headers=self.headers, params=params)
            return r.json()
        except Exception as ex:
            print(f'Error connecting with {url} - {ex}')

    def post(self, path, data, params=None):
        """
        Executes the post request with the given path and params and data returns json response
        """
        url = self._make_url(path)
        try:
            r = requests.post(url, headers=self.headers, params=params, json=data)
            return r.json()
        except Exception as ex:
            print(f'Error connecting with {url} - {ex}')


api_cli = TMDBApiClient()


def get_movie_id(movie_name, year):
    """
    Function to search for movie ID by name and year
    https://developer.themoviedb.org/reference/search-movie
    """
    path = "search/movie"
    params = {
        "api_key": API_KEY,
        "query": movie_name,
        "year": year
    }

    response = api_cli.get(path, params=params)
    results = response.get("results", [])
    if results:
        return results[0]["id"]  # Return the first match


def add_movie_rating(movie_id, rating):
    """
    Function to add rating to a movie
    https://developer.themoviedb.org/reference/movie-add-rating
    """
    path = f"movie/{movie_id}/rating"
    
    data = {
        "value": rating
    }
    response  = api_cli.post(path, data=data)
    if response['status_code'] == 1:
        return True
    else:
        print(f"Failed to add rating for movie ID {movie_id}: {response.json()}")
        return False


def process_movies_add_ratings():
    movies = get_movies('rating-movies')
    # Process each movie
    for item in movies:
        movie = item["movie"]
        movie_name = movie['title']
        rating = item["rating"]
        tmdb_id = movie["ids"]["tmdb"]
            
            # Add rating to TMDb
        if add_movie_rating(tmdb_id, rating):
            print(f"Successfully added rating {rating} for {movie_name}")
       
def find_recommendations(minimum_rating_watched=7, minimum_rating_recommendations=6, excluded_categories=[]):
    # https://developer.themoviedb.org/reference/movie-recommendations
    movies = get_movies('rating-movies')
    watched_movies_ids = get_movies_ids(movies)
    filtred_movie_ids = get_movies_ids(movies, minimum_rating_watched)

    filtred_recommendations = dict()    

    contador = 0
    total = len(filtred_movie_ids)
    for movie_id in filtred_movie_ids:
        contador += 1
        print(F'Getting recommendations: {contador} of {total}')
        path = f"movie/{movie_id}/recommendations"        

        response = api_cli.get(path, params={"page": 1})
        total_pages = response['total_pages']

        filter_movie_recommendations(response['results'], watched_movies_ids, filtred_recommendations, minimum_rating_recommendations, excluded_categories)

        if total_pages > 1:
            # we must get the results on the other pages too starting from the second now:
            for i in range(2, total_pages):
                response = response = api_cli.get(path, params={"page": {i}})
                filter_movie_recommendations(response['results'], watched_movies_ids, filtred_recommendations, minimum_rating_recommendations, excluded_categories)
                
    return filtred_recommendations


def get_movies_ids(movies, minimum_rating_watched=0):
    if minimum_rating_watched == 0:
        # we dont filter by ratings return all ids
        return set(item["movie"]["ids"]["tmdb"] for item in movies)
    else:
        # get the movie ids filtering rating bigger than the minimum_rating_watched
        return set(item["movie"]["ids"]["tmdb"] for item in movies if item['rating'] >= minimum_rating_watched)


def filter_movie_recommendations(recommendations, watched_movies_ids, filtred_recommendations, minimum_rating=6, excluded_categories=[]):
    """
    Filter the movie recomentadions that the rating is bigger or equals to minimun_rating 
    and the movie is not in the list of watched movies 
    """
    for movie in recommendations:
        movie_id = movie['id']
        if movie_id not in filtred_recommendations:
            # si ya esta entre los recomentados no anadimos de nuevo
            language = movie['original_language']
            if language in ('es', 'pt', 'en'):
                rating = movie['vote_average']    
                if rating >= minimum_rating and movie_id not in watched_movies_ids:
                    # if the rating is bigger than the minimum rating and the movie is not in the watched movies 
                    # add to the dict of filtred_recommendations
                    categories = movie['genre_ids']
                    if any(category in excluded_categories for category in categories):
                        # this movie has at least one category that we dont want i dont add it to the list
                        continue

                    filtred_recommendations[movie_id] = {'title': movie['original_title'],
                                                         'rating':rating,
                                                         'language':language,
                                                         'popularity':movie['popularity'] ,
                                                         'release_date': movie['release_date'],
                                                         'vote_count': movie['vote_count']}

def get_movies(file_name):
    with open(f'{DIRECTORY}/{file_name}.json', 'r', encoding='utf-8') as file:
        movies = json.load(file)
    return movies

def get_existing_recommendation_files():
    """Get list of existing JSON files specifically named 'recommendations_N.json'."""
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
    # Only match files exactly like 'recommendations_\d+\.json'
    files = [f for f in os.listdir(DIRECTORY) if re.match(r'^recommendations_\d+\.json$', f)]
    return sorted(files, key=lambda x: int(re.search(r'_(\d+)\.json$', x).group(1)))

def get_next_file_number(files):
    """Determine the next file number for a new JSON file."""
    if not files:
        return 1
    last_file = files[-1]
    last_number = int(re.search(r'_(\d+)\.json$', last_file).group(1))
    return last_number + 1

def write_recommendations(filtred_recommendations, filename):
    # Write to recommendations to JSON file
    filepath = f'{DIRECTORY}/{filename}'

    sorted_recommendations = dict(
    sorted(
        filtred_recommendations.items(),
        key=lambda x: (-x[1]['rating'], -x[1]['popularity'], x[1]['language'])
    )
    )

    with open(filepath, 'w') as f:
        json.dump(sorted_recommendations, f, indent=4)
    print(f"Recommendations saved to {filepath}")

def save_recommendations(filtred_recommendations):
    """Save movie recommendations to a JSON file."""

    if len(filtred_recommendations):
        filename = get_recommendation_file_name()
        if filename is not None:
            write_recommendations(filtred_recommendations, filename)
    else:
        print('No recommendations found, try to add movies to list of rating-movies')
    
    

def get_recommendation_file_name():
    files = get_existing_recommendation_files()

    if not files:
        # No existing files, create new one
        filename = f'recommendations_1.json'
    else:
        # ask if wants to overwrite or create new one
        print("Want to overwrite an existing file or create a new one? (C: Create new file, O: Overwrite existing file)")
        overwrite = input()
        if overwrite.upper() == 'O':
            # Multiple files, ask which to overwrite
            if len(files) == 1:
                filename = files[0]
            else:
                print("Existing recommendations files:")
                for i, f in enumerate(files, 1):
                    print(f"{i}: {f}")
                print("Which file to overwrite? (Enter number or 'cancel'): ")
                choice = input('  ')
                if choice.lower() == 'cancel':
                    print("Operation cancelled.")
                    return
                try:
                    file_index = int(choice) - 1
                    if 0 <= file_index < len(files):
                        filename = files[file_index]
                    else:
                        print("Invalid number. Operation cancelled.")
                        return
                except ValueError:
                    print("Invalid input. Operation cancelled.")
                    return
        else:
            # Create new file with next number
            next_number = get_next_file_number(files)
            filename = f'recommendations_{next_number}.json'

    return filename


def print_filtred_recommendations(file_number, minimun_rating=0, minimum_popularity=0, language='', minimum_year=0, minimum_vote_count=0):
    filename = f'recommendations_{file_number}'
    movies = get_movies(filename)    

    filtred_movies = dict()

    for movie_id, movie in movies.items():
        if minimun_rating != 0:
            if movie['rating'] < minimun_rating:
                continue
        if minimum_popularity != 0:
            if movie['popularity'] < minimum_popularity:
                continue
        if language != '':
            if movie['language'] != language:
                continue

        if minimum_year != 0:
            year = int(movie['release_date'].split('-')[0])
            if year < minimum_year:
                continue
        if minimum_vote_count != 0:
            if movie['vote_count'] < minimum_vote_count:
                continue
        
        filtred_movies[movie_id] = movie

    print(json.dumps(filtred_movies, indent=4))



# process_movies_add_ratings()


# 878 Science Fiction
# 16 Animation
# 14 Fantasy
# 27 Horror
filtred_recommendations = find_recommendations(excluded_categories=[878, 27, 16, 14])
save_recommendations(filtred_recommendations)


print_filtred_recommendations(1, minimun_rating=8, minimum_popularity=1, minimum_vote_count=1000, minimum_year=2000)