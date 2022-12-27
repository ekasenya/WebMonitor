from data_handler.data_saver_constants import DataSaverTypes
from data_handler.base_data_saver import BaseDataSaver


class PostgreSqlDataSaver(BaseDataSaver):
    @staticmethod
    def get_type():
        return DataSaverTypes.POSTGRE_SQL

    def save_data_item(self):
        raise NotImplementedError()
