from data_saver_constants import DataSaverTypes
from postgre_sql_data_saver import PostgreSqlDataSaver
from base_data_saver import BaseDataSaver


def init_data_saver(data_saver_type: str) -> BaseDataSaver:
    """
    Create an object for save data metrics

    :type data_saver_type: str
    :rtype: BaseDataSaver
    """

    print('init_data_saver')
    if not DataSaverTypes.has_value(data_saver_type):
        raise TypeError()

    data_saver = None
    if data_saver_type == DataSaverTypes.POSTGRE_SQL.value:
        data_saver = PostgreSqlDataSaver()

    return data_saver
