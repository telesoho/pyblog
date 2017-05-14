# coding=utf-8
"""
主应用
"""
from flask import Flask
THE_APP = Flask(__name__)

@THE_APP.route("/")
def index():
    """
    Index file
    """
    return "Hello World!"

if __name__ == "__main__":
    THE_APP.config.from_object("default_settings")
    THE_APP.config.from_envvar('PYBLOG_ENV')
    THE_APP.run()
