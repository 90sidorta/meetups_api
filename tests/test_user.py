import pytest

from app.schemas.users import UserResponse
from app.schemas.auth import AccessToken


def test_create_user(client):
    res = client.post(
        "/users/",
        json={
            "email": "test2@test.com",
            "username": "testowy",
            "password": "testtest2",
        },
    )
    new_user = UserResponse(**res.json())
    assert new_user.email == "test2@test.com"
    assert new_user.username == "testowy"
    assert res.status_code == 201


def test_login_user(client, test_load_users, test_user):
    res = client.post(
        "/login", data={"username": "test0@test.com", "password": "testtest2"}
    )
    AccessToken(**res.json())
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test2@test.com", "testtest22", 403),
        ("test22@test.com", "testtest2", 403),
        ("test22@test.com", "testtest22", 403),
        (None, "testtest2", 422),
        ("test2@test.com", None, 422),
    ],
)
def test_login_invalid_credential(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    if status_code == 403:
        assert res.json()["detail"] == "Incorrect username or password"


@pytest.mark.parametrize(
    "limit, skip, search, length",
    [
        ("20", "0", None, 20),
        ("20", "20", None, 6),
        ("20", "0", "bo", 3),
    ],
)
def test_get_users(client, test_load_users, limit, skip, search, length):
    url = (
        f"?limit={limit}&skip={skip}&search={search}"
        if search
        else f"?limit={limit}&skip={skip}"
    )
    res = client.get(f"/users/{url}")
    assert res.status_code == 200
    users_response = res.json()
    assert len(users_response) == length
