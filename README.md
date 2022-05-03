<!-- omit in toc -->
# pyll-json-errors

Python library to implement LeafLink flavored JSON API errors in HTTP APIs.

---

> It's pronounced "pill".

* [Package Documentation](#package-documentation)
* [Requirements](#requirements)
* [Library Documentation](#library-documentation)
* [Example and Driver Applications](#example-and-driver-applications)
  * [Django REST Framework](#django-rest-framework)
  * [Flask Driver](#flask-driver)
  * [Marshmallow Driver](#marshmallow-driver)
* [Contributing](#contributing)


## Package Documentation

See https://pyll-dev-docs.leaflink.com/stable/index.html for `pyll-json-errors` package documentation.


## Requirements
* Python 3.6 or higher


## Library Documentation
See the library's integration docs [here](https://pyll-dev-docs.leaflink.com/stable/index.html).


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
For guidance of on setting up a development environment and contributing to Pyll JSON Errors see our
[contributing](https://github.com/LeafLink/pyll-json-errors/blob/main/CONTRIBUTING.md) doc.
