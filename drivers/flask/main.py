from flask import Flask, abort

from pyll_json_errors import flask

app = Flask(__name__)
flask.wrap_app(app)


@app.route("/")
def hello_world():
    return {"msg": "hello world"}


@app.route("/errors/<int:status>")
def error(status):
    abort(status)
