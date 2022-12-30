import mock
import pytest

from data_handler.postgre_sql_data_saver import PostgreSqlDataSaver


@pytest.fixture(scope="module")
def args():
    return mock.Mock()


@pytest.fixture(scope="module")
def config() -> dict:
    return {
        'kafka_consumer': {
            'topic': 'web_monitor_topic',
            'sleep_interval': 5,
            'connection': {
                'bootstrap_servers': 'broker: 9092',
                'group_id': 'web_monitor_group_1',
                'consumer_timeout_ms': '10000'
            }
        },
        'postgre_sql': {
            'connection': {
                'host': 'localhost',
                'port': 5432,
                'dbname': 'postgres',
                'user': 'postgres',
                'password': 'postgres'
            },
            'reconnect': {
                'tries': 5,
                'delay': 1,
                'backoff': 2
            }
        }
    }


@pytest.fixture(scope="module")
# TODO: create and init db
def postgre_sql_data_saver() -> PostgreSqlDataSaver:
    return PostgreSqlDataSaver()
