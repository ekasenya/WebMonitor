class BaseDataSaver:
    @staticmethod
    def get_type() -> str:
        raise NotImplementedError()

    def init(self):
        raise NotImplementedError()

    def finalize(self):
        raise NotImplementedError()

    def save_data_item(self, data: dict):
        raise NotImplementedError()
