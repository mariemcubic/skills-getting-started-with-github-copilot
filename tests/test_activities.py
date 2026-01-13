"""Tests for the activities endpoints."""
import pytest


def test_get_activities(client):
    """Test retrieving all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data
    assert "Tennis Club" in data
    assert "Drama Club" in data


def test_get_activities_has_correct_structure(client):
    """Test that activities have the correct structure."""
    response = client.get("/activities")
    data = response.json()
    
    # Check one activity has the expected fields
    basketball = data["Basketball Team"]
    assert "description" in basketball
    assert "schedule" in basketball
    assert "max_participants" in basketball
    assert "participants" in basketball
    assert isinstance(basketball["participants"], list)


def test_get_activities_participants_are_emails(client):
    """Test that participants are stored as email addresses."""
    response = client.get("/activities")
    data = response.json()
    
    # Check that participants are email addresses
    for activity_name, activity in data.items():
        for participant in activity["participants"]:
            assert "@" in participant
            assert "mergington.edu" in participant
