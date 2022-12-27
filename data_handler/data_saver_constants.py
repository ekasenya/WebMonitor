from enum import Enum


class DataSaverTypes(Enum):
    POSTGRE_SQL = 'postgre_sql'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
