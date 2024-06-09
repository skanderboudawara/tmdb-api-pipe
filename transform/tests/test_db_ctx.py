import pytest
from psycopg2 import OperationalError
from psycopg2.extensions import STATUS_READY

from clib.db_ctx import SqlContext

class MockCursor:
    def __init__(self):
        self.rowcount = 0
        self.results = []

    def execute(self, query, query_arg=None):
        self.query = query
        self.query_arg = query_arg

    def fetchall(self):
        return self.results

    def fetchmany(self, size):
        return self.results[:size]

    def close(self):
        pass

class MockConnection:
    def __init__(self, status=STATUS_READY):
        self.status = status
        self.cursor_instance = MockCursor()

    def cursor(self):
        return self.cursor_instance

    def commit(self):
        pass

    def close(self):
        pass

@pytest.fixture
def mock_connect(monkeypatch):
    def _mock_connect(*args, **kwargs):
        return MockConnection()
    monkeypatch.setattr('lib.db_ctx.connect', _mock_connect)

@pytest.fixture
def mock_connect_failure(monkeypatch):
    def _mock_connect(*args, **kwargs):
        raise OperationalError("Unable to connect to the database")
    monkeypatch.setattr('lib.db_ctx.connect', _mock_connect)

@pytest.fixture
def mock_connect_not_ready(monkeypatch):
    def _mock_connect(*args, **kwargs):
        return MockConnection(status=None)
    monkeypatch.setattr('lib.db_ctx.connect', _mock_connect)

def test_sql_context_initialization(mock_connect):
    context = SqlContext('localhost', 'user', 'password', 'database', '5432')
    assert context.connection.status == STATUS_READY

def test_sql_context_initialization_failure(mock_connect_failure):
    with pytest.raises(OperationalError):
        SqlContext('localhost', 'user', 'password', 'database', '5432')

def test_sql_context_execute_query(mock_connect):
    context = SqlContext('localhost', 'user', 'password', 'database', '5432')
    query = "SELECT * FROM table"
    context.connection.cursor_instance.results = [(1, 'result1'), (2, 'result2')]

    count_rows, results = context.execute_query(query)
    assert count_rows == 0
    assert results == [(1, 'result1'), (2, 'result2')]

def test_sql_context_execute_query_no_fetch(mock_connect):
    context = SqlContext('localhost', 'user', 'password', 'database', '5432')
    query = "INSERT INTO table (col1) VALUES (%s)"
    context.execute_query(query, fetch=False)
    assert context.connection.cursor_instance.query == query

def test_sql_context_check_connection(mock_connect, capsys):
    context = SqlContext('localhost', 'user', 'password', 'database', '5432')
    context.check_connection()
    captured = capsys.readouterr()
    assert "The connection is ready for use." in captured.out

def test_sql_context_check_connection_not_ready(mock_connect_not_ready, capsys):
    context = SqlContext('localhost', 'user', 'password', 'database', '5432')
    context.check_connection()
    captured = capsys.readouterr()
    assert "The connection is not ready." in captured.out
