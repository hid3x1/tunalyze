"""This module provides classes for processing data retrieved from Spotify's API.

It includes an abstract base class, DataProcessor, for generic data processing and
specific subclasses for processing different types of Spotify API responses, such as
audio features and audio analysis data.
"""

from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    """Abstract base class for processing data from different types of Spotify API responses.

    This class provides a template for processing raw data into a structured format.
    """

    @abstractmethod
    def process_data(self, raw_data: dict[str, Any]) -> list[dict[str, Any]]:
        """Abstract method to be implemented by subclasses for processing raw data.

        Args:
            raw_data (Dict[str, Any]): Raw data to be processed.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing processed data.
        """

    def __repr__(self) -> str:
        """Return a string representation of the data processor."""
        return f"{self.__class__.__name__}()"


class AudioFeaturesProcessor(DataProcessor):
    """Processor class for handling audio features data from Spotify's audio_features API.

    This class extracts relevant fields from the audio_features response and structures them into a list of dictionaries.
    """

    def process_data(self, raw_data: dict[str, Any]) -> list[dict[str, Any]]:
        """Processes the 'audio_features' data from Spotify API response.

        Args:
            raw_data (Dict[str, Any]): The 'audio_features' response from Spotify API.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing processed audio features.
        """
        return [
            {
                "acousticness": track["acousticness"],
                "analysis_url": track["analysis_url"],
                "danceability": track["danceability"],
                "duration_ms": track["duration_ms"],
                "energy": track["energy"],
                "id": track["id"],
                "instrumentalness": track["instrumentalness"],
                "key": track["key"],
                "liveness": track["liveness"],
                "loudness": track["loudness"],
                "mode": track["mode"],
                "speechiness": track["speechiness"],
                "tempo": track["tempo"],
                "time_signature": track["time_signature"],
                "track_href": track["track_href"],
                "type": track["type"],
                "uri": track["uri"],
                "valence": track["valence"],
            }
            for track in raw_data["audio_features"]
            if track
        ]


# class AudioAnalysisProcessor(DataProcessor):
#     """Processor class for handling audio analysis data from Spotify's audio_analysis API.

#     This class is intended to extract and structure data from the audio_analysis response.
#     """

#     def process_data(self, raw_data: dict[str, Any]) -> list[dict[str, Any]]:
#         """Processes the 'audio_analysis' data from Spotify API response.

#         Args:
#             raw_data (Dict[str, Any]): The 'audio_analysis' response from Spotify API.

#         Returns:
#             List[Dict[str, Any]]: A list of dictionaries containing processed audio analysis data.
#         """
#         try:
#             processed_data = []
#             # Meta and Track data processing
#             meta_data = self._process_meta(raw_data.get("meta", {}))
#             track_data = self._process_track(raw_data.get("track", {}))

#             processed_data.append({"meta": meta_data})
#             processed_data.append({"track": track_data})

#             for section_name in ["bars", "beats", "sections", "segments", "tatums"]:
#                 section_items = raw_data.get(section_name, [])
#                 process_func = getattr(
#                     self, f"_process_{section_name}_item", self._process_default_item
#                 )
#                 processed_section = [process_func(item) for item in section_items]
#                 processed_data.append({section_name: processed_section})
#         except KeyError as e:
#             _error_message = f"Unexpected data structure in raw_data: missing key {e}"
#             raise ValueError(_error_message) from e
#         else:
#             return processed_data

#     def _process_meta(self, meta: dict) -> dict:
#         """Process meta data from the audio_analysis response."""
#         return {
#             "analyzer_version": meta.get("analyzer_version"),
#             "platform": meta.get("platform"),
#             "detailed_status": meta.get("detailed_status"),
#             "status_code": meta.get("status_code"),
#             "timestamp": meta.get("timestamp"),
#             "analysis_time": meta.get("analysis_time"),
#             "input_process": meta.get("input_process"),
#         }

#     def _process_track(self, track: dict) -> dict:
#         """Process track data from the audio_analysis response."""
#         return {
#             "num_samples": track.get("num_samples"),
#             "duration": track.get("duration"),
#             "sample_md5": track.get("sample_md5"),
#             "offset_seconds": track.get("offset_seconds"),
#             "window_seconds": track.get("window_seconds"),
#             "analysis_sample_rate": track.get("analysis_sample_rate"),
#             "analysis_channels": track.get("analysis_channels"),
#             "end_of_fade_in": track.get("end_of_fade_in"),
#             "start_of_fade_out": track.get("start_of_fade_out"),
#             "loudness": track.get("loudness"),
#             "tempo": track.get("tempo"),
#             "tempo_confidence": track.get("tempo_confidence"),
#             "time_signature": track.get("time_signature"),
#             "time_signature_confidence": track.get("time_signature_confidence"),
#             "key": track.get("key"),
#             "key_confidence": track.get("key_confidence"),
#             "mode": track.get("mode"),
#             "mode_confidence": track.get("mode_confidence"),
#             "codestring": track.get("codestring"),
#             "code_version": track.get("code_version"),
#             "echoprintstring": track.get("echoprintstring"),
#             "echoprint_version": track.get("echoprint_version"),
#             "synchstring": track.get("synchstring"),
#             "synch_version": track.get("synch_version"),
#             "rhythmstring": track.get("rhythmstring"),
#             "rhythm_version": track.get("rhythm_version"),
#         }

#     def _process_default_item(self, item: dict) -> dict:
#         """Default processing for common fields."""
#         return {
#             "start": item.get("start"),
#             "duration": item.get("duration"),
#             "confidence": item.get("confidence"),
#         }

#     def _process_sections_item(self, item: dict) -> dict:
#         """Processes an individual item from the sctionss section."""
#         section_data = self._process_default_item(item)
#         section_data.update(
#             {
#                 "loudness": item.get("loudness"),
#                 "tempo": item.get("tempo"),
#                 "tempo_confidence": item.get("tempo_confidence"),
#                 "key": item.get("key"),
#                 "key_confidence": item.get("key_confidence"),
#                 "mode": item.get("mode"),
#                 "mode_confidence": item.get("mode_confidence"),
#                 "time_signature": item.get("time_signature"),
#                 "time_signature_confidence": item.get("time_signature_confidence"),
#             }
#         )
#         return section_data

#     def _process_segments_item(self, item: dict) -> dict:
#         """Processes an individual item from the segments section."""
#         segment_data = self._process_default_item(item)
#         segment_data.update(
#             {
#                 "loudness_start": item.get("loudness_start"),
#                 "loudness_max": item.get("loudness_max"),
#                 "loudness_max_time": item.get("loudness_max_time"),
#                 "loudness_end": item.get("loudness_end"),
#                 "pitches": item.get("pitches"),
#                 "timbre": item.get("timbre"),
#             }
#         )
#         return segment_data
