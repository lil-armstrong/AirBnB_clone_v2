#!/usr/bin/python3
"""script that starts a Flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def hello_world():
    """GET route to /"""
    return "Hello HBNB!"


@app.route("/hbnb", methods=['GET'], strict_slashes=False)
def hbnb():
    """GET route to /hbnb"""
    return "HBNB"


@app.route("/c/", methods=['GET'], strict_slashes=False)
def hbnb(name=""):
    """Dynamic route to /c/<name>"""
    return "C "+name.replace('_', ' ')


if __name__ == "__main__":
    app.run(host="0.0.0.0")
