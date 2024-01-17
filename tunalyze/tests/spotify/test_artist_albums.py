import pytest
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOauthError

from src.spotify.artist_albums import SpotifyArtistAlbums, SpotifyArtistAlbumsFactory

# Constants for testing
VALID_ARTIST_URI = "spotify:artist:1vCWHaC5f2uS3yhpwWbIA6"
INVALID_ARTIST_URI = "invalid_uri"
VALID_INCLUDE_GROUPS = "album,single"
VALID_LIMIT = 10
VALID_OFFSET = 0


@pytest.fixture()
def mock_spotify_client(mocker):
    """A pytest fixture that creates a mock SpotifyClient."""
    mock = mocker.patch("src.spotify.client.SpotifyClient", autospec=True)
    mock_instance = mock.return_value
    mock_instance.sp.artist_albums.return_value = {"albums": "mock albums"}
    mock_instance.sp.artist_albums.side_effect = [
        SpotifyException("Error"),
        SpotifyOauthError("Auth Error"),
    ]
    return mock_instance


# URI validation tests
def test_validate_artist_uri():
    """Test the URI validation in SpotifyArtistAlbums initialization."""
    # Valid URI
    valid_artist_albums = SpotifyArtistAlbums(VALID_ARTIST_URI)
    assert valid_artist_albums.artist_uri == VALID_ARTIST_URI.split(":")[-1]

    # Invalid URI
    with pytest.raises(ValueError, match=SpotifyArtistAlbums._INVALID_URI_MESSAGE):
        SpotifyArtistAlbums(INVALID_ARTIST_URI)


# Initialization tests
def test_spotify_artist_albums_initialization():
    """Test the initialization of SpotifyArtistAlbums with valid parameters."""
    artist_albums = SpotifyArtistAlbums(
        VALID_ARTIST_URI, VALID_INCLUDE_GROUPS, VALID_LIMIT, VALID_OFFSET
    )
    assert artist_albums.artist_uri == VALID_ARTIST_URI.split(":")[-1]
    assert artist_albums.include_groups == VALID_INCLUDE_GROUPS
    assert artist_albums.limit == VALID_LIMIT
    assert artist_albums.offset == VALID_OFFSET


# Context manager tests
def test_spotify_artist_albums_context_manager(mock_spotify_client):
    """Test the context manager functionality of SpotifyArtistAlbums."""
    with SpotifyArtistAlbums(VALID_ARTIST_URI) as artist_albums:
        assert artist_albums.client.sp is not None
    with pytest.raises(AttributeError):
        _ = artist_albums.client


# Test the get_albums method
def test_get_albums_method(mock_spotify_client):
    """Test the get_albums method of SpotifyArtistAlbums."""
    artist_albums = SpotifyArtistAlbums(
        VALID_ARTIST_URI, VALID_INCLUDE_GROUPS, VALID_LIMIT, VALID_OFFSET
    )
    result = artist_albums.get_albums()
    assert result == {"albums": "mock albums"}
    mock_spotify_client.sp.artist_albums.assert_called_once_with(
        artist_id=VALID_ARTIST_URI.split(":")[-1],
        album_type=VALID_INCLUDE_GROUPS,
        limit=VALID_LIMIT,
        offset=VALID_OFFSET,
    )


def test_get_albums_method_handles_exceptions(mock_spotify_client):
    """Test the exception handling in the get_albums method of SpotifyArtistAlbums."""
    artist_albums = SpotifyArtistAlbums(
        VALID_ARTIST_URI, VALID_INCLUDE_GROUPS, VALID_LIMIT, VALID_OFFSET
    )

    # Testing SpotifyException handling
    result = artist_albums.get_albums()
    assert "error" in result

    # Reset mock to test SpotifyOAuthError
    mock_spotify_client.sp.artist_albums.side_effect = SpotifyOauthError("Auth Error")

    # Testing SpotifyOAuthError handling
    result = artist_albums.get_albums()
    assert "error" in result


# Test the __str__ method
def test_str_method():
    """Test the string representation of SpotifyArtistAlbums."""
    artist_albums = SpotifyArtistAlbums(
        VALID_ARTIST_URI, VALID_INCLUDE_GROUPS, VALID_LIMIT, VALID_OFFSET
    )
    assert (
        str(artist_albums)
        == f"SpotifyArtistAlbums(artist_uri={VALID_ARTIST_URI.split(':')[-1]}, include_groups={VALID_INCLUDE_GROUPS}, limit={VALID_LIMIT}, offset={VALID_OFFSET})"
    )


# Test SpotifyArtistAlbumsFactory with different include_group
@pytest.mark.parametrize(
    ("factory_method", "include_groups"),
    [
        (SpotifyArtistAlbumsFactory.artist_albums, None),
        (SpotifyArtistAlbumsFactory.artist_albums_album, "album"),
        (SpotifyArtistAlbumsFactory.artist_albums_single, "single"),
        (SpotifyArtistAlbumsFactory.artist_albums_appears_on, "appears_on"),
        (SpotifyArtistAlbumsFactory.artist_albums_compilation, "compilation"),
        (SpotifyArtistAlbumsFactory.artist_albums_album_single, "album,single"),
        (SpotifyArtistAlbumsFactory.artist_albums_album_appears_on, "album,appears_on"),
        (
            SpotifyArtistAlbumsFactory.artist_albums_album_compilation,
            "album,compilation",
        ),
        # Add more methods and corresponding search types here
    ],
)

# Test SpotifyArtistAlbumsFactory
def test_spotify_artist_albums_factory(factory_method, include_groups):
    """Test the factory methods of SpotifyArtistAlbumsFactory for creating artist albums instances."""
    artist_albums = factory_method(VALID_ARTIST_URI, VALID_LIMIT, VALID_OFFSET)
    assert isinstance(artist_albums, SpotifyArtistAlbums)
    assert artist_albums.artist_uri == VALID_ARTIST_URI.split(":")[-1]
    assert artist_albums.include_groups == include_groups
    assert artist_albums.limit == VALID_LIMIT
    assert artist_albums.offset == VALID_OFFSET
