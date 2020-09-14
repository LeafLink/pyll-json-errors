"""
Contains convenient functions for creating :obj:`~pyll_json_errors.models.JsonErrorArray` objects
for commonly used errors.
"""
from pyll_json_errors.models import JsonError, JsonErrorArray


def _generic_error(title, detail, status):
    return JsonErrorArray([JsonError(title=title, detail=detail, status=status)])


def error400(*, title="Bad Request", detail=None):
    """Create a generic JSON error with status code 400.

    Args:
        title (str, optional): The title to associate with the error.
        detail (str, optional): The detail to associate with the error.

    Returns:
        ~pyll_json_errors.models.JsonErrorArray: A JsonErrorArray containing one error.
    """
    return _generic_error(title, detail, 400)


def error403(*, title="Forbidden", detail=None):
    """Create a generic JSON error with status code 403.

    Args:
        title (str, optional): The title to associate with the error.
        detail (str, optional): The detail to associate with the error.

    Returns:
        ~pyll_json_errors.models.JsonErrorArray: A JsonErrorArray containing one error.
    """
    return _generic_error(title, detail, 403)


def error404(*, title="Not found", detail=None):
    """Create a generic JSON error with status code 404.

    Args:
        title (str, optional): The title to associate with the error.
        detail (str, optional): The detail to associate with the error.

    Returns:
        ~pyll_json_errors.models.JsonErrorArray: A JsonErrorArray containing one error.
    """
    return _generic_error(title, detail, 404)
