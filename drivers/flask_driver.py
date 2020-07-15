"""Driver application for test and examples of Flask integration."""
from flask import Flask, abort, url_for
from werkzeug import exceptions as w_exceptions

from pyll_json_errors import exceptions, flask, JsonError, JsonErrorArray

app = Flask(__name__)
flask.wrap_app(app)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/")
def index():
    """Lists all available endpoints."""
    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append(f"http://localhost:5000{url}")
            links.sort()
    return {"endpoints": links}


@app.route("/errors/403")
def error403():
    """403s are automatically captured and converted for wrapped apps."""
    abort(403)


@app.route("/errors/404")
def error404():
    """404s are automatically captured and converted for wrapped apps."""
    abort(404)


@app.route("/errors/basic")
def basic():
    """Basic example of creating a JsonError, and returning a response via flask.make_response()."""
    err = JsonError(status=400, title="Some Issue", detail="This is an error.")
    return flask.make_response(json_errors=JsonErrorArray([err]))


@app.route("/errors/raised/array")
def raised_array():
    """Basic example of multiple errors returned via flask.make_response()."""
    err1 = JsonError(status=400, title="Some Issue", detail="This is error 1.")
    err2 = JsonError(status=422, title="Dependency Failure", detail="This is error 2.")
    array = JsonErrorArray([err1, err2])
    raise exceptions.ConcreteJsonError("", array)


@app.route("/errors/raised/list")
def raised_list():
    """Example of returning errors by raising exceptions.ConcreteJsonError()."""
    err1 = JsonError(status=400, title="Some Issue", detail="This is error 1.")
    err2 = JsonError(status=422, title="Dependency Failure", detail="This is error 2.")
    raise exceptions.ConcreteJsonError("", [err1, err2])


@app.route("/errors/werkzeug/httpException")
def flask_http_exception():
    """Example of transforming a werkzeug HTTPException into JsonError objects and returning a response via raising
    exceptions.ConcreteJsonError().
    """
    exc = w_exceptions.HTTPException()
    errs = flask.HttpExceptionTransform().to_list(sources=[exc])
    raise exceptions.ConcreteJsonError("", errs)


@app.route("/errors/werkzeug/badRequest")
def flask_bad_request():
    """Example of transforming a werkzeug BadRequest into JsonError objects and returning a response via raising
    exceptions.ConcreteJsonError().
    """
    exc = w_exceptions.BadRequest()
    errs = flask.HttpExceptionTransform().to_list(sources=[exc])
    raise exceptions.ConcreteJsonError("", errs)
