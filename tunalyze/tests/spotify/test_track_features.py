import pytest
from spotipy.exceptions import SpotifyException

from src.spotify.error_handler import SpotifyErrorHandler
from src.spotify.track_features import SpotifyTrackFeatures


@pytest.fixture()
def spotify_track_features(mocker):
    """Fixture to create a mock SpotifyTrackFeatures object."""
    mocker.patch("src.spotify.track_features.SpotifyAPIBase")
    return SpotifyTrackFeatures()


@pytest.fixture()
def mock_spotify_api(spotify_track_features, mocker):
    """Fixture to create a mock SpotifyTrackFeatures object."""
    return mocker.patch.object(spotify_track_features.client.sp, "audio_features")


def test_validate_track_uris_valid(spotify_track_features):
    """Test that validate_track_uris returns True for valid track URIs."""
    valid_uris = ["spotify:track:123", "spotify:track:456"]
    assert spotify_track_features.validate_track_uris(valid_uris) is True


def test_validate_track_uris_invalid(spotify_track_features):
    """Test that validate_track_uris returns False for invalid track URIs."""
    invalid_uris = ["invalid:uri", "123"]
    assert spotify_track_features.validate_track_uris(invalid_uris) is False


def test_fetch_audio_features_no_tracks(spotify_track_features):
    """Test fetching audio features with no tracks raises ValueError with specific message."""
    with pytest.raises(ValueError, match=spotify_track_features._NO_TRACKS_MSG):
        spotify_track_features.fetch_audio_features([])


def test_fetch_audio_features_invalid_uris(spotify_track_features):
    """Test fetching audio features with invalid URIs raises ValueError with specific message."""
    with pytest.raises(
        ValueError, match=spotify_track_features._INVALID_TRACK_URIS_MSG
    ):
        spotify_track_features.fetch_audio_features(["invalid:uri"])


def test_fetch_audio_features_success(spotify_track_features, mock_spotify_api):
    """Test successful fetching of audio features."""
    track_uris = ["spotify:track:123", "spotify:track:456"]
    mock_spotify_api.return_value = [
        {"id": "123", "features": "data"},
        {"id": "456", "features": "data"},
    ]

    result = spotify_track_features.fetch_audio_features(track_uris)

    assert result == [
        {"id": "123", "features": "data"},
        {"id": "456", "features": "data"},
    ]
    mock_spotify_api.assert_called_once_with(track_uris[:100])


def test_fetch_audio_features_spotify_exception(spotify_track_features, mocker):
    """Test handling of SpotifyException during fetching of audio features."""
    mocker.patch("src.spotify.track_features.SpotifyErrorHandler.handle_error")
    mocker.patch(
        "src.spotify.track_features.SpotifyTrackFeatures.get_batch_audio_features",
        side_effect=SpotifyException(404, "Not found"),
    )

    track_uris = ["spotify:track:123"]

    result = spotify_track_features.fetch_audio_features(track_uris)

    assert result is None
    spotify_track_features.get_batch_audio_features.assert_called_once_with(
        track_uris, 0
    )
    SpotifyErrorHandler.handle_error.assert_called_once()


def test_get_batch_audio_features(spotify_track_features, mock_spotify_api):
    """Test fetching a batch of audio features."""
    mock_spotify_api.return_value = [{"id": "123", "features": "data"}]
    track_uris = ["spotify:track:123"]
    result = spotify_track_features.get_batch_audio_features(track_uris, 0)

    assert result == [{"id": "123", "features": "data"}]
    mock_spotify_api.assert_called_once_with(track_uris)


def test_fetch_audio_features_api_error(spotify_track_features, mocker):
    """Test handling of API error during fetching of audio features."""
    mocker.patch("src.spotify.track_features.SpotifyErrorHandler.handle_error")
    mocker.patch.object(
        spotify_track_features.client.sp,
        "audio_features",
        side_effect=SpotifyException(500, "Server Error"),
    )

    track_uris = ["spotify:track:123"]

    result = spotify_track_features.fetch_audio_features(track_uris)

    assert result is None
    spotify_track_features.client.sp.audio_features.assert_called_once_with(
        track_uris[:100]
    )
    SpotifyErrorHandler.handle_error.assert_called_once()
