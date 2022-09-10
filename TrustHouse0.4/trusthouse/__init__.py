import os
from flask import Flask

from .extensions import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trusthouse.sqlite3"
    app.config["TRACK_MODIFICATIONS"] = True

    db.init_app(app)

    return app
    