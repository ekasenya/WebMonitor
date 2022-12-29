import mock
import asyncio
import pytest
import aiohttp

from web_monitor.main import check_website

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_check_website_url(client):
    url = 'some_url'
    check_info = await check_website(client, url, None)
    assert check_info.url == url
    assert check_info.available
    assert check_info.response_time


@pytest.mark.asyncio
async def test_check_website_invalid_url(client):
    url = 'some_url'
    with mock.patch.object(client, 'get', side_effect=aiohttp.InvalidURL):
        check_info = await check_website(client, url, None)
    assert check_info.url == url
    assert not check_info.available
    assert not check_info.response_time
