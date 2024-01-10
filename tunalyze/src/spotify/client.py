"""This module provides a class for managing Spotify client operations using the Spotipy library."""

from types import TracebackType

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from src.config import Config


class SpotifyClient:
    """Class to handle Spotify client operations."""

    def __init__(self) -> None:
        """Initialize the Spotify client with authentication."""
        config = Config()
        self._auth_manager = SpotifyClientCredentials(
            client_id=config.client_id,
            client_secret=config.client_secret,
        )
        self.sp = spotipy.Spotify(
            auth_manager=self._auth_manager,
            requests_timeout=5,
            retries=3,
            status_retries=3,
            language="en",
        )

    def __enter__(self) -> "SpotifyClient":
        """Enable use of the 'with' statement for the Spotify client.

        Returns:
            SpotifyClient: The instance of the SpotifyClient.
        """
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Clean-up code for the Spotify client.

        Args:
            exc_type: Exception type.
            exc_val: Exception value.
            exc_tb: Exception traceback.
        """
        # Add any necessary clean-up code here. For now, it's a pass.

    def __repr__(self) -> str:
        """Return a developer-friendly string representation of the SpotifyClient object.

        This representation includes the client ID and client secret obtained
        from the Config instance, reflecting the current authentication state.
        """
        config = Config()
        return f"SpotifyClient(client_id={config.client_id}, client_secret={config.client_secret})"
