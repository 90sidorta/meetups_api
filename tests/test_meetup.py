import pytest

from app import schema

## Create ###
@pytest.mark.parametrize("title, description, address, published, price, limit", [
    ("Test Title", "Test description", "Test Street 2/2", True, 20, 100),
    ("Test Title", "Test description", "Test Street 2/2", True, 0, 0),
    ("Test Title", "Test description", "Test Street 2/2", False, 10, 10)
])
def test_create_meetup(authorized_client, test_load_users, title, description, published, price, limit, address):
    res = authorized_client.post("/meetups/",
    json={"title": title, "description": description, "published": published, "price": price, "limit": limit, "address": address}
    )
    assert res.status_code == 201
    meetup_response = res.json()
    schema.MeetupAddData(**meetup_response)
    assert meetup_response["title"] == title
    assert meetup_response["description"] == description
    assert meetup_response["published"] == published
    assert meetup_response["price"] == price
    assert meetup_response["limit"] == limit
    assert meetup_response["address"] == address


def test_create_meetup_mandatory_only(authorized_client, test_load_users):
    res = authorized_client.post("/meetups/",
    json={"title": "title", "description": "description", "address": "address"}
    )
    assert res.status_code == 201
    meetup_response = res.json()
    schema.MeetupAddData(**meetup_response)


def test_create_meetup_unauthorized(client):
    res = client.post("/meetups/",
    json={"title": "string", "description": "string", "published": True, "price": 0, "limit": 0, "address": "string"}
    )
    assert res.status_code == 401
    meetup_response = res.json()
    assert meetup_response["detail"] == "Not authenticated"


### Read ###
@pytest.mark.parametrize("limit, skip, search, length", [
    ("20", "0", None, 20),
    ("20", "20", None, 20),
    ("20", "0", "coh", 10),
])
def test_get_meetups_unauthorized(client, limit, skip, search, length, test_load_meetups):
    url = f"?limit={limit}&skip={skip}&search={search}" if search else f"?limit={limit}&skip={skip}"
    res = client.get(f"/meetups/{url}")
    def validate(meetup):
        return schema.MeetupResponse(**meetup)
    assert res.status_code == 200
    meetup_response = res.json()
    meetup_map = map(validate, meetup_response)
    assert len(meetup_response) == length
    

@pytest.mark.parametrize("limit, skip, search, length", [
    ("20", "0", None, 20),
    ("20", "20", None, 20),
    ("20", "0", "coh", 10),
])
def test_get_meetups(authorized_client, test_load_users, limit, skip, search, length, test_load_meetups):
    url = f"?limit={limit}&skip={skip}&search={search}" if search else f"?limit={limit}&skip={skip}"
    res = authorized_client.get(f"/meetups/{url}")
    def validate(meetup):
        return schema.MeetupResponse(**meetup)
    assert res.status_code == 200
    meetup_response = res.json()
    meetup_map = map(validate, meetup_response)
    assert len(meetup_response) == length


def test_get_one_meetup(authorized_client, test_load_users, test_load_meetups):
    res = authorized_client.get(f"/meetups/1")
    meetup = res.json()
    assert res.status_code == 200
    schema.MeetupResponse(**meetup)


def test_get_one_meetup_unauthorized(client, test_load_meetups):
    res = client.get(f"/meetups/1")
    meetup = res.json()
    assert res.status_code == 200
    schema.MeetupResponse(**meetup)


def test_get_one_meetup_not_exists(authorized_client, test_load_users, test_load_meetups):
    res = authorized_client.get(f"/meetups/999")
    meetup = res.json()
    assert res.status_code == 404
    assert meetup["detail"] == "No meetup with id: 999 found!"


# Update ###
def test_update_meetup_not_exists(authorized_client, test_load_users, test_load_meetups):
    res = authorized_client.put(f"/meetups/999",
    json={"title": "title", "description": "title", "address": "address" }
    )
    meetup = res.json()
    assert res.status_code == 404
    assert meetup["detail"] == "No meetup with id: 999 found!"


def test_update_meetup_unauthorized(client, test_load_users, test_load_meetups):
    res = client.put(f"/meetups/1",
    json={"title": "title", "description": "title", "address": "address" }
    )
    meetup = res.json()
    assert res.status_code == 401
    assert meetup["detail"] == "Not authenticated"


def test_update_meetup_other_user(authorized_client, test_load_users, test_load_meetups):
    res = authorized_client.put(f"/meetups/1",
    json={"title": "title", "description": "title", "address": "address" }
    )
    meetup_response = res.json()
    assert res.status_code == 403
    assert meetup_response["detail"] == "Cannot modify other user meetup!"


def test_update_meetup_mine(authorized_client, test_load_users, test_load_meetups):
    res = authorized_client.put(f"/meetups/298",
    json={"title": "title", "description": "description", "address": "address", "published":False, "price":10.95,"limit":7456 }
    )
    meetup_response = res.json()
    assert res.status_code == 200
    assert meetup_response["title"] == "title"
    assert meetup_response["description"] == "description"
    assert meetup_response["address"] == "address"
    assert meetup_response["published"] == False
    assert meetup_response["limit"] == 7456


def test_update_meetup_invalid(authorized_client, test_load_users, test_load_meetups):
    res = authorized_client.put(f"/meetups/298",
    json={"title": 321, "description": True, "address": None, "published":False, "price":10.95,"limit":7456 }
    )
    assert res.status_code == 500


## Delete ###
def test_delete_meetup_not_exists(authorized_client, test_load_users, test_load_meetups):
    res = authorized_client.delete(f"/meetups/999")
    meetup = res.json()
    assert res.status_code == 404
    assert meetup["detail"] == "No meetup with id: 999 found!"


def test_delete_meetup_unauthorized(client, test_load_meetups):
    res = client.delete(f"/meetups/1")
    meetup_response = res.json()
    assert res.status_code == 401
    assert meetup_response["detail"] == "Not authenticated"


def test_delete_meetup_other_user(authorized_client, test_load_users, test_load_meetups):
    res = authorized_client.delete(f"/meetups/1")
    meetup_response = res.json()
    assert res.status_code == 403
    assert meetup_response["detail"] == "Cannot delete other user meetup!"


def test_delete_meetup_mine(authorized_client, test_load_users, test_load_meetups):
    res = authorized_client.delete(f"/meetups/298")
    assert res.status_code == 204

    