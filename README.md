# pyll-json-errors

Internal LeafLink Python library to implement JSON API errors in HTTP APIs.

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
`poetry install`

### Helpful Commands
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

#### Flask Driver
A basic Flask server for integration testing can be started by running: `. ./bin/flask-driver.sh`

#### Marshmallow Driver
Basic Marshmallow schema and validation example. Can be ran via: `. ./bin/marshmallow-driver.sh`
