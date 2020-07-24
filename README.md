# pyll-json-errors

Internal LeafLink Python library to implement JSON API errors in HTTP APIs.

---

[![CircleCI](https://circleci.com/gh/LeafLink/pyll-json-errors.svg?style=svg&circle-token=70111963b87fa2b476fece5740320b4dc464ad11)](https://circleci.com/gh/LeafLink/pyll-json-errors)
[![codecov](https://codecov.io/gh/LeafLink/pyll-json-errors/branch/master/graph/badge.svg?token=ICZFRWIZAC)](https://codecov.io/gh/LeafLink/pyll-json-errors)

> It's pronounced "pill".

- [Development](#development)
  * [Requirements](#requirements)
  * [Setup Development Environment](#setup-development-environment)
  * [Helpful Commands](#helpful-commands)
  * [Running Python](#running-python)
  * [Driver Applications](#driver-applications)
    * [Flask Driver](#flask-driver)


## Development

### Requirements
* [Poetry](https://python-poetry.org/)

### Setup Development Environment
`poetry install -E all`

### Helpful Commands
* `make docs-serve`: Spin up a local server to view documentation, port 5001.
* `make format`: Fixes linting issues automatically.
* `make lint`: Lints code and outputs to console.
* `make test`: Runs unit tests.

### Running Python
Poetry manages Python environments for you. Thus any Python commands should be ran via Poetry. Example:

```bash
poetry run python ./path/to/script.py
```

### Driver Applications
Various driver applications can be found in `./drivers`. Use these to test integrations with various Python libraries.

#### Django REST Framework
A basic DRF application for integration testing can be started by running: `. ./bin/drf-driver.sh`

#### Flask Driver
A basic Flask application for integration testing can be started by running: `. ./bin/flask-driver.sh`

#### Marshmallow Driver
Basic Marshmallow schema and validation example. Can be ran via: `. ./bin/marshmallow-driver.sh`
