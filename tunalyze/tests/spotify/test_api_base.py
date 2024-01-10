import pytest

from src.spotify.api_base import SpotifyAPIBase
from src.spotify_client import SpotifyClient


@pytest.fixture()
def api_base(mocker):
    """Fixture to create a SpotifyAPIBase instance with a mocked SpotifyClient."""
    mocker.patch("spotify_api_base.SpotifyClient")
    return SpotifyAPIBase()


def test_initialization(api_base):
    """Test if SpotifyAPIBase initializes the Spotify client correctly."""
    assert isinstance(api_base.client, SpotifyClient)


def test_enter_method(api_base):
    """Test the __enter__ method of SpotifyAPIBase."""
    returned_value = api_base.__enter__()
    assert returned_value == api_base


def test_exit_method(api_base):
    """Test the __exit__ method of SpotifyAPIBase."""
    api_base.__exit__(None, None, None)
    with pytest.raises(AttributeError):
        _ = (
            api_base.client
        )  # This should raise AttributeError since client should be deleted


def test_str_representation(api_base):
    """Test the string representation of SpotifyAPIBase."""
    assert str(api_base) == "SpotifyAPIBase"
