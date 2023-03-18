from fastapi.testclient import TestClient
import json
from main import app
from pytest import fixture



client = TestClient(app)

def test_user_login_success():
    response = client.post("/api/authenticate", 
                        json={
                            "email": "tanmay@reunion.org",
                            "password": "tanmay"
                            })
    assert response.status_code == 200
    assert "token" in response.json()

def test_user_login_fail():
    response = client.post("/api/authenticate", 
                        json={
                            "email": "tanmay@reunion.org",
                            "password": "invalidpassword"
                            })
    assert response.status_code == 401
    assert "Access Denied" in response.json()

def test_get_user_details_success():
    token = "<insert valid JWT token here>"
    response = client.get("/api/user", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "username" in response.json()
    assert "followers" in response.json()
    assert "following" in response.json()

def test_add_comment_success():
    token = "<insert valid JWT token here>"
    response = client.post("/api/comment/1", 
                        headers={"Authorization": f"Bearer {token}"}, 
                        json={
                            "comment": "Great post!"
                            })
    assert response.status_code == 200
    assert "Comment-ID" in response.json()

def test_add_comment_fail():
    token = "<insert valid JWT token here>"
    response = client.post("/api/comment/1", 
                        headers={"Authorization": f"Bearer {token}"}, 
                        json={
                            "comment": ""
                            })
    assert response.status_code == 400
    assert "Abort" in response.json()

def test_follow_user_success():
    token = "<insert valid JWT token here>"
    response = client.post("/api/follow/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "following"

def test_unfollow_user_success():
    token = "<insert valid JWT token here>"
    response = client.delete("/api/follow/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "unfollowed"


@fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_add_post(client):
    payload = {
        "title": "Test title",
        "description": "Test description"
    }
    response = client.post("/api/posts/", json=payload)
    assert response.status_code == 200
    assert "Post-ID" in response.json()
    assert "Title" in response.json()
    assert "Description" in response.json()
    assert "Created Time(UTC)" in response.json()


def test_add_post_empty_title(client):
    payload = {
        "title": "",
        "description": "Test description"
    }
    response = client.post("/api/posts/", json=payload)
    assert response.status_code == 400
    assert "Oops!" in response.json()


def test_add_post_empty_description(client):
    payload = {
        "title": "Test title",
        "description": ""
    }
    response = client.post("/api/posts/", json=payload)
    assert response.status_code == 400
    assert "Oops!" in response.json()


def test_delete_post(client):
    response = client.delete("/api/posts/1")
    assert response.status_code == 200
    assert "Success" in response.json()


def test_delete_post_not_exists(client):
    response = client.delete("/api/posts/100")
    assert response.status_code == 400
    assert "Abort" in response.json()


def test_delete_post_not_author(client):
    response = client.delete("/api/posts/2")
    assert response.status_code == 400
    assert "Abort" in response.json()


def test_get_all_posts(client):
    response = client.get("/api/all_posts")
    assert response.status_code == 200
    for post in response.json():
        assert "id" in post
        assert "title" in post
        assert "desc" in post
        assert "created_at" in post
        assert "comments" in post
        assert "likes" in post
