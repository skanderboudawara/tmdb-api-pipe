"""
This library manages the movie list db creation
"""

import json
from typing import Optional
from ..db_ctx import SqlContext, get_credentials
from ..api_ctx import tmdb_response

class MovieList():
    """
    This class is used to recreate MovieList
    
    :param fetch_all: (bool), to fetch all information from all pages. Else a single page. Default False.
    
    :returns: None
    """
    def __init__(self, fetch_all: Optional[bool] = False) -> None:
        if not isinstance(fetch_all, bool):
            raise TypeError("fetch_all must be a boolean")
        self.fetch_all = fetch_all
        self.movies = {}

    @staticmethod
    def get_tmdb_movie_list(page: int) -> dict:
        """
        This static method will retrive the list of movies based on the page
        
        :param page: (int), page number
        
        :returns: (dict), api response
        """
        if not isinstance(page, int):
            raise TypeError("page must be an integer")
        url = f"https://api.themoviedb.org/3/movie/changes?page={page!s}"

        response = tmdb_response(url)
        
        return json.loads(response.text) if response else None

    def fetch(self) -> None:
        """
        This method will query the API response for List of movies. Default first page.
        
        If fetch_all is True, a recursion will be performed on all the pages
        
        :param: None
        
        :returns: None
        """
        actual_page = 1
        api_response = self.get_tmdb_movie_list(actual_page)
        total_pages = api_response["total_pages"]
        self.movies = api_response["results"]

        if self.fetch_all:
            while actual_page < total_pages:
                actual_page += 1
                api_response = self.get_tmdb_movie_list(actual_page)
                self.movies += api_response["results"]
                print(f"processed page {actual_page!s}, movies to be processed {len(self.movies)!s}")

        with SqlContext(**get_credentials()) as sql_context:
            query = """
                INSERT INTO public.movie_list 
                    (movie_id, is_movie_adult) 
                VALUES 
                    (%(movie_id)s, %(is_movie_adult)s)
                ON CONFLICT (movie_id) DO NOTHING;
            """
            for result in self.movies:
                sql_context.execute_query(
                    query=query,
                    query_arg={
                        "movie_id": result["id"],
                        "is_movie_adult": result["adult"],
                    },
                    fetch=False,
                )
