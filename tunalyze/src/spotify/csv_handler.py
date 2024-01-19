"""CSVHandler module for handling CSV file operations using the Polars library."""

from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import polars as pl


class InvalidTimezoneError(ValueError):
    """Exception raised for invalid timezone input."""

    def __init__(self, timezone: str) -> None:
        """Initializes the InvalidTimezoneError with the provided timezone.

        Args:
            timezone (str): The invalid timezone that caused the error.
        """
        super().__init__(f"Invalid timezone specified: {timezone}")


class FileValidator:
    """A class for validating file existence and accessibility."""

    @staticmethod
    def validate_file_exists(filepath: str) -> None:
        """Checks if the given file exists.

        Args:
            filepath (str): The path to the file to check.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        file_not_found_msg = f"The file {filepath} does not exist."
        if not Path(filepath).exists():
            raise FileNotFoundError(file_not_found_msg)


class CSVHandler:
    """A class for handling CSV file operations using the Polars library.

    Attributes:
        base_filename (str): The base filename to use for generating CSV filenames.
        timezone (datetime.timezone): The timezone for generating timestamps. Defaults to UTC.
    """

    def __init__(
        self, base_filename: str = "data_export", timezone: str | None = None
    ) -> None:
        """Initializes the CSVHandler with a base filename and timezone.

        Args:
            base_filename (str): The base filename to use for generating CSV filenames.
                                  Defaults to "data_export".
            timezone (Optional[datetime.timezone]): The timezone to use for timestamps.
                                                    Defaults to UTC if None.
        """
        self.base_filename = base_filename
        try:
            self.timezone = (
                ZoneInfo(timezone) if timezone is not None else ZoneInfo("UTC")
            )
        except ZoneInfoNotFoundError as e:
            raise InvalidTimezoneError(timezone) from e

    def generate_filename(self, suffix: str = "") -> str:
        """Generates a filename with a timestamp and optional suffix.

        Args:
            suffix (str): An optional suffix for the filename. Defaults to an empty string.

        Returns:
            str: Generated filename with timestamp and suffix.
        """
        timestamp = datetime.now(self.timezone).strftime("%Y%m%d_%H%M%S")
        return f"{self.base_filename}_{timestamp}{suffix}.csv"

    def array_to_dataframe(
        self, data: list[Any], columns: list | None = None
    ) -> pl.DataFrame:
        """Converts a list of data into a Polars DataFrame.

        Args:
            data (list[Any]): A list of data to convert.
            columns (Optional[list[str]]): Column names for the DataFrame. Defaults to None.

        Returns:
            pl.DataFrame: A Polars DataFrame created from the given data.
        """
        dataframe = pl.DataFrame(data)
        if columns:
            dataframe.columns = columns
        return dataframe

    def export_to_csv(
        self, dataframe: pl.DataFrame, filename: str | None = None
    ) -> None:
        """Exports a Polars DataFrame to a CSV file.

        Args:
            dataframe (pl.DataFrame): The DataFrame to be exported.
            filename (Optional[str]): The filename for the exported CSV. If None, a filename is generated.
                                      Defaults to None.
        """
        if filename is None:
            filename = self.generate_filename()
        dataframe.write_csv(filename)

    def read_csv(self, filepath: str, **kwargs: Any) -> pl.DataFrame:  # noqa: ANN401
        """Reads a CSV file into a Polars DataFrame.

        Args:
            filepath (str): Path to the CSV file to be read.
            **kwargs: Additional keyword arguments for `pl.read_csv`.
        """
        FileValidator.validate_file_exists(filepath)
        return pl.read_csv(filepath, **kwargs)

    def __str__(self) -> str:
        """Returns a string representation of the CSVHandler object.

        Returns:
            str: A string representation of the CSVHandler.
        """
        return f"CSVHandler(base_filename='{self.base_filename}')"

    def __repr__(self) -> str:
        """Returns an official string representation of the CSVHandler object.

        Returns:
            str: An official string representation of the CSVHandler.
        """
        return f"CSVHandler(base_filename='{self.base_filename}')"
