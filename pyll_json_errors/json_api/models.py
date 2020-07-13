"""Representations of various JSON API objects.

https://jsonapi.org/format
"""
import json
from abc import ABC, abstractmethod


class BaseJson(ABC):
    @abstractmethod
    def as_dict(self):
        """
        Converts object into a dictionary.

        Returns:
            dict: Dictionary representation of object. Must only contain
                Python primitives.
        """

    def serialized(self):
        return json.dumps(self.as_dict())


class JsonErrorSourceParameter(BaseJson):
    def __init__(self, *, parameter):
        self.parameter = parameter

    def as_dict(self):
        return {"parameter": self.parameter}


class JsonErrorSourcePointer(BaseJson):
    def __init__(self, *, pointer):
        self.pointer = pointer

    def as_dict(self):
        return {"pointer": self.pointer}


class JsonError(BaseJson):
    def __init__(self, *, id=None, status=None, code=None, title=None, detail=None, source=None, meta=None):
        self.id = id
        self.status = status
        self.code = code
        self.title = title
        self.detail = detail

        if source is not None:
            if not isinstance(source, [JsonErrorSourceParameter, JsonErrorSourcePointer]):
                raise TypeError(
                    f"source must be either {JsonErrorSourceParameter.__name__} or {JsonErrorSourcePointer.__name__}."
                )
        self.source = source

        if meta is not None:
            if not isinstance(meta, [BaseJson, dict]):
                raise TypeError(f"meta must be either {BaseJson.__name__} concrete class or dict.")
        self.meta = meta

    def as_dict(self):
        # basic params
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


class JsonErrorsArray(BaseJson):
    def __init__(self, errors=[]):
        self.errors = errors

    def _unique_status_codes(self):
        """Get the list of unique status codes among the errors."""
        uniques = set([int(error.status) for error in self.errors if error.status is not None])
        return list(uniques)

    def _round_down(self, num):
        """Round a number down to the nearest hundreds."""
        return int(math.floor(num / 100.0)) * 100

    @property
    def status(self):
        status = None
        uniques = self._unique_status_codes()

        if len(uniques) == 1:
            status = uniques[0]
        else:
            ordered = sorted(uniques, reverse=True)
            status = self._round_down(ordered[0])

        return status

    def as_dict(self):
        return {"errors": [error.as_dict() for error in self.errors]}

    def as_json(self):
        """Returns JsonErrorsArray as a JSON compliant string."""
        return json.dumps(self.as_dict())

    def __str__(self):
        return f"<{self.__class__.__name}>({self.status}) Length: {len(self.errors)}"
