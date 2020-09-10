"""Library exception classes."""
from pyll_json_errors.models import JsonError, JsonErrorArray


class JsonErrorException(Exception):
    """Base class for all library exceptions."""


class ConcreteJsonError(JsonErrorException):
    """An exception containing JSON error objects.

    Convenient for raising an exception and using attached errors for some further processing.

    Args:
        message (:obj:`str`): Exception message.
        json_errors (:obj:`~pyll_json_errors.models.JsonErrorArray` or :obj:`list`):
            A list of :obj:`~pyll_json_errors.models.JsonError` errors to attach to the exception.

    Raises:
        TypeError: Raised if passed :code:`json_errors` are not the expected type.
    """

    def __init__(self, message, json_errors):
        super().__init__(message)
        if isinstance(json_errors, JsonErrorArray):
            self.json_errors = json_errors
        elif isinstance(json_errors, (list, tuple)):
            for json_error in json_errors:
                if not isinstance(json_error, JsonError):
                    raise TypeError(f"All instances of errors must be {JsonError.__name__}.")
            self.json_errors = JsonErrorArray(json_errors)
        else:
            raise TypeError(f"errors must be {JsonErrorArray.__name__} or list/tuple of {JsonError.__name__}.")
