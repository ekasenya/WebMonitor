import logging

import psycopg2
import psycopg2.errors as pg_errors
from retry import retry

from data_handler.base_data_saver import BaseDataSaver
from data_handler.data_saver_constants import DataSaverTypes

logger = logging.getLogger('postgre_sql_data_saver')


WEBSITE_READ_SQL = '''
SELECT website_id from public.websites
WHERE url = %(url)s
'''

WEBSITE_READ_BY_ID_SQL = '''
SELECT url from public.websites
WHERE website_id = %(website_id)s
'''


WEBSITE_INSERT_SQL = '''
INSERT INTO public.websites
(url)
VALUES(%(url)s)
RETURNING website_id
'''


WEB_MONITORING_INSERT_SQL = '''
INSERT INTO public.websites_check_results
(website_id, available, request_ts, response_time, http_code, pattern_matched)
VALUES(%(website_id)s, %(available)s, %(request_ts)s, %(response_time)s, %(http_code)s, %(pattern_matched)s)
RETURNING check_id
'''


WEB_MONITORING_READ_BY_CHECK_ID_SQL = '''
SELECT * from public.websites_check_results
WHERE check_id = %(check_id)s
'''


class PostgreSqlDataSaver(BaseDataSaver):
    @staticmethod
    def get_type() -> str:
        return DataSaverTypes.POSTGRE_SQL.value

    def __init__(self, config: dict):
        self.db_conn = None
        self.config = config['postgre_sql']

    def init(self):
        self._connect_db()

    def finalize(self):
        if self.db_conn and not self.db_conn.closed:
            self.db_conn.close()

    def _connect_db(self):
        @retry(**self.config['reconnect'])
        def _connect_db_with_retry():
            self.db_conn = psycopg2.connect(**self.config['connection'])
            logger.info('Connected to db: {host}:{port}'.format(host=self.config['connection']['host'], port=self.config['connection']['port']))

        _connect_db_with_retry()

    def _get_cursor(self):
        return self.db_conn.cursor()

    def _get_website_id(self, cursor, url: str):
        cursor.execute(WEBSITE_READ_SQL, {'url': url})
        record = cursor.fetchone()
        if not record:
            cursor.execute(WEBSITE_INSERT_SQL, {'url': url})
            record = cursor.fetchone()

        return record[0]

    def save_data_item(self, data: dict):
        # the second attempt for the case when db was disconnected and connection was restored
        for _ in range(2):
            try:
                cursor = self._get_cursor()
                try:
                    website_id = self._get_website_id(cursor, data['url'])
                    cursor.execute(WEB_MONITORING_INSERT_SQL, {'website_id': website_id,
                                                               'available': data['available'],
                                                               'request_ts': data['request_ts'],
                                                               'response_time': data['response_time'],
                                                               'http_code': data['http_code'],
                                                               'pattern_matched': data['pattern_matched'],
                                                               })
                    record = cursor.fetchone()
                    self.db_conn.commit()
                    logger.info('Record {check_id} with check data for {url} inserted to db'.format(check_id=record[0],
                                                                                                    url=data['url']))
                    return record[0]
                finally:
                    if cursor:
                        cursor.close()
            except (pg_errors.DatatypeMismatch, pg_errors.InvalidTextRepresentation) as ex:
                logger.error('Incorrect record data. Skipping. {}'.format(str(ex)))
            except Exception as ex:
                if self.db_conn.closed:
                    logger.warning('Db connection was closed. Try to reconnect')
                    self._connect_db()
                else:
                    raise ex
