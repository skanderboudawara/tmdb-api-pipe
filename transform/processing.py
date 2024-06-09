"""
This is the main processing that will call the api calls and filling the postgreSQL
"""
from clib.transform.movie_list import MovieList
from clib.transform.movie_info import MovieInfo

movies_transform = MovieList(True)
movies_transform.fetch()

movies_info_transform = MovieInfo()
movies_info_transform.fetch()
