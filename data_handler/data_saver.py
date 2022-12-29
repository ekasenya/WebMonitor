#!/usr/bin/.env python3

import logging

from data_handler.data_saver_constants import DataSaverTypes
from data_handler.postgre_sql_data_saver import PostgreSqlDataSaver
from data_handler.base_data_saver import BaseDataSaver


logger = logging.getLogger('data_saver')


def init_data_saver(data_saver_type: str, config: dict) -> BaseDataSaver:
    """
    Create an object for save data metrics

    :param config: configuration
    :type data_saver_type: str
    :rtype: BaseDataSaver
    """

    logger.info('Start creating data saver. Type: {}'.format(data_saver_type))

    if not DataSaverTypes.has_value(data_saver_type):
        raise TypeError()

    data_saver = None
    if data_saver_type == DataSaverTypes.POSTGRE_SQL.value:
        data_saver = PostgreSqlDataSaver(config)

    logger.info('Data saver is created')

    return data_saver
