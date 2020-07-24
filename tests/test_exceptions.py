"""pyll_json_errors.exceptions"""
import pytest

from pyll_json_errors import exceptions, models


def test__ConcreteJsonError__not_JsonErrorArray():
    """If passing an object, must be a JsonErrorArray."""
    with pytest.raises(TypeError):
        exceptions.ConcreteJsonError("", 4)


def test__ConcreteJsonError__not_JsonError_list():
    """If passing a list/tuple, must all be JsonError."""
    with pytest.raises(TypeError):
        exceptions.ConcreteJsonError("", [4])


def test__ConcreteJsonError__from_JsonErrors():
    """Create exception from a list of JsonErrors."""
    err = models.JsonError(title="test")
    exc = exceptions.ConcreteJsonError("", [err])
    assert isinstance(exc.json_errors, models.JsonErrorArray)
    assert len(exc.json_errors.errors) == 1


def test__ConcreteJsonError__from_JsonErrorArray():
    """Create exception from a single JsonErrorArray."""
    array = models.JsonErrorArray(errors=[models.JsonError(title="test")])
    exc = exceptions.ConcreteJsonError("", array)
    assert isinstance(exc.json_errors, models.JsonErrorArray)
    assert len(exc.json_errors.errors) == 1
