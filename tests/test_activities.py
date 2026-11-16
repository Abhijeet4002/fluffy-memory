"""Tests for GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for retrieving all activities."""

    def test_get_all_activities_returns_success(self, client, reset_activities):
        """
        GIVEN the API is running
        WHEN requesting all activities
        THEN return 200 status code
        """
        # Arrange
        # (no specific setup needed, using default state)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200

    def test_get_all_activities_returns_all_activities(self, client, reset_activities):
        """
        GIVEN the API is running with activities
        WHEN requesting all activities
        THEN return all activities in response
        """
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert len(data) == 3
        for activity_name in expected_activities:
            assert activity_name in data

    def test_get_activities_returns_correct_structure(self, client, reset_activities):
        """
        GIVEN the API is running
        WHEN requesting all activities
        THEN each activity has required fields
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            for field in required_fields:
                assert field in activity_data, f"Missing field '{field}' in {activity_name}"

    def test_get_activities_includes_participants(self, client, reset_activities):
        """
        GIVEN activities have signed-up participants
        WHEN requesting all activities
        THEN participants list includes all signed-up students
        """
        # Arrange
        expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert data["Chess Club"]["participants"] == expected_chess_participants

    def test_get_activities_empty_activities_have_empty_participants(self, client, reset_activities):
        """
        GIVEN activities with no participants
        WHEN requesting all activities
        THEN activities have empty participant lists
        """
        # Arrange
        from src.app import activities as app_activities
        app_activities["Empty Activity"] = {
            "description": "Test activity",
            "schedule": "Monday 3:00 PM",
            "max_participants": 10,
            "participants": []
        }

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert data["Empty Activity"]["participants"] == []

    def test_get_activities_returns_max_participants_field(self, client, reset_activities):
        """
        GIVEN the API is running
        WHEN requesting all activities
        THEN each activity includes max_participants field
        """
        # Arrange
        expected_chess_max = 12

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert data["Chess Club"]["max_participants"] == expected_chess_max
