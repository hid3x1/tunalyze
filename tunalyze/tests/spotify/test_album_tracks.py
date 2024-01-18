import pytest
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOauthError

from src.spotify.album_tracks import SpotifyAlbumTracks


@pytest.fixture()
def valid_album_tracks():
    """Fixture for creating a SpotifyAlbumTracks instance with a valid URI."""
    return SpotifyAlbumTracks("spotify:album:validSpotifyID", limit=10, offset=0)


@pytest.fixture()
def invalid_album_tracks():
    """Fixture for creating a SpotifyAlbumTracks instance with an invalid URI."""
    return lambda: SpotifyAlbumTracks("invalidUri")


@pytest.fixture()
def mock_successful_response(mocker):
    """Fixture for mocking a successful response from the Spotify API."""
    mock_response = {
        "items": [
            {"name": "Track 1", "id": "track1"},
            {"name": "Track 2", "id": "track2"},
        ]
    }
    return mocker.patch(
        "src.spotify.api_base.SpotifyAPIBase.client.sp.album_tracks",
        return_value=mock_response,
    )


@pytest.fixture()
def mock_spotify_exception(mocker):
    """Fixture for mocking a SpotifyException from the Spotify API."""
    return mocker.patch(
        "src.spotify.api_base.SpotifyAPIBase.client.sp.album_tracks",
        side_effect=SpotifyException(400, "Bad Request"),
    )


@pytest.fixture()
def mock_oauth_error(mocker):
    """Fixture for mocking a SpotifyOauthError from the Spotify API."""
    return mocker.patch(
        "src.spotify.api_base.SpotifyAPIBase.client.sp.album_tracks",
        side_effect=SpotifyOauthError(),
    )


def test_init_valid_uri(valid_album_tracks):
    """Test successful initialization with a valid URI."""
    assert valid_album_tracks.album_uri == "validSpotifyID"


def test_init_invalid_uri(invalid_album_tracks):
    """Test initialization with an invalid URI."""
    expected_error_message = (
        "Invalid album URI format. Expected format: 'spotify:album:<Spotify ID>'."
    )
    with pytest.raises(ValueError, match=expected_error_message):
        invalid_album_tracks()


def test_get_tracks_success(valid_album_tracks, mock_successful_response):
    """Test successful retrieval of tracks."""
    tracks = valid_album_tracks.get_tracks()
    assert tracks == mock_successful_response.return_value


def test_get_tracks_spotify_exception(valid_album_tracks, mock_spotify_exception):
    """Test handling of SpotifyException."""
    with pytest.raises(SpotifyException):
        valid_album_tracks.get_tracks()


def test_get_tracks_oauth_error(valid_album_tracks, mock_oauth_error):
    """Test handling of SpotifyOauthError."""
    with pytest.raises(SpotifyOauthError):
        valid_album_tracks.get_tracks()


# Additional tests can be added as needed.
