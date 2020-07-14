"""pyll_json_errors.contrib.flask"""
from flask import Response

from pyll_json_errors.contrib import flask


def test__make_response(json_error_array_factory):
    """Test making a Flask Response from a JsonErrorArray object."""
    array = json_error_array_factory()
    resp = flask.make_response(json_errors=array)

    assert isinstance(resp, Response)
    assert resp.status_code == array.status
    assert resp.is_json
