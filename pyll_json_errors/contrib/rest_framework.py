"""Integrate JSON API errors with Django REST Framwork.

[Django REST Framework](https://www.django-rest-framework.org/)

See the [driver DRF app](https://github.com/LeafLink/pyll-json-errors/tree/master/drivers/django_rest_framework)
for examples on integrating `pyll_json_errors` with DRF.
"""

from pyll_json_errors import _check_dependency

_check_dependency("django", __name__)
_check_dependency("rest_framework", __name__)
_check_dependency("werkzeug", __name__)

from django.http.response import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler
from werkzeug.http import HTTP_STATUS_CODES

from pyll_json_errors import constants, models, transform


class DRFTransform(transform.BaseTransform):
    """A transform to flatten DRF exception response data.

    This transform handles any and all exceptions raised by DRF, regardless of
    exception type and content.
    """

    def get_title(self, status_code, pointer, error):
        """Get the title of the error to be returned to the user.

        Args:
            status_code (int): The status code of the error.
            pointer (List[str]): A list of pointer segments to the field which raised
                the initial errors.
            error (rest_framework.exceptions.ErrorDetail): The DRF-provided detail string
                of the error.

        Returns:
            str: The title of the message.
        """
        return HTTP_STATUS_CODES.get(status_code, None)

    def get_status_code(self, status_code, pointer, error):
        """Get the status code of the error message.

        Args:
            status_code (int): The status code of the error.
            pointer (List[str]): A list of pointer segments to the field which raised
                the initial errors.
            error (rest_framework.exceptions.ErrorDetail): The DRF-provided detail string
                of the error.

        Returns:
            int: The status code to be associated with this error detail.
        """
        return status_code

    def get_detail(self, status_code, pointer, error):
        """Get the error detail.

        Args:
            status_code (int): The status code of the error.
            pointer (List[str]): A list of pointer segments to the field which raised
                the initial errors.
            error (rest_framework.exceptions.ErrorDetail): The DRF-provided detail string
                of the error.

        Returns:
            str: The detail message associated with this error.
        """
        return str(error)

    def get_code(self, status_code, pointer, error):
        """Get the code associated with this error detail.

        Args:
            status_code (int): The status code of the error.
            pointer (List[str]): A list of pointer segments to the field which raised
                the initial errors.
            error (rest_framework.exceptions.ErrorDetail): The DRF-provided detail string
                of the error.

        Returns:
            str: The code associated with this error detail.
        """
        return str(error.code)

    def get_source(self, status_code, pointer, error):
        """Get the pointer to the field which raised this error.

        Args:
            status_code (int): The status code of the error.
            pointer (List[str]): A list of pointer segments to the field which raised
                the initial errors.
            error (rest_framework.exceptions.ErrorDetail): The DRF-provided detail string
                of the error.

        Returns:
            pyll_json_errors.models.JsonErrorSourcePointer: An object which contains the
                pointer to the field responsible for the error.
        """
        return models.JsonErrorSourcePointer(keys=pointer)

    def make_error_dict(self, status_code, pointer, error):
        """Get the entire error detail in a JSON API compatible object.

        Args:
            status_code (int): The status code of the error.
            pointer (List[str]): A list of pointer segments to the field which raised
                the initial errors.
            error (rest_framework.exceptions.ErrorDetail): The DRF-provided detail string
                of the error.

        Returns:
            pyll_json_errors.models.JsonError: An object which houses the entire error
                detail, which can be formatted into JSON API spec.
        """
        props = {
            "title": self.get_title(status_code, pointer, error),
            "status": self.get_status_code(status_code, pointer, error),
            "detail": self.get_detail(status_code, pointer, error),
            "code": self.get_code(status_code, pointer, error),
        }

        if pointer:
            props["source"] = self.get_source(status_code, pointer, error)

        return models.JsonError(**props)

    def _compose_error(self, err_source, err_details, status_code):
        """Compose an individual, potentially nested error message.

        Args:
            err_source (Union[str, list]): The base pointer to where the exception was
                generated. An empty list is interpreted to mean a sourceless error.
            err_details (Union[list, dict, rest_framework.exceptions.ErrorDetail]):
                The detais for the specific error.
            status_code (int): The status code generated by Django's base error
                handler.

        Returns:
            list: A list of JsonError objects which have been flattened.
        """
        errors = []

        def _recurse(pointer, error):
            """Inner recursive method to handle indefinitely nested validation errors"""

            if isinstance(error, dict):
                # handling a dictionary of suberrors
                for prop, err in error.items():
                    _recurse(pointer + [str(prop),], err)

            elif isinstance(error, list):
                # handle a list of suberrors
                for num, err in enumerate(error):
                    if isinstance(err, dict):
                        # there are errors nested further within this list item
                        _recurse(pointer + [str(num),], err)
                    elif isinstance(err, (str, exceptions.ErrorDetail)):
                        # there are no nested errors within this list item
                        _recurse(pointer, err)

            else:
                errors.append(self.make_error_dict(status_code, pointer, error))

        if not isinstance(err_source, list) and err_source:
            # ensure source is a list
            err_source = [err_source,]
        elif not isinstance(err_source, list) and not err_source:
            # err_source is None
            err_source = []

        _recurse(err_source, err_details)
        return errors

    def make_json_errors(self, sources):
        """Transform django rest framework errors into models.JsonError objects.

        Args:
            sources (List[rest_framework.exceptions.APIException]): The exception raised by DRF.
        Returns:
            List[models.JsonError]: A list of JsonError objects representing errors raised
                by DRF.
        """
        errors = []

        for source in sources:
            if isinstance(source.detail, dict):
                for err_source, err_details in source.detail.items():
                    errors += self._compose_error(str(err_source), err_details, source.status_code)
            else:
                # catch validation errors with flat details, no source
                errors += self._compose_error(None, source.detail, source.status_code)

        return errors


def make_response(error_array):
    """Format a list of errors into a DRF response object.

    Args:
        error_array (pyll_json_errors.models.JsonErrorArray): The list of errors to be formatted into the response.

    Returns:
        rest_framework.response.Response: A response containing the formatted errors
            which can be returned to the user.
    """
    return Response(error_array.as_dict(), status=error_array.status, content_type=constants.HEADER_CONTENT_TYPE_VALUE)


def reformat_response(exc, context):
    """Reformat the error response data provided by base django.

    This method should be called from within a custom error handler implemented by the
    user. See https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling
    for more information. This method can also be called directly as a custom exception
    handler.

    Args:
        exc (rest_framework.exceptions.APIException): The exception that caused this
            errors response to be returned.
        context (dict): A dictonary of additional details passed from the rest framework.

    Returns:
        rest_framework.respose.Response: A response formatted in the JSON api spec.
    """
    # call the drf base exception handler first
    response = exception_handler(exc, context)

    # custom logic is needed to handle the 404 exception, as it is a Django base
    # exception, not a DRF exception by default.
    if isinstance(exc, Http404):
        exc = exceptions.NotFound(exc)

    if response and isinstance(exc, exceptions.APIException):
        # call the transform
        transform = DRFTransform()
        error_array = transform.to_array(sources=[exc,])

        # return a DRF response, preserving any background work from DRF
        new = make_response(error_array)
        response.data = new.data
        response.status_code = new.status_code
        response[constants.HEADER_CONTENT_TYPE_NAME] = new[constants.HEADER_CONTENT_TYPE_NAME]

    return response
