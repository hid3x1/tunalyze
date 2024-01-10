import pytest

from src.config import Config
from src.spotify.client import SpotifyClient


# Fixture for mocked Config class
@pytest.fixture()
def mock_config(mocker):
    """A pytest fixture to mock the Config class.

    It sets up mocked client_id and client_secret properties for the Config class using pytest-mocker.
    Returns a tuple of the mocked client_id and client_secret for further assertions in tests.
    """
    mocker.patch.object(Config, "__init__", return_value=None)
    client_id = mocker.patch.object(
        Config,
        "client_id",
        new_callable=mocker.PropertyMock,
        return_value="test_client_id",
    )
    client_secret = mocker.patch.object(
        Config,
        "client_secret",
        new_callable=mocker.PropertyMock,
        return_value="test_client_secret",
    )
    return client_id, client_secret


# Fixture for SpotifyClient instance
@pytest.fixture()
def spotify_client(mock_config):
    """A pytest fixture to create a SpotifyClient instance.

    It uses the mock_config fixture to set up a mocked Config class before instantiating the SpotifyClient.
    Returns an instance of SpotifyClient for use in tests.
    """
    return SpotifyClient()


# Test for SpotifyClient initialization
def test_init_spotify_client(spotify_client, mock_config):
    """Test the initialization of SpotifyClient."""
    client_id, client_secret = mock_config
    client_id.assert_called_once()
    client_secret.assert_called_once()
    assert spotify_client._auth_manager.client_id == "test_client_id"
    assert spotify_client._auth_manager.client_secret == "test_client_secret"


# Test for entering and exiting the context manager
def test_enter_exit_spotify_client(spotify_client):
    """Test the __enter__ and __exit__ methods of SpotifyClient."""
    with spotify_client as client:
        assert isinstance(client, SpotifyClient)
    # Add any necessary assertions for the __exit__ method if needed


# Test for the representation of SpotifyClient
def test_repr_spotify_client(spotify_client):
    """Test the __repr__ method of SpotifyClient."""
    repr_string = repr(spotify_client)
    assert (
        repr_string
        == "SpotifyClient(client_id=test_client_id, client_secret=test_client_secret)"
    )
