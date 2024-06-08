import pytest
import os
import requests
import pytest
import backoff

from lib.api_ctx import fatal_code, tmdb_response

class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code

def test_fatal_code_400(monkeypatch):
    mock_response = MockResponse(400)
    def mock_get_response():
        return mock_response
    assert fatal_code(mock_get_response()) is True

def test_fatal_code_404(monkeypatch):
    mock_response = MockResponse(404)
    def mock_get_response():
        return mock_response
    assert fatal_code(mock_get_response()) is True

def test_fatal_code_500(monkeypatch):
    mock_response = MockResponse(500)
    def mock_get_response():
        return mock_response
    assert fatal_code(mock_get_response()) is False

def test_fatal_code_200(monkeypatch):
    mock_response = MockResponse(200)
    def mock_get_response():
        return mock_response
    assert fatal_code(mock_get_response()) is False


class MockApiResponse:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or {}

    def json(self):
        return self._json_data

@pytest.fixture
def mock_get(monkeypatch):
    def _mock_get(url, headers, timeout):
        return MockApiResponse(200, {"key": "value"})
    monkeypatch.setattr(requests, 'get', _mock_get)

@pytest.fixture
def mock_get_failure(monkeypatch):
    def _mock_get(url, headers, timeout):
        return MockApiResponse(500)
    monkeypatch.setattr(requests, 'get', _mock_get)

@pytest.fixture
def mock_get_fatal(monkeypatch):
    def _mock_get(url, headers, timeout):
        return MockApiResponse(400)
    monkeypatch.setattr(requests, 'get', _mock_get)

@pytest.fixture
def mock_getenv(monkeypatch):
    monkeypatch.setattr(os, 'getenv', lambda x: 'dummy_token')

@pytest.fixture
def mock_fatal_code(monkeypatch):
    monkeypatch.setattr('lib.api_ctx.fatal_code', lambda x: False)

@pytest.fixture
def mock_fatal_code_true(monkeypatch):
    monkeypatch.setattr('lib.api_ctx.fatal_code', lambda x: 400 <= x.status_code < 500)

def test_tmdb_response_success(mock_get, mock_getenv):
    response = tmdb_response("http://dummyurl.com")
    assert response.status_code == 200
    assert response.json() == {"key": "value"}

def test_tmdb_response_failure(mock_get_failure, mock_getenv, mock_fatal_code):
    response = tmdb_response("http://dummyurl.com")
    assert response is None
