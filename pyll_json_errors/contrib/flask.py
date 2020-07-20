"""Integrate JSON API errors into Flask applications.

[Flask docs](https://flask.palletsprojects.com/en/1.1.x/)

See the [driver Flask app](https://github.com/LeafLink/pyll-json-errors/tree/master/drivers/flask_drive.py)
for examples on integrating `pyll_json_errors` into Flask.
"""
from pyll_json_errors import _check_dependency

_check_dependency("flask", __name__)

from flask import Response

from pyll_json_errors import constants, exceptions, generics, models, transform


def make_response(*, json_errors, mimetype=constants.HEADER_CONTENT_TYPE_VALUE):
    """Create a Flask Response object from a JsonErrorArray.

    Args:
        json_errors (models.JsonErrorArray): The errors array to generate an HTTP response from.
        mimetype (str): The mimetype the Response will return with.

    Returns:
        flask.Response: A Flask Response object which can be returned from a Flask view controller function.
    """
    return Response(json_errors.serialized(), status=json_errors.status, mimetype=mimetype)


def wrap_app(app):
    """Wraps a Flask application, adding various error handlers automatically.

    Wrapping an application provides automatic JSON API errors responses for 403 and 404 responses.
    It also provides automatic JSON API error responses for view controllers which raise `exceptions.ConcreteJsonError`
    errors.

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


class HttpExceptionTransform(transform.BaseTransform):
    """werkzeug HTTPExceptions transformer."""

    def make_json_errors(self, sources):
        """Transform werkzeug HTTPExceptions into models.JsonError objects.

        Args:
            sources (List[werkzeug.exceptions.HTTPException]): A list of HTTPExceptions to transform.

        Returns:
            List[models.JsonError]: A list of JsonError objects representing each HTTPException. Returned list will
                be the same length as `sources`.
        """
        return [
            models.JsonError(status=source.code, title=source.name, detail=source.description) for source in sources
        ]
