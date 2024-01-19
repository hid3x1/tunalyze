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


# example usage
if __name__ == "__main__":
    from src.spotify.csv_handler import CSVHandler
    from src.spotify.data_processor import AudioFeaturesProcessor

    track_uris = [
        "spotify:track:0YTM7bCx451c6LQbkddy4Q",
        "spotify:track:3wT58LylGS5wfXLBWRsMaZ",
        "spotify:track:1VoTe7qVyqyMNLgZpQeugO",
        "spotify:track:7Fe2z1doVotACIjPuO0wQI",
        "spotify:track:08c3tqCZN3PQcLA5VNkXt9",
        "spotify:track:3UyBvmAK2MjkCpuJtYzQ40",
        "spotify:track:1hAloWiinXLPQUJxrJReb1",
        "spotify:track:62q2gPY4OnQCGnw7T4JWg1",
        "spotify:track:5stUI9U3VGp2j4sbqJEiVI",
        "spotify:track:5m2m2FUgFbIGQkl9sEoBi4",
    ]

    track_features = SpotifyTrackFeatures()
    raw_features = track_features.fetch_audio_features(track_uris)

    processor = AudioFeaturesProcessor()
    structured_data = processor.process_data({"audio_features": raw_features})

    csv_handler = CSVHandler("spotify_data")
    spotify_data = csv_handler.array_to_dataframe(structured_data)
    csv_handler.export_to_csv(spotify_data)