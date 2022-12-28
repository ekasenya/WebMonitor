import logging

from data_saver_constants import DataSaverTypes
from base_data_saver import BaseDataSaver

import psycopg2

logger = logging.getLogger('posgre_sql_data_saver')


WEBSITE_READ_SQL = '''
SELECT website_id from information_schema.websites
WHERE url = %(url)s
'''


WEBSITE_INSERT_SQL = '''
INSERT INTO information_schema.websites
(url)
VALUES(%(url)s)
RETURNING website_id
'''


WEB_MONITORING_INSERT_SQL = '''
INSERT INTO information_schema.websites_check_results
(website_id, available, request_ts, response_time, http_code, pattern_matched)
VALUES(%(website_id)s, %(available)s, %(request_ts)s, %(response_time)s, %(http_code)s, %(pattern_matched)s)
RETURNING check_id
'''


class PostgreSqlDataSaver(BaseDataSaver):
    @staticmethod
    def get_type():
        return DataSaverTypes.POSTGRE_SQL.value

    def __init__(self):
        self.db_conn = None

    def init(self, config):
        self.db_conn = psycopg2.connect(dbname=config['postgre_sql']['dbname'], user=config['postgre_sql']['user'],
                                        password=config['postgre_sql']['password'], host=config['postgre_sql']['host'],
                                        port=config['postgre_sql']['port'])

    def finalize(self):
        if self.db_conn:
            self.db_conn.close()

    def _get_website_id(self, cursor, url):
        cursor.execute(WEBSITE_READ_SQL, {'url': url})
        record = cursor.fetchone()
        if not record:
            cursor.execute(WEBSITE_INSERT_SQL, {'url': url})
            record = cursor.fetchone()

        return record[0]

    def save_data_item(self, data):
        cursor = self.db_conn.cursor()
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
        logger.info('Record {check_id} with check data for {url} inserted to db'.format(check_id=record[0], url=data['url']))
