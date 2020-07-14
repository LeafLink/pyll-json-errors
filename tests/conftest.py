"""Pytest config."""

from pyll_json_errors import models

import pytest


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
            meta={"some": "meta"},
        )

    return _factory


@pytest.fixture
def json_error_array_factory(json_error_factory):
    def _factory():
        return models.JsonErrorArray([json_error_factory(), json_error_factory()])

    return _factory
