import pytest


def test_attend_meetup(authorized_client, test_load_users, test_load_meetups, test_load_attends):
    res = authorized_client.post("/attends/", json={"meetup_id": 2, "join": True})
    attend_res = res.json()
    assert res.status_code == 201
    assert attend_res["meetup_id"] == 2
    assert attend_res["user_id"] == 1


def test_attend_meetup_unauthorized(client, test_load_users, test_load_meetups, test_load_attends):
    res = client.post("/attends/", json={"meetup_id": 2, "join": True})
    attend_res = res.json()
    assert res.status_code == 401
    assert attend_res["detail"] == "Not authenticated"


def test_attend_twice(authorized_client, test_load_users, test_load_meetups, test_load_attends):
    res = authorized_client.post("/attends/", json={"meetup_id": 1, "join": True})
    attend_res = res.json()
    assert res.status_code == 409
    assert attend_res["detail"] == "You have already signed up for this meetup!"


def test_attend_own(authorized_client, test_load_users, test_load_meetups, test_load_attends):
    res = authorized_client.post("/attends/", json={"meetup_id": 298, "join": True})
    attend_res = res.json()
    assert res.status_code == 403
    assert attend_res["detail"] == "This is your own meetup!"


def test_attend_nonexistent(authorized_client, test_load_users, test_load_meetups, test_load_attends):
    res = authorized_client.post("/attends/", json={"meetup_id": 999, "join": True})
    attend_res = res.json()
    assert res.status_code == 404
    assert attend_res["detail"] == "This meetup does not exist!"


def test_cancel_attend(authorized_client, test_load_users, test_load_meetups, test_load_attends):
    res = authorized_client.post("/attends/", json={"meetup_id": 1, "join": False})
    attend_res = res.json()
    assert res.status_code == 201
    assert attend_res["meetup_id"] == 1
    assert attend_res["user_id"] == 1


def test_cancel_attend_nonexistent(authorized_client, test_load_users, test_load_meetups, test_load_attends):
    res = authorized_client.post("/attends/", json={"meetup_id": 999, "join": False})
    attend_res = res.json()
    assert res.status_code == 404
    assert attend_res["detail"] == "This meetup does not exist!"


def test_cancel_attend_unattended(authorized_client, test_load_users, test_load_meetups, test_load_attends):
    res = authorized_client.post("/attends/", json={"meetup_id": 10, "join": False})
    attend_res = res.json()
    assert res.status_code == 404
    assert attend_res["detail"] == "You did not signed up for this meetup!"

