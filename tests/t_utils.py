import os
from unittest.mock import mock_open

import pytest

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
