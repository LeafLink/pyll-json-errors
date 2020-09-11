"""Integrate Pyll JSON API errors into Flask applications.

In order to use this module, the :code:`flask` optional dependency must be installed. See :ref:`Installation`.

`Flask docs <https://flask.palletsprojects.com/en/1.1.x/>`_

See the :gh:`driver Flask app <drivers/flask_driver.py>`
for examples on integrating :mod:`pyll_json_errors` into Flask.
"""
from pyll_json_errors import _check_dependency

_check_dependency("flask", __name__)

from flask import Response

from pyll_json_errors import constants, exceptions, generics, models, transform


def make_response(*, json_errors, mimetype=constants.HEADER_CONTENT_TYPE_VALUE):
    """Create a Flask :py:class:`~flask.Response` object from a :obj:`~pyll_json_errors.models.JsonErrorArray` object.

    Args:
        json_errors (~pyll_json_errors.models.JsonErrorArray): The errors array to generate an HTTP response from.
        mimetype (str): The mimetype the Flask :py:class:`~flask.Response` will return with.

    Returns:
        flask.Response: A Flask :py:class:`~flask.Response` object which can be returned from a Flask
        view controller function.
    """
    return Response(json_errors.serialized(), status=json_errors.status, mimetype=mimetype)


def wrap_app(app):
    """Wraps a :py:class:`flask.Flask` application, adding various error handlers automatically.

    Wrapping an application provides automatic JSON API errors responses for 403 and 404 responses.
    It also provides automatic JSON API error responses for view controllers which raise
    :class:`~pyll_json_errors.exceptions.ConcreteJsonError` errors.

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
    """Transform :py:class:`werkzeug.exceptions.HTTPException` objects."""

    def make_json_errors(self, sources):
        """
        Transform :py:class:`werkzeug.exceptions.HTTPException` objects
        into :obj:`~pyll_json_errors.models.JsonError` objects.

        Args:
            sources (list): A list of :py:class:`werkzeug.exceptions.HTTPException` objects to transform.

        Returns:
            list: A list of :obj:`~pyll_json_errors.models.JsonError` objects representing each
            :py:class:`werkzeug.exceptions.HTTPException` object. Returned list will be same length as :code:`sources`.
        """
        return [
            models.JsonError(status=source.code, title=source.name, detail=source.description) for source in sources
        ]
