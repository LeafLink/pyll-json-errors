"""pyll_json_errors.contrib.flask"""
import pytest
from flask import Response
from werkzeug import exceptions

from pyll_json_errors.contrib import flask


def test__make_response(json_error_array_factory):
    """Test making a Flask Response from a JsonErrorArray object."""
    array = json_error_array_factory()
    resp = flask.make_response(json_errors=array)

    assert isinstance(resp, Response)
    assert resp.status_code == array.status
    assert resp.is_json


@pytest.mark.parametrize(
    "exc_classes",
    [
        [exceptions.BadRequest],
        [exceptions.Unauthorized],
        [exceptions.Forbidden],
        [exceptions.NotFound],
        [exceptions.MethodNotAllowed],
        [exceptions.Unauthorized, exceptions.MethodNotAllowed],
    ],
)
def test__HttpExceptionTransform__make_json_errors(exc_classes):
    """Test HttpExceptionTransform class."""
    excs = [klass() for klass in exc_classes]
    json_errors = flask.HttpExceptionTransform().make_json_errors(excs)
    for exc, json_error in zip(excs, json_errors):
        assert json_error.status == exc.code
        assert json_error.title == exc.name
        assert json_error.detail == exc.description
