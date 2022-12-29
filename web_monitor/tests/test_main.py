import aiohttp
import mock
import pytest

from web_monitor.main import check_website, check_config

pytest_plugins = ('pytest_asyncio',)

TEST_URL = 'some_url'


@pytest.mark.asyncio
async def test_check_website_url(client):
    check_info = await check_website(client, TEST_URL, None)
    assert check_info.url == TEST_URL
    assert check_info.available
    assert check_info.response_time


@pytest.mark.asyncio
async def test_check_website_invalid_url(client):
    with mock.patch.object(client, 'get', side_effect=aiohttp.InvalidURL):
        check_info = await check_website(client, TEST_URL, None)
    assert check_info.url == TEST_URL
    assert not check_info.available
    assert not check_info.response_time


@pytest.mark.parametrize('config', [
    {'web_monitoring': {'check_frequency': 5}},
    {'web_monitoring': {'check_frequency': 300}},
    {'web_monitoring': {'check_frequency': 10}}
])
def test_check_config_success(config):
    assert check_config(config)


@pytest.mark.parametrize('config', [
    {'web_monitoring': {'check_frequency': 0}},
    {'web_monitoring': {'check_frequency': 400}}
])
def test_check_config_failed(config):
    with pytest.raises(ValueError):
        check_config(config)
