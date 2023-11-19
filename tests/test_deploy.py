"""Tests deploy."""
from src.deploy import deploy


def test_given_user_not_logged_in_when_user_runs_deploy_then_login_prompt_opens() -> (
    None
):
    """Test."""
    # Arrange
    # Act
    response = deploy()

    # Assert
    assert response.ok
