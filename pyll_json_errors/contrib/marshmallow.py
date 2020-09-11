"""Integrate Pyll JSON API errors with Marshmallow validation and schemas.

In order to use this module, the :code:`marshmallow` optional dependency must be installed. See :ref:`Installation`.

`Marshmallow docs <https://marshmallow.readthedocs.io/en/stable/>`_

See the :gh:`driver Marshmallow app <drivers/marshmallow_driver.py>`
for examples on integrating :mod:`pyll_json_errors` with Marshmallow.
"""
from pyll_json_errors import _check_dependency

_check_dependency("marshmallow", __name__)

from pyll_json_errors import models, transform, utils


class ValidationErrorTransform(transform.BaseTransform):
    """Transform :py:class:`marshmallow.exceptions.ValidationError` objects."""

    validation_error_status = 400
    """int: HTTP status code for validation failure responses."""

    def make_json_errors(self, sources):
        """Transform :py:class:`marshmallow.exceptions.ValidationError` objects.

        Args:
            sources (list): A list of Marshmallow :py:class:`~marshmallow.exceptions.ValidationError` objects.

        Returns:
            list: A list of :obj:`~pyll_json_errors.models.JsonError` objects representing the provided
            Marshmallow :py:class:`~marshmallow.exceptions.ValidationError`. Returned list will be greater than or
            equal to the length of :code:`source`.
        """
        errors = []
        json_errors = []

        # Iterate thru sources and flatten all errors, collect in `errors`.
        for source in sources:
            source_errors = [(key, value) for key, value in utils.flatten_dict(data=source.messages)]
            errors.extend(source_errors)

        # Assemble list of JSON errors.
        for (keys, error) in errors:
            source = models.JsonErrorSourcePointer(keys=keys)
            json_errors.append(models.JsonError(status=self.validation_error_status, detail=error, source=source))

        return json_errors
