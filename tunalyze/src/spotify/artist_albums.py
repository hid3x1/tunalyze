"""This module provides classes to interact with the Spotify API for retrieving albums of specific artists.

It includes the SpotifyArtistAlbums class for making API requests to Spotify and a factory class
SpotifyArtistAlbumsFactory for creating instances of SpotifyArtistAlbums with different configurations.
"""

import re
from typing import Any

from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOauthError

from src.spotify.api_base import SpotifyAPIBase
from src.spotify.error_handler import SpotifyErrorHandler


class SpotifyArtistAlbums(SpotifyAPIBase):
    """This class is used to interact with the Spotify API to get albums of a specific artist.

    Attributes:
        artist_uri (str): The Spotify URI of the artist.
        include_groups (str|None): A comma-separated list of album types to return.
        limit (int): The number of items to return. Default is 10.
        offset (int): The offset of the first item to return. Default is 0. Optional.
    """

    _MIN_LIMIT = 1
    _MAX_LIMIT = 50
    _LIMIT_ERROR_MESSAGE = (
        f"Limit must be between {_MIN_LIMIT} and {_MAX_LIMIT}, inclusive."
    )
    _INVALID_URI_MESSAGE = (
        "Invalid artist URI format. Expected format: 'spotify:artist:<Spotify ID>'."
    )

    def __init__(
        self,
        artist_uri: str,
        include_groups: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> None:
        """Initializes the SpotifyArtistAlbums instance with the provided parameters.

        Args:
            artist_uri (str): The Spotify URI of the artist. Must be in the format 'spotify:artist:<Spotify ID>'.
            include_groups (str|None): A comma-separated list of album types to return. Optional.
            limit (int): The number of items to return. Default is 10. Optional.
            offset (int): The offset of the first item to return. Default is 0. Optional.

        Raises:
            ValueError: If the artist URI format is invalid or the limit is outside the allowed range.
        """
        super().__init__()

        # Validate artist URI
        pattern = r"^spotify:artist:[0-9a-zA-Z]+$"
        if not re.match(pattern, artist_uri):
            raise ValueError(self._INVALID_URI_MESSAGE)
        self.artist_uri = artist_uri.split(":")[-1]
        self.include_groups = include_groups

        # Validate limit
        if not self._MIN_LIMIT <= limit <= self._MAX_LIMIT:
            raise ValueError(self._LIMIT_ERROR_MESSAGE)
        self.limit = limit
        self.offset = offset

    def __enter__(self) -> "SpotifyArtistAlbums":
        """Reinitialize the client upon entering a context and return SpotifyArtistAlbums instance."""
        super().__enter__()
        return self

    def get_albums(self) -> dict[str, Any]:
        """Retrieves the albums of the specified artist from the Spotify API.

        Returns:
            dict[str, Any]: A dictionary containing information about the artist's albums.
                            If an error occurs, it returns a dictionary with an error key.
        """
        try:
            return self.client.sp.artist_albums(
                artist_id=self.artist_uri,
                album_type=self.include_groups,
                limit=self.limit,
                offset=self.offset,
            )
        except (SpotifyException, SpotifyOauthError) as e:
            return SpotifyErrorHandler.handle_error(e)

    def __str__(self) -> str:
        """Return the string representation of the SpotifyArtistAlbums object.

        Returns:
            str: The string representation of the SpotifyArtistAlbums object.
        """
        return f"SpotifyArtistAlbums(artist_uri={self.artist_uri}, include_groups={self.include_groups}, limit={self.limit}, offset={self.offset})"


class SpotifyArtistAlbumsFactory:
    """Factory class to create SpotifyArtistAlbums objects for different album group types."""

    @staticmethod
    def artist_albums(
        artist_uri: str, limit: int = 10, offset: int = 0
    ) -> SpotifyArtistAlbums:
        """Create a SpotifyArtistAlbums instance for retrieving all types of an artist's albums.

        Args:
            artist_uri (str): The Spotify URI of the artist.
            limit (int): The number of albums to return. Default is 10.
            offset (int): The offset of the first item to return. Default is 0.

        Returns:
            SpotifyArtistAlbums: An instance of SpotifyArtistAlbums.
        """
        return SpotifyArtistAlbums(artist_uri, None, limit, offset)

    @staticmethod
    def artist_albums_album(
        artist_uri: str, limit: int = 10, offset: int = 0
    ) -> SpotifyArtistAlbums:
        """Create a SpotifyArtistAlbums instance for retrieving an artist's 'album' type albums.

        Args:
            artist_uri (str): The Spotify URI of the artist.
            limit (int): The number of albums to return. Default is 10.
            offset (int): The offset of the first item to return. Default is 0.

        Returns:
            SpotifyArtistAlbums: An instance of SpotifyArtistAlbums.
        """
        return SpotifyArtistAlbums(artist_uri, "album", limit, offset)

    @staticmethod
    def artist_albums_single(
        artist_uri: str, limit: int = 10, offset: int = 0
    ) -> SpotifyArtistAlbums:
        """Create a SpotifyArtistAlbums instance for retrieving an artist's 'single' type albums.

        Args:
            artist_uri (str): The Spotify URI of the artist.
            limit (int): The number of albums to return. Default is 10.
            offset (int): The offset of the first item to return. Default is 0.

        Returns:
            SpotifyArtistAlbums: An instance of SpotifyArtistAlbums.
        """
        return SpotifyArtistAlbums(artist_uri, "single", limit, offset)

    @staticmethod
    def artist_albums_appears_on(
        artist_uri: str, limit: int = 10, offset: int = 0
    ) -> SpotifyArtistAlbums:
        """Create a SpotifyArtistAlbums instance for retrieving an artist's 'appears_on' type albums.

        Args:
            artist_uri (str): The Spotify URI of the artist.
            limit (int): The number of albums to return. Default is 10.
            offset (int): The offset of the first item to return. Default is 0.

        Returns:
            SpotifyArtistAlbums: An instance of SpotifyArtistAlbums.
        """
        return SpotifyArtistAlbums(artist_uri, "appears_on", limit, offset)

    @staticmethod
    def artist_albums_compilation(
        artist_uri: str, limit: int = 10, offset: int = 0
    ) -> SpotifyArtistAlbums:
        """Create a SpotifyArtistAlbums instance for retrieving an artist's 'compilation' type albums.

        Args:
            artist_uri (str): The Spotify URI of the artist.
            limit (int): The number of albums to return. Default is 10.
            offset (int): The offset of the first item to return. Default is 0.

        Returns:
            SpotifyArtistAlbums: An instance of SpotifyArtistAlbums.
        """
        return SpotifyArtistAlbums(artist_uri, "compilation", limit, offset)

    @staticmethod
    def artist_albums_album_single(
        artist_uri: str, limit: int = 10, offset: int = 0
    ) -> SpotifyArtistAlbums:
        """Create a SpotifyArtistAlbums instance for retrieving an artist's 'album' and 'single' type albums.

        Args:
        artist_uri (str): The Spotify URI of the artist.
        limit (int): The number of albums to return. Default is 10.
        offset (int): The offset of the first item to return. Default is 0.

        Returns:
        SpotifyArtistAlbums: An instance of SpotifyArtistAlbums.
        """
        return SpotifyArtistAlbums(artist_uri, "album,single", limit, offset)

    @staticmethod
    def artist_albums_album_appears_on(
        artist_uri: str, limit: int = 10, offset: int = 0
    ) -> SpotifyArtistAlbums:
        """Create a SpotifyArtistAlbums instance for retrieving an artist's 'album' and 'appears_on' type albums.

        Args:
        artist_uri (str): The Spotify URI of the artist.
        limit (int): The number of albums to return. Default is 10.
        offset (int): The offset of the first item to return. Default is 0.

        Returns:
        SpotifyArtistAlbums: An instance of SpotifyArtistAlbums.
        """
        return SpotifyArtistAlbums(artist_uri, "album,appears_on", limit, offset)

    @staticmethod
    def artist_albums_album_compilation(
        artist_uri: str, limit: int = 10, offset: int = 0
    ) -> SpotifyArtistAlbums:
        """Create a SpotifyArtistAlbums instance for retrieving an artist's 'album' and 'compilation' type albums.

        Args:
        artist_uri (str): The Spotify URI of the artist.
        limit (int): The number of albums to return. Default is 10.
        offset (int): The offset of the first item to return. Default is 0.

        Returns:
        SpotifyArtistAlbums: An instance of SpotifyArtistAlbums.
        """
        return SpotifyArtistAlbums(artist_uri, "album,compilation", limit, offset)


# Example usage
if __name__ == "__main__":
    artist_uri = "spotify:artist:1vCWHaC5f2uS3yhpwWbIA6"
    with SpotifyArtistAlbumsFactory.artist_albums_album_single(
        artist_uri, limit=1
    ) as artist_albums:
        album_results = artist_albums.get_albums()
        if "error" in album_results:
            print(album_results["error"])  # noqa: T201
        else:
            print(album_results)  # noqa: T201
