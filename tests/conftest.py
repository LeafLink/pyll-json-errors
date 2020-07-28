"""Pytest config."""
import pytest

from flask import Flask, abort

from pyll_json_errors import models


@pytest.fixture
def json_error_factory():
    def _factory():
        source = models.JsonErrorSourceParameter(parameter="some-param")
        return models.JsonError(
            id="some-id",
            status=400,
            code="c-400",
            title="some-title",
            detail="some-detail",
            source=source,
            meta=models.JsonError(title="nested-error"),
        )

    return _factory


@pytest.fixture
def json_error_array_factory(json_error_factory):
    def _factory():
        return models.JsonErrorArray([json_error_factory(), json_error_factory()])

    return _factory


@pytest.fixture
def flask_client_factory():
    def _factory(name):
        app = Flask(name)
        app.config["TESTING"] = True

        @app.route("/<int:status>")
        def status(status):
            abort(status)

        return app.test_client()

    return _factory


@pytest.fixture
def complex_error_sample():
    inp = {
        "simpleError": "red",
        "simpleErrorList": ["orange", 1],
        "objectError": {"a": "yellow", "b": 2, "c": ["green", 3]},
        1: "blue",
        2: ["purple", 4],
        "listedObjects": [{"1": "lime", 2: ["maroon", 5]}, {3: "pink", "d": ["jade", 6]}],
    }
    outp = (
        ("/simpleError", "red"),
        ("/simpleErrorList", "orange"),
        ("/simpleErrorList", "1"),
        ("/objectError/a", "yellow"),
        ("/objectError/b", "2"),
        ("/objectError/c", "green"),
        ("/objectError/c", "3"),
        ("/1", "blue"),
        ("/2", "purple"),
        ("/2", "4"),
        ("/listedObjects/0/1", "lime"),
        ("/listedObjects/0/2", "maroon"),
        ("/listedObjects/0/2", "5"),
        ("/listedObjects/1/3", "pink"),
        ("/listedObjects/1/d", "jade"),
        ("/listedObjects/1/d", "6"),
    )

    return inp, outp
