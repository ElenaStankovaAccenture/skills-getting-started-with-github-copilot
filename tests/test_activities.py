"""
Tests for the activities endpoints.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify all activities are returned
    assert len(data) == 9
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert "Basketball Team" in data
    assert "Tennis Club" in data
    assert "Art Studio" in data
    assert "Theater Club" in data
    assert "Science Club" in data
    assert "Debate Team" in data


def test_get_activities_contains_required_fields(client):
    """Test that each activity has the required fields."""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity in data.items():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)


def test_get_activities_has_correct_participant_counts(client):
    """Test that activities have the correct initial participant counts."""
    response = client.get("/activities")
    data = response.json()
    
    # Verify specific participant counts
    assert len(data["Chess Club"]["participants"]) == 2
    assert len(data["Programming Class"]["participants"]) == 2
    assert len(data["Basketball Team"]["participants"]) == 1
    assert len(data["Science Club"]["participants"]) == 1


def test_get_activities_has_correct_participants(client):
    """Test that activities have the correct participants."""
    response = client.get("/activities")
    data = response.json()
    
    # Verify specific participants
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
    assert "emma@mergington.edu" in data["Programming Class"]["participants"]
    assert "alex@mergington.edu" in data["Basketball Team"]["participants"]
