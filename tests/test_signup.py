"""Tests for POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestSignup:
    """Test suite for activity signup functionality."""

    def test_successful_signup_adds_participant(self, client, reset_activities):
        """
        GIVEN a valid activity and email
        WHEN posting to signup endpoint
        THEN participant is added to activity
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        initial_count = len(client.get("/activities").json()[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        updated_count = len(client.get("/activities").json()[activity_name]["participants"])
        assert updated_count == initial_count + 1
        assert email in client.get("/activities").json()[activity_name]["participants"]

    def test_successful_signup_returns_success_message(self, client, reset_activities):
        """
        GIVEN a valid activity and email
        WHEN posting to signup endpoint
        THEN return success message
        """
        # Arrange
        activity_name = "Programming Class"
        email = "alice@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_duplicate_registration_prevented(self, client, reset_activities):
        """
        GIVEN a student already signed up for an activity
        WHEN attempting to sign up again
        THEN signup is rejected
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 400
        assert "already" in response.json()["detail"].lower()

    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities):
        """
        GIVEN a non-existent activity
        WHEN attempting to sign up
        THEN return 404 not found
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_at_max_capacity_rejected(self, client, reset_activities):
        """
        GIVEN an activity at max capacity
        WHEN attempting to sign up a new student
        THEN signup is rejected with capacity error
        """
        # Arrange
        from src.app import activities as app_activities
        activity_name = "Full Activity"
        app_activities[activity_name] = {
            "description": "At capacity",
            "schedule": "Monday 3:00 PM",
            "max_participants": 2,
            "participants": ["student1@mergington.edu", "student2@mergington.edu"]
        }
        email = "student3@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 400
        assert "capacity" in response.json()["detail"].lower()

    def test_signup_to_activity_with_one_spot_left(self, client, reset_activities):
        """
        GIVEN an activity with one spot available
        WHEN signing up a new student
        THEN signup succeeds
        """
        # Arrange
        from src.app import activities as app_activities
        activity_name = "Almost Full Activity"
        app_activities[activity_name] = {
            "description": "One spot left",
            "schedule": "Monday 3:00 PM",
            "max_participants": 2,
            "participants": ["student1@mergington.edu"]
        }
        email = "student2@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        updated_activity = client.get("/activities").json()[activity_name]
        assert email in updated_activity["participants"]
        assert len(updated_activity["participants"]) == 2

    def test_signup_multiple_different_students_to_same_activity(self, client, reset_activities):
        """
        GIVEN an activity with available spots
        WHEN multiple different students sign up
        THEN all signups succeed
        """
        # Arrange
        activity_name = "Programming Class"
        emails = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]

        # Act
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup?email={email}"
            )
            assert response.status_code == 200

        # Assert
        updated_activity = client.get("/activities").json()[activity_name]
        for email in emails:
            assert email in updated_activity["participants"]
