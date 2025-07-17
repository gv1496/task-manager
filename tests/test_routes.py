import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import create_app
from app.database import Base, engine, SessionLocal
from app.models import Task


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    client = app.test_client()
    yield client
    # Teardown DB after test
    Base.metadata.drop_all(bind=engine)


def test_create_task(client):
    res = client.post("/tasks", json={"title": "Write tests"})
    assert res.status_code == 200
    assert res.json["title"] == "Write tests"
    assert res.json["done"] is False


def test_get_tasks(client):
    client.post("/tasks", json={"title": "Task 1"})
    res = client.get("/tasks")
    assert res.status_code == 200
    assert isinstance(res.json, list)
    assert res.json[0]["title"] == "Task 1"


def test_mark_done(client):
    client.post("/tasks", json={"title": "Complete me"})
    res = client.put("/tasks/1")
    assert res.status_code == 200
    assert "marked as done" in res.json["message"]


def test_delete_task(client):
    client.post("/tasks", json={"title": "Remove me"})
    res = client.delete("/tasks/1")
    assert res.status_code == 200
    assert "deleted" in res.json["message"]
