import pytest
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOauthError

from src.spotify.search import SpotifySearch, SpotifySearchFactory
from src.spotify_client import SpotifyClient

# Constants for testing
VALID_QUERY = "test query"
INVALID_QUERY = 123  # An invalid query type for testing
VALID_SEARCH_TYPE = "artist"
INVALID_SEARCH_TYPE = 123  # An invalid search type for testing
VALID_LIMIT = 10
INVALID_LIMIT = 100  # Out of valid range for testing
VALID_MARKET = "US"
INVALID_MARKET = 123  # An invalid market type for testing


@pytest.fixture()
def mock_spotify_client(mocker):
    """A pytest fixture that creates a mock SpotifyClient."""
    mock = mocker.patch("src.spotify_client.SpotifyClient", autospec=True)
    mock_instance = mock.return_value
    mock_instance.sp.search.return_value = {"results": "mock results"}
    mock_instance.sp.search.side_effect = [
        SpotifyException("Error"),
        SpotifyOauthError("Auth Error"),
    ]
    return mock_instance


# Test initialization with valid and invalid parameters
def test_spotify_search_initialization():
    """Test the initialization of SpotifySearch with valid and invalid parameters."""
    # Valid initialization
    search = SpotifySearch(VALID_QUERY, VALID_SEARCH_TYPE, VALID_LIMIT, VALID_MARKET)
    assert search.query == VALID_QUERY
    assert search.search_type == VALID_SEARCH_TYPE
    assert search.limit == VALID_LIMIT
    assert search.market == VALID_MARKET

    # Invalid limit
    with pytest.raises(ValueError, match=SpotifySearch._LIMIT_ERROR_MESSAGE) as excinfo:
        SpotifySearch(VALID_QUERY, VALID_SEARCH_TYPE, INVALID_LIMIT, VALID_MARKET)
    assert str(excinfo.value) == SpotifySearch._LIMIT_ERROR_MESSAGE

    # More test cases for other invalid parameters can be added here


# Test the context manager functionality
def test_spotify_search_context_manager(mock_spotify_client):
    """Test the context manager functionality of SpotifySearch."""
    with SpotifySearch(
        VALID_QUERY, VALID_SEARCH_TYPE, VALID_LIMIT, VALID_MARKET
    ) as search:
        assert isinstance(search.client, SpotifyClient)
    # Test if client is deleted after exiting the context
    with pytest.raises(AttributeError):
        _ = search.client


# Test the search method
def test_search_method(mock_spotify_client):
    """Test the search method of SpotifySearch."""
    search = SpotifySearch(VALID_QUERY, VALID_SEARCH_TYPE, VALID_LIMIT, VALID_MARKET)
    result = search.search()
    assert result == {"results": "mock results"}
    mock_spotify_client.sp.search.assert_called_once_with(
        q=VALID_QUERY, limit=VALID_LIMIT, type=VALID_SEARCH_TYPE, market=VALID_MARKET
    )


def test_search_method_handles_exceptions(mock_spotify_client):
    """Test the search method of SpotifySearch handles exceptions correctly."""
    search = SpotifySearch(VALID_QUERY, VALID_SEARCH_TYPE, VALID_LIMIT, VALID_MARKET)

    # Testing SpotifyException handling
    result = search.search()
    assert (
        "error" in result
    )  # Replace this with the actual structure of the error response

    # Reset mock to test SpotifyOAuthError
    mock_spotify_client.sp.search.side_effect = SpotifyOauthError("Auth Error")

    # Testing SpotifyOAuthError handling
    result = search.search()
    assert (
        "error" in result
    )  # Replace this with the actual structure of the error response


# Test the __str__ method
def test_str_method():
    """Test the string representation of SpotifySearch."""
    search = SpotifySearch(VALID_QUERY, VALID_SEARCH_TYPE, VALID_LIMIT, VALID_MARKET)
    assert (
        str(search)
        == f"SpotifySearch(query={VALID_QUERY}, limit={VALID_LIMIT}, type={VALID_SEARCH_TYPE}, market={VALID_MARKET})"
    )


# Test SpotifySearchFactory
@pytest.mark.parametrize(
    ("method", "search_type"),
    [
        (SpotifySearchFactory.artist_search, "artist"),
        (SpotifySearchFactory.track_search, "track"),
        (SpotifySearchFactory.album_search, "album"),
        (SpotifySearchFactory.playlist_search, "playlist"),
        (SpotifySearchFactory.artist_track_search, "artist,track"),
        (SpotifySearchFactory.artist_album_search, "artist,album"),
        (SpotifySearchFactory.artist_playlist_search, "artist,playlist"),
        (SpotifySearchFactory.track_album_search, "track,album"),
        (SpotifySearchFactory.track_playlist_search, "track,playlist"),
        (SpotifySearchFactory.album_playlist_search, "album,playlist"),
        (SpotifySearchFactory.artist_track_album_search, "artist,track,album"),
        (SpotifySearchFactory.artist_track_playlist_search, "artist,track,playlist"),
        (SpotifySearchFactory.artist_album_playlist_search, "artist,album,playlist"),
        (SpotifySearchFactory.track_album_playlist_search, "track,album,playlist"),
        (
            SpotifySearchFactory.artist_track_album_playlist_search,
            "artist,track,album,playlist",
        ),
        # Add more methods and corresponding search types here
    ],
)
def test_spotify_search_factory(method, search_type):
    """Test the SpotifySearchFactory methods for creating search instances."""
    search = method(VALID_QUERY, VALID_LIMIT, VALID_MARKET)
    assert isinstance(search, SpotifySearch)
    assert search.query == VALID_QUERY
    assert search.search_type == search_type
    assert search.limit == VALID_LIMIT
    assert search.market == VALID_MARKET


# More tests can be added to cover all factory methods and scenarios
