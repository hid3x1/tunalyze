import importlib

import pytest

from src import config


@pytest.fixture()
def _mock_env_vars_with_values(mocker) -> None:
    """Setup mock environment variables with values.

    This fixture is intended for internal use in tests.
    """
    mocker.patch(
        "os.getenv",
        side_effect=lambda key: {
            "SPOTIFY_CLIENT_ID": "test_id",
            "SPOTIFY_CLIENT_SECRET": "test_secret",
        }.get(key),
    )
    importlib.reload(config)


@pytest.fixture()
def _mock_env_vars_with_none(mocker) -> None:
    """Setup mock environment variables with None.

    This fixture is intended for internal use in tests.
    """
    mocker.patch("os.getenv", return_value=None)
    importlib.reload(config)


@pytest.mark.usefixtures("_mock_env_vars_with_values")
def test_config_with_env_vars():
    """Test if environment variables are correctly used."""
    # Create a Config instance
    config_instance = config.Config()

    # Check if the values are correctly set
    assert config_instance.client_id == "test_id"
    assert config_instance.client_secret == "test_secret"


@pytest.mark.usefixtures("_mock_env_vars_with_none")
def test_config_without_env_vars():
    """Test the default values when environment variables are not set."""
    # Create a Config instance
    config_instance = config.Config()

    # Check if the values are None
    assert config_instance.client_id is None
    assert config_instance.client_secret is None


@pytest.mark.usefixtures("_mock_env_vars_with_values")
def test_config_str_representation():
    """Test the string representation of the Config object."""
    config_instance = config.Config()

    # Check the string representation
    assert (
        str(config_instance) == "Config(client_id=test_id, client_secret=test_secret)"
    )
