"""Helpers to created Flask responses."""
from flask import Response

from pyll_json_errors import constants, exceptions, generics


def make_response(*, json_errors, mimetype=constants.HEADER_CONTENT_TYPE_VALUE):
    """Create a Flask Response object from JsonErrorArray.

    Args:
        json_errors (models.JsonErrorArray): The errors to return in response.
        mimetype (str): The mimetype the Response will return with. Defaults to constants.HEADER_CONTENT_TYPE_VALUE.

    Returns:
        flask.Response: A Flask Response object which can be returned from a Flask view controller function.
    """
    return Response(json_errors.as_json(), status=json_errors.status, mimetype=mimetype)


def wrap_app(app):
    """Wraps a Flask application, adding various error handlers automatically.

    Args:
        app (flask.Flask): The Flask object to wrap.

    Returns:
        None
    """

    @app.errorhandler(403)
    def forbidden(error):
        return make_response(json_errors=generics.error403())

    @app.errorhandler(404)
    def not_found(error):
        return make_response(json_errors=generics.error404())

    @app.errorhandler(exceptions.ConcreteJsonError)
    def concrete_json_error(error):
        return make_response(json_errors=error.json_errors)
