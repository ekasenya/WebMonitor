import pytest

from data_handler.postgre_sql_data_saver import PostgreSqlDataSaver


@pytest.fixture(scope="module")
# use mock for simplify test. It should be replaced with testing db
def db_connection():
    pass


@pytest.fixture(scope="module")
# use mock for simplify test. It should be replaced with testing db
def postgre_sql_data_saver():
    return PostgreSqlDataSaver(
        {'connection': {'dbname': 'test_db', 'host': '127.0.0.1', 'port': '5432', 'user': 'user',
                        'password': 'password'},
         'reconnect': {'tries': 3, 'delay': 1, 'backoff': 2}
         }
    )
