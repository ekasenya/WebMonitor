import pytest
import mock

import psycopg2.errors as pg_errors

from data_handler.postgre_sql_data_saver import PostgreSqlDataSaver, WEBSITE_READ_BY_ID_SQL, \
    WEB_MONITORING_READ_BY_CHECK_ID_SQL
from data_handler.tests.conftest import postgre_sql_data_saver


TEST_URL = 'https://www.google.com'


@mock.patch("psycopg2.connect")
def test_connect_db(postgre_sql_data_saver: PostgreSqlDataSaver):
    postgre_sql_data_saver._connect_db()


def test_check_get_website_id(postgre_sql_data_saver: PostgreSqlDataSaver):
    postgre_sql_data_saver.init()
    try:
        cursor = postgre_sql_data_saver._get_cursor()
        try:
            url_id = postgre_sql_data_saver._get_website_id(TEST_URL)
            assert url_id
            assert url_id == postgre_sql_data_saver._get_website_id(TEST_URL)

            cursor.execute(WEBSITE_READ_BY_ID_SQL, {'website_id': url_id})
            record = cursor.fetchone()
            assert record
            assert record[0] == TEST_URL
        finally:
            if cursor:
                cursor.close()
    finally:
        postgre_sql_data_saver.finalize()


@pytest.mark.parametrize('data_item', [
    {
        'url': TEST_URL, 'available': True, 'request_ts': 1672346559, 'response_time': 10, 'http_code': 200,
        'pattern_matched': True
    },
    {
        'url': TEST_URL, 'available': True, 'request_ts': 1672346560, 'response_time': 10, 'http_code': 200,
        'pattern_matched': None
    },
    {
        'url': TEST_URL, 'available': None, 'request_ts': 1672346561, 'response_time': None, 'http_code': None,
        'pattern_matched': None
    }
])
def test_save_data_item(postgre_sql_data_saver: PostgreSqlDataSaver, data_item: dict):
    postgre_sql_data_saver.init()
    try:
        check_id = postgre_sql_data_saver.save_data_item(data=data_item)
        assert check_id
        cursor = postgre_sql_data_saver._get_cursor()
        try:
            cursor.execute(WEB_MONITORING_READ_BY_CHECK_ID_SQL, {'check_id': check_id})
            record = cursor.fetchone()
            assert record
        finally:
            if cursor:
                cursor.close()
    finally:
        postgre_sql_data_saver.finalize()


@pytest.mark.parametrize('data_item, expected_exception', [
    (
            {
                'url': TEST_URL, 'available': TEST_URL, 'request_ts': 1672346559, 'response_time': 10, 'http_code': 200,
                'pattern_matched': True
            },
            pg_errors.InvalidTextRepresentation
    ),
    (
            {
                'url': True, 'available': True, 'request_ts': 1672346559, 'response_time': 10, 'http_code': 200,
                'pattern_matched': None
            },
            pg_errors.DatatypeMismatch
    )
])
def test_save_incorrect_data_item(postgre_sql_data_saver: PostgreSqlDataSaver, data_item: dict, expected_exception):
    postgre_sql_data_saver.init()
    try:
        with pytest.raises(expected_exception):
            postgre_sql_data_saver.save_data_item(data=data_item)
    finally:
        postgre_sql_data_saver.finalize()