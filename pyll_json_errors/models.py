"""Python representations of various JSON API errors objects.

[JSON API Error Format](https://jsonapi.org/format/#error-objects)
"""
import json
import math
from abc import ABC, abstractmethod

from pyll_json_errors import constants


class BaseJson(ABC):
    """Abstract class which all concrete JSON API object classes inherit."""

    @abstractmethod
    def as_dict(self):
        """
        Converts the object into a dictionary containing only Python primitives.
        Must be implemented by concrete subclasses.

        Returns:
            dict: Dictionary representation of objects containing only Python primitives.
        """

    def serialized(self):
        """Get object as stringified JSON.

        Returns:
            str: The object as stringified JSON.
        """
        return json.dumps(self.as_dict())


class JsonErrorSourceParameter(BaseJson):
    """Represents a parameter type JSON API error `source` object.

    Args:
        parameter (str): The name of the query parameter causing the issue.
    """

    def __init__(self, *, parameter):
        self.parameter = parameter

    def as_dict(self):
        return {"parameter": self.parameter}


class JsonErrorSourcePointer(BaseJson):
    """Represents a pointer type JSON API error `source` object.

    Notes: See documentation for `pyll_json_errors.utils.flatten_dict` for more information and example keys.

    Args:
       keys (Tuple[str]): An tuple of strings which represents the path of the error in some object.

    Example:
        ```python
        {
            "one": {
                "two": ["some error"]
            }
            "list": [
                {
                    "error": "hello world"
                },
                {
                    "error": "foobar"
                }
            ]
        }

        # "some error"'s keys would be ("one", "two")
        # "hello world"'s keys would be ("list", "0", "error")
        # "foobar"'s keys would be ("list", "1", "error")
        ```
    """

    def __init__(self, *, keys):
        self.keys = keys

    @property
    def pointer(self):
        """Get the final JSON pointer representation of the keys.

        Returns:
            str: The final stringified pointer.

        Example:
            ```python
                JsonErrorSourcePointer(keys=("one", "two", "three")).pointer  # "/one/two/three"
            ```
        """
        return constants.JSON_POINTER_SEPARATOR + constants.JSON_POINTER_SEPARATOR.join(self.keys)

    def as_dict(self):
        return {"pointer": self.pointer}


class JsonError(BaseJson):
    """Represents a single JSON error object.

    Attributes:
        id (Optional[str]): A unique identifier for this particular occurrence of the problem.
        status (Optional[str]): The HTTP status code applicable to this problem, expressed as a string value.
        code (Optional[str]): An application-specific error code, expressed as a string value.
        title (Optional[str]): A short, human-readable summary of the problem that SHOULD NOT change from occurrence
            to occurrence of the problem.
        detail (Optional[str]): A human-readable explanation specific to this occurrence of the problem.
        source (Optional[Union[JsonErrorSourceParameter, JsonErrorSourcePointer]]): An object containing references
            to the source of the error.
        meta (Optional[Union[BaseJson, dict]]): Non-standard meta-information about the error.

    Raises:
        TypeError: Raised if `source` or `meta` are not the expected types.
    """

    def __init__(self, *, id=None, status=None, code=None, title=None, detail=None, source=None, meta=None):
        self.id = id
        self.status = status
        self.code = code
        self.title = title
        self.detail = detail

        if source is not None:
            if not isinstance(source, (JsonErrorSourceParameter, JsonErrorSourcePointer)):
                raise TypeError(
                    f"source must be either {JsonErrorSourceParameter.__name__} or {JsonErrorSourcePointer.__name__}."
                )
        self.source = source

        if meta is not None:
            if not isinstance(meta, (BaseJson, dict)):
                raise TypeError(f"meta must be either {BaseJson.__name__} concrete class or dict.")
        self.meta = meta

    def as_dict(self):
        """
        Converts the object into a dictionary containing only Python primitives. Resulting dictionary will _only_
        contain keys with values, there will not be any keys with a value of `None`.

        Returns:
            dict: Dictionary representation of objects containing only Python primitives.
        """
        data = {
            key: str(getattr(self, key))
            for key in ["id", "status", "code", "title", "detail"]
            if getattr(self, key, None) is not None
        }

        # source is always BaseJson
        if self.source is not None:
            data["source"] = self.source.as_dict()

        # meta can be either dict or BaseJson
        meta_value = self.meta
        if isinstance(self.meta, BaseJson):
            meta_value = self.meta.as_dict()
        if meta_value is not None:
            data["meta"] = meta_value

        return data


class JsonErrorArray(BaseJson):
    """Representation of multiple `pyll_json_errors.models.JsonError` objects.

    Manages various attributes of the top level "errors" JSON API object.


    Attributes:
        errors (List[pyll_json_errors.models.JsonError]): The list of JsonError objects.
        fallback_status (int): The fallback HTTP status code to use for HTTP responses if one cannot be derived from
            provided errors. Defaults to 400.
        override_status (Optional[int]): If set, this value will always be returned as the status.
    """

    def __init__(self, errors=[]):
        self.errors = errors
        self.fallback_status = 400
        self.override_status = None

    def _unique_status_codes(self):
        """Get the list of unique status codes among the errors."""
        uniques = set([int(error.status) for error in self.errors if error.status is not None])
        return list(uniques)

    def _round_down(self, num):
        """Round a number down to the nearest hundreds."""
        return int(math.floor(num / 100.0)) * 100

    @property
    def status(self):
        """Get the HTTP status code that represents the collection of JsonErrors as a whole.

        If `override_status` is set, that is returned.
        Else, try to derive the status from `errors`. If there is only one error, return that error's status,
        else return the highest status of all errors, rounded down to the nearest 100th.
        If that does not result in a value, `fallback_status` is returned.

        Returns:
            int: The HTTP status code.
        """
        status = self.fallback_status
        uniques = self._unique_status_codes()

        if self.override_status is not None:
            status = self.override_status
        elif len(uniques) == 1:
            status = uniques[0]
        elif len(uniques) > 1:
            ordered = sorted(uniques, reverse=True)
            status = self._round_down(ordered[0])

        return status

    def as_dict(self):
        return {"errors": [error.as_dict() for error in self.errors]}

    def __str__(self):
        return f"<{self.__class__.__name__}>({self.status}) Length: {len(self.errors)}"
