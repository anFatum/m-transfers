from http import HTTPStatus


def get_api_endpoint(controller: str):
    return f"/{controller}"


def test_list_users_unauthorized(client):
    rv = client.get(get_api_endpoint("users"))
    assert rv.status_code == HTTPStatus.UNAUTHORIZED


def test_list_users_ok(client):
    rv = client.get(get_api_endpoint("users"), headers={"Authorization": "Bearer ABC"})
    assert rv.status_code == HTTPStatus.OK
