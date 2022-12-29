import pytest
import mock


@pytest.fixture(scope="module")
def client():
    def _get(*args, **kwargs):
        return resp

    resp = mock.MagicMock()
    resp.text = 'some text'
    client = mock.MagicMock()
    client.get = _get

    return client
