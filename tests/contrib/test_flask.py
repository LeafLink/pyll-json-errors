"""pyll_json_errors.contrib.flask"""
import pytest
from flask import Flask, Response
from werkzeug import exceptions

from pyll_json_errors.contrib import flask
from pyll_json_errors.exceptions import ConcreteJsonError


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


def test__wrap_app():
    """Test wrapping.

    See: https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.error_handler_spec
    """
    app = Flask(__name__)
    flask.wrap_app(app)

    assert 403 in app.error_handler_spec[None]
    assert 404 in app.error_handler_spec[None]
    assert ConcreteJsonError in app.error_handler_spec[None][None]


@pytest.mark.parametrize("status", [403, 404])
def test__wrap_403(flask_client_factory, status):
    client = flask_client_factory(__name__)
    resp = client.get(f"/{status}")

    assert resp.status_code == status
