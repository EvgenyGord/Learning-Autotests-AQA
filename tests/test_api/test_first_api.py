import pytest
import requests

@pytest.mark.xfail
@pytest.mark.api
def test_create_user(api_url):
    payload_json = {
        "id": 0,
        "username": "string",
        "firstName": "string",
        "lastName": "string",
        "email": "string",
        "password": "string",
        "phone": "string",
        "userStatus": 0
    }
    response = requests.post(f"{api_url}/user", json=payload_json)

    assert response.status_code == 201
    print(response.json())