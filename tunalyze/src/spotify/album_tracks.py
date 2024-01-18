"""This module provides the SpotifyAlbumTracks class for interacting with the Spotify API.

It allows users to retrieve tracks from a specific album using its Spotify URI.
"""

import re
from typing import Any

from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOauthError

from src.spotify.api_base import SpotifyAPIBase
from src.spotify.error_handler import SpotifyErrorHandler


class SpotifyAlbumTracks(SpotifyAPIBase):
    """This class is used to interact with the Spotify API to get tracks of a specific album.

    Attributes:
        album_uri (str): The Spotify URI of the album.
        limit (int): The number of items to return. Default is 10.
        offset (int): The offset of the first item to return. Default is 0.
    """

    _MIN_LIMIT = 1
    _MAX_LIMIT = 50
    _LIMIT_ERROR_MESSAGE = (
        f"Limit must be between {_MIN_LIMIT} and {_MAX_LIMIT}, inclusive."
    )
    _INVALID_URI_MESSAGE = (
        "Invalid album URI format. Expected format: 'spotify:album:<Spotify ID>'."
    )

    def __init__(
        self,
        album_uri: str,
        limit: int = 20,
        offset: int = 0,
    ) -> None:
        """Initializes the SpotifyAlbumTracks instance with the provided parameters.

        Args:
            album_uri (str): The Spotify URI of the album. Must be in the format 'spotify:album:<Spotify ID>'.
            limit (int): The number of items to return. Default is 20. Optional.
            offset (int): The offset of the first item to return. Default is 0. Optional.

        Raises:
            ValueError: If the album URI format is invalid or the limit is outside the allowed range.
        """
        super().__init__()

        # Validate album URI
        pattern = r"^spotify:album:[0-9a-zA-Z]+$"
        if not re.match(pattern, album_uri):
            raise ValueError(self._INVALID_URI_MESSAGE)
        self.album_uri = album_uri.split(":")[-1]

        # Validate limit
        if not self._MIN_LIMIT <= limit <= self._MAX_LIMIT:
            raise ValueError(self._LIMIT_ERROR_MESSAGE)
        self.limit = limit
        self.offset = offset

    def __enter__(self) -> "SpotifyAlbumTracks":
        """Reinitialize the client upon entering a context and return SpotifyAlbumTracks instance."""
        super().__enter__()
        return self

    def get_tracks(self) -> dict[str, Any]:
        """Retrieves the tracks of the specified album from the Spotify API.

        Returns:
            dict[str, Any]: A dictionary containing information about the album's tracks.
                            If an error occurs, it returns a dictionary with an error key.
        """
        try:
            return self.client.sp.album_tracks(
                album_id=self.album_uri,
                limit=self.limit,
                offset=self.offset,
            )
        except (SpotifyException, SpotifyOauthError) as e:
            return SpotifyErrorHandler.handle_error(e)

    def __str__(self) -> str:
        """Return the string representation of the SpotifyAlbumTracks object.

        Returns:
            str: The string representation of the SpotifyAlbumTracks object.
        """
        return f"SpotifyAlbumTracks(album_uri={self.album_uri}, limit={self.limit}, offset={self.offset})"


if __name__ == "__main__":
    # Example usage of the SpotifyAlbumTracks class
    spotify_album_uri = "spotify:album:68w73FF3dYC6C3RWdcV0Yl"  # Replace <Spotify ID> with an actual Spotify Album ID
    album_tracks = SpotifyAlbumTracks(spotify_album_uri, limit=20, offset=0)

    with album_tracks:
        tracks = album_tracks.get_tracks()
        print("Tracks in the album:")
        for track in tracks["items"]:
            print(f"- {track['name']} (URI: {track['uri']})")
