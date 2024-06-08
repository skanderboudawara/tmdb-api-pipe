"""
This is the main processing that will call the api calls and filling the postgreSQL
"""
from lib.transforms.movie_list_lib import MovieList
from lib.transforms.movie_info_lib import MovieInfo

movies_transform = MovieList(True)
movies_transform.fetch()

movies_info_transform = MovieInfo()
movies_info_transform.fetch()
