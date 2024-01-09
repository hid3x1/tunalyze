import pytest
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOauthError

from src.spotify_error_handler import SpotifyErrorHandler


# Fixtures
@pytest.fixture()
def auth_error_exception():
    """Fixture to provide a SpotifyException instance for authentication errors."""
    return SpotifyException(http_status=401, msg="Unauthorized", code="auth_error")


@pytest.fixture()
def rate_limit_exception():
    """Fixture to provide a SpotifyException instance for rate limit exceeded errors."""
    return SpotifyException(
        http_status=429, msg="Too Many Requests", code="rate_limit_error"
    )


@pytest.fixture()
def generic_spotify_exception():
    """Fixture to provide a generic SpotifyException instance."""
    return SpotifyException(
        http_status=500, msg="Internal Server Error", code="server_error"
    )


@pytest.fixture()
def oauth_error_exception():
    """Fixture to provide a SpotifyOAuthError instance."""
    return SpotifyOauthError("OAuth error")


@pytest.fixture()
def unexpected_exception():
    """Fixture to provide a generic Exception instance."""
    return Exception("Unexpected error")


# Test Functions
def test_handle_authentication_error(auth_error_exception):
    """Test handling of SpotifyException with an authentication error."""
    result = SpotifyErrorHandler.handle_error(auth_error_exception)
    assert result == {"error": "Authentication failed: Check your Spotify credentials."}


def test_handle_rate_limit_error(rate_limit_exception):
    """Test handling of SpotifyException with a rate limit exceeded error."""
    result = SpotifyErrorHandler.handle_error(rate_limit_exception)
    assert result == {"error": "Rate limit exceeded: Try again later."}


def test_handle_generic_spotify_exception(generic_spotify_exception):
    """Test handling of a generic SpotifyException."""
    result = SpotifyErrorHandler.handle_error(generic_spotify_exception)
    assert result == {"error": f"Spotify API error: {generic_spotify_exception}"}


def test_handle_oauth_error(oauth_error_exception):
    """Test handling of a SpotifyOAuthError."""
    result = SpotifyErrorHandler.handle_error(oauth_error_exception)
    assert result == {"error": f"OAuth error: {oauth_error_exception}"}


def test_handle_unexpected_error(unexpected_exception):
    """Test handling of an unexpected generic Exception."""
    result = SpotifyErrorHandler.handle_error(unexpected_exception)
    assert result == {"error": f"An unexpected error occurred: {unexpected_exception}"}
