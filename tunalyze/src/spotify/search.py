"""This module provides a class for searching Spotify's music catalog.

It uses the Spotify API to perform search queries for artists, albums, tracks, etc.
"""

from types import TracebackType
from typing import Any

from spotify_client import SpotifyClient


class SpotifySearch:
    """SpotifySearch is a class for performing search queries using the Spotify API.

    Attributes:
        query (str): The search query.
        search_type (str): The type of search (e.g., 'artist', 'album').
        limit (int): The number of search results to return.
        market (str): The market in which the search is performed.
    """

    _MIN_LIMIT = 1
    _MAX_LIMIT = 50
    _LIMIT_ERROR_MESSAGE = (
        f"Limit must be between {_MIN_LIMIT} and {_MAX_LIMIT}, inclusive."
    )

    def __init__(
        self, query: str, search_type: str, limit: int = 10, market: str | None = None
    ) -> None:
        """Initialize the SpotifySearch object with search parameters.

        Args:
            query (str): The search query.
            search_type (str): The type of search (e.g., 'artist', 'album').
            limit (int): The number of search results to return. Must be between _MIN_LIMIT and _MAX_LIMIT, inclusive.
            market (str | None): The market in which the search is performed, default is None.

        Raises:
            ValueError: If the limit is outside the range of _MIN_LIMIT to _MAX_LIMIT.
        """
        if not self._MIN_LIMIT <= limit <= self._MAX_LIMIT:
            raise ValueError(self._LIMIT_ERROR_MESSAGE)

        self.query = query
        self.search_type = search_type
        self.limit = limit
        self.market = market

    def __enter__(self) -> "SpotifySearch":
        """Enter the runtime context related to this object.

        Returns:
            SpotifySearch: The SpotifySearch object itself.
        """
        self.client = SpotifyClient()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the runtime context related to this object.

        Args:
            exc_type (type[BaseException] | None): The exception type if raised.
            exc_value (BaseException | None): The exception value if raised.
            traceback (TracebackType | None): The traceback information if an exception was raised.
        """
        del self.client

    def search(self) -> dict[str, Any]:
        """Perform the search query using the Spotify API.

        Returns:
            dict[str, Any]: The search results returned by the Spotify API.
        """
        return self.client.sp.search(
            q=self.query, limit=self.limit, type=self.search_type, market=self.market
        )

    def __str__(self) -> str:
        """Return the string representation of the SpotifySearch object.

        Returns:
            str: The string representation of the SpotifySearch object.
        """
        return f"SpotifySearch(query={self.query}, limit={self.limit}, type={self.search_type}, market={self.market})"


class SpotifySearchFactory:
    """Factory class to create SpotifySearch objects for different search types."""

    @staticmethod
    def create_search(
        query: str, search_type: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for a specified search type."""
        return SpotifySearch(query, search_type, limit, market)

    @staticmethod
    def artist_search(
        query: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for an artist search.

        Args:
            query (str): The search query for artists.
            limit (int): The number of search results to return. Default is 10.
            market (str | None): The market in which the search is performed. Default is None.

        Returns:
            SpotifySearch: An instance of SpotifySearch configured for an artist search.
        """
        return SpotifySearch(query, "artist", limit, market)

    @staticmethod
    def track_search(
        query: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for a track search.

        Args:
            query (str): The search query for tracks.
            limit (int): The number of search results to return. Default is 10.
            market (str | None): The market in which the search is performed. Default is None.

        Returns:
            SpotifySearch: An instance of SpotifySearch configured for a track search.
        """
        return SpotifySearch(query, "track", limit, market)

    @staticmethod
    def album_search(
        query: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for an album search.

        Args:
            query (str): The search query for albums.
            limit (int): The number of search results to return. Default is 10.
            market (str | None): The market in which the search is performed. Default is None.

        Returns:
            SpotifySearch: An instance of SpotifySearch configured for an album search.
        """
        return SpotifySearch(query, "album", limit, market)

    @staticmethod
    def playlist_search(
        query: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for a playlist search.

        Args:
            query (str): The search query for playlists.
            limit (int): The number of search results to return. Default is 10.
            market (str | None): The market in which the search is performed. Default is None.

        Returns:
            SpotifySearch: An instance of SpotifySearch configured for a playlist search.
        """
        return SpotifySearch(query, "playlist", limit, market)

    @staticmethod
    def artist_track_search(
        query: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for an artist-track search.

        Args:
            query (str): The search query for artist-tracks.
            limit (int): The number of search results to return. Default is 10.
            market (str | None): The market in which the search is performed. Default is None.

        Returns:
            SpotifySearch: An instance of SpotifySearch configured for an artist-track search.
        """
        return SpotifySearch(query, "artist,track", limit, market)

    @staticmethod
    def artist_album_search(
        query: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for an artist-album search.

        Args:
            query (str): The search query for artist-albums.
            limit (int): The number of search results to return. Default is 10.
            market (str | None): The market in which the search is performed. Default is None.

        Returns:
            SpotifySearch: An instance of SpotifySearch configured for an artist-album search.
        """
        return SpotifySearch(query, "artist,album", limit, market)

    @staticmethod
    def artist_playlist_search(
        query: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for an artist-playlist search.

        Args:
            query (str): The search query for artist-playlists.
            limit (int): The number of search results to return. Default is 10.
            market (str | None): The market in which the search is performed. Default is None.

        Returns:
            SpotifySearch: An instance of SpotifySearch configured for an artist-playlist search.
        """
        return SpotifySearch(query, "artist,playlist", limit, market)

    @staticmethod
    def track_album_search(
        query: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for a track-album search.

        Args:
            query (str): The search query for track-albums.
            limit (int): The number of search results to return. Default is 10.
            market (str | None): The market in which the search is performed. Default is None.

        Returns:
            SpotifySearch: An instance of SpotifySearch configured for a track-album search.
        """
        return SpotifySearch(query, "track,album", limit, market)

    @staticmethod
    def track_playlist_search(
        query: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for a track-playlist search.

        Args:
            query (str): The search query for track-playlists.
            limit (int): The number of search results to return. Default is 10.
            market (str | None): The market in which the search is performed. Default is None.

        Returns:
            SpotifySearch: An instance of SpotifySearch configured for a track-playlist search.
        """
        return SpotifySearch(query, "track,playlist", limit, market)

    @staticmethod
    def album_playlist_search(
        query: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for an album-playlist search.

        Args:
            query (str): The search query for album-playlists.
            limit (int): The number of search results to return. Default is 10.
            market (str | None): The market in which the search is performed. Default is None.

        Returns:
            SpotifySearch: An instance of SpotifySearch configured for an album-playlist search.
        """
        return SpotifySearch(query, "album,playlist", limit, market)

    @staticmethod
    def artist_track_album_search(
        query: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for an artist-track-album search.

        Args:
            query (str): The search query for artist-track-albums.
            limit (int): The number of search results to return. Default is 10.
            market (str | None): The market in which the search is performed. Default is None.

        Returns:
            SpotifySearch: An instance of SpotifySearch configured for an artist-track-album search.
        """
        return SpotifySearch(query, "artist,track,album", limit, market)

    @staticmethod
    def artist_track_playlist_search(
        query: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for an artist-track-playlist search.

        Args:
            query (str): The search query for artist-track-playlists.
            limit (int): The number of search results to return. Default is 10.
            market (str | None): The market in which the search is performed. Default is None.

        Returns:
            SpotifySearch: An instance of SpotifySearch configured for an artist-track-playlist search.
        """
        return SpotifySearch(query, "artist,track,playlist", limit, market)

    @staticmethod
    def artist_album_playlist_search(
        query: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for an artist-album-playlist search.

        Args:
            query (str): The search query for artist-album-playlists.
            limit (int): The number of search results to return. Default is 10.
            market (str | None): The market in which the search is performed. Default is None.

        Returns:
            SpotifySearch: An instance of SpotifySearch configured for an artist-album-playlist search.
        """
        return SpotifySearch(query, "artist,album,playlist", limit, market)

    @staticmethod
    def track_album_playlist_search(
        query: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for a track-album-playlist search.

        Args:
            query (str): The search query for track-album-playlists.
            limit (int): The number of search results to return. Default is 10.
            market (str | None): The market in which the search is performed. Default is None.

        Returns:
            SpotifySearch: An instance of SpotifySearch configured for a track-album-playlist search.
        """
        return SpotifySearch(query, "track,album,playlist", limit, market)

    @staticmethod
    def artist_track_album_playlist_search(
        query: str, limit: int = 10, market: str | None = None
    ) -> SpotifySearch:
        """Create a SpotifySearch instance for an artist-track-album-playlist search.

        Args:
            query (str): The search query for artist-track-album-playlists.
            limit (int): The number of search results to return. Default is 10.
            market (str | None): The market in which the search is performed. Default is None.

        Returns:
            SpotifySearch: An instance of SpotifySearch configured for an artist-track-album-playlist search.
        """
        return SpotifySearch(query, "artist,track,album,playlist", limit, market)


# Example usage
if __name__ == "__main__":
    with SpotifySearchFactory.artist_search("New", 1) as artist_search:
        artist_results = artist_search.search()
        print(artist_results)  # noqa: T201
