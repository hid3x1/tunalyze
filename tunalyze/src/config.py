"""This module defines a configuration class for loading environment variables."""

import os

from dotenv import load_dotenv


class Config:
    """Singleton class for loading configuration settings from environment variables."""

    _instance = None

    def __new__(cls) -> "Config":
        """Create a new instance of Config if it doesn't exist, or return the existing instance.

        Returns:
            Config: The singleton instance of the Config class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load()
        return cls._instance

    def load(self) -> None:
        """Loads environment variables. This method is intended for internal use."""
        load_dotenv(verbose=True)
        self._client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self._client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    @property
    def client_id(self) -> str | None:
        """Client ID for Spotify. Returns None if not set."""
        return self._client_id

    @property
    def client_secret(self) -> str | None:
        """Client Secret for Spotify. Returns None if not set."""
        return self._client_secret

    def __str__(self) -> str:
        """String representation of the Config object."""
        return f"Config(client_id={self.client_id}, client_secret={self.client_secret})"
