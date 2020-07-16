"""Contains convenient functions for creating generic JsonErrorArray objects."""
from pyll_json_errors.models import JsonError, JsonErrorArray


def _generic_error(title, detail, status):
    return JsonErrorArray([JsonError(title=title, detail=detail, status=status)])


def error400(*, title="Bad Request", detail=None):
    """Create a generic JSON error with status code 400.

    Args:
        title (Optional[str]): The title to associate with the error.
        detail (Optional[str]): The detail to associate with the error.

    Returns:
        models.JsonErrorArray: A JsonErrorArray containing one error.
    """
    return _generic_error(title, detail, 400)


def error403(*, title="Forbidden", detail=None):
    """Create a generic JSON error with status code 403.

    Args:
        title (Optional[str]): The title to associate with the error.
        detail (Optional[str]): The detail to associate with the error.

    Returns:
        models.JsonErrorArray: A JsonErrorArray containing one error.
    """
    return _generic_error(title, detail, 403)


def error404(*, title="Not found", detail=None):
    """Create a generic JSON error with status code 404.

    Args:
        title (Optional[str]): The title to associate with the error.
        detail (Optional[str]): The detail to associate with the error.

    Returns:
        models.JsonErrorArray: A JsonErrorArray containing one error.
    """
    return _generic_error(title, detail, 404)
