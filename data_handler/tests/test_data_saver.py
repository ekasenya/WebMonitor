import pytest

from data_handler.data_saver_constants import DataSaverTypes
from data_handler.data_saver import init_data_saver


def test_init_data_saver():
    assert init_data_saver(DataSaverTypes.POSTGRE_SQL.value, {'postgre_sql': ''})


def test_init_data_saver_wrong_type():
    with pytest.raises(TypeError):
        init_data_saver('wrong_type', {'postgre_sql': ''})


def test_init_data_saver_wrong_config():
    with pytest.raises(KeyError):
        init_data_saver(DataSaverTypes.POSTGRE_SQL.value, {})
