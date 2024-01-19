from pathlib import Path

import polars as pl
import pytest

from src.spotify.csv_handler import CSVHandler, FileValidator, InvalidTimezoneError

EXPECTED_CSV_LINE_COUNT = 4  # Header rows + 3 data rows


@pytest.fixture()
def csv_handler():
    """Provide a CSVHandler instance with default parameters for testing."""
    return CSVHandler("test_data", "UTC")


def test_csv_handler_initialization(csv_handler):
    """Test initialization of the CSVHandler class."""
    assert csv_handler.base_filename == "test_data"
    assert str(csv_handler.timezone) == "UTC"


def test_csv_handler_str(csv_handler):
    """Test the string representation of the CSVHandler class."""
    assert str(csv_handler) == "CSVHandler(base_filename='test_data')"


def test_csv_handler_repr(csv_handler):
    """Test the official string representation of the CSVHandler class."""
    assert repr(csv_handler) == "CSVHandler(base_filename='test_data')"


def test_csv_handler_initialization_invalid_timezone():
    """Test CSVHandler initialization with an invalid timezone, expecting an InvalidTimezoneError."""
    with pytest.raises(InvalidTimezoneError):
        CSVHandler("test_data", "Invalid/Timezone")


def test_generate_filename(csv_handler):
    """Test the generate_filename method of CSVHandler."""
    filename = csv_handler.generate_filename("_suffix")
    assert filename.startswith("test_data_")
    assert filename.endswith("_suffix.csv")


def test_array_to_dataframe(csv_handler):
    """Test the array_to_dataframe method of CSVHandler, converting a list of data to a DataFrame."""
    data = [{"column1": 1, "column2": "A"}]
    converted_dataframe = csv_handler.array_to_dataframe(data)
    assert isinstance(converted_dataframe, pl.DataFrame)
    assert converted_dataframe.shape == (1, 2)


def test_export_to_csv(mocker, csv_handler):
    """Test the export_to_csv method of CSVHandler using a mock to avoid actual file writing."""
    mock_write_csv = mocker.patch("polars.DataFrame.write_csv")
    dataframe = pl.DataFrame({"column1": [1, 2, 3]})
    csv_handler.export_to_csv(dataframe, "test_export.csv")
    mock_write_csv.assert_called_once_with("test_export.csv")


def test_export_to_csv_real(csv_handler, tmp_path):
    """Test the export_to_csv method with a real file interaction, ensuring that a CSV file is correctly written to the file system."""
    test_dataframe = pl.DataFrame({"column1": [1, 2, 3]})
    file_path = tmp_path / "test_export.csv"
    csv_handler.export_to_csv(test_dataframe, str(file_path))
    assert file_path.exists()
    assert file_path.read_text().count("\n") == EXPECTED_CSV_LINE_COUNT


def test_read_csv(mocker, csv_handler):
    """Test the read_csv method of CSVHandler using a mock to simulate reading from a file."""
    mock_read_csv = mocker.patch(
        "polars.read_csv", return_value=pl.DataFrame({"column1": [1, 2, 3]})
    )
    loaded_dataframe = csv_handler.read_csv("test_data.csv")
    mock_read_csv.assert_called_once_with("test_data.csv")
    assert isinstance(loaded_dataframe, pl.DataFrame)


def test_read_csv_real(csv_handler, tmp_path):
    """Test the read_csv method with a real file interaction, ensuring that a CSV file is correctly read into a DataFrame."""
    file_path = tmp_path / "test_read.csv"
    file_path.write_text("column1\n1\n2\n3")
    loaded_dataframe = csv_handler.read_csv(str(file_path))
    assert isinstance(loaded_dataframe, pl.DataFrame)
    assert loaded_dataframe.shape == (3, 1)
    assert loaded_dataframe["column1"].to_list() == [1, 2, 3]


def test_read_csv_file_not_found(csv_handler):
    """Test the read_csv method of CSVHandler with a non-existent file, expecting a FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        csv_handler.read_csv("nonexistent_file.csv")


def test_validate_file_exists(tmp_path):
    """Test the validate_file_exists method of FileValidator, checking both existing and non-existing file scenarios."""
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("content")

    FileValidator.validate_file_exists(str(test_file))

    with pytest.raises(FileNotFoundError):
        FileValidator.validate_file_exists(str(tmp_path / "nonexistent_file.txt"))
