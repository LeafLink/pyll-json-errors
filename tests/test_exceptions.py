"""pyll_json_errors.exceptions"""
import pytest

from pyll_json_errors import exceptions


def test__ConcreteJsonError__not_JsonErrorArray():
    """If passing an object, must be a JsonErrorArray."""
    with pytest.raises(TypeError):
        exceptions.ConcreteJsonError("", 4)


def test__ConcreteJsonError__not_JsonError_list():
    """If passing a list/tuple, must all be JsonError."""
    with pytest.raises(TypeError):
        exceptions.ConcreteJsonError("", [4])
