from flask import Flask, abort

from pyll_json_errors import exceptions, flask, JsonError, JsonErrorArray

app = Flask(__name__)
flask.wrap_app(app)


@app.route("/")
def hello_world():
    return {"msg": "hello world"}


@app.route("/errors/<int:status>")
def error(status):
    abort(status)


@app.route("/errors/basic")
def basic():
    err = JsonError(status=400, title="Some Issue", detail="This is an error.")
    return flask.make_response(json_errors=JsonErrorArray([err]))


@app.route("/errors/raised/array")
def raised_array():
    err1 = JsonError(status=400, title="Some Issue", detail="This is error 1.")
    err2 = JsonError(status=422, title="Dependency Failure", detail="This is error 2.")
    array = JsonErrorArray([err1, err2])
    raise exceptions.ConcreteJsonError("", array)


@app.route("/errors/raised/list")
def raised_list():
    err1 = JsonError(status=400, title="Some Issue", detail="This is error 1.")
    err2 = JsonError(status=422, title="Dependency Failure", detail="This is error 2.")
    raise exceptions.ConcreteJsonError("", [err1, err2])
