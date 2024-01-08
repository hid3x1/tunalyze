import pytest

from src.config import Config


@pytest.fixture()
def _mock_env_vars_with_values(mocker) -> None:
    """Setup mock environment variables with values."""
    mocker.patch(
        "os.getenv",
        side_effect=lambda key: {
            "SPOTIFY_CLIENT_ID": "test_id",
            "SPOTIFY_CLIENT_SECRET": "test_secret",
        }.get(key),
    )


@pytest.fixture()
def _mock_env_vars_with_none(mocker) -> None:
    """Setup mock environment variables with None."""
    mocker.patch("os.getenv", return_value=None)


@pytest.mark.usefixtures("_mock_env_vars_with_values")
def test_config_with_env_vars():
    """Test if environment variables are correctly used."""
    # Create a Config instance
    config = Config()

    # Check if the values are correctly set
    assert config.client_id == "test_id"
    assert config.client_secret == "test_secret"


@pytest.mark.usefixtures("_mock_env_vars_with_none")
def test_config_without_env_vars():
    """Test the default values when environment variables are not set."""
    # Create a Config instance
    config = Config()

    # Check if the values are None
    assert config.client_id is None
    assert config.client_secret is None


def test_config_str_representation():
    """Test the string representation of the Config object."""
    config = Config()
    # Manually set the client_id and client_secret for testing
    config._client_id = "test_id"
    config._client_secret = "test_secret"

    # Check the string representation
    assert str(config) == "Config(client_id=test_id, client_secret=test_secret)"
