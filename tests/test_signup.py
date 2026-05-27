"""
Tests for the signup and participant management endpoints.
"""

import pytest


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup"""
    
    def test_signup_adds_student_to_activity(self, client):
        """Test that signing up a student adds them to an activity."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "new_student@mergington.edu"}
        )
        
        assert response.status_code == 200
        assert response.json()["message"] == "Signed up new_student@mergington.edu for Chess Club"
        
        # Verify student was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "new_student@mergington.edu" in activities["Chess Club"]["participants"]
    
    def test_signup_activity_not_found(self, client):
        """Test that signing up for a non-existent activity returns 404."""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_signup_duplicate_student(self, client):
        """Test that signing up an already registered student returns 400."""
        # michael@mergington.edu is already in Chess Club
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is already signed up for this activity"
    
    def test_signup_multiple_students(self, client):
        """Test that multiple students can sign up for the same activity."""
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email1}
        )
        response2 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email2}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify both were added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email1 in activities["Chess Club"]["participants"]
        assert email2 in activities["Chess Club"]["participants"]
    
    def test_signup_same_student_different_activities(self, client):
        """Test that the same student can sign up for different activities."""
        email = "versatile_student@mergington.edu"
        
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        response2 = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify student is in both activities
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Programming Class"]["participants"]


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/participants"""
    
    def test_remove_participant_success(self, client):
        """Test that removing a participant removes them from an activity."""
        # michael@mergington.edu is in Chess Club
        response = client.delete(
            "/activities/Chess Club/participants",
            params={"email": "michael@mergington.edu"}
        )
        
        assert response.status_code == 200
        assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    
    def test_remove_participant_activity_not_found(self, client):
        """Test that removing from a non-existent activity returns 404."""
        response = client.delete(
            "/activities/Nonexistent Activity/participants",
            params={"email": "student@mergington.edu"}
        )
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_remove_participant_not_in_activity(self, client):
        """Test that removing a non-participant returns 404."""
        response = client.delete(
            "/activities/Chess Club/participants",
            params={"email": "not_a_member@mergington.edu"}
        )
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"
    
    def test_remove_multiple_participants(self, client):
        """Test that multiple participants can be removed."""
        # Chess Club has michael@mergington.edu and daniel@mergington.edu
        response1 = client.delete(
            "/activities/Chess Club/participants",
            params={"email": "michael@mergington.edu"}
        )
        response2 = client.delete(
            "/activities/Chess Club/participants",
            params={"email": "daniel@mergington.edu"}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify both were removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert len(activities["Chess Club"]["participants"]) == 0
    
    def test_remove_participant_then_add_again(self, client):
        """Test that a removed participant can sign up again."""
        email = "michael@mergington.edu"
        
        # Remove
        delete_response = client.delete(
            "/activities/Chess Club/participants",
            params={"email": email}
        )
        assert delete_response.status_code == 200
        
        # Sign up again
        signup_response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Verify they're back in the activity
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
