"""Module for handling base interactions with the Spotify API.

This module provides the SpotifyAPIBase class, which serves as a foundation
for interacting with the Spotify API, handling client initialization and
basic context management.
"""

from types import TracebackType

from src.spotify.client import SpotifyClient


class SpotifyAPIBase:
    """Base class for Spotify API interactions.

    This class provides basic functionalities for initializing and managing
    the connection with the Spotify API. It is intended to be extended by
    other classes that implement specific functionalities of the Spotify API.
    """

    def __init__(self) -> None:
        """Initialize the SpotifyAPIBase instance.

        Sets up the basic configuration and initializes the Spotify client.
        """
        self.initialize_client()

    def initialize_client(self) -> None:
        """Initialize the Spotify client."""
        self.client = SpotifyClient()

    def __enter__(self) -> "SpotifyAPIBase":
        """Reinitialize the client upon entering a context."""
        self.initialize_client()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the runtime context related to this object.

        Cleans up the client instance and handles any exceptions that occurred
        during the context's execution.

        Args:
            exc_type (type[BaseException] | None): The exception type if raised.
            exc_value (BaseException | None): The exception value if raised.
            traceback (TracebackType | None): The traceback information if an exception was raised.
        """
        del self.client

    def __str__(self) -> str:
        """Return a string representation of the SpotifyAPIBase instance."""
        return "SpotifyAPIBase"
