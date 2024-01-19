"""This module provides functionality for fetching audio features from Spotify track URIs."""

from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOauthError

from src.spotify.api_base import SpotifyAPIBase
from src.spotify.error_handler import SpotifyErrorHandler


class SpotifyTrackFeatures(SpotifyAPIBase):
    """A class to fetch audio features for Spotify tracks.

    Inherits from SpotifyAPIBase to utilize Spotify's Web API.
    """

    _INVALID_TRACK_URIS_MSG = "Invalid track URIs provided. Each URI must be a string starting with 'spotify:track:'."
    _NO_TRACKS_MSG = "No track URIs provided."

    def __init__(self) -> None:
        """Initializes the SpotifyTrackFeatures class."""
        super().__init__()

    def validate_track_uris(self, track_uris: list[str]) -> bool:
        """Validates the list of track URIs.

        Args:
            track_uris (list[str]): List of Spotify track URIs.

        Returns:
            bool: True if validation is successful, False otherwise.
        """
        return all(
            isinstance(uri, str) and uri.startswith("spotify:track:")
            for uri in track_uris
        )

    def fetch_audio_features(self, track_uris: list[str]) -> list[dict] | None:
        """Fetches audio features for the given Spotify track URIs.

        This method fetches audio features in batches of up to 100 tracks per request.

        Args:
            track_uris (list[str]): List of Spotify track URIs.

        Returns:
            list[dict] | None: List of audio features for each track URI, or None in case of an error.
        """
        if not track_uris:
            raise ValueError(self._NO_TRACKS_MSG)

        if not self.validate_track_uris(track_uris):
            raise ValueError(self._INVALID_TRACK_URIS_MSG)
        try:
            return [
                feature
                for i in range(0, len(track_uris), 100)
                for feature in self.get_batch_audio_features(track_uris, i)
            ]
        except (SpotifyException, SpotifyOauthError) as e:
            SpotifyErrorHandler.handle_error(e)
            return None

    def get_batch_audio_features(
        self, track_uris: list[str], start_index: int
    ) -> list[dict]:
        """Fetches a batch of audio features from Spotify starting at the specified index.

        Args:
            track_uris (list[str]): List of Spotify track URIs.
            start_index (int): Starting index for the batch.

        Returns:
            list[dict]: Audio features for the tracks in the batch.
        """
        return self.client.sp.audio_features(
            tracks=track_uris[start_index : start_index + 100]
        )

    def __str__(self) -> str:
        """Returns a human-readable representation of the SpotifyTrackFeatures object.

        Returns:
            str: A string representation of the SpotifyTrackFeatures object.
        """
        return "SpotifyTrackFeatures()"

    def __repr__(self) -> str:
        """Returns an official string representation of the SpotifyTrackFeatures object.

        Returns:
            str: An official string representation of the SpotifyTrackFeatures object.
        """
        return f"{self.__class__.__name__}()"
