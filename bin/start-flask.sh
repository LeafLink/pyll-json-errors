#! /bin/bash

DIR=$(cd `dirname $0` && pwd)

export FLASK_ENV=development
export FLASK_APP="$DIR/../drivers/flask/main.py"

poetry run python -m flask run
