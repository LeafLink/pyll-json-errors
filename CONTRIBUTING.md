# Contributing

## Requirements
* Python 3.6 or higher
* [Git](https://git-scm.com/)
* [Poetry](https://python-poetry.org/)

## Setup Development Environment

### Prerequisites
* Ensure you've installed Git and Poetry.
* Ensure you've installed Python 3.6 or higher.
  * [PyEnv](https://github.com/pyenv/pyenv) is a great tool to do this.

### First Time Setup
* `git clone https://github.com/LeafLink/pyll-json-errors.git`
* `cd pyll-json-errors`
* `poetry install -E all`

### Testing
All pull requests must include unit tests for changes. Unit tests can be ran via `make test`.

### Linting and Formatting
All code should pass our linting standards. `make lint` will lint your code and output to the console.
`make format` will automatically fix any linting issues.

### Docs
Preview your docs as HTML locally by running `make docs-serve`. This will spin up a local server on port 5001.

### Misc

#### Running Python Scripts
Poetry manages your python environment. Thus any Python commands should be ran via Poetry. Example:

```bash
poetry run python ./path/to/script.py
```
