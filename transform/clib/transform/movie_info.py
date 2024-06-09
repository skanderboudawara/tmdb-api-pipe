"""
This library manages the movie list db creation
"""

import json
from typing import Optional
from ..db_ctx import SqlContext, get_credentials
from ..api_ctx import tmdb_response
import datetime

class DateTimeEncoder(json.JSONEncoder):
    """
    This class is used to manage the DateTime values in the JSON dict
    """
    def default(self, obj: any) -> any:
        """
        This method is responsible on converting the datetime object to isoformat
        
        :param obj: (any), if datatime -> isofroma else keep as is
        
        :returns: (any), converted object
        """
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)


class MovieInfo():
    """
    This class is used to recreate MovieList
    
    :param fetch_all: (boolean), to fetch the information of all the information. Default True.
    :param force_update: (boolean), to update previous retreivied data. Default False.
    :param movie_id: (int), to update a specific movie id when fetch_all is False. Default to None.
    
    :returns: none
    """
    def __init__(
        self,
        fetch_all   : Optional[bool] = True,
        force_update: Optional[bool] = False,
        movie_id    : Optional[int] = None
    ) -> None:
        if not isinstance(fetch_all, bool):
            raise TypeError("fetch_all must be a boolean")
        if not isinstance(force_update, bool):
            raise TypeError("force_update must be a boolean")
        if movie_id and not isinstance(movie_id, int):
            raise TypeError("movie_id must be an integer")
        if movie_id and fetch_all:
            raise ValueError("When movie_id is assigne fetch_all must be False")
        self.force_update = force_update
        if fetch_all:
            with SqlContext(**get_credentials()) as sql_context:
                self.count_processing, self.movie_ids = sql_context.execute_query(
                  query="SELECT * FROM public.get_movie_ids(%(force_update)s);",
                  query_arg={"force_update": self.force_update},
                )
                self.movie_ids = self.movie_ids[0][0]
        if movie_id:
            self.movie_ids = [movie_id]

    @staticmethod
    def get_tmdb_movie_info(move_id: int) -> dict:
        """
        This static method will retrive the movie information based on the movie id
        
        :param page: (int), page number
        
        :returns: (dict), api response
        """
        if not isinstance(move_id, int):
            raise TypeError("movie_id must be an integer")
        url = f"https://api.themoviedb.org/3/movie/{move_id!s}?language=en-US"

        response = tmdb_response(url)
        
        return json.loads(response.text) if response else None

    def fetch(self) -> None:
        """
        This method is dedicated to fetch the information of each movie based on movie_id
        
        - Request the information of the movie id
        - Format the response
        
        :param: None
        
        :returns: None
        """
        for index, movie_id in enumerate(self.movie_ids):
          print(f"[{index!s}] - {movie_id!s}")
          movie_info = self.get_tmdb_movie_info(int(movie_id))
          if not movie_info or not self.check_info(movie_info):
            print("fail")
            continue
          print("pass")
          movie_info = self.reformat_info(movie_info)
          with SqlContext(**get_credentials()) as sql_context:
            query = """
                CALL public.insert_or_update_movie_info(%(movie_id)s, %(dict_params)s::json, %(force_update)s)
            """
            sql_context.execute_query(
                query=query,
                query_arg={
                  "movie_id" : movie_id,
                  "dict_params" : json.dumps(movie_info, cls=DateTimeEncoder),
                  "force_update" : self.force_update,
                },
                fetch=False,
            )
            
    @staticmethod
    def check_info(info: dict) -> None:
        """
        This method check the types of each information before processing
        
        :param info: (dict), dict to test types
        
        :returns: (bool), if a dict do not respect the needed type it will return False else True
        """
        types_mockup = {
            "id": int,
            "genres": list,
            "imdb_id": str,
            "original_title": str,
            "overview": str,
            "popularity": float,
            "runtime": int,
            "budget": int,
            "revenue": int,
            "release_date": str,
            "status": str,
            "vote_average": float,
            "vote_count": int
        }
        for info_name, info_type in types_mockup.items():
            if info[info_name] and not isinstance(info[info_name], info_type):
                print(f"{info_name} has not the right type {info_type}")
                return False
        return True

    @staticmethod
    def reformat_info(info):
      """
      This method will reformat the API response to a preformatted dict to be ingested by PostgreSQL db
      
      :param info: (dict), dict input
      
      :returns: (dict), dict output
      """
      if not isinstance(info, dict):
          raise TypeError("info must be  dict")
      return {
          "movie_id"       : info["id"],
          "genres"         : [genre["name"] for genre in info["genres"]] if info["genres"] else None,
          "imdb_id"        : str(info["imdb_id"]),
          "original_title" : info["original_title"],
          "overview"       : info["overview"],
          "popularity"     : info["popularity"],
          "runtime"        : info["runtime"],
          "budget"         : info["budget"],
          "revenue"        : info["revenue"],
          "release_date"   : datetime.datetime.strptime(info["release_date"], "%Y-%m-%d").date() if info["release_date"] else None,
          "status"         : info["status"],
          "vote_average"   : info["vote_average"],
          "vote_count"     : info["vote_count"],
      }

