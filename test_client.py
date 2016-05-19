from CloudFoundry import Client 

import mock
import requests

@mock.patch('requests.get')
@mock.patch('requests.post')
def test_inits(mocked_post, mocked_get):
    """ Validate the the client can be initalized """
    # Create a mock 
    class MockRequest:
        def json(self):
            return {'token_endpoint': 'test'}
    mock_request = MockRequest()
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

