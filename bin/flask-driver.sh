#! /bin/bash

DIR=$(cd `dirname $0` && pwd)

FLASK_ENV=development
FLASK_APP="$DIR/../drivers/flask_driver.py"

FLASK_ENV=$FLASK_ENV FLASK_APP=$FLASK_APP poetry run python -m flask run
