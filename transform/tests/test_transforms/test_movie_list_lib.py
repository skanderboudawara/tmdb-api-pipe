import pytest
import json
from lib.transforms.movie_list_lib import MovieList

@pytest.fixture
def mock_tmdb_response(monkeypatch):
    def _mock_tmdb_response(url):
        class MockResponse:
            def __init__(self, json_data):
                self.text = json.dumps(json_data)
        
        if "page=1" in url:
            return MockResponse({
                "total_pages": 2,
                "results": [{"id": 1, "adult": False}, {"id": 2, "adult": True}]
            })
        elif "page=2" in url:
            return MockResponse({
                "total_pages": 2,
                "results": [{"id": 3, "adult": False}]
            })
        return MockResponse({"total_pages": 1, "results": []})

    monkeypatch.setattr('lib.api_ctx.tmdb_response', _mock_tmdb_response)

@pytest.fixture
def mock_sql_context(monkeypatch):
    class MockCursor:
        def execute(self, query, query_arg):
            self.query = query
            self.query_arg = query_arg
        def close(self):
            pass
        def fetchall(self):
            return []
        def fetchmany(self, limit):
            return []

    class MockConnection:
        def cursor(self):
            return MockCursor()
        def commit(self):
            pass
        def close(self):
            pass

    def _mock_connect(*args, **kwargs):
        return MockConnection()

    monkeypatch.setattr('lib.db_ctx.connect', _mock_connect)

def test_movie_list_initialization():
    movie_list = MovieList(fetch_all=True)
    assert movie_list.fetch_all is True
    assert isinstance(movie_list.movies, dict)

def test_get_tmdb_movie_list(mock_tmdb_response):
    response = MovieList.get_tmdb_movie_list(1)
    assert response is not None
    assert 'total_pages' in response
    assert 'results' in response
    assert len(response['results']) == 100

def test_fetch_all_movies(mock_tmdb_response, mock_sql_context):
    movie_list = MovieList(fetch_all=True)
    movie_list.fetch()

    assert len(movie_list.movies) == 3
    assert movie_list.movies[0]['id'] == 1
    assert movie_list.movies[1]['id'] == 2
    assert movie_list.movies[2]['id'] == 3

def test_sql_insertion(mock_tmdb_response, mock_sql_context, monkeypatch):
    queries_executed = []

    def mock_execute_query(self, query, query_arg=None, fetch=True, offset=None, limit=None):
        queries_executed.append((query, query_arg))

    monkeypatch.setattr('lib.db_ctx.SqlContext.execute_query', mock_execute_query)

    movie_list = MovieList(fetch_all=True)
    movie_list.fetch()

    assert len(queries_executed) == 3
    for query, query_arg in queries_executed:
        assert query == """
                INSERT INTO public.movie_list 
                    (movie_id, is_movie_adult) 
                VALUES 
                    (%(movie_id)s, %(is_movie_adult)s)
                ON CONFLICT (movie_id) DO NOTHING;
            """
        assert query_arg is not None
        assert 'movie_id' in query_arg
        assert 'is_movie_adult' in query_arg
