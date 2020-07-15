from abc import ABC, abstractmethod

from pyll_json_errors.models import JsonErrorArray


class BaseTransform(ABC):
    @abstractmethod
    def make_json_errors(self, sources):
        """Implement this function to convert some source object into a list of JsonErrors.

        Args:
            sources (List[Any]): A list of source objects to convert.

        Returns:
            List[models.JsonError]: A list of JsonError objects. Do not return a JsonErrorArray.
        """

    def to_list(self, *, sources):
        """Transform source data into a list of JsonError objects.

        Args:
            sources (List[Any]): A list of source objects to convert.

        Returns:
            List[models.JsonError]: A list of JsonErrors.
        """
        return self.make_json_errors(sources)

    def to_array(self, *, sources):
        """Transform source data into a single JsonErrorArray object.

        Args:
            sources (List[Any]): A list of source objects to convert.

        Returns:
            models.JsonErrorArray: A single JsonErrorArray object
        """
        return JsonErrorArray(self.make_json_errors(sources))
