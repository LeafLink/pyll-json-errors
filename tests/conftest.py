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
