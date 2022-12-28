class BaseDataSaver:
    @staticmethod
    def get_type():
        raise NotImplementedError()

    def init(self, config):
        raise NotImplementedError()

    def finalize(self):
        raise NotImplementedError()

    def save_data_item(self, data):
        raise NotImplementedError()
