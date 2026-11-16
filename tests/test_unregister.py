"""Tests for DELETE /activities/{activity_name}/unregister endpoint."""

import pytest


class TestUnregister:
    """Test suite for activity unregistration functionality."""

    def test_successful_unregister_removes_participant(self, client, reset_activities):
        """
        GIVEN a student signed up for an activity
        WHEN requesting to unregister
        THEN participant is removed from activity
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        initial_count = len(client.get("/activities").json()[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 200
        updated_count = len(client.get("/activities").json()[activity_name]["participants"])
        assert updated_count == initial_count - 1
        assert email not in client.get("/activities").json()[activity_name]["participants"]

    def test_successful_unregister_returns_success_message(self, client, reset_activities):
        """
        GIVEN a student signed up for an activity
        WHEN requesting to unregister
        THEN return success message
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_nonexistent_activity_returns_404(self, client, reset_activities):
        """
        GIVEN a non-existent activity
        WHEN attempting to unregister
        THEN return 404 not found
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_unregister_nonexistent_participant_returns_400(self, client, reset_activities):
        """
        GIVEN a student not signed up for an activity
        WHEN attempting to unregister
        THEN return 400 bad request
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notstudent@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"].lower()

    def test_unregister_participant_no_longer_appears_in_list(self, client, reset_activities):
        """
        GIVEN a student signed up for an activity
        WHEN unregistering that student
        THEN participant no longer appears in activity's participant list
        """
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"
        initial_participants = client.get("/activities").json()[activity_name]["participants"]
        assert email in initial_participants

        # Act
        client.delete(f"/activities/{activity_name}/unregister?email={email}")

        # Assert
        updated_participants = client.get("/activities").json()[activity_name]["participants"]
        assert email not in updated_participants
        assert len(updated_participants) == len(initial_participants) - 1

    def test_unregister_multiple_participants_sequentially(self, client, reset_activities):
        """
        GIVEN multiple students signed up for an activity
        WHEN unregistering them one by one
        THEN each unregistration succeeds and participant is removed
        """
        # Arrange
        from src.app import activities as app_activities
        activity_name = "Multi Student Activity"
        app_activities[activity_name] = {
            "description": "Test activity",
            "schedule": "Monday 3:00 PM",
            "max_participants": 10,
            "participants": ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]
        }
        emails_to_remove = ["alice@mergington.edu", "bob@mergington.edu"]

        # Act
        for email in emails_to_remove:
            response = client.delete(
                f"/activities/{activity_name}/unregister?email={email}"
            )
            assert response.status_code == 200

        # Assert
        updated_participants = client.get("/activities").json()[activity_name]["participants"]
        assert "charlie@mergington.edu" in updated_participants
        for email in emails_to_remove:
            assert email not in updated_participants

    def test_unregister_then_signup_again_allowed(self, client, reset_activities):
        """
        GIVEN a student unregisters from an activity
        WHEN that student signs up again
        THEN signup succeeds
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act - Unregister
        client.delete(f"/activities/{activity_name}/unregister?email={email}")

        # Assert first unregister
        participants = client.get("/activities").json()[activity_name]["participants"]
        assert email not in participants

        # Act - Sign up again
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert second signup
        assert response.status_code == 200
        participants = client.get("/activities").json()[activity_name]["participants"]
        assert email in participants
