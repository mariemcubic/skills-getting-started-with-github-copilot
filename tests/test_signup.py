"""Tests for the signup functionality."""
import pytest


def test_signup_for_activity(client):
    """Test signing up for an activity."""
    response = client.post(
        "/activities/Basketball%20Team/signup?email=newemail@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "newemail@mergington.edu" in data["message"]


def test_signup_appears_in_participants(client):
    """Test that signup adds the participant to the activities list."""
    email = "test@mergington.edu"
    
    # Sign up
    response = client.post(
        f"/activities/Art%20Studio/signup?email={email}"
    )
    assert response.status_code == 200
    
    # Verify participant was added
    activities = client.get("/activities").json()
    assert email in activities["Art Studio"]["participants"]


def test_signup_invalid_activity(client):
    """Test signing up for a non-existent activity."""
    response = client.post(
        "/activities/NonExistent%20Activity/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_already_registered(client):
    """Test that signing up twice for the same activity fails."""
    email = "test@mergington.edu"
    activity = "Science%20Club"
    
    # First signup should succeed
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response1.status_code == 200
    
    # Second signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"].lower()


def test_signup_multiple_participants_for_same_activity(client):
    """Test multiple different participants can sign up for the same activity."""
    activity = "Chess%20Club"
    email1 = "person1@mergington.edu"
    email2 = "person2@mergington.edu"
    
    # First signup
    response1 = client.post(f"/activities/{activity}/signup?email={email1}")
    assert response1.status_code == 200
    
    # Second signup
    response2 = client.post(f"/activities/{activity}/signup?email={email2}")
    assert response2.status_code == 200
    
    # Verify both are in participants
    activities = client.get("/activities").json()
    assert email1 in activities["Chess Club"]["participants"]
    assert email2 in activities["Chess Club"]["participants"]
