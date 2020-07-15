"""Marshmallow integrations.

https://marshmallow.readthedocs.io/en/stable/
"""

from pyll_json_errors import constants, models, transform, utils


class ValidationErrorTransform(transform.BaseTransform):
    """Transform Marshmallow ValidationErrors to JsonErrors"""

    validation_error_status = 400

    def make_json_errors(self, sources):
        errors = []
        json_errors = []

        # Iterate thru sources and flatten all errors, collect in `errors`.
        for source in sources:
            source_errors = [
                (f"{constants.JSON_POINTER_SEPARATOR}{key}", value)
                for key, value in utils.flatten_dict(
                    data=source.messages, separator=constants.JSON_POINTER_SEPARATOR
                ).items()
            ]
            errors.extend(source_errors)

        for (field, error) in errors:
            source = models.JsonErrorSourcePointer(pointer=field)
            if isinstance(error, (list, tuple, set)):
                for err in error:
                    json_errors.append(models.JsonError(status=self.validation_error_status, detail=err, source=source))
            else:
                json_errors.append(models.JsonError(status=self.validation_error_status, detail=err, source=source))

        return json_errors
