"""Integrate JSON API errors with Marshmallow validation and schemas.

[Marshmallow docs](https://marshmallow.readthedocs.io/en/stable/)

See the [driver Marshmallow app](https://github.com/LeafLink/pyll-json-errors/tree/master/drivers/marshmallow_drive.py)
for examples on integrating `pyll_json_errors` with Marshmallow.
"""
from pyll_json_errors import _check_dependency

_check_dependency("marshmallow", __name__)

from pyll_json_errors import models, transform, utils


class ValidationErrorTransform(transform.BaseTransform):
    """Marshmallow ValidationErrors transformer."""

    validation_error_status = 400
    """HTTP status code for validation failure responses. (`400`)"""

    def make_json_errors(self, sources):
        """Transform marshmallow ValidationErrors into models.JsonError objects.

        Args:
            sources (List[marshmallow.exceptions.ValidationError]): A list of ValidationErrors to transform.

        Returns:
            List[models.JsonError]: A list of JsonError objects representing all ValidationErrors. Returned list will
                be greater than or equal to the length of `source`.
        """
        errors = []
        json_errors = []

        # Iterate thru sources and flatten all errors, collect in `errors`.
        for source in sources:
            source_errors = [(key, value) for key, value in utils.flatten_dict(data=source.messages).items()]
            errors.extend(source_errors)

        # Assemble list of JSON errors.
        for (keys, error) in errors:
            source = models.JsonErrorSourcePointer(keys=keys)
            # If multiple errors are associated with one field, create a separate error object for each.
            if isinstance(error, (list, tuple, set)):
                for err in error:
                    json_errors.append(models.JsonError(status=self.validation_error_status, detail=err, source=source))
            # Else is one-to-one.
            else:
                json_errors.append(models.JsonError(status=self.validation_error_status, detail=error, source=source))

        return json_errors
