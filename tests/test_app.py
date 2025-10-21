import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307
    # Should redirect to /static/index.html
    assert "/static/index.html" in str(response.url)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_for_activity_success():
    # Use a unique email to avoid duplicate error
    test_email = "pytestuser@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={test_email}")
    assert response.status_code == 200
    assert f"Signed up {test_email} for Chess Club" in response.json()["message"]
    # Check participant is added
    activities = client.get("/activities").json()
    assert test_email in activities["Chess Club"]["participants"]

def test_signup_for_activity_duplicate():
    test_email = "pytestuser@mergington.edu"
    # Try to sign up again
    response = client.post(f"/activities/Chess Club/signup?email={test_email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
