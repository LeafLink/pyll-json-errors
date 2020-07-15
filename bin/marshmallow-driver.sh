#! /bin/bash

DIR=$(cd `dirname $0` && pwd)
FILEPATH="$DIR/../drivers/marshmallow_driver.py"

poetry run python $FILEPATH
