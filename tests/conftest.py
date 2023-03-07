import pytest
import json
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.authentication import create_access_token
from app.config import settings
from app.database import get_db
from app.main import app
from app import models
from app.database import Base


DB_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/{settings.DB_NAME}"

engine_new = create_engine(DB_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_new)
cur_path = os.path.dirname(__file__)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine_new)
    Base.metadata.create_all(bind=engine_new)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def get_test_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {}
    user_data["id"] = 1
    return user_data


@pytest.fixture
def test_token(test_user):
    return create_access_token(sub=test_user["id"])


@pytest.fixture
def authorized_client(client, test_token):
    client.headers = {**client.headers, "Authorization": f"Bearer {test_token}"}
    return client


@pytest.fixture
def test_load_users(session):
    data = open(f"{cur_path}/data/users.json")
    users = json.load(data)

    def create_user_model(user_data):
        return models.User(**user_data)

    user_map = map(create_user_model, users)
    user_list = list(user_map)

    session.add_all(user_list)
    session.commit()
    users_data = session.query(models.User).all()
    return users_data


@pytest.fixture
def test_load_meetups(session, test_load_users):
    data = open(f"{cur_path}/data/meetups.json")
    meetups = json.load(data)

    def create_meetup_model(meetup_data):
        return models.Meetup(**meetup_data)

    meetup_map = map(create_meetup_model, meetups)
    meetup_list = list(meetup_map)

    session.add_all(meetup_list)
    session.commit()
    users_data = session.query(models.Meetup).all()
    return users_data


@pytest.fixture
def test_load_attends(session, test_load_users, test_load_meetups):
    data = open(f"{cur_path}/data/attend.json")
    attends_data = json.load(data)

    def create_attend_model(meetup_data):
        return models.Atend(**meetup_data)

    attend_map = map(create_attend_model, attends_data)
    attend_list = list(attend_map)

    session.add_all(attend_list)
    session.commit()
    attends_data = session.query(models.Atend).all()
    return attends_data
