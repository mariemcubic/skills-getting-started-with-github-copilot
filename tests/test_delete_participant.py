"""Tests for the delete participant functionality."""
import pytest


def test_remove_participant(client):
    """Test removing a participant from an activity."""
    # First, add a participant
    email = "remove_test@mergington.edu"
    client.post(f"/activities/Debate%20Team/signup?email={email}")
    
    # Verify they're in the list
    activities = client.get("/activities").json()
    assert email in activities["Debate Team"]["participants"]
    
    # Remove the participant
    response = client.delete(
        f"/activities/Debate%20Team/participants/{email}"
    )
    assert response.status_code == 200
    assert "message" in response.json()
    
    # Verify they're no longer in the list
    activities = client.get("/activities").json()
    assert email not in activities["Debate Team"]["participants"]


def test_remove_nonexistent_participant(client):
    """Test removing a participant that's not in an activity."""
    response = client.delete(
        "/activities/Tennis%20Club/participants/notreal@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_remove_participant_invalid_activity(client):
    """Test removing a participant from a non-existent activity."""
    response = client.delete(
        "/activities/Invalid%20Activity/participants/test@mergington.edu"
    )
    assert response.status_code == 404


def test_remove_participant_from_activity_with_multiple(client):
    """Test removing one participant while others remain."""
    activity = "Programming%20Class"
    email_to_remove = "remove@mergington.edu"
    email_to_keep = "keep@mergington.edu"
    
    # Add participants
    client.post(f"/activities/{activity}/signup?email={email_to_remove}")
    client.post(f"/activities/{activity}/signup?email={email_to_keep}")
    
    # Verify both are there
    activities = client.get("/activities").json()
    assert email_to_remove in activities["Programming Class"]["participants"]
    assert email_to_keep in activities["Programming Class"]["participants"]
    
    # Remove one
    response = client.delete(
        f"/activities/Programming%20Class/participants/{email_to_remove}"
    )
    assert response.status_code == 200
    
    # Verify only one remains
    activities = client.get("/activities").json()
    assert email_to_remove not in activities["Programming Class"]["participants"]
    assert email_to_keep in activities["Programming Class"]["participants"]
