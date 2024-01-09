"""This module provides a class for handling exceptions thrown by the Spotify API.

It processes exceptions and returns user-friendly error messages.
"""

from typing import Any

from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOauthError


class SpotifyErrorHandler:
    """A class for handling exceptions thrown by the Spotify API.

    Processes exceptions and returns user-friendly error messages.
    """

    _HTTP_STATUS_UNAUTHORIZED = 401
    _HTTP_STATUS_TOO_MANY_REQUESTS = 429

    @staticmethod
    def handle_error(exception: SpotifyException | SpotifyOauthError) -> dict[str, Any]:
        """Handles exceptions from the Spotify API.

        Args:
            exception (Exception): The exception that occurred.

        Returns:
            dict[str, Any]: A dictionary containing an error message.
        """
        if isinstance(exception, SpotifyException):
            if exception.http_status == SpotifyErrorHandler._HTTP_STATUS_UNAUTHORIZED:
                return {
                    "error": "Authentication failed: Check your Spotify credentials."
                }
            if (
                exception.http_status
                == SpotifyErrorHandler._HTTP_STATUS_TOO_MANY_REQUESTS
            ):
                return {"error": "Rate limit exceeded: Try again later."}
            return {"error": f"Spotify API error: {exception}"}
        if isinstance(exception, SpotifyOauthError):
            return {"error": f"OAuth error: {exception}"}
        return {"error": f"An unexpected error occurred: {exception}"}
