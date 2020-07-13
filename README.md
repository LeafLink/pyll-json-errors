# pyll-json-errors

Internal LeafLink Python library to implement JSON API errors in HTTP APIs.

> It's pronounced "pill".

- [JSON API Error Implementation](#json-api-error-implementation)
  * [Remarks](#remarks)
  * [Deviations](#deviations)
- [Development](#development)
  * [Requirements](#requirements)
  * [Setup Development Environment](#setup-development-environment)
  * [Helpful Commands](#helpful-commands)
  * [Running Python](#running-python)
  * [Driver Applications](#driver-applications)
    * [Flask Driver](#flask-driver)

## JSON API Error Implementation
See [the JSON API error spec](https://jsonapi.org/format/#errors), and
[examples](https://jsonapi.org/examples/#error-objects).

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

### Deviations
LeafLink API errors deviate from JSON API errors in two ways:

1. LeafLink APIs do not wrap request bodies in the `data` top level key. Thus, error `source.pointer` properties will
never begin with `/data/`, they will begin with `/`.
2. Error responses will return a `Content-Type` of `application/json`, not `application/vnd.api+json`. This is because
we do not strictly meet the JSON API error spec.


## Development

### Requirements
* [Poetry](https://python-poetry.org/)

### Setup Development Environment
`poetry install`

### Helpful Commands
* `make format`: Fixes linting issues in `./pyll_json_errors`.
* `make lint`: Lints code and outputs to console.
* `make test`: Runs unit tests.

### Running Python
Poetry manages Python environments for you. Thus any Python commands should be ran via Poetry. Example:

```bash
poetry run python ./path/to/script.py
```

### Driver Applications
Various driver applications can be found in `./drivers`. Use these to test integrations with various python libraries.

#### Flask Driver
A basic Flask server for integration testing can be started by running: `. ./bin/start-flask.py`
