"""
Test suite for Mergington High School API

Uses the AAA (Arrange-Act-Assert) testing pattern for clear test structure.
"""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestRootEndpoint:
    """Tests for GET / endpoint"""
    
    def test_root_redirects_to_index(self):
        # Arrange
        expected_redirect_url = "/static/index.html"
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == expected_redirect_url


class TestActivitiesEndpoint:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self):
        # Arrange
        expected_keys = {"Chess Club", "Programming Class", "Gym Class", "Soccer Team", 
                        "Basketball Club", "Art Club", "Drama Club", "Science Club", "Mathletes"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        assert set(activities.keys()) == expected_keys
    
    def test_get_activities_returns_correct_structure(self):
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["participants"], list)


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_successful_signup_adds_participant(self):
        # Arrange
        activity_name = "Chess Club"
        test_email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert test_email in activities[activity_name]["participants"]
    
    def test_signup_returns_success_message(self):
        # Arrange
        activity_name = "Programming Class"
        test_email = "coder@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        result = response.json()
        
        # Assert
        assert response.status_code == 200
        assert result["message"] == f"Signed up {test_email} for {activity_name}"


class TestUnregisterEndpoint:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""
    
    def test_successful_unregister_removes_participant(self):
        # Arrange
        activity_name = "Chess Club"
        participant_to_remove = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{participant_to_remove}"
        )
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert participant_to_remove not in activities[activity_name]["participants"]
    
    def test_unregister_returns_success_message(self):
        # Arrange
        activity_name = "Soccer Team"
        participant_to_remove = "alex@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{participant_to_remove}"
        )
        result = response.json()
        
        # Assert
        assert response.status_code == 200
        assert result["message"] == f"Unregistered {participant_to_remove} from {activity_name}"
