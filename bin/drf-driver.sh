#! /bin/bash

DIR=$(cd `dirname $0` && pwd)
FILEPATH="$DIR/../drivers/django-rest-framework/myapi/manage.py"

poetry run python $FILEPATH migrate
poetry run python $FILEPATH runserver 0.0.0.0:8005
