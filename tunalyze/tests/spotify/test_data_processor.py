import pytest

from src.spotify.data_processor import AudioAnalysisProcessor, AudioFeaturesProcessor


@pytest.fixture()
def audio_features_processor():
    """Fixture for creating an AudioFeaturesProcessor instance."""
    return AudioFeaturesProcessor()


# AudioFeaturesProcessorのテスト
def test_audio_features_processor(audio_features_processor):
    """Test that AudioFeaturesProcessor processes data correctly with full and valid data."""
    sample_data = {
        "audio_features": [
            {
                "acousticness": 0.934,
                "analysis_url": "https://api.spotify.com/v1/audio-analysis/6rqhFgbbKwnb9MLmUQDhG6",
                "danceability": 0.358,
                "duration_ms": 242187,
                "energy": 0.211,
                "id": "6rqhFgbbKwnb9MLmUQDhG6",
                "instrumentalness": 0.002,
                "key": 1,
                "liveness": 0.108,
                "loudness": -11.84,
                "mode": 1,
                "speechiness": 0.0339,
                "tempo": 77.169,
                "time_signature": 4,
                "track_href": "https://api.spotify.com/v1/tracks/6rqhFgbbKwnb9MLmUQDhG6",
                "type": "audio_features",
                "uri": "spotify:track:6rqhFgbbKwnb9MLmUQDhG6",
                "valence": 0.0373,
            }
        ]
    }
    expected_output = [
        {
            "acousticness": 0.934,
            "analysis_url": "https://api.spotify.com/v1/audio-analysis/6rqhFgbbKwnb9MLmUQDhG6",
            "danceability": 0.358,
            "duration_ms": 242187,
            "energy": 0.211,
            "id": "6rqhFgbbKwnb9MLmUQDhG6",
            "instrumentalness": 0.002,
            "key": 1,
            "liveness": 0.108,
            "loudness": -11.84,
            "mode": 1,
            "speechiness": 0.0339,
            "tempo": 77.169,
            "time_signature": 4,
            "track_href": "https://api.spotify.com/v1/tracks/6rqhFgbbKwnb9MLmUQDhG6",
            "type": "audio_features",
            "uri": "spotify:track:6rqhFgbbKwnb9MLmUQDhG6",
            "valence": 0.0373,
        }
    ]
    assert audio_features_processor.process_data(sample_data) == expected_output


def test_audio_features_processor_with_partial_data(audio_features_processor):
    """Test AudioFeaturesProcessor with partially missing fields in data."""
    sample_data = {
        "audio_features": [
            {
                "acousticness": 0.7,
                # Other fields like 'danceability' are missing
                "energy": 0.8,
                "id": "sample_track_id",
                # Other fields are also missing
            }
        ]
    }
    expected_output = [
        {
            "acousticness": 0.7,
            "energy": 0.8,
            "id": "sample_track_id",
            # Missing fields are not included in the output
        }
    ]
    assert audio_features_processor.process_data(sample_data) == expected_output


def test_audio_features_processor_with_edge_cases(audio_features_processor):
    """Test AudioFeaturesProcessor with edge case values in data."""
    sample_data = {
        "audio_features": [
            {
                "acousticness": -1,  # Out-of-range value
                "danceability": 1.5,  # Out-of-range value
                "duration_ms": "not_a_number",  # Invalid data type
                "energy": 0.8,
                "id": "sample_track_id",
                "instrumentalness": 2,  # Out-of-range value
            }
        ]
    }
    expected_output = [
        {
            "acousticness": -1,  # Abnormal values are preserved
            "danceability": 1.5,  # Abnormal values are preserved
            "duration_ms": "not_a_number",  # Invalid data type is preserved
            "energy": 0.8,
            "id": "sample_track_id",
            "instrumentalness": 2,  # Abnormal values are preserved
        }
    ]
    assert audio_features_processor.process_data(sample_data) == expected_output


def test_audio_features_processor_with_empty_data(audio_features_processor):
    """Test AudioFeaturesProcessor with empty audio_features data."""
    assert audio_features_processor.process_data({"audio_features": []}) == []


def test_audio_features_processor_with_invalid_structure(audio_features_processor):
    """Test AudioFeaturesProcessor with invalid data structure (missing 'audio_features' key)."""
    with pytest.raises(KeyError):
        audio_features_processor.process_data({"invalid_key": []})


# @pytest.fixture()
# def audio_analysis_processor():
#     return AudioAnalysisProcessor()


# def test_audio_analysis_processor(audio_analysis_processor):
#     sample_data = {
#         # Sample data including keys such as 'meta', 'track', 'sections', 'segments', etc.
#     }
#     # Define expected output data structure
#     expected_output = [
#         # Output structure tailored to the test case
#     ]
#     assert audio_analysis_processor.process_data(sample_data) == expected_output


# def test_audio_analysis_processor_with_incomplete_data(audio_analysis_processor):
#     with pytest.raises(ValueError):
#         audio_analysis_processor.process_data({})
