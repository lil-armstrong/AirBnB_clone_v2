#!/usr/bin/python3
''' script that starts a Flask web application'''
from flask import Flask

app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def hello_world():
    '''GET route to /'''
    return "Hello HBNB!"
