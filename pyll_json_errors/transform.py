"""Transform classes are the primary interface for converting error of any type into Pyll JSON Errors."""
from abc import ABC, abstractmethod

from pyll_json_errors.models import JsonErrorArray


class BaseTransform(ABC):
    """Base abstract class which all transform classes must inherit.

    When adding a new type of transform (say for a new module in :mod:`pyll_json_errors.contrib`), they should inherit
    from this class and implement :meth:`~pyll_json_errors.transform.BaseTransform.make_json_errors`.
    """

    @abstractmethod
    def make_json_errors(self, sources):
        """Convert some source objects into a list of JsonErrors.

        This method is implemented by concrete subclasses of :class:`~pyll_json_errors.transform.BaseTransform`.
        This method should be considered semi-private. Use it for concrete class implementation,
        but use :meth:`~pyll_json_errors.transform.to_list` or :meth:`~pyll_json_errors.transform.to_array`
        when performing actual transformations.

        Args:
            sources (list): A list of source error objects to convert.

        Returns:
            list: A list of :obj:`~pyll_json_errors.models.JsonError` objects. Does not return a
                :obj:`~pyll_json_errors.models.JsonErrorArray`.
        """

    def to_list(self, *, sources):
        """Transform source data into a list of :obj:`~pyll_json_errors.models.JsonError` objects.

        Args:
            sources (list): A list of source error objects to convert.

        Returns:
            list: A list of :obj:`~pyll_json_errors.models.JsonError` objects.
        """
        return self.make_json_errors(sources)

    def to_array(self, *, sources):
        """Transform source data into a single :obj:`~pyll_json_errors.models.JsonErrorArray` object.

        Args:
            sources (list): A list of source error objects to convert.

        Returns:
            ~pyll_json_errors.models.JsonErrorArray: A single :obj:`~pyll_json_errors.models.JsonErrorArray` object.
        """
        return JsonErrorArray(self.make_json_errors(sources))
