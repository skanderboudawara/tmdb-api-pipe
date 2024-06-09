"""
This library is used to request API response

Backoff module is used to handle Exceptions errors.
"""
import backoff
import requests
import os
from typing import Union

def fatal_code(error_code: int) -> bool:
    """
    Fatal code of response backoff

    :params error_code: (int), response

    ::returns: (bool), error value response
    """
    if not isinstance(error_code, int):
        raise TypeError("error_code must be an integer")
    return 400 <= error_code.status_code < 500

@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_time=300,
    giveup=fatal_code,
)
def tmdb_response(url: str) -> Union[dict, None]:
    """
    Get the API response from tmdb
    
    :param url: (str), the API url to request
    
    :returns: Union[dict, None], if a response return a dict else None
    """
    if not isinstance(url, str):
        raise TypeError("url must be a string")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('BEARER_TOKEN')}"
    }

    response = requests.get(url, headers=headers, timeout=300)
    
    if response.status_code == 200:
        return response
    return None