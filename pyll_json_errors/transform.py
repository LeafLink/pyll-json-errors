"""Contains abstract transformation class."""
from abc import ABC, abstractmethod

from pyll_json_errors.models import JsonErrorArray


class BaseTransform(ABC):
    """Base abstract class which all transformer classes inherit.

    When adding a new type of transformer (say for a new module in `pyll_json_errors.contrib`), they should inherit
    from this class and implement `make_json_errors()`.
    """

    @abstractmethod
    def make_json_errors(self, sources):
        """Convert some source objects into a list of JsonErrors.

        This class is implemented by concrete subclasses of BaseTransform. This method should be considered
        semi-private. Use it for concrete class implementation, but use `to_list()` or `to_arrary()` when performing
        actual transformations.

        Args:
            sources (List[Any]): A list of source objects to convert.

        Returns:
            List[pyll_json_errors.models.JsonError]: A list of `pyll_json_errors.models.JsonError` objects.
                **Does not return a `pyll_json_errors.models.JsonErrorArray`.**
        """

    def to_list(self, *, sources):
        """Transform source data into a list of `pyll_json_errors.models.JsonError` objects.

        Args:
            sources (List[Any]): A list of source objects to convert.

        Returns:
            List[pyll_json_errors.models.JsonError]: A list of `pyll_json_errors.models.JsonError` objects.
        """
        return self.make_json_errors(sources)

    def to_array(self, *, sources):
        """Transform source data into a single `pyll_json_errors.models.JsonErrorArray` object.

        Args:
            sources (List[Any]): A list of source objects to convert.

        Returns:
            pyll_json_errors.models.JsonErrorArray: A single `pyll_json_errors.models.JsonErrorArray` object.
        """
        return JsonErrorArray(self.make_json_errors(sources))
