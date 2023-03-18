import requests
from enum import Enum
import json


class QueryType(Enum):
    Movie = 0
    Query = 1


def call_themoviedb_api(query, queryType):

    # Read in api key from configuration file
    with open('config.json') as file:
        _config = json.load(file)

    api_key = _config['themoviedb_api']

    # Construct query string
    url = "https://api.themoviedb.org/3/"

    match queryType:
        case QueryType.Movie:  # Movie
            url = url + 'movie/{}?api_key={}&language=en-US'.format(query, api_key)
        case QueryType.Query:  # Query
            url = url + 'search/movie?api_key={}&query={}'.format(api_key, query)

    result = requests.get(url)

    data = result.json()

    return data


def movie_search():
    # Asks user to enter the title of a film
    _query = input("Please enter the title of the film you would like to find:  ")
    results = call_themoviedb_api(_query, QueryType.Query)

    print(results)

    if len(results["results"]) == 0:
        print("No search results found.")
        return

    for result in results["results"]:
        title = result["title"]
        id = result["id"]
        release_date = result["release_date"]
        # Prints results of the search with every movie containing the words from the query
        print("Movie title: {}".format(title))
        # Release date included to make it easier for users to find the right movie
        print("Movie release: {}".format(release_date))
        print("Movie id: {}".format(id))
        print()

    while True:
        try:
            movie_id = int(
                input("Please now enter the ID of the film you would like to find: "))
            break
        except ValueError:
            print("That's not a movie ID. Please enter a number.")

    # Now asks the user to enter the ID from the list they have been given.
    results = call_themoviedb_api(movie_id, QueryType.Movie)

    items = [
        'title', 'homepage', 'overview', 'release_date', 'runtime', 'budget'
    ]  # creates list for text file
    
    genre_names = []
    for genre in results["genres"]:
        genre_names.append(genre['name'])
    genres = ", ".join(genre_names)

    production_company_names = []
    for company in results['production_companies']:
        production_company_names.append(company['name'])
    production_companies = ", ".join(production_company_names)

    # writes and appends text file so programme can be run multiple times
    with open('{}.txt'.format(results['title']), 'a+') as text_file:
        for item in items:
            text_file.write(item.capitalize() + ': ' + str(results[item]) + '\n')
        text_file.write('Genres: ' + genres + '\n')
        text_file.write('Production Companies: ' + production_companies + '\n')

    # Prints results into console
    print("Movie title: {}".format(results['title']))
    print("Homepage: {}".format(results['homepage']))
    print("Genres: {}".format(genres))
    print("Movie overview: {}".format(results['overview']))
    print("Release_date: {}".format(results['release_date']))
    print("Run time: {} minutes".format(results['runtime']))
    print("Production companies: {}".format(production_companies))
    print("Movie budget: ${}".format(results['budget']))


movie_search()
# can be ran multiple times and information will copy into text file
