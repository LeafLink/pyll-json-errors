"""Generic JsonErrorArrays."""
from pyll_json_errors.models import JsonError, JsonErrorArray


def _generic_error(title, detail, status):
    return JsonErrorArray([JsonError(title=title, detail=detail, status=status)])


def error400(*, title="Bad Request", detail=None):
    return _generic_error(title, detail, 400)


def error403(*, title="Forbidden", detail=None):
    return _generic_error(title, detail, 403)


def error404(*, title="Not found", detail=None):
    return _generic_error(title, detail, 404)
