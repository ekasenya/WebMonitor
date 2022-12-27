from data_handler.data_saver_constants import DataSaverTypes


class BaseDataSaver:
    @staticmethod
    def get_type():
        raise NotImplementedError()

    def save_data_item(self):
        raise NotImplementedError()
