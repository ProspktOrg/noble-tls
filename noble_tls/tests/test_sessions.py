import asyncio

import pytest
from unittest.mock import patch, MagicMock
from ..sessions import Session
from ..utils.structures import CaseInsensitiveDict
from ..utils.identifiers import Client

import pytest
from unittest.mock import MagicMock, patch
from ..sessions import Session
import asyncio


@pytest.mark.asyncio
async def test_session_initialization():
    session = Session()
    assert session.timeout_seconds == 30, "Default timeout should be 30 seconds"
    assert isinstance(session.headers, CaseInsensitiveDict), "Headers should be a CaseInsensitiveDict"
    assert session.isAws == False, "Default isAws should be False"


@pytest.mark.asyncio
async def test_session_initialization_aws():
    session = Session(isAws=True)
    assert session.timeout_seconds == 30, "Default timeout should be 30 seconds"
    assert isinstance(session.headers, CaseInsensitiveDict), "Headers should be a CaseInsensitiveDict"
    assert session.isAws == True, "isAws should be True when specified"


@pytest.mark.asyncio
async def test_session_execute_request(mocker):
    # Mock external calls
    mocker.patch('ctypes.string_at', return_value=b'{"status": 200, "body": "OK", "headers": {}, "id": "mock_id"}')
    mocker.patch('ctypes.cdll.LoadLibrary')
    mocker.patch('noble_tls.c.cffi.get_request_func', return_value=MagicMock())
    mocker.patch('noble_tls.c.cffi.get_free_memory_func', return_value=MagicMock())

    session = Session()

    # Prepare a mock response to be returned by the patched request function
    mock_response = '{"status": 200, "body": "OK", "headers": {}, "id": "mock_id"}'.encode('utf-8')

    # Mock asyncio loop
    mock_loop = MagicMock()
    mocker.patch('asyncio.get_event_loop', return_value=mock_loop)

    # Create a mock future object and set the result to the mock response
    mock_future = asyncio.Future()
    mock_future.set_result(mock_response)

    # Patch loop.run_in_executor to return the mock future
    mock_loop.run_in_executor = MagicMock(return_value=mock_future)

    # Execute a simple GET request
    response = await session.get('http://example.com')

    assert response.status_code == 200, "Response should have a status code of 200"
    assert response.text == 'OK', "Response body should be 'OK'"


@pytest.mark.asyncio
async def test_session_with_safari_ios_26_0():
    session = Session(client=Client.SAFARI_IOS_26_0)
    assert session.client_identifier == "safari_ios_26_0"


@pytest.mark.asyncio
async def test_session_with_chrome_146():
    session = Session(client=Client.CHROME_146)
    assert session.client_identifier == "chrome_146"


@pytest.mark.asyncio
async def test_session_with_chrome_146_psk():
    session = Session(client=Client.CHROME_146_PSK)
    assert session.client_identifier == "chrome_146_PSK"


@pytest.mark.asyncio
async def test_session_with_firefox_146():
    session = Session(client=Client.FIREFOX_146)
    assert session.client_identifier == "firefox_146"


@pytest.mark.asyncio
async def test_session_with_firefox_147():
    session = Session(client=Client.FIREFOX_147)
    assert session.client_identifier == "firefox_147"
