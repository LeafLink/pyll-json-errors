# pyll-json-errors

Python library to implement LeafLink flavored JSON API errors in HTTP APIs.

---

[![CircleCI](https://circleci.com/gh/LeafLink/pyll-json-errors.svg?style=svg&circle-token=70111963b87fa2b476fece5740320b4dc464ad11)](https://circleci.com/gh/LeafLink/pyll-json-errors)
[![codecov](https://codecov.io/gh/LeafLink/pyll-json-errors/branch/master/graph/badge.svg?token=ICZFRWIZAC)](https://codecov.io/gh/LeafLink/pyll-json-errors)

> It's pronounced "pill".

- [Package Documentation](#package-documentation)
- [Requirements](#requirements)
- [Library Documentation](#library-documentation)
- [Example and Driver Applications](#example-and-driver-applications)
  * [Django REST Framework](#django-rest-framework)
  * [Flask Driver](#flask-driver)
  * [Marshmallow Driver](#marshmallow-driver)
- [Contributing](#contributing)


## Package Documentation

See https://pyll-dev-docs.leaflink.com/stable/index.html for `pyll-json-errors` package documentation.


## Requirements
* Python 3.6 or higher


## Library Documentation
See the library's integration docs [here](http://tba).


## Example and Driver Applications
Various example and driver applications can be found in `./drivers`. Use these to test integrations
with various Python libraries.

### Django REST Framework
A basic DRF application for integration testing can be started by running: `. ./bin/drf-driver.sh`

### Flask Driver
A basic Flask application for integration testing can be started by running: `. ./bin/flask-driver.sh`

### Marshmallow Driver
Basic Marshmallow schema and validation example. Can be ran via: `. ./bin/marshmallow-driver.sh`


## Contributing
For guidance of on setting up a development environment and contributing to Pyll JSON Error see our
[contributing](https://github.com/LeafLink/pyll-json-errors/blob/master/CONTRIBUTING.md) doc.
