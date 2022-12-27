from data_handler.data_saver_constants import DataSaverTypes
from data_handler.postgre_sql_data_saver import PostgreSqlDataSaver
from data_handler.base_data_saver import BaseDataSaver


def create_data_saver(data_saver_type: str) -> BaseDataSaver:
    """
    Create an object for save data metrics

    :type data_saver_type: str
    :rtype: BaseDataSaver
    """
    if not DataSaverTypes.has_value(data_saver_type):
        raise TypeError()

    data_saver = None
    if data_saver_type == DataSaverTypes.POSTGRE_SQL:
        data_saver = PostgreSqlDataSaver()

    return data_saver
