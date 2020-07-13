"""Generic JsonErrorArrays."""
from pyll_json_errors.json_api.models import JsonError, JsonErrorsArray


def _generic_error(title, detail, status):
    return JsonError(title=title, detail=detail, status=status)


def _generic_error_array(errors=[]):
    return JsonErrorsArray(errors)


def error403(*, title="Forbidden", detail=None):
    error = _generic_error(title, detail, 403)
    return _generic_error_array([error])


def error404(*, title="Not found", detail=None):
    error = _generic_error(title, detail, 404)
    return _generic_error_array([error])
