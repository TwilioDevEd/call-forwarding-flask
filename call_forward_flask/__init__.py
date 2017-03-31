import os

from call_forward_flask.config import (
    config_env_files,
)

from flask import Flask

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.sqlite'
db = SQLAlchemy()


def prepare_app(environment='development', p_db=db):
    """Set up environment configuration, import views."""
    app.config.from_object(config_env_files[environment])
    p_db.init_app(app)
    # load views by importing them
    from call_forward_flask import views
    return app


def save_and_commit(item):
    """db.save now saves and commits."""
    db.session.add(item)
    db.session.commit()
db.save = save_and_commit
