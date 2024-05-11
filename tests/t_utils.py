import pytest
from unittest.mock import patch, mock_open
import os
from scripts.utils import (
    json_dict_manip as jdm,
    metadata_retriever as mr
)


def test_insert_dict_between_keys_happy_path():
    original_dict = {"a": 1, "b": 2, "c": 3}
    new_dict = {"d": 4}
    result = jdm.insert_dict_between_keys(original_dict, "a", "c", new_dict)
    assert result == {"a": 1, "d": 4, "b": 2, "c": 3}


def test_insert_dict_between_keys_with_nonexistent_keys():
    original_dict = {"a": 1, "b": 2, "c": 3}
    new_dict = {"d": 4}
    with pytest.raises(ValueError):
        jdm.insert_dict_between_keys(original_dict, "x", "y", new_dict)


def test_insert_dict_between_keys_with_key_before_after_key_after():
    original_dict = {"a": 1, "b": 2, "c": 3}
    new_dict = {"d": 4}
    with pytest.raises(ValueError):
        jdm.insert_dict_between_keys(original_dict, "b", "a", new_dict)


def test_insert_dict_between_keys_with_empty_new_dict():
    original_dict = {"a": 1, "b": 2, "c": 3}
    new_dict = {}
    result = jdm.insert_dict_between_keys(original_dict, "a", "c", new_dict)
    assert result == original_dict


def test_metadata_retriever_mp3_file():
    filename = "test.mp3"
    base_path = "/path/to/mp3"
    with patch("builtins.open", mock_open(read_data="data")) as mock_file:
        assert mr.get_metadata(filename, base_path) == {
            "File": filename,
            "Type": "MP3",
            "Duration": 10.0,
            "Bytes": os.path.getsize(filename)
        }
    mock_file.assert_called_once_with(filename, 'rb')


# def test_metadata_retriever_wav_file():
#     filename = "test.wav"
#     base_path = "/path/to/wav"
#     with patch("builtins.open", mock_open(read_data="data")) as mock_file:
#         assert mr.get_metadata(filename, base_path) == {
#             "File": filename,
#             "Type": "WAV",
#             "Duration": 10.0,
#             "Bytes": 1000
#         }
#     mock_file.assert_called_once_with(filename, 'rb')
#
#
# def test_metadata_retriever_unsupported_file_format():
#     filename = "test.txt"
#     base_path = "/path/to/txt"
#     with pytest.raises(Exception):
#         mr.get_metadata(filename, base_path)
#
#
# def test_metadata_retriever_output_path_provided():
#     filename = "test.mp3"
#     base_path = "/path/to/mp3"
#     output_path = "/path/to/output"
#     with patch("builtins.open", mock_open(read_data="data")) as mock_file:
#         assert mr.get_metadata(filename, base_path, output_path) == {
#             "File": filename,
#             "Type": "MP3",
#             "Duration": 10.0,
#             "Bytes": os.path.getsize(filename)
#         }
#     mock_file.assert_called_once_with(filename, 'rb')
