"""pyll_json_errors.contrib.marshmallow"""
from marshmallow import ValidationError

from pyll_json_errors.contrib import marshmallow


def test__ValidationErrorTransform__make_json_errors__simple():
    err = ValidationError({"one": "error"})
    json_errors = marshmallow.ValidationErrorTransform().make_json_errors([err])

    assert json_errors[0].status == 400
    assert json_errors[0].source.pointer == "/one"
    assert json_errors[0].detail == "error"


def test__ValidationErrorTransform__make_json_errors__nested():
    err = ValidationError({"one": {"two": "error"}})
    json_errors = marshmallow.ValidationErrorTransform().make_json_errors([err])

    assert json_errors[0].status == 400
    assert json_errors[0].source.pointer == "/one/two"
    assert json_errors[0].detail == "error"


def test__ValidationErrorTransform__make_json_errors__multiple_same_field():
    err = ValidationError({"one": {"two": ["error1", "error2"]}})
    json_errors = marshmallow.ValidationErrorTransform().make_json_errors([err])

    assert len(json_errors) == 2

    for json_error in json_errors:
        assert json_error.status == 400
        assert json_error.source.pointer == "/one/two"
    assert json_errors[0].detail == "error1"
    assert json_errors[1].detail == "error2"


def test__ValidationErrorTransform__make_json_errors__numbered():
    err = ValidationError({"one": {0: "error0", 1: "error1"}})
    json_errors = marshmallow.ValidationErrorTransform().make_json_errors([err])

    assert len(json_errors) == 2

    for json_error in json_errors:
        assert json_error.status == 400
    assert json_errors[0].source.pointer == "/one/0"
    assert json_errors[0].detail == "error0"
    assert json_errors[1].source.pointer == "/one/1"
    assert json_errors[1].detail == "error1"


def test__ValidationErrorTransform__make_json_errors__multiple_sources():
    errs = [ValidationError({"one": {0: "error0", 1: "error1"}}), ValidationError({"two": "error2"})]
    json_errors = marshmallow.ValidationErrorTransform().make_json_errors(errs)

    assert len(json_errors) == 3

    for json_error in json_errors:
        assert json_error.status == 400
    assert json_errors[0].source.pointer == "/one/0"
    assert json_errors[0].detail == "error0"
    assert json_errors[1].source.pointer == "/one/1"
    assert json_errors[1].detail == "error1"
    assert json_errors[2].source.pointer == "/two"
    assert json_errors[2].detail == "error2"
