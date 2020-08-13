## Installation
TBA

### Optional Dependencies
See [Poetry's](https://python-poetry.org/docs/pyproject/#extras) documentation on installing optional dependencies.

* Django REST Framework dependencies can be installed by using the `rest_framework` extras flag.
* Flask dependencies can be installed by using the `flask` extras flag.
* Marshmallow dependencies can be installed by using the `marshmallow` extras flag.
* All dependencies can be installed by using the `all` extras flag.

If you're integrating into an existing project which already has the dependencies you need, just install the base
`pyll_json_error` package.

## Overview
pyll_json_errors is broken into two primary pieces:

* Model classes to represent JSON API error objects, located in the `pyll_json_errors.models` sub-module.
* Helper classes to transform those models into HTTP responses, located in the `pyll_json_errors.contrib` sub-module.

### Model Classes
At a basic level, `pyll_json_errors.models.JsonError` objects should be created, fed into
`pyll_json_errors.models.JsonErrorArray`, then serialized with `.serialized()`.

Example:

```python
# some_module.py
from pyll_json_errors import models

err_one = models.JsonError(
    id="someId",
    status=400,
    code="custom-code-XXX",
    title="Validation Error",
    detail="'leaflink.com' is not a valid email domain.",
    source=models.JsonErrorSourcePointer(keys=("user", "email"))
)
err_two = models.JsonError(
    status="401",
    title="Unauthorized",
    detail="You do not have access to LeafLink email domains."
)

array = models.JsonErrorArray([err_one, err_two])

# array.status
# 400

# array.serialized()
# {"errors": [{"id": "someId", "status": "400", "code": "custom-code-XXX", "title": "Validation Error", "detail": "'leaflink.com' is not a valid email domain.", "source": {"pointer": "/user/email"}}, {"status": "401", "title": "Unauthorized", "detail": "You do not have access to LeafLink email domains."}]}
```


### Contrib Module
Various helpers are available for popular Python libraries.

* Django REST Framework (`pyll_json_errors.contrib.rest_framework`)
* Flask (`pyll_json_errors.contrib.flask`)
* Marshmallow (`pyll_json_errors.contrib.marshmallow`)


## JSON API Errors
See [the JSON API error spec](https://jsonapi.org/format/#errors) and
[examples](https://jsonapi.org/examples/#error-objects).

### Deviations
LeafLink API errors deviate from JSON API errors in two ways:

1. LeafLink APIs do not wrap request bodies in the `data` top level key. Thus, error `source.pointer` properties will
never begin with `/data/`, they will begin with `/`.
2. Error responses will return a `Content-Type` of `application/json`, not `application/vnd.api+json`. This is because
we do not strictly meet the JSON API error spec.

### Remarks
Error `title` properties should _always_ be the same for the same error type. Example:

```javascript
// No
{
    "errors": [
        {
            ...,
            "title": "Product #123 not found."
        },
        {
            ...,
            "title": "Order #456 not found."
        }
    ]
}

// Yes
{
    "errors": [
        {
            ...,
            "title": "Not found.",
            "detail": "Product #123 could not be found."
        },
        {
            ...,
            "title": "Not found.",
            "detail": "Order #456 could not be found."
        }
    ]
}
```


## Development
See the project's [GitHub page](https://github.com/LeafLink/pyll-json-errors) for development information.
