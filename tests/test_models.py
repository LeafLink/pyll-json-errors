"""pyll_json_errors.models"""
import pytest

from pyll_json_errors import models


def test__JsonErrorSourceParameter__as_dict():
    """JsonErrorSourceParameter as a dictionary."""
    para = "param"
    mod = models.JsonErrorSourceParameter(parameter=para)
    assert mod.as_dict() == {"parameter": para}


def test__JsonErrorSourcePointer__as_dict():
    """JsonErrorSourcePointer as a dictionary."""
    pointer = "/some/pointer"
    mod = models.JsonErrorSourcePointer(pointer=pointer)
    assert mod.as_dict() == {"pointer": pointer}


def test__JsonError____init__(json_error_factory):
    """Check passing incorrect typed objects to JsonError init."""
    _ = json_error_factory()

    with pytest.raises(TypeError):
        models.JsonError(source=4)

    with pytest.raises(TypeError):
        models.JsonError(meta=4)


def test__JsonError__as_dict(json_error_factory):
    """Test getting JsonError as a dictionary."""
    err = json_error_factory()
    data = err.as_dict()
    for key in ["id", "status", "code", "title", "detail", "source", "meta"]:
        assert key in data


def test__JsonErrorArray___unique_status_codes(json_error_array_factory):
    """Test getting a list of unique status codes from the list of errors."""
    array = json_error_array_factory()
    assert array._unique_status_codes() == [400]

    array.errors[0].status = 401
    for status in [400, 401]:
        assert status in array._unique_status_codes()


def test__JsonErrorArray__status__override(json_error_array_factory):
    """Explicitly set array status."""
    array = json_error_array_factory()
    array.override_status = 566
    assert array.status == 566


def test__JsonErrorArray__status__unique_len_1(json_error_array_factory):
    """When either all error status are uniform, or only one error."""
    array = json_error_array_factory()

    array.errors[0].status = 400
    array.errors[1].status = 400
    assert array.status == 400

    del array.errors[1]
    assert array.status == 400


def test__JsonErrorArray__status__unique_len_gt_1(json_error_array_factory):
    """More than one unique status code among errors"""
    array = json_error_array_factory()

    array.errors[0].status = 402
    array.errors[1].status = 405
    assert array.status == 400

    array.errors[0].status = 402
    array.errors[1].status = 566
    assert array.status == 500


def test__JsonErrorArray__status__fallback(json_error_array_factory):
    """Fallback status is used when none of the errors provide a status."""
    array = json_error_array_factory()

    array.errors[0].status = None
    array.errors[1].status = None
    assert array.status == 400

    array.fallback_status = 566
    assert array.status == 566


def test__JsonErrorArray__status__mixed(json_error_array_factory):
    """Some errors have status, other do not."""
    array = json_error_array_factory()

    array.errors[0].status = 566
    array.errors[1].status = None
    assert array.status == 566


def test__JsonErrorArray__as_dict(json_error_array_factory):
    """Get JsonErrorArray as dictionary."""
    array = json_error_array_factory()
    assert "errors" in array.as_dict()


def test__JsonErrorArray__serialized(json_error_array_factory):
    """Test getting object as a json string."""
    array = json_error_array_factory()
    data = array.serialized()
    assert isinstance(data, str)


def test__JsonErrorArray____str__(json_error_array_factory):
    """Test printing object as string."""
    array = json_error_array_factory()
    assert str(array) == "<JsonErrorArray>(400) Length: 2"
