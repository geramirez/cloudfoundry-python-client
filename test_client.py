from CloudFoundry import Client 

import mock
import requests

class MockInfoRequest:
    def json(self):
        return {
            'token_endpoint': 'test',
        }

class MockTokenRequest:
    def json(self):
        return {
                'expires_in': 900,
            }

class MockTokenRequestLoggedOut:
    def json(self):
        return {
            'expires_in': -1
        }

class MockTokenRequestFail:
    def json(self):
        return {
            'error': 'Error message' 
        }

@mock.patch('requests.get')
@mock.patch('requests.post')
def test_inits(mocked_post, mocked_get):
    """ Validate the the client can be initalized """
    # Create a mock 
    mock_request = MockInfoRequest()
    mocked_get.spy(mock_request, 'json')
    mocked_get.return_value = mock_request

    # Initialize Client
    client = Client(
        api_url="https://api.bosh-lite.com",
        username="admin",
        password="admin",
    )
    # Validate
    requests.get.assert_called_once_with(
        'https://api.bosh-lite.com/v2/info', verify=True
    )
    requests.post.assert_called_once_with(
        headers={
            'accept': 'application/json',
            'authorization': 'Basic Y2Y6'
        },
        params={
            'username': 'admin',
            'grant_type': 'password',
            'password': 'admin'
        },
        url='test/oauth/token',
        verify=True
    )


@mock.patch('requests.get')
@mock.patch('requests.post')
def test_is_logged_in(mocked_post, mocked_get):
    """ Validate the the client is logged in when token
    is not expired"""
    # Create a mock 
    mock_request = MockInfoRequest()
    mocked_get.spy(mock_request, 'json')
    mocked_get.return_value = mock_request
    mock_post_request = MockTokenRequest()
    mocked_post.spy(mock_post_request, 'json')
    mocked_post.return_value = mock_post_request

    # Initialize Client and 
    client = Client(
        api_url="https://api.bosh-lite.com",
        username="admin",
        password="admin",
    )

    logged_in = client.is_logged_in() 

    # Validate
    logged_in == True
    assert requests.post.call_count ==  1


@mock.patch('requests.get')
@mock.patch('requests.post')
def test_is_logged_in_token_expired(mocked_post, mocked_get):
    """ Validate the the client is logged out when token
    is expired but it's saved"""
    # Create a mock 
    mock_request = MockInfoRequest()
    mocked_get.spy(mock_request, 'json')
    mocked_get.return_value = mock_request
    mock_post_request = MockTokenRequestLoggedOut()
    mocked_post.spy(mock_post_request, 'json')
    mocked_post.return_value = mock_post_request

    # Initialize Client and 
    client = Client(
        api_url="https://api.bosh-lite.com",
        username="admin",
        password="admin",
    )
    logged_in = client.is_logged_in() 

    # Validate
    assert logged_in == True 
    assert requests.post.call_count ==  2

@mock.patch('requests.get')
@mock.patch('requests.post')
def test_is_logged_in_token_expired_and_it_fails(mocked_post, mocked_get):
    """ Validate the the client is logged out when token
    is expired and post returns and error"""
    # Create a mock 
    mock_request = MockInfoRequest()
    mocked_get.spy(mock_request, 'json')
    mocked_get.return_value = mock_request
    mock_post_request = MockTokenRequestLoggedOut()
    mocked_post.spy(mock_post_request, 'json')
    mocked_post.return_value = mock_post_request

    # Initialize Client and 
    client = Client(
        api_url="https://api.bosh-lite.com",
        username="admin",
        password="admin",
    )
    mock_request = MockTokenRequestFail()
    mocked_post.spy(mock_request, 'json')
    mocked_post.return_value = mock_request
    logged_in = client.is_logged_in() 

    # Validate
    assert logged_in == False 
    assert requests.post.call_count ==  2
