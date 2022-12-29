class BaseDataSaver:
    """Base class for data save functionality"""
    @staticmethod
    def get_type() -> str:
        """
        return data saver type
        :rtype: str
        """
        raise NotImplementedError()

    def init(self):
        raise NotImplementedError()

    def finalize(self):
        """
        Close and clear all resources
        """
        raise NotImplementedError()

    def save_data_item(self, data: dict):
        """
        Save data to storage
        """
        raise NotImplementedError()
