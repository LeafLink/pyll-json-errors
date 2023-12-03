<!-- omit in toc -->
# pyll-json-errors

[![Contact Us](https://img.shields.io/badge/slack-%23pod--nap-pink.svg?logo=slack)](https://leaflink.slack.com/archives/C055KDEDUNQ)
[![Released via semantic-release with PR titles](https://img.shields.io/badge/release_method-semantic_release_via_PR_titles-blue)](https://leaflink.atlassian.net/wiki/spaces/DEVOPS/pages/2828566530/Releasing+applications+with+semantic-release+via+PR+titles)

Python library to implement LeafLink flavored JSON API errors in HTTP APIs.

---

[![llp-ci](https://github.com/LeafLink/pyll-json-errors/actions/workflows/main.yaml/badge.svg)](https://github.com/LeafLink/pyll-json-errors/actions/workflows/main.yaml)

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
* Python 3.8 or higher

## Installation
Version 0.2.6 and lower are available via GitHub releases.

Version 0.2.7 and up are available via the LeafLink Private Python Package repository. Documentation located [here](https://leaflink.atlassian.net/wiki/spaces/EN/pages/2359559238/How+To+Private+Python+Packages)

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
